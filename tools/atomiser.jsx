import { useState, useRef } from "react";

const BRAND = {
  bg: "#0d0d0d",
  surface: "#141414",
  card: "#1a1a1a",
  border: "#2a2a2a",
  gold: "#c9a84c",
  goldLight: "#e8c97a",
  goldDim: "#8a6e2f",
  text: "#f0ece0",
  muted: "#888070",
  accent: "#d4a843",
};

const SYSTEM_PROMPT = `You are a medical content strategist for Dr Nor Faizal Ahmad Bahuri — a Consultant Neurosurgeon and Interventional Pain Specialist at KPJ Tawakkal Specialist Hospital, Kuala Lumpur. Oxford DPhil. He treats brain/spine tumours, headaches, migraines, and chronic pain through minimally invasive, precision-led care.

Brand voice: Human first, credentials second. Warm authority. Never a hospital. Always Dr Faizal — the person who saves lives and has a story worth telling.

Given a long-form Insight article, extract and produce EXACTLY this JSON structure (no markdown, no preamble, raw JSON only):

{
  "quote_card": {
    "quote": "The single most powerful, emotionally resonant sentence from the article. Under 20 words. Should work as a standalone thought.",
    "context": "A one-line framing for the quote (10 words max)"
  },
  "linkedin_essay": {
    "hook": "First line that stops the scroll. Bold claim or provocative question. Under 15 words.",
    "body": "3–4 short paragraphs expanding the core argument. Conversational, peer-to-peer tone for GPs and specialists. Each paragraph 2–3 sentences. Use line breaks between paragraphs.",
    "cta": "One closing line directing to the full article. Natural, not salesy."
  },
  "reel_script": {
    "hook": "Opening spoken line for camera. 5–8 words. Grabs attention in first second.",
    "body": "45–60 second script. Conversational Malay-English mix acceptable. Written as spoken word, not prose. Short punchy sentences. Include one patient-relevant analogy or story beat.",
    "outro": "Closing line with soft call to action. Under 10 words."
  },
  "carousel": {
    "title_slide": "Short punchy carousel title. 5–7 words.",
    "slides": [
      {"number": 1, "heading": "Short heading", "body": "2–3 sentence explanation. Clear and patient-friendly."},
      {"number": 2, "heading": "Short heading", "body": "2–3 sentence explanation."},
      {"number": 3, "heading": "Short heading", "body": "2–3 sentence explanation."},
      {"number": 4, "heading": "Short heading", "body": "2–3 sentence explanation."},
      {"number": 5, "heading": "Short heading", "body": "2–3 sentence explanation."}
    ],
    "closing_slide": "Final slide text. One insight + one CTA line."
  }
}`;

const TABS = [
  { id: "quote_card", label: "Quote Card", icon: "❝" },
  { id: "linkedin_essay", label: "LinkedIn", icon: "💼" },
  { id: "reel_script", label: "Reel Script", icon: "🎬" },
  { id: "carousel", label: "Carousel", icon: "📋" },
];

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button onClick={copy} style={{
      background: copied ? BRAND.goldDim : "transparent",
      border: `1px solid ${copied ? BRAND.gold : BRAND.border}`,
      color: copied ? BRAND.gold : BRAND.muted,
      padding: "6px 14px",
      borderRadius: "4px",
      fontSize: "11px",
      letterSpacing: "0.08em",
      cursor: "pointer",
      transition: "all 0.2s",
      fontFamily: "inherit",
    }}>
      {copied ? "COPIED" : "COPY"}
    </button>
  );
}

function QuoteCardView({ data }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
      <div style={{
        background: `linear-gradient(135deg, #1a1508 0%, #0d0d0d 60%, #1a1205 100%)`,
        border: `1px solid ${BRAND.goldDim}`,
        borderRadius: "12px",
        padding: "48px 40px",
        position: "relative",
        overflow: "hidden",
      }}>
        <div style={{
          position: "absolute", top: "20px", left: "32px",
          fontSize: "80px", color: BRAND.goldDim, opacity: 0.3,
          fontFamily: "Georgia, serif", lineHeight: 1,
        }}>❝</div>
        <p style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: "22px", lineHeight: 1.6,
          color: BRAND.text, margin: "20px 0 24px",
          position: "relative", zIndex: 1,
        }}>{data.quote}</p>
        <p style={{
          fontFamily: "'DM Sans', sans-serif",
          fontSize: "13px", color: BRAND.gold,
          letterSpacing: "0.12em", textTransform: "uppercase",
          margin: 0,
        }}>— {data.context}</p>
        <div style={{
          position: "absolute", bottom: "16px", right: "20px",
          fontSize: "11px", color: BRAND.goldDim, letterSpacing: "0.1em",
        }}>drnorfaizal.com</div>
      </div>
      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <CopyButton text={`"${data.quote}"\n\n— ${data.context}\n\ndrnorfaizal.com`} />
      </div>
    </div>
  );
}

