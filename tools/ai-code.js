#!/usr/bin/env node

/**
 * ai-code — Claude for code troubleshooting
 * Usage:
 *   node ai-code.js "fix this bug" [--file path/to/file]
 *   node ai-code.js          (interactive mode)
 */

import Anthropic from "@anthropic-ai/sdk";
import readline from "readline";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { config } from "dotenv";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
config({ path: path.resolve(__dirname, "../.env") });

// ─── CONFIG ──────────────────────────────────────────────────────────────────

const MODEL = "claude-sonnet-4-20250514";

const SYSTEM = `You are the backend and code specialist for drnorfaizal.com —
a neurosurgeon's personal brand website and content system.
Your role: write, review, debug, and refactor code only.
Stack: HTML/CSS/JS, Node.js, Hugo, GitHub Actions, Python.
Be precise, concise, and production-ready. No fluff.`;

// ─── CLAUDE CALL ─────────────────────────────────────────────────────────────

async function ask(prompt, contextFile = null) {
  const client = new Anthropic();

  let userContent = prompt;
  if (contextFile && fs.existsSync(contextFile)) {
    const fileContent = fs.readFileSync(contextFile, "utf-8");
    userContent = `File: ${path.basename(contextFile)}\n\`\`\`\n${fileContent}\n\`\`\`\n\n${prompt}`;
  }

  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 2048,
    system: SYSTEM,
    messages: [{ role: "user", content: userContent }],
  });

  return response.content[0].text;
}

// ─── CLI ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length > 0) {
    const fileFlag = args.indexOf("--file");
    const contextFile = fileFlag !== -1 ? args[fileFlag + 1] : null;
    const prompt = args.find((a, i) => !a.startsWith("--") && args[i - 1] !== "--file");

    if (!prompt) {
      console.error('Usage: node ai-code.js "your prompt" [--file path/to/file]');
      process.exit(1);
    }

    console.log("\n🔵 Claude (code)\n" + "─".repeat(50));
    const response = await ask(prompt, contextFile);
    console.log(response);
    console.log("─".repeat(50) + "\n");
    return;
  }

  // Interactive mode
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log("\n╔══════════════════════════════════════╗");
  console.log("║     ai-code — Claude for code        ║");
  console.log("╚══════════════════════════════════════╝\n");

  const loop = () => {
    rl.question("You → ", async (input) => {
      const trimmed = input.trim();
      if (!trimmed || trimmed === "exit") {
        console.log("\nGoodbye.\n");
        rl.close();
        return;
      }

      console.log("\n[Claude 🔵]\n");
      try {
        const response = await ask(trimmed);
        console.log(response);
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
