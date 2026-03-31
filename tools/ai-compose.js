#!/usr/bin/env node

/**
 * ai-compose — Gemini for composing content ideas
 * All output is automatically saved to Raw Ideas Inbox in Notion.
 * Usage:
 *   node ai-compose.js "write a TikTok hook about spine surgery" [--file path/to/file]
 *   node ai-compose.js          (interactive mode)
 */

import { GoogleGenerativeAI } from "@google/generative-ai";
import { Client } from "@notionhq/client";
import readline from "readline";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { config } from "dotenv";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
config({ path: path.resolve(__dirname, "../.env") });

// ─── CONFIG ──────────────────────────────────────────────────────────────────

const MODEL = "gemini-2.5-pro";

const SYSTEM = `You are the content and language specialist for Dr Nor Faizal Ahmad Bahuri —
Oxford-trained Consultant Neurosurgeon & Interventional Pain Specialist based in Kuala Lumpur.
Your role: generate, translate, and refine all written content.
Voice: Human first, credentials second.
Bilingual: Bahasa Malaysia for reach, English for authority.
Platforms: TikTok, Instagram, YouTube, Facebook, LinkedIn.
Brand: Batik scrubs. Precision care. Approachable expertise.
Never clinical or corporate. Always Dr Faizal — the person.`;

// ─── GEMINI CALL ─────────────────────────────────────────────────────────────

async function ask(prompt, contextFile = null) {
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
  const model = genAI.getGenerativeModel({ model: MODEL, systemInstruction: SYSTEM });

  let userContent = prompt;
  if (contextFile && fs.existsSync(contextFile)) {
    const fileContent = fs.readFileSync(contextFile, "utf-8");
    userContent = `Context file: ${path.basename(contextFile)}\n\`\`\`\n${fileContent}\n\`\`\`\n\n${prompt}`;
  }

  const result = await model.generateContent(userContent);
  return result.response.text();
}

// ─── NOTION — RAW IDEAS INBOX ────────────────────────────────────────────────

async function saveToInbox(prompt, response) {
  const notion = new Client({ auth: process.env.NOTION_API_KEY });
  const dbId = process.env.NOTION_RAW_IDEAS_DB_ID;
  if (!dbId) return;

  const idea = prompt.length > 100 ? prompt.slice(0, 97) + "..." : prompt;
  const notes = response.length > 2000 ? response.slice(0, 1997) + "..." : response;
  const today = new Date().toISOString().slice(0, 10);

  await notion.pages.create({
    parent: { database_id: dbId },
    properties: {
      Idea: { title: [{ type: "text", text: { content: idea } }] },
      Notes: { rich_text: [{ type: "text", text: { content: notes } }] },
      Status: { select: { name: "Raw" } },
      Format: { select: { name: "Not Sure Yet" } },
      Source: { select: { name: "Random" } },
      "Captured On": { date: { start: today } },
    },
  });
}

// ─── CLI ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length > 0) {
    const fileFlag = args.indexOf("--file");
    const contextFile = fileFlag !== -1 ? args[fileFlag + 1] : null;
    const prompt = args.find((a, i) => !a.startsWith("--") && args[i - 1] !== "--file");

    if (!prompt) {
      console.error('Usage: node ai-compose.js "your prompt" [--file path/to/file]');
      process.exit(1);
    }

    console.log("\n🟢 Gemini (compose)\n" + "─".repeat(50));
    const response = await ask(prompt, contextFile);
    console.log(response);
    console.log("─".repeat(50));
    await saveToInbox(prompt, response);
    console.log("📝 Saved to Raw Ideas Inbox\n");
    return;
  }

  // Interactive mode
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log("\n╔══════════════════════════════════════╗");
  console.log("║   ai-compose — Gemini for content    ║");
  console.log("║   All output → Raw Ideas Inbox       ║");
  console.log("╚══════════════════════════════════════╝\n");

  const loop = () => {
    rl.question("You → ", async (input) => {
      const trimmed = input.trim();
      if (!trimmed || trimmed === "exit") {
        console.log("\nGoodbye.\n");
        rl.close();
        return;
      }

      console.log("\n[Gemini 🟢]\n");
      try {
        const response = await ask(trimmed);
        console.log(response);
        await saveToInbox(trimmed, response);
        console.log("\n📝 Saved to Raw Ideas Inbox");
      } catch (err) {
        console.error(`\n❌ ${err.message}\n`);
      }

      console.log("\n" + "─".repeat(50) + "\n");
      loop();
    });
  };

  loop();
}

main().catch(console.error);
