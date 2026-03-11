import streamlit as st
import anthropic
import json
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Refined Communication",
    page_icon="✦",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Cinzel:wght@400;600&display=swap');

:root {
  --cream:   #f5f0e8;
  --ivory:   #faf7f2;
  --gold:    #b8960c;
  --gold-lt: #d4af37;
  --ink:     #1a1410;
  --muted:   #5a4e42;
  --rose:    #8b3a52;
  --rose-lt: #c4697e;
  --border:  #d6c9b8;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--cream) !important;
  font-family: 'EB Garamond', Georgia, serif !important;
  color: var(--ink) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

.masthead {
  text-align: center;
  padding: 2.5rem 1rem 0.5rem;
  border-bottom: 2px solid var(--gold);
  margin-bottom: 2rem;
}
.masthead-eyebrow {
  font-family: 'Cinzel', serif;
  font-size: 0.65rem;
  letter-spacing: 0.35em;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 0.4rem;
}
.masthead-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.9rem;
  font-weight: 300;
  font-style: italic;
  color: var(--ink);
  line-height: 1.1;
  margin: 0;
}
.masthead-sub {
  font-family: 'EB Garamond', serif;
  font-size: 0.95rem;
  color: var(--muted);
  margin-top: 0.5rem;
  font-style: italic;
}

.section-label {
  font-family: 'Cinzel', serif;
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 0.4rem;
}

textarea {
  font-family: 'EB Garamond', Georgia, serif !important;
  font-size: 1.05rem !important;
  background: var(--ivory) !important;
  color: var(--ink) !important;
  border: 1px solid var(--border) !important;
  border-radius: 2px !important;
  padding: 0.85rem 1rem !important;
}
textarea:focus { border-color: var(--gold) !important; box-shadow: none !important; }

.stButton > button {
  font-family: 'Cinzel', serif !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  background: var(--rose) !important;
  color: var(--cream) !important;
  border: none !important;
  border-radius: 1px !important;
  padding: 0.6rem 2rem !important;
  width: 100% !important;
  transition: background 0.2s ease !important;
}
.stButton > button:hover { background: var(--rose-lt) !important; }

.result-card {
  background: var(--ivory);
  border: 1px solid var(--border);
  border-left: 3px solid var(--rose);
  padding: 1.4rem 1.6rem;
  margin: 1rem 0;
  border-radius: 1px;
}
.result-card.gold-accent { border-left-color: var(--gold); }
.result-card h4 {
  font-family: 'Cinzel', serif;
  font-size: 0.58rem;
  letter-spacing: 0.3em;
  color: var(--gold);
  text-transform: uppercase;
  margin: 0 0 0.8rem 0;
}
.result-card p, .result-card li {
  font-family: 'EB Garamond', Georgia, serif;
  font-size: 1.05rem;
  line-height: 1.75;
  color: var(--ink);
  margin: 0 0 0.4rem 0;
}
.elevated-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.18rem;
  font-style: italic;
  line-height: 1.8;
  color: var(--ink);
}
.refined-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.05rem;
  font-style: italic;
  color: var(--muted);
  line-height: 1.7;
}

.vocab-item {
  background: #ede7dc;
  border-left: 2px solid var(--gold);
  padding: 0.55rem 0.9rem;
  margin: 0.45rem 0;
  border-radius: 1px;
}
.vocab-word {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--rose);
}
.vocab-body {
  font-size: 0.92rem;
  color: var(--muted);
  line-height: 1.6;
}

.ornament { text-align: center; color: var(--gold); font-size: 1.1rem; margin: 1.2rem 0; }
[data-testid="stSpinner"] p { font-style: italic; color: var(--muted) !important; }
</style>
""", unsafe_allow_html=True)

# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div class="masthead-eyebrow">✦ &nbsp; A Communication Atelier &nbsp; ✦</div>
  <div class="masthead-title">Refined<br>Communication</div>
  <div class="masthead-sub">Where the unpolished becomes the unforgettable.</div>
</div>
""", unsafe_allow_html=True)

# ── API Key: secrets → env → user input ──────────────────────────────────────
api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or os.environ.get("ANTHROPIC_API_KEY", "")

