// 1 - this is the older version
// import { config } from "dotenv";
// config();

// import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
// import { initializeAgentExecutorWithOptions } from "langchain/agents";
// import { SerpAPI } from "@langchain/community/tools/serpapi";

// const model = new ChatGoogleGenerativeAI({
//   model: "models/gemini-3.6-flash", // Free-tier model
//   maxOutputTokens: 2048,
//   temperature: 0.7,
//   apikey: process.env.GOOGLE_API_KEY,
// });

// // Directly using built-in tool
// const searchTool = new SerpAPI(process.env.GOOGLE_SEARCH_SERPAPI_KEY, {
//   location: "India", // Optional: Set region
// });

// const agent = await initializeAgentExecutorWithOptions([searchTool], model);

// // Try a question
// const res = await agent.invoke({
//   input: "What is the latest news about ISRO?",
// });

// console.log("Final Output:", res.output);










// 2
import { config } from "dotenv";
config();

import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { createAgent, tool } from "langchain";
import { SerpAPI } from "@langchain/community/tools/serpapi";

const model = new ChatGoogleGenerativeAI({
  model: "gemini-3.6-flash",
  maxOutputTokens: 2048,
  temperature: 0.7,
  apiKey: process.env.GOOGLE_GENAI_API_KEY,
});

const searchTool = new SerpAPI(
  process.env.GOOGLE_SEARCH_SERPAPI_KEY,
  {
    location: "India",
  }
);

const agent = createAgent({
  model,
  tools: [searchTool],
});

const result = await agent.invoke({
  messages: [
    {
      role: "user",
      content: "What is the latest news about ISRO?",
    },
  ],
});

console.log(result);