function LinkedInView({ data }) {
  const full = `${data.hook}\n\n${data.body}\n\n${data.cta}`;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      <div style={{
        background: BRAND.card, border: `1px solid ${BRAND.border}`,
        borderRadius: "12px", padding: "32px",
      }}>
        <p style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: "18px", color: BRAND.gold, marginBottom: "20px",
          lineHeight: 1.5,
        }}>{data.hook}</p>
        {data.body.split("\n\n").map((p, i) => (
          <p key={i} style={{
            fontFamily: "'DM Sans', sans-serif",
            fontSize: "15px", color: BRAND.text,
            lineHeight: 1.7, marginBottom: "16px",
          }}>{p}</p>
        ))}
        <p style={{
          fontFamily: "'DM Sans', sans-serif",
          fontSize: "14px", color: BRAND.gold,
          borderTop: `1px solid ${BRAND.border}`,
          paddingTop: "16px", marginTop: "8px",
        }}>{data.cta}</p>
      </div>
      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <CopyButton text={full} />
      </div>
    </div>
  );
}

function ReelView({ data }) {
  const full = `HOOK:\n${data.hook}\n\n---\n\n${data.body}\n\n---\n\nOUTRO:\n${data.outro}`;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      <div style={{
        background: BRAND.card, border: `1px solid ${BRAND.border}`,
        borderRadius: "12px", overflow: "hidden",
      }}>
        <div style={{
          background: `linear-gradient(90deg, ${BRAND.goldDim}22, transparent)`,
          borderBottom: `1px solid ${BRAND.border}`,
          padding: "12px 24px", display: "flex", alignItems: "center", gap: "8px",
        }}>
          <span style={{ fontSize: "16px" }}>🎬</span>
          <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: "11px", color: BRAND.gold, letterSpacing: "0.1em", textTransform: "uppercase" }}>Opening Hook</span>
        </div>
        <div style={{ padding: "20px 24px" }}>
          <p style={{
            fontFamily: "'Playfair Display', Georgia, serif",
            fontSize: "20px", color: BRAND.text, lineHeight: 1.5, margin: 0,
          }}>{data.hook}</p>
        </div>
        <div style={{
          borderTop: `1px solid ${BRAND.border}`,
          background: `linear-gradient(90deg, #1a1205, transparent)`,
          padding: "12px 24px", display: "flex", alignItems: "center", gap: "8px",
        }}>
          <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: "11px", color: BRAND.muted, letterSpacing: "0.1em", textTransform: "uppercase" }}>Script Body</span>
        </div>
        <div style={{ padding: "20px 24px" }}>
          {data.body.split("\n").filter(Boolean).map((line, i) => (
            <p key={i} style={{
              fontFamily: "'DM Sans', sans-serif",
              fontSize: "15px", color: BRAND.text,
              lineHeight: 1.8, marginBottom: "10px",
            }}>{line}</p>
          ))}
        </div>
        <div style={{
          borderTop: `1px solid ${BRAND.border}`,
          background: `linear-gradient(90deg, ${BRAND.goldDim}22, transparent)`,
          padding: "16px 24px",
        }}>
          <p style={{
            fontFamily: "'DM Sans', sans-serif",
            fontSize: "14px", color: BRAND.gold, margin: 0, fontStyle: "italic",
          }}>{data.outro}</p>
        </div>
      </div>
      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <CopyButton text={full} />
      </div>
    </div>
  );
}

