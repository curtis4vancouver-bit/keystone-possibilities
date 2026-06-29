import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema, CallToolResultSchema, ListToolsResultSchema } from "@modelcontextprotocol/sdk/types.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const agentsConfigFile = path.join(__dirname, "agents.json");
const cachedToolsFile = path.join(__dirname, "cached_tools.json");

const server = new Server({
  name: "keystone-multiplexer-gateway",
  version: "4.0.0",
}, {
  capabilities: {
    tools: {},
  }
});

class AgentManager {
  constructor(name, config) {
    this.agentName = name;
    this.config = config;
    this.client = null;
    this.transport = null;
    this.cachedTools = null;
    this.idleTimeout = null;
    this.TTL_MS = 300000; // 5 minutes TTL to conserve resources
    this.connectionPromise = null;
  }

  async connect() {
    if (this.client) {
      this.resetIdleTimer();
      return this.client;
    }
    
    if (this.connectionPromise) {
        return this.connectionPromise;
    }

    this.connectionPromise = (async () => {
        let command = this.config.command;
        let args = [...(this.config.args || [])];

        // Resolve relative script paths relative to the multiplexer directory (__dirname)
        args = args.map(arg => {
          if (typeof arg === "string" && (arg.startsWith("../") || arg.startsWith("./") || arg.startsWith("agents/"))) {
            return path.resolve(__dirname, arg);
          }
          return arg;
        });

        if (typeof command === "string" && (command.startsWith("../") || command.startsWith("./"))) {
          command = path.resolve(__dirname, command);
        }

        const env = { ...process.env, ...(this.config.env || {}) };
        
        console.error(`[Multiplexer] Spawning agent process for: ${this.agentName} (${command}) with args: ${args.join(" ")}`);
        this.transport = new StdioClientTransport({
          command: command,
          args: args,
          env: env,
          cwd: path.resolve(__dirname, "..") // Workspace root
        });
        
        this.client = new Client({
          name: `multiplexer-client-${this.agentName}`,
          version: "1.0.0"
        }, {
          capabilities: { tools: {} }
        });

        // 45-second connection timeout to allow virtual env / node startups on Windows
        const timeout = new Promise((_, reject) =>
          setTimeout(() => reject(new Error(`Connection timeout for ${this.agentName}`)), 45000)
        );
        await Promise.race([this.client.connect(this.transport), timeout]);
        console.error(`[Multiplexer] Dynamic connection established with sub-agent: ${this.agentName}`);
        this.resetIdleTimer();
        return this.client;
    })().catch((err) => {
        console.error(`[Multiplexer] Failed connection to ${this.agentName}:`, err.message);
        this.client = null;
        this.transport = null;
        this.connectionPromise = null;
        this.cachedTools = null;
        throw err;
    });
    
    return this.connectionPromise;
  }

  resetIdleTimer() {
    if (this.idleTimeout) clearTimeout(this.idleTimeout);
    this.idleTimeout = setTimeout(() => this.disconnect(), this.TTL_MS);
  }

  async disconnect() {
    if (this.client) {
      try {
        await this.transport.close();
      } catch (e) {}
      this.client = null;
      this.transport = null;
      this.connectionPromise = null;
      this.cachedTools = null;
      console.error(`[Multiplexer] Suspended sub-agent (TTL): ${this.agentName}`);
    }
  }

  async getTools() {
    if (this.cachedTools && this.client) return this.cachedTools;
    try {
      const client = await this.connect();
      const response = await client.request({ method: "tools/list" }, ListToolsResultSchema);
      this.cachedTools = response.tools;
      return this.cachedTools;
    } catch (e) {
      this.client = null;
      this.transport = null;
      this.connectionPromise = null;
      throw e;
    }
  }

  async callTool(toolName, params) {
    let client;
    try {
        client = await this.connect();
        const result = await client.request({
            method: "tools/call",
            params: { name: toolName, arguments: params }
        }, CallToolResultSchema);
        this.resetIdleTimer();
        return result;
    } catch (e) {
      this.client = null;
      this.transport = null;
      this.connectionPromise = null;
      throw new Error(`[Sub-Agent ${this.agentName} Tool Error in '${toolName}']: ${e.message}`);
    }
  }
}

const agentManagers = new Map();

async function refreshToolCache() {
  console.error("[Multiplexer] Refreshing sub-agent tools cache file...");
  
  // Reload agents.json dynamically to catch any newly added or modified agents
  try {
    if (fs.existsSync(agentsConfigFile)) {
      const configRaw = fs.readFileSync(agentsConfigFile, "utf8");
      const agentsConfig = JSON.parse(configRaw);
      
      for (const [name, config] of Object.entries(agentsConfig)) {
        if (!agentManagers.has(name)) {
          console.error(`[Multiplexer] Dynamically registering newly discovered sub-agent: ${name}`);
          agentManagers.set(name, new AgentManager(name, config));
        } else {
          // Update config in case it changed
          agentManagers.get(name).config = config;
        }
      }
      
      // Remove any agents that were deleted from config
      for (const name of agentManagers.keys()) {
        if (!(name in agentsConfig)) {
          console.error(`[Multiplexer] Dynamically removing deleted sub-agent: ${name}`);
          const manager = agentManagers.get(name);
          await manager.disconnect();
          agentManagers.delete(name);
        }
      }
    }
  } catch (err) {
    console.error(`[Multiplexer] Error reloading agents config during cache refresh: ${err.message}`);
  }

  const cache = {};
  for (const [name, manager] of agentManagers.entries()) {
    if (manager.config.enabled === false) {
      console.error(`[Multiplexer] Sub-agent ${name} is disabled. Skipping tools query.`);
      cache[name] = [];
      continue;
    }
    
    try {
      console.error(`[Multiplexer] Querying tools for: ${name}...`);
      const tools = await manager.getTools();
      cache[name] = tools.map(t => ({
        name: t.name,
        description: t.description,
        inputSchema: t.inputSchema
      }));
      console.error(`[Multiplexer] Success! Cached ${tools.length} tools for ${name}.`);
      await manager.disconnect();
    } catch (e) {
      console.error(`[Multiplexer] Warning: Skip/Empty tools cache for ${name} (${e.message})`);
      cache[name] = [];
    }
  }
  
  fs.writeFileSync(cachedToolsFile, JSON.stringify(cache, null, 2));
  console.error("[Multiplexer] Tools cache written to disk.");
}

