#!/usr/bin/env node

/**
 * Curator — drnorfaizal.com
 * Uses Gemini to generate daily/weekly content briefs → posts to Notion
 *
 * Usage:
 *   node curator.js daily
 *   node curator.js weekly
 *   node curator.js daily --dry-run
 */

import { config } from "dotenv";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { Client } from "@notionhq/client";
import { markdownToBlocks } from "@tryfabric/martian";
import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
config({ path: resolve(dirname(fileURLToPath(import.meta.url)), "../.env") });

// Load .env from project root (one level up from ai-router/)
const __dirname = dirname(fileURLToPath(import.meta.url));
try {
  const env = readFileSync(resolve(__dirname, "../.env"), "utf-8");
  for (const line of env.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    const val = trimmed.slice(eq + 1).trim();
    if (key && !process.env[key]) process.env[key] = val;
  }
} catch {}

// ─── CONFIG ──────────────────────────────────────────────────────────────────

const GEMINI_MODEL = "gemini-2.5-pro";

const SYSTEM_PROMPT = `You are the content curator for Dr Nor Faizal Ahmad Bahuri —
Oxford-trained Consultant Neurosurgeon & Interventional Pain Specialist, Kuala Lumpur.
Voice: Human first, credentials second.
Bilingual: Bahasa Malaysia for reach, English for authority.
Platforms: TikTok, Instagram, YouTube, Facebook, LinkedIn.
Brand: Batik scrubs. Precision care. Approachable expertise.
Never clinical or corporate. Always Dr Faizal — the person.
Format output as clean Markdown with headers and bullet points.`;

// ─── PROMPTS ─────────────────────────────────────────────────────────────────

function dailyPrompt() {
  const today = new Date().toLocaleDateString("en-MY", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return `Generate today's content brief for Dr Faizal's social media.

**Date:** ${today}

Include:

## 1. TikTok / Reel (Bahasa Malaysia)
- Hook (first 3 seconds)
- Key message
- Call to action

## 2. Instagram Caption (English)
Educational angle, 150–200 words.

## 3. LinkedIn Post Idea
Professional authority angle — one paragraph + topic.

## 4. Story / Quote
Short-form thought for Instagram or Facebook Stories. One sentence.`;
}

function weeklyPrompt() {
  const weekOf = new Date().toLocaleDateString("en-MY", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return `Generate a full week content calendar for Dr Faizal's social media.

**Week of:** ${weekOf}

For each day Monday to Sunday, provide:
- **Theme** (e.g., spine, pain management, patient stories, behind-the-scenes, neurosurgery myth)
- **TikTok/Reel** — concept and hook in Bahasa Malaysia
- **Instagram** — post topic in English
- **LinkedIn** — professional angle

Format as a structured day-by-day plan with clear headers.`;
}

// ─── GEMINI ──────────────────────────────────────────────────────────────────

async function generate(type) {
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
  const model = genAI.getGenerativeModel({
    model: GEMINI_MODEL,
    systemInstruction: SYSTEM_PROMPT,
  });

  const prompt = type === "weekly" ? weeklyPrompt() : dailyPrompt();
  const result = await model.generateContent(prompt);
  return result.response.text();
}

// ─── NOTION ──────────────────────────────────────────────────────────────────

async function postToNotion(title, markdown) {
  const notion = new Client({ auth: process.env.NOTION_API_KEY });
  const parentId = process.env.NOTION_CURATOR_PAGE_ID;

  // Convert markdown → Notion blocks using martian
  const blocks = markdownToBlocks(markdown);

  // Notion allows max 100 children per request
  const page = await notion.pages.create({
    parent: { page_id: parentId },
    properties: {
      title: {
        title: [{ type: "text", text: { content: title } }],
      },
    },
    children: blocks.slice(0, 100),
  });

  // Append remaining blocks if content exceeds 100
  if (blocks.length > 100) {
    await notion.blocks.children.append({
      block_id: page.id,
      children: blocks.slice(100, 200),
    });
  }

  return page.url;
}

// ─── MAIN ────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const type = args[0];
  const dryRun = args.includes("--dry-run");

  if (!type || !["daily", "weekly"].includes(type)) {
    console.error("Usage: node curator.js [daily|weekly] [--dry-run]");
    process.exit(1);
  }

  if (!process.env.GEMINI_API_KEY) {
    console.error("❌ Missing GEMINI_API_KEY in .env");
    process.exit(1);
  }

  const dateStr = new Date().toLocaleDateString("en-MY", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  const title =
    type === "weekly"
      ? `📊 Weekly Plan — ${dateStr}`
      : `📡 Daily Brief — ${dateStr}`;

  console.log(`\n🟢 Generating ${type} brief with Gemini...\n`);

  const content = await generate(type);

  if (dryRun) {
    console.log(`── ${title} ──\n`);
    console.log(content);
    console.log("\n[dry run — Notion not updated]\n");
    return;
  }

  if (!process.env.NOTION_API_KEY || !process.env.NOTION_CURATOR_PAGE_ID) {
    console.error(
      "❌ Missing NOTION_API_KEY or NOTION_CURATOR_PAGE_ID in .env"
    );
    process.exit(1);
  }

  console.log("📝 Posting to Notion...");
  const url = await postToNotion(title, content);

  console.log(`\n✅ ${title}`);
  console.log(`   ${url}\n`);
}

main().catch((err) => {
  console.error(`\n❌ ${err.message}\n`);
  process.exit(1);
});