function CarouselView({ data }) {
  const [active, setActive] = useState(0);
  const slides = [
    { heading: data.title_slide, body: "Title slide", isTitle: true },
    ...data.slides,
    { heading: "Closing", body: data.closing_slide, isClosing: true },
  ];
  const full = `CAROUSEL: ${data.title_slide}\n\n` +
    data.slides.map(s => `${s.number}. ${s.heading}\n${s.body}`).join("\n\n") +
    `\n\nCLOSING:\n${data.closing_slide}`;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
        {slides.map((s, i) => (
          <button key={i} onClick={() => setActive(i)} style={{
            background: active === i ? BRAND.gold : "transparent",
            border: `1px solid ${active === i ? BRAND.gold : BRAND.border}`,
            color: active === i ? BRAND.bg : BRAND.muted,
            padding: "6px 14px", borderRadius: "4px",
            fontSize: "11px", letterSpacing: "0.08em",
            cursor: "pointer", fontFamily: "inherit",
            transition: "all 0.2s",
          }}>
            {s.isTitle ? "TITLE" : s.isClosing ? "CLOSE" : `SLIDE ${s.number}`}
          </button>
        ))}
      </div>
      <div style={{
        background: `linear-gradient(135deg, #1a1508 0%, #0d0d0d 100%)`,
        border: `1px solid ${BRAND.goldDim}`,
        borderRadius: "12px", padding: "48px 40px",
        minHeight: "220px", display: "flex",
        flexDirection: "column", justifyContent: "center",
        position: "relative",
      }}>
        <div style={{
          position: "absolute", top: "12px", right: "16px",
          fontFamily: "'DM Sans', sans-serif", fontSize: "10px",
          color: BRAND.goldDim, letterSpacing: "0.1em",
        }}>
          {active + 1} / {slides.length}
        </div>
        <p style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: slides[active].isTitle ? "26px" : "20px",
          color: slides[active].isTitle ? BRAND.gold : BRAND.text,
          lineHeight: 1.4, marginBottom: "16px",
        }}>{slides[active].heading}</p>
        {!slides[active].isTitle && (
          <p style={{
            fontFamily: "'DM Sans', sans-serif",
            fontSize: "15px", color: slides[active].isClosing ? BRAND.gold : BRAND.muted,
            lineHeight: 1.7, margin: 0,
          }}>{slides[active].body}</p>
        )}
        <div style={{
          position: "absolute", bottom: "16px", right: "20px",
          fontSize: "11px", color: BRAND.goldDim, letterSpacing: "0.1em",
        }}>drnorfaizal.com</div>
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", gap: "8px" }}>
          <button onClick={() => setActive(Math.max(0, active - 1))} disabled={active === 0} style={{
            background: "transparent", border: `1px solid ${BRAND.border}`,
            color: active === 0 ? BRAND.border : BRAND.muted,
            padding: "6px 16px", borderRadius: "4px", cursor: active === 0 ? "default" : "pointer",
            fontFamily: "inherit", fontSize: "13px",
          }}>←</button>
          <button onClick={() => setActive(Math.min(slides.length - 1, active + 1))} disabled={active === slides.length - 1} style={{
            background: "transparent", border: `1px solid ${BRAND.border}`,
            color: active === slides.length - 1 ? BRAND.border : BRAND.muted,
            padding: "6px 16px", borderRadius: "4px", cursor: active === slides.length - 1 ? "default" : "pointer",
            fontFamily: "inherit", fontSize: "13px",
          }}>→</button>
        </div>
        <CopyButton text={full} />
      </div>
    </div>
  );
}

