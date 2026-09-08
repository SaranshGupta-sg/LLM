import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// 1. Create MCP Server instance
const server = new McpServer({
  name: "Currency Converter MCP Server",
  version: "1.0.0",
});

server.tool(
  "convertCurrency",
  "Convert amount from one currency to another (no  API key required)",
  {
    amount: z.number().describe("Amount to convert,  e.g., 100"),
    from: z.string().describe("Base currency code,  e.g., USD"),
    to: z.string().describe("Target currency code,  e.g., INR"),
  },
  async ({ amount, from, to }) => {
    try {
      const res = await fetch(
        `https://open.er-api.com/v6/latest/${from.toUpperCase()}`,
      );
      const data = await res.json();
      if (data.result !== "success" || !data.rates[to.toUpperCase()]) {
        return {
          content: [
            {
              type: "text",
              text: `Conversion failed or unsupported currency: ${to}`,
            },
          ],
        };
      }
      const rate = data.rates[to.toUpperCase()];
      const converted = (amount * rate).toFixed(2);
      const text = `${amount} ${from.toUpperCase()} ≈ ${converted} ${to.toUpperCase()}`;
      return { content: [{ type: "text", text }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }] };
    }
  },
);

// Start the server with stdio transport
async function startServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(
    "✅MCP convert Currency Server started  and ready to receive requests",
  );
}
startServer().catch((error) => {
  console.error("❌Failed to start server:", error);
  process.exit(1);
});








// {
//   "mcpServers": {
//     "Currency Converter": {
//       "command": "node",
//       "args": [
//         "D:/CodewithHarry/LLM/MCP/currencyConverter.js"
//       ]
//     }
//   }
// }