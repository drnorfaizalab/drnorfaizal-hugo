#!/usr/bin/env node

/**
 * atomise — break a long-form post into platform-ready atomic content pieces
 * Each piece is saved separately to Raw Ideas Inbox in Notion.
 *
 * Usage:
 *   node tools/atomise.js path/to/index.en.md
 *   node tools/atomise.js "glioblastoma treatment journey"   (topic brief)
 */

import { GoogleGenerativeAI } from "@google/generative-ai";
import { Client } from "@notionhq/client";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { config } from "dotenv";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
config({ path: path.resolve(__dirname, "../.env") });

// ─── CONFIG ──────────────────────────────────────────────────────────────────

const MODEL = "gemini-2.5-pro";

const SYSTEM = `You are the content atomiser for Dr Nor Faizal Ahmad Bahuri —
Oxford-trained Consultant Neurosurgeon & Interventional Pain Specialist, KPJ Tawakkal KL.

Given a long-form insight post or topic brief, produce exactly 5 atomic pieces.
Format your entire response as valid JSON — an array of 5 objects.

Each object must have:
  "platform": one of TikTok | Instagram | LinkedIn | Facebook | WhatsApp
  "language": BM or EN
  "format":   short label (e.g. "Hook + Script", "Caption", "Post", "Broadcast Message")
  "content":  the ready-to-use copy

Platform rules:
- TikTok:    BM. Hook (1 punchy line) then 90-second script. Conversational, quick cuts.
- Instagram: BM. Caption with hook, 3-5 lines, 5 hashtags. Story-led.
- LinkedIn:  EN. Professional 150-200 word post. Patient outcome or clinical insight framing.
- Facebook:  BM. Patient-friendly 100-150 word post. Warm, educational, ends with soft CTA.
- WhatsApp:  BM. Broadcast message under 100 words. Direct, trustworthy, one clear CTA.

Brand voice: Human first, credentials second. Never clinical distance, never corporate.
He wears batik scrubs. He names the procedure, the nerve, the moment.`;

// ─── GEMINI ───────────────────────────────────────────────────────────────────

async function atomise(input) {
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
  const model = genAI.getGenerativeModel({ model: MODEL, systemInstruction: SYSTEM });

  const result = await model.generateContent(input);
  const raw = result.response.text().trim();

  // Strip markdown code fences if Gemini wraps the JSON
  const cleaned = raw.replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "").trim();
  return JSON.parse(cleaned);
}

// ─── NOTION ───────────────────────────────────────────────────────────────────

async function saveToInbox(platform, format, language, content, sourceLabel) {
  const notion = new Client({ auth: process.env.NOTION_API_KEY });
  const dbId = process.env.NOTION_RAW_IDEAS_DB_ID;
  if (!dbId) return;

  const title = `[${platform}/${language}] ${sourceLabel}`;
  const notes = content.length > 2000 ? content.slice(0, 1997) + "..." : content;
  const today = new Date().toISOString().slice(0, 10);

  const formatMap = {
    TikTok: "TikTok",
    Instagram: "Instagram",
    LinkedIn: "LinkedIn",
    Facebook: "Facebook",
    WhatsApp: "Not Sure Yet", // fallback — WhatsApp may not be a Notion option
  };

  await notion.pages.create({
    parent: { database_id: dbId },
    properties: {
      Idea: { title: [{ type: "text", text: { content: title } }] },
      Notes: { rich_text: [{ type: "text", text: { content: notes } }] },
      Status: { select: { name: "Raw" } },
      Format: { select: { name: formatMap[platform] ?? "Not Sure Yet" } },
      Source: { select: { name: "Atomiser" } },
      "Captured On": { date: { start: today } },
    },
  });
}

// ─── MAIN ─────────────────────────────────────────────────────────────────────

async function main() {
  const arg = process.argv.slice(2).join(" ").trim();

  if (!arg) {
    console.error('Usage: node tools/atomise.js path/to/post.md');
    console.error('       node tools/atomise.js "topic or brief"');
    process.exit(1);
  }

  let input;
  let sourceLabel;

  if (fs.existsSync(arg)) {
    input = fs.readFileSync(arg, "utf-8");
    sourceLabel = path.basename(path.dirname(arg)) || path.basename(arg);
  } else {
    input = arg;
    sourceLabel = arg.length > 60 ? arg.slice(0, 57) + "..." : arg;
  }

  console.log("\n⚛  Atomising content via Gemini...\n");

  let pieces;
  try {
    pieces = await atomise(input);
  } catch (err) {
    console.error("Failed to parse Gemini response as JSON:", err.message);
    process.exit(1);
  }

  for (const piece of pieces) {
    const { platform, language, format, content } = piece;
    console.log(`─── ${platform} (${language}) — ${format} ${"─".repeat(Math.max(0, 40 - platform.length - language.length - format.length))}`);
    console.log(content);
    console.log();

    try {
      await saveToInbox(platform, format, language, content, sourceLabel);
      console.log(`📝 Saved to Raw Ideas Inbox\n`);
    } catch (err) {
      console.warn(`⚠  Notion save failed for ${platform}: ${err.message}\n`);
    }
  }

  console.log(`Done. ${pieces.length} pieces saved for: ${sourceLabel}`);
}

main().catch(console.error);
