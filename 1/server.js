import express from "express";
import dotenv from "dotenv";
import path from "path";

// import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { ChatGroq } from "@langchain/groq";
import { createAgent } from "langchain";
import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";

dotenv.config();

const port = 3000;
const app = express();

app.use(express.json());

const __dirname = path.resolve();

const model = new ChatGroq({
  model: "openai/gpt-oss-20b",
  maxOutputTokens: 2048,
  temperature: 0.7,
  apiKey: process.env.GROQ_API_KEY,
});

const getMenuTool = new DynamicStructuredTool({
  name: "getMenuTool",

  description: "Returns today's menu for breakfast, lunch, or dinner.",

  schema: z.object({
    category: z.string().describe("Type of food: breakfast, lunch, or dinner"),
  }),

  func: async ({ category }) => {
    const menus = {
      breakfast: "Aloo Paratha, Poha, Masala Chai",
      lunch: "Paneer, Roti",
      dinner: "Lassi, Dal-Bati",
    };

    return menus[category.toLowerCase()] || "No menu found for that category.";
  },
});

const agent = createAgent({
  model,
  tools: [getMenuTool],
  systemPrompt: "You are a helpful assistant that uses tools when needed.",
});

app.get("/", (req, res) => {
  return res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/api/chat", async (req, res) => {
  const userInput = req.body.input;

  console.log("userInput:", userInput);

  try {
    const response = await agent.invoke(
      {
        messages: [
          {
            role: "user",
            content: userInput,
          },
        ],
      },
      {
        recursionLimit: 10,
      },
    );

    console.log("Agent full Response:", response);

    const lastMessage = response.messages[response.messages.length - 1];

    if (lastMessage?.content) {
      return res.json({
        output: lastMessage.content,
      });
    }

    return res.status(500).json({
      output: "Agent couldn't find a valid answer.",
    });
  } catch (err) {
    console.log("Error during agent execution:", err);

    return res.status(500).json({
      output: "Agent reached the maximum number of steps. Please try again.",
    });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
