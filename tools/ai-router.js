#!/usr/bin/env node

/**
 * AI Router — drnorfaizal.com
 * Claude  → code, backend, logic
 * Gemini  → content, language, bilingual (BM/EN)
 */

import Anthropic from "@anthropic-ai/sdk";
import { GoogleGenerativeAI } from "@google/generative-ai";
import readline from "readline";
import fs from "fs";
import path from "path";

// ─── CONFIG ──────────────────────────────────────────────────────────────────

const CLAUDE_MODEL = "claude-sonnet-4-20250514";
const GEMINI_MODEL = "gemini-1.5-pro";

const CLAUDE_SYSTEM = `You are the backend and code specialist for drnorfaizal.com — 
a neurosurgeon's personal brand website and content system. 
Your role: write, review, debug, and refactor code only.
Stack: HTML/CSS/JS, Node.js, GitHub Pages or similar static host.
Be precise, concise, and production-ready. No fluff.`;

const GEMINI_SYSTEM = `You are the content and language specialist for Dr Nor Faizal Ahmad Bahuri — 
Oxford-trained Consultant Neurosurgeon & Interventional Pain Specialist based in Kuala Lumpur.
Your role: generate, translate, and refine all written content.
Voice: Human first, credentials second. 
Bilingual: Bahasa Malaysia for reach, English for authority.
Platforms: TikTok, Instagram, YouTube, Facebook, LinkedIn.
Brand: Batik scrubs. Precision care. Approachable expertise.
Never clinical or corporate. Always Dr Faizal — the person.`;

// ─── TASK ROUTER ─────────────────────────────────────────────────────────────

const CODE_KEYWORDS = [
  "fix", "build", "debug", "refactor", "function", "component",
  "deploy", "html", "css", "js", "javascript", "node", "api",
  "backend", "frontend", "website", "code", "script", "error",
  "install", "github", "npm", "route", "server", "database"
];

const CONTENT_KEYWORDS = [
  "write", "caption", "post", "reel", "tiktok", "instagram",
  "translate", "bahasa", "bm", "english", "script", "hook",
  "content", "social", "audience", "story", "bio", "description",
  "email", "newsletter", "article", "blog", "voice", "tone"
];

function detectAgent(input) {
  const lower = input.toLowerCase();

  const codeScore = CODE_KEYWORDS.filter(k => lower.includes(k)).length;
  const contentScore = CONTENT_KEYWORDS.filter(k => lower.includes(k)).length;

  if (codeScore === 0 && contentScore === 0) return "ambiguous";
  return codeScore >= contentScore ? "claude" : "gemini";
}

// ─── CLAUDE CALL ─────────────────────────────────────────────────────────────

async function askClaude(prompt, contextFile = null) {
  const client = new Anthropic();

  let userContent = prompt;
  if (contextFile && fs.existsSync(contextFile)) {
    const fileContent = fs.readFileSync(contextFile, "utf-8");
    userContent = `File: ${path.basename(contextFile)}\n\`\`\`\n${fileContent}\n\`\`\`\n\n${prompt}`;
  }

  const response = await client.messages.create({
    model: CLAUDE_MODEL,
    max_tokens: 2048,
    system: CLAUDE_SYSTEM,
    messages: [{ role: "user", content: userContent }],
  });

  return response.content[0].text;
}

// ─── GEMINI CALL ─────────────────────────────────────────────────────────────

async function askGemini(prompt, contextFile = null) {
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
  const model = genAI.getGenerativeModel({
    model: GEMINI_MODEL,
    systemInstruction: GEMINI_SYSTEM,
  });

  let userContent = prompt;
  if (contextFile && fs.existsSync(contextFile)) {
    const fileContent = fs.readFileSync(contextFile, "utf-8");
    userContent = `Context file: ${path.basename(contextFile)}\n\`\`\`\n${fileContent}\n\`\`\`\n\n${prompt}`;
  }

  const result = await model.generateContent(userContent);
  return result.response.text();
}

// ─── CLI INTERFACE ────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  // Direct mode: node ai-router.js --claude "fix this bug"
  // Direct mode: node ai-router.js --gemini "write a caption" --file post.md
  if (args.length > 0) {
    const forceAgent = args.includes("--claude") ? "claude"
                     : args.includes("--gemini") ? "gemini"
                     : null;

    const fileFlag = args.indexOf("--file");
    const contextFile = fileFlag !== -1 ? args[fileFlag + 1] : null;

    const promptIndex = args.findIndex(a => !a.startsWith("--") && args[args.indexOf(a) - 1] !== "--file");
    const prompt = args[promptIndex];

    if (!prompt) {
      console.error("Usage: node ai-router.js [--claude|--gemini] \"your prompt\" [--file path/to/file]");
      process.exit(1);
    }

    const agent = forceAgent || detectAgent(prompt);

    if (agent === "ambiguous") {
      console.log("\n⚠️  Ambiguous task. Please use --claude or --gemini flag.\n");
      process.exit(1);
    }

    console.log(`\n🤖 Routing to: ${agent === "claude" ? "Claude (code)" : "Gemini (content)"}\n`);
    console.log("─".repeat(50));

    const response = agent === "claude"
      ? await askClaude(prompt, contextFile)
      : await askGemini(prompt, contextFile);

    console.log(response);
    console.log("─".repeat(50));
    return;
  }

  // Interactive mode
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log("\n╔══════════════════════════════════════╗");
  console.log("║     AI Router — drnorfaizal.com      ║");
  console.log("║  Claude = code  |  Gemini = content  ║");
  console.log("╚══════════════════════════════════════╝\n");
  console.log("Commands: --claude, --gemini, --file <path>, exit\n");

  const ask = () => {
    rl.question("You → ", async (input) => {
      const trimmed = input.trim();
      if (!trimmed || trimmed === "exit") {
        console.log("\nGoodbye.\n");
        rl.close();
        return;
      }

      const agent = trimmed.startsWith("--claude") ? "claude"
                  : trimmed.startsWith("--gemini") ? "gemini"
                  : detectAgent(trimmed);

      const cleanPrompt = trimmed.replace(/^--(claude|gemini)\s*/, "");

      if (agent === "ambiguous") {
        console.log("\n⚠️  Not sure which AI to use. Add --claude or --gemini.\n");
        ask();
        return;
      }

      console.log(`\n[${agent === "claude" ? "Claude 🔵" : "Gemini 🟢"}]\n`);

      try {
        const response = agent === "claude"
          ? await askClaude(cleanPrompt)
          : await askGemini(cleanPrompt);
        console.log(response);
      } catch (err) {
        console.error(`\n❌ Error: ${err.message}\n`);
      }

      console.log("\n" + "─".repeat(50) + "\n");
      ask();
    });
  };

  ask();
}

main().catch(console.error);