export default function Atomiser() {
  const [article, setArticle] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState("quote_card");
  const [error, setError] = useState("");
  const [progress, setProgress] = useState("");

  const atomise = async () => {
    if (!article.trim() || article.trim().length < 100) {
      setError("Please paste your full Insight article (at least a few paragraphs).");
      return;
    }
    setError("");
    setResult(null);
    setLoading(true);
    setProgress("Reading your article...");

    try {
      setTimeout(() => setProgress("Extracting atoms..."), 1200);
      setTimeout(() => setProgress("Crafting platform formats..."), 2800);
      setTimeout(() => setProgress("Polishing outputs..."), 5000);

      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: SYSTEM_PROMPT,
          messages: [{ role: "user", content: `Here is the Insight article to atomise:\n\n${article}` }],
        }),
      });

      const data = await response.json();
      const raw = data.content?.find(b => b.type === "text")?.text || "";
      const clean = raw.replace(/```json|```/g, "").trim();
      const parsed = JSON.parse(clean);
      setResult(parsed);
      setActiveTab("quote_card");
    } catch (e) {
      setError("Something went wrong parsing the output. Try again or shorten your article.");
    } finally {
      setLoading(false);
      setProgress("");
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: BRAND.bg,
      fontFamily: "'DM Sans', sans-serif",
      color: BRAND.text,
      padding: "0",
    }}>
      <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet" />

      {/* Header */}
      <div style={{
        borderBottom: `1px solid ${BRAND.border}`,
        padding: "28px 40px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        background: `linear-gradient(90deg, #0d0d0d, #111008)`,
      }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <div style={{
              width: "6px", height: "32px",
              background: `linear-gradient(180deg, ${BRAND.gold}, ${BRAND.goldDim})`,
              borderRadius: "3px",
            }} />
            <div>
              <h1 style={{
                fontFamily: "'Playfair Display', Georgia, serif",
                fontSize: "22px", color: BRAND.gold,
                margin: 0, fontWeight: 400, letterSpacing: "0.02em",
              }}>Content Atomiser</h1>
              <p style={{
                fontSize: "12px", color: BRAND.muted,
                margin: "2px 0 0", letterSpacing: "0.08em",
              }}>DR NOR FAIZAL · drnorfaizal.com</p>
            </div>
          </div>
        </div>
        <div style={{
          fontSize: "11px", color: BRAND.goldDim,
          letterSpacing: "0.1em", textTransform: "uppercase",
        }}>One article → Four formats</div>
      </div>

      <div style={{ maxWidth: "860px", margin: "0 auto", padding: "40px 24px" }}>

        {/* Input */}
        {!result && (
          <div style={{ marginBottom: "32px" }}>
            <label style={{
              display: "block", marginBottom: "12px",
              fontSize: "12px", color: BRAND.gold,
              letterSpacing: "0.1em", textTransform: "uppercase",
            }}>
              Paste your Insight article
            </label>
            <textarea
              value={article}
              onChange={e => setArticle(e.target.value)}
              placeholder="Paste your full article here — the longer and richer the source, the better the atoms extracted..."
              rows={14}
              style={{
                width: "100%", boxSizing: "border-box",
                background: BRAND.surface,
                border: `1px solid ${article.length > 100 ? BRAND.goldDim : BRAND.border}`,
                borderRadius: "8px", padding: "20px",
                color: BRAND.text, fontSize: "15px",
                lineHeight: 1.7, resize: "vertical",
                fontFamily: "'DM Sans', sans-serif",
                outline: "none",
                transition: "border-color 0.2s",
              }}
            />
            {article.length > 0 && (
              <div style={{
                textAlign: "right", fontSize: "11px",
                color: article.length > 100 ? BRAND.goldDim : BRAND.muted,
                marginTop: "6px",
              }}>
                {article.length} characters
              </div>
            )}
            {error && (
              <p style={{ color: "#c0614a", fontSize: "13px", marginTop: "8px" }}>{error}</p>
            )}
            <button
              onClick={atomise}
              disabled={loading || article.trim().length < 100}
              style={{
                marginTop: "20px", width: "100%",
                background: loading || article.trim().length < 100
                  ? BRAND.surface
                  : `linear-gradient(135deg, ${BRAND.gold}, ${BRAND.goldDim})`,
                border: `1px solid ${BRAND.goldDim}`,
                color: loading || article.trim().length < 100 ? BRAND.muted : BRAND.bg,
                padding: "16px 32px",
                borderRadius: "8px",
                fontSize: "13px", letterSpacing: "0.12em",
                textTransform: "uppercase", fontWeight: 500,
                cursor: loading || article.trim().length < 100 ? "not-allowed" : "pointer",
                fontFamily: "inherit",
                transition: "all 0.3s",
              }}
            >
              {loading ? `${progress}` : "Atomise →"}
            </button>
          </div>
        )}

        {/* Results */}
        {result && (
          <div>
            {/* Reset */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "28px" }}>
              <div>
                <h2 style={{
                  fontFamily: "'Playfair Display', Georgia, serif",
                  fontSize: "20px", color: BRAND.gold, margin: 0, fontWeight: 400,
                }}>Your atoms are ready.</h2>
                <p style={{ fontSize: "13px", color: BRAND.muted, margin: "4px 0 0" }}>
                  4 formats extracted — copy each one to its platform.
                </p>
              </div>
              <button onClick={() => { setResult(null); setArticle(""); }} style={{
                background: "transparent", border: `1px solid ${BRAND.border}`,
                color: BRAND.muted, padding: "8px 16px", borderRadius: "4px",
                fontSize: "11px", letterSpacing: "0.08em",
                cursor: "pointer", fontFamily: "inherit",
              }}>
                ← NEW ARTICLE
              </button>
            </div>

            {/* Tabs */}
            <div style={{
              display: "flex", gap: "4px",
              borderBottom: `1px solid ${BRAND.border}`,
              marginBottom: "28px",
            }}>
              {TABS.map(tab => (
                <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
                  background: activeTab === tab.id
                    ? `linear-gradient(180deg, ${BRAND.goldDim}22, transparent)`
                    : "transparent",
                  border: "none",
                  borderBottom: `2px solid ${activeTab === tab.id ? BRAND.gold : "transparent"}`,
                  color: activeTab === tab.id ? BRAND.gold : BRAND.muted,
                  padding: "12px 20px", marginBottom: "-1px",
                  fontSize: "13px", letterSpacing: "0.06em",
                  cursor: "pointer", fontFamily: "inherit",
                  transition: "all 0.2s",
                }}>
                  <span style={{ marginRight: "6px" }}>{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Tab content */}
            {activeTab === "quote_card" && <QuoteCardView data={result.quote_card} />}
            {activeTab === "linkedin_essay" && <LinkedInView data={result.linkedin_essay} />}
            {activeTab === "reel_script" && <ReelView data={result.reel_script} />}
            {activeTab === "carousel" && <CarouselView data={result.carousel} />}
          </div>
        )}
      </div>
    </div>
  );
}
