import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const agentsConfigFile = path.resolve(__dirname, "agents.json");

async function testHealth() {
  console.log("Loading agents.json from:", agentsConfigFile);
  const config = JSON.parse(fs.readFileSync(agentsConfigFile, "utf8"));
  const healthConfig = config.health;
  
  if (!healthConfig) {
    console.error("Health agent not found in config.");
    return;
  }
  
  console.log("Health Config:", healthConfig);
  
  let command = healthConfig.command;
  let args = [...(healthConfig.args || [])];
  
  // Resolve relative script paths relative to the multiplexer directory
  args = args.map(arg => {
    if (typeof arg === "string" && (arg.startsWith("../") || arg.startsWith("./") || arg.startsWith("agents/"))) {
      return path.resolve(__dirname, arg);
    }
    return arg;
  });
  
  if (typeof command === "string" && (command.startsWith("../") || command.startsWith("./"))) {
    command = path.resolve(__dirname, command);
  }
  
  console.log("Resolved command:", command);
  console.log("Resolved args:", args);
  
  const env = { ...process.env, ...(healthConfig.env || {}) };
  const workspaceRoot = path.resolve(__dirname, "..");
  console.log("Workspace root / cwd:", workspaceRoot);
  
  const transport = new StdioClientTransport({
    command: command,
    args: args,
    env: env,
    cwd: workspaceRoot
  });
  
  const client = new Client({
    name: "diagnostic-client-health",
    version: "1.0.0"
  }, {
    capabilities: { tools: {} }
  });
  
  console.log("Connecting to health agent stdio...");
  try {
    await client.connect(transport);
    console.log("Success! Connected to health agent.");
    const response = await client.request({ method: "tools/list" }, {
      method: "tools/list"
    });
    console.log("Tools returned by health agent:");
    console.log(JSON.stringify(response.tools, null, 2));
  } catch (e) {
    console.error("Failed to connect or query health agent:", e);
  } finally {
    try {
      await transport.close();
    } catch(e) {}
  }
}

testHealth().catch(console.error);
