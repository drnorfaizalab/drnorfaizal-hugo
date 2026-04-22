// atomiser-server.js
// Local proxy server — keeps your API key out of the browser
// Run with: node atomiser-server.js
// Requires: npm install express cors dotenv @google/generative-ai

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
const PORT = 3131;

app.use(cors({ origin: ['http://localhost:1313', 'http://127.0.0.1:1313'] }));
app.use(express.json({ limit: '50kb' }));

// Health check
app.get('/health', (req, res) => {
  const hasKey = !!process.env.GEMINI_API_KEY;
  res.json({ status: 'ok', key_loaded: hasKey });
});

// Atomise endpoint
app.post('/atomise', async (req, res) => {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'GEMINI_API_KEY not found in .env' });
  }

  const { article } = req.body;
  if (!article || article.trim().length < 100) {
    return res.status(400).json({ error: 'Article too short — minimum 100 characters.' });
  }

  const SYSTEM = `You are the content atomiser for Dr Nor Faizal Ahmad Bahuri — Consultant Neurosurgeon & Interventional Pain Specialist, KPJ Tawakkal Specialist Hospital, Kuala Lumpur. Oxford DPhil. He writes in batik scrubs, not white coats.

BRAND VOICE
- Human first, credentials second
- Warm authority — never clinical distance, never corporate speak
- Specific and precise — name the procedure, the nerve, the moment
- Storytelling that earns trust before asking for anything
- Never a hospital spokesperson. Always Dr Faizal — the person

LANGUAGE RULES
- quote_card → English
- linkedin_essay → English (audience: GPs and specialists)
- reel_script → Bahasa Malaysia ONLY. This is spoken-word for TikTok/Instagram Reels. Write exactly how Dr Faizal speaks on camera — warm, direct, conversational Malaysian doctor. Use natural everyday BM, not textbook BM. Short sentences. Think out loud. Use "saya" not "kami". Allowed: natural code-switching for medical terms (e.g. "tumor otak", "saraf", "pembedahan"). Avoid: formal BM constructions, passive voice, government-report language, stiff connectors like "Oleh yang demikian" or "Sehubungan itu".
- carousel → Bahasa Malaysia ONLY. Patient-friendly. Simple words. Like explaining to a family member, not writing a medical textbook.

Return ONLY a raw JSON object. No markdown. No backticks. No explanation. No preamble. Just the JSON.

Use this exact schema:
{
  "quote_card": {
    "quote": "The single most powerful emotionally resonant sentence from the article. English. Under 20 words.",
    "context": "One-line framing for the quote. English. Under 10 words."
  },
  "linkedin_essay": {
    "hook": "First line that stops the scroll. Bold claim or provocative question. English. Under 15 words.",
    "body": "3 short paragraphs for GPs and specialists. Conversational peer-to-peer tone. English. Each paragraph 2-3 sentences. Separate paragraphs with double newlines.",
    "cta": "One natural closing line directing to the full article. English."
  },
  "reel_script": {
    "hook": "Opening spoken line for camera. Bahasa Malaysia. 5-8 words. Grabs attention in first second. Natural spoken BM, not written BM.",
    "body": "45-60 second spoken word script. Bahasa Malaysia throughout. Short punchy sentences. One patient-relevant analogy or story beat. Written as Dr Faizal actually speaks — warm, clear, human. No stiff formal BM.",
    "outro": "Soft call to action closing line. Bahasa Malaysia. Under 10 words."
  },
  "carousel": {
    "title_slide": "Short punchy carousel title. Bahasa Malaysia. 5-7 words.",
    "slides": [
      {"number": 1, "heading": "Slide heading in BM", "body": "2-3 sentence patient-friendly explanation in BM. Simple everyday language."},
      {"number": 2, "heading": "Slide heading in BM", "body": "2-3 sentence explanation in BM."},
      {"number": 3, "heading": "Slide heading in BM", "body": "2-3 sentence explanation in BM."},
      {"number": 4, "heading": "Slide heading in BM", "body": "2-3 sentence explanation in BM."},
      {"number": 5, "heading": "Slide heading in BM", "body": "2-3 sentence explanation in BM."}
    ],
    "closing_slide": "Final insight line in BM. One CTA line in BM."
  }
}`;

  try {
    const genai = new GoogleGenerativeAI(apiKey);
    const model = genai.getGenerativeModel({
      model: 'gemini-2.5-pro',
      systemInstruction: SYSTEM
    });

    const response = await model.generateContent('Atomise this article:\n\n' + article);
    const raw = response.response.text();
    const clean = raw.replace(/```json/g, '').replace(/```/g, '').trim();

    let parsed;
    try {
      parsed = JSON.parse(clean);
    } catch (e) {
      return res.status(500).json({ error: 'Failed to parse model response as JSON.', raw: clean.substring(0, 300) });
    }

    res.json({ result: parsed });

  } catch (err) {
    res.status(500).json({ error: err.message || 'Unexpected error calling Gemini API.' });
  }
});

app.listen(PORT, () => {
  console.log(`\n✓ Atomiser server running at http://localhost:${PORT}`);
  console.log(`✓ API key loaded: ${!!process.env.GEMINI_API_KEY}`);
  console.log(`✓ Accepting requests from http://localhost:1313\n`);
});
