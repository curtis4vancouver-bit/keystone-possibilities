import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { ListToolsResultSchema } from "@modelcontextprotocol/sdk/types.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const agentsConfigFile = path.join(__dirname, "agents.json");
const cachedToolsFile = path.join(__dirname, "cached_tools.json");

class AgentManager {
  constructor(name, config) {
    this.agentName = name;
    this.config = config;
    this.client = null;
    this.transport = null;
    this.cachedTools = null;
    this.idleTimeout = null;
    this.connectionPromise = null;
  }

  async connect() {
    if (this.client) return this.client;
    if (this.connectionPromise) return this.connectionPromise;

    this.connectionPromise = (async () => {
        let command = this.config.command;
        let args = [...(this.config.args || [])];

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
        
        console.log(`[Diagnostic] Spawning agent process for: ${this.agentName} (${command}) with args: ${args.join(" ")}`);
        this.transport = new StdioClientTransport({
          command: command,
          args: args,
          env: env,
          cwd: path.resolve(__dirname, "..")
        });
        
        this.client = new Client({
          name: `multiplexer-client-${this.agentName}`,
          version: "1.0.0"
        }, {
          capabilities: { tools: {} }
        });

        const timeout = new Promise((_, reject) =>
          setTimeout(() => reject(new Error(`Connection timeout for ${this.agentName}`)), 15000)
        );
        await Promise.race([this.client.connect(this.transport), timeout]);
        console.log(`[Diagnostic] Connection established with sub-agent: ${this.agentName}`);
        return this.client;
    })().catch((err) => {
        console.error(`[Diagnostic] Failed connection to ${this.agentName}:`, err.message);
        this.client = null;
        this.transport = null;
        this.connectionPromise = null;
        throw err;
    });
    
    return this.connectionPromise;
  }

  async disconnect() {
    if (this.client) {
      try {
        await this.transport.close();
      } catch (e) {}
      this.client = null;
      this.transport = null;
      this.connectionPromise = null;
      console.log(`[Diagnostic] Separated sub-agent: ${this.agentName}`);
    }
  }

  async getTools() {
    try {
      const client = await this.connect();
      const response = await client.request({ method: "tools/list" }, ListToolsResultSchema);
      return response.tools;
    } catch (e) {
      this.client = null;
      this.transport = null;
      this.connectionPromise = null;
      throw e;
    }
  }
}

async function testCacheGen() {
  console.log("Reading agents.json...");
  const configRaw = fs.readFileSync(agentsConfigFile, "utf8");
  const agentsConfig = JSON.parse(configRaw);
  
  const cache = {};
  
  for (const [name, config] of Object.entries(agentsConfig)) {
    if (config.enabled === false) {
      console.log(`Sub-agent ${name} is disabled.`);
      continue;
    }
    
    const manager = new AgentManager(name, config);
    try {
      console.log(`Querying tools for: ${name}...`);
      const tools = await manager.getTools();
      cache[name] = tools.map(t => ({
        name: t.name,
        description: t.description,
        inputSchema: t.inputSchema
      }));
      console.log(`Success! Found ${tools.length} tools for ${name}.`);
    } catch (e) {
      console.error(`[ERROR] Failed to query ${name}:`, e);
      cache[name] = [];
    } finally {
      await manager.disconnect();
    }
  }
  
  console.log("\nFinal tools count mapping:");
  console.log(Object.keys(cache).reduce((acc, key) => {
    acc[key] = cache[key].length;
    return acc;
  }, {}));

  fs.writeFileSync(cachedToolsFile, JSON.stringify(cache, null, 2));
  console.log(`[Diagnostic] Successfully wrote tools cache to: ${cachedToolsFile}`);
}

testCacheGen().catch(console.error);
