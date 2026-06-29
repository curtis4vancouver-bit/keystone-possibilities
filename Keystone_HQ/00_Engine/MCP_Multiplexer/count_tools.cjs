const { Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { StdioClientTransport } = require('@modelcontextprotocol/sdk/client/stdio.js');

async function execute() {
  const transport = new StdioClientTransport({
    command: 'node',
    args: ['index.js']
  });
  const client = new Client({ name: 'test', version: '1.0.0' }, { capabilities: {} });
  await client.connect(transport);

  console.log("Connected. Fetching tools...");
  try {
    const response = await client.request({ method: "tools/list" }, require('@modelcontextprotocol/sdk/types.js').ListToolsResultSchema);
    console.log(`Total tools returned: ${response.tools.length}`);
  } catch (e) {
    console.error("Error:", e);
  }

  process.exit(0);
}
execute().catch(console.error);
