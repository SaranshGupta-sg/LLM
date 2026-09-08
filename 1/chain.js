// This is chain in LLM
// 1. - this method is the old version
// import { config } from "dotenv";
// config();

// import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
// import { LLMChain } from "langchain/chains";
// import { PromptTemplate } from "@langchain/core/prompts";

// // 1. Setup the model
// const model = new ChatGoogleGenerativeAI({
//   model: "models/gemini-3.6-flash", // Free-tier model
//   maxOutputTokens: 2048,
//   temperature: 0.7,
//   apiKey: process.env.GOOGLE_GENAI_API_KEY,
// });

// // 2. Create a prompt
// const prompt = PromptTemplate.fromTemplate(
//   "Explain the concept of {topic} to a beginner.",
// );

// // 3. Build a chain
// const chain = new LLMChain({
//   llm: model,
//   prompt: prompt,
// });

// // Run it
// const res = await chain.run("Quantum Computing");
// console.log("Gemini Response:\n", res);









// 2. - this method is the new version, but in this we get the AIMessage object data in which not only text but metaData also present
// import { config } from "dotenv";
// config();

// import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
// import { PromptTemplate } from "@langchain/core/prompts";


// // 1. Setup model
// const model = new ChatGoogleGenerativeAI({
//   model: "gemini-3.6-flash",
//   maxOutputTokens: 2048,
//   temperature: 0.7,
//   apiKey: process.env.GOOGLE_GENAI_API_KEY,
// });

// // 2. Create prompt
// const prompt = PromptTemplate.fromTemplate(
//   "Explain the concept of {topic} to a beginner."
// );

// // 3. Create chain
// const chain = prompt.pipe(model);

// // 4. Run
// const response = await chain.invoke({
//   topic: "Quantum Computing",
// });

// console.log(response.content);









// 3. this method is the new version and also it converts the AIMessage object data in the plain string format
import { config } from "dotenv";
config();

import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { PromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

const model = new ChatGoogleGenerativeAI({
  model: "gemini-3.6-flash",
  maxOutputTokens: 2048,
  temperature: 0.7,
  apiKey: process.env.GOOGLE_GENAI_API_KEY,
});

const prompt = PromptTemplate.fromTemplate(
  "Explain the concept of {topic} to a beginner."
);

const outputParser = new StringOutputParser();

const chain = prompt.pipe(model).pipe(outputParser);

const response = await chain.invoke({
  topic: "Quantum Computing",
});

console.log(response);