async function start() {
  if (!fs.existsSync(agentsConfigFile)) {
    console.error(`[Multiplexer] Config file not found at ${agentsConfigFile}`);
    process.exit(1);
  }
  
  const configRaw = fs.readFileSync(agentsConfigFile, "utf8");
  const agentsConfig = JSON.parse(configRaw);
  
  for (const [name, config] of Object.entries(agentsConfig)) {
    agentManagers.set(name, new AgentManager(name, config));
  }

  // Automatic boot cache generation if missing or empty
  if (!fs.existsSync(cachedToolsFile) || fs.readFileSync(cachedToolsFile, "utf8").trim() === "{}" || fs.readFileSync(cachedToolsFile, "utf8").trim() === "") {
    await refreshToolCache();
  }

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "mcp_multiplexer_list_agents",
          description: "Lists all configured Keystone sub-agents, their startup commands, and their current activity/warm status.",
          inputSchema: { type: "object", properties: {}, required: [] }
        },
        {
          name: "mcp_multiplexer_list_all_tools",
          description: "Instantly returns a structured breakdown of ALL available tools supported by all sub-agents, read from the schema cache. Use this to discover available sub-agent tools.",
          inputSchema: { type: "object", properties: {}, required: [] }
        },
        {
          name: "mcp_multiplexer_execute_tool",
          description: "Gateway dynamic execution: Spins up the target sub-agent in the background, executes the requested tool, and returns the standard result. ZERO IDE refreshes required.",
          inputSchema: {
            type: "object",
            properties: {
              agentName: { 
                type: "string", 
                description: "Name of the sub-agent to invoke (e.g. 'youtube_manager', 'google_workspace', 'davinci_resolve', 'content_engine', 'music_production', 'search_console')" 
              },
              toolName: { 
                type: "string", 
                description: "The specific tool name to run (e.g. 'search_emails', 'davinci_resolve_add_text_clip', 'youtube_upload')" 
              },
              arguments: { 
                type: "object", 
                description: "The JSON arguments required by the target tool's schema." 
              }
            },
            required: ["agentName", "toolName", "arguments"]
          }
        },
        {
          name: "mcp_multiplexer_refresh_tool_cache",
          description: "Re-interrogates all sub-agents to regenerate the cached_tools.json schema file. Run this after updating a sub-agent's code or dependencies.",
          inputSchema: { type: "object", properties: {}, required: [] }
        },
        {
          name: "mcp_multiplexer_reset_all_agents",
          description: "Force-stops and shuts down all active sub-agent processes running in the background.",
          inputSchema: { type: "object", properties: {}, required: [] }
        }
      ]
    };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    
    if (name === "mcp_multiplexer_list_agents") {
      const config = JSON.parse(fs.readFileSync(agentsConfigFile, "utf8"));
      const list = Object.keys(config).map(k => {
        const manager = agentManagers.get(k);
        return {
          agent: k,
          command: config[k].command,
          args: config[k].args || [],
          is_active: manager ? !!manager.client : false
        };
      });
      return {
        content: [{ type: "text", text: JSON.stringify(list, null, 2) }]
      };
    }
    
    if (name === "mcp_multiplexer_list_all_tools") {
      if (!fs.existsSync(cachedToolsFile)) {
        await refreshToolCache();
      }
      const cacheContent = fs.readFileSync(cachedToolsFile, "utf8");
      return {
        content: [{ type: "text", text: cacheContent }]
      };
    }
    
    if (name === "mcp_multiplexer_refresh_tool_cache") {
      await refreshToolCache();
      return {
        content: [{ type: "text", text: "Successfully regenerated cached_tools.json schemas for all sub-agents." }]
      };
    }

    if (name === "mcp_multiplexer_reset_all_agents") {
      let resetCount = 0;
      for (const [agentName, manager] of agentManagers.entries()) {
        if (manager.client) {
          await manager.disconnect();
          resetCount++;
        }
      }
      return {
        content: [{ type: "text", text: `Emergency shutdown complete: Disconnected ${resetCount} active background sub-agents.` }]
      };
    }

    if (name === "mcp_multiplexer_execute_tool") {
      const { agentName, toolName, arguments: toolArgs } = args;
      const manager = agentManagers.get(agentName);
      if (!manager) {
        throw new Error(`Sub-agent '${agentName}' not found. Available agents: ${Array.from(agentManagers.keys()).join(', ')}`);
      }
      
      const result = await manager.callTool(toolName, toolArgs || {});
      return result;
    }
    
    throw new Error(`Tool not found: ${name}`);
  });

  const stdioTransport = new StdioServerTransport();
  await server.connect(stdioTransport);
  console.error(`[Multiplexer V4] Dynamic Gateway Server active. Managing ${agentManagers.size} sub-agents silently.`);
}

start().catch((err) => {
  console.error("[Multiplexer] Fatal error on start:", err);
  process.exit(1);
});