if not api_key:
    st.markdown('<div class="section-label">API Key Required</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        label_visibility="collapsed",
    )
    if not api_key:
        st.info("Enter your Anthropic API key above, or add `ANTHROPIC_API_KEY` to your Streamlit secrets.")
        st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ── Input area ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your Raw Composition</div>', unsafe_allow_html=True)
user_text = st.text_area(
    label="",
    value=st.session_state.input_text,
    placeholder="Type or paste your text here — however rough, however unvarnished.",
    height=150,
    key="text_input",
    label_visibility="collapsed",
)

col1, col2 = st.columns([3, 1])
with col1:
    refine_btn = st.button("✦  Refine & Illuminate", use_container_width=True)
with col2:
    clear_btn = st.button("Clear All", use_container_width=True)

if clear_btn:
    st.session_state.result = None
    st.session_state.input_text = ""
    st.rerun()

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a sophisticated dual-purpose language coach and elevated communication stylist.

When given a piece of text, respond ONLY in this exact JSON structure (no markdown, no backticks, no preamble — pure JSON only):

{
  "elevated_version": "The rephrased text in a composed, elegantly formidable style — calm, articulate, subtly authoritative. Uses elevated but realistic vocabulary. No sarcasm, no dramatics. Refined firmness only. Should feel poised, slightly imperious in a charming way, using rich vocabulary with deliberate cadence. Same message but elevated significantly.",
  "refined_version": "A polished, elevated version of the original — grammatically perfect, well-structured, sophisticated but not theatrical. This is what the person SHOULD have written.",
  "grammar_notes": "2-3 specific grammar or punctuation issues found in the original. Be precise and kind. If no issues, say so graciously.",
  "structure_feedback": "1-2 sentences on the logical flow, argument structure, or clarity of thought.",
  "improvement_tip": "One actionable, specific tip to elevate their communication going forward.",
  "vocab_upgrades": [
    {
      "original": "word or phrase they used",
      "elevated": "more sophisticated alternative",
      "meaning": "clear definition in plain English",
      "example": "A sentence using the elevated word naturally"
    }
  ]
}

vocab_upgrades: provide exactly 2-3 items. Choose words that are elevated but genuinely usable — not absurdly obscure. Realistic elevation, not theatrical excess."""


def call_claude(text: str, key: str) -> dict:
    client = anthropic.Anthropic(api_key=key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── Trigger ───────────────────────────────────────────────────────────────────
if refine_btn and user_text.strip():
    with st.spinner("Composing an elevated rendering…"):
        try:
            st.session_state.result = call_claude(user_text.strip(), api_key)
            st.session_state.input_text = user_text.strip()
        except json.JSONDecodeError as e:
            st.error(f"Could not parse the response. Please try again. ({e})")
        except Exception as e:
            st.error(f"Something went awry: {e}")

elif refine_btn and not user_text.strip():
    st.warning("You must provide something to refine.")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result
    st.markdown('<div class="ornament">· · · ✦ · · ·</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
      <h4>✦ &nbsp; Elevated Rendering</h4>
      <p class="elevated-text">{r.get('elevated_version','')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card gold-accent">
      <h4>✦ &nbsp; Your Polished Original</h4>
      <p class="refined-text">{r.get('refined_version','')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ornament">· · · ✦ · · ·</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Refinement Notes</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
      <h4>Grammar &amp; Mechanics</h4>
      <p>{r.get('grammar_notes','')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
      <h4>Structure &amp; Thought</h4>
      <p>{r.get('structure_feedback','')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card gold-accent">
      <h4>One Skill to Cultivate</h4>
      <p>{r.get('improvement_tip','')}</p>
    </div>
    """, unsafe_allow_html=True)

    vocab = r.get("vocab_upgrades", [])
    if vocab:
        st.markdown('<div class="ornament">· · · ✦ · · ·</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Lexical Elevation</div>', unsafe_allow_html=True)
        for v in vocab:
            st.markdown(f"""
            <div class="vocab-item">
              <div>
                <span class="vocab-word">{v.get('elevated','')}</span>
                &nbsp;<span style="color:var(--muted);font-size:0.85rem;">&#8592; instead of &ldquo;{v.get('original','')}&rdquo;</span>
              </div>
              <div class="vocab-body">
                <em>{v.get('meaning','')}</em><br>
                <span style="color:var(--ink);">{v.get('example','')}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="ornament" style="margin-top:2rem;">✦</div>', unsafe_allow_html=True)
