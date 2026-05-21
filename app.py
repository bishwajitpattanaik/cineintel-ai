import streamlit as st
from PIL import Image
import time
import json
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineIntel · Movie Intelligence Platform",
    page_icon=Image.open("logo.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,600;1,9..40,300&family=Space+Mono:wght@400;700&display=swap');

/* ── Root variables ── */
:root {
    --bg:      #E50914;
    --ink:     #0D0D0D;
    --white:   #FFFFFF;
    --offwhite:#FFF5F5;
    --gold:    #FFD700;
    --gold-lt: #FFE566;
    --dark:    #1A0000;
    --card-bg: rgba(0,0,0,0.75);
    --muted:   rgba(255,255,255,0.55);
    --border:  rgba(255,215,0,0.3);
}

/* ── Background ── */
html, body { margin: 0; padding: 0; }

[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.main {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 70% 50% at 80% 10%, rgba(255,255,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 10% 90%, rgba(0,0,0,0.25) 0%, transparent 60%) !important;
}

section[data-testid="stSidebar"],
[data-testid="stHeader"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1280px !important; }

/* ── Global text ── */
* { font-family: 'DM Sans', sans-serif !important; color: var(--white); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,215,0,0.4); border-radius: 3px; }

/* ═══════════════════════════════════════
   HERO
═══════════════════════════════════════ */
.hero-wrap {
    display: flex;
    align-items: flex-end;
    gap: 1.5rem;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}

.hero-icon { font-size: 3.2rem; line-height: 1; }
.hero-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 4.2rem !important;
    line-height: 0.95 !important;
    letter-spacing: 0.04em;
    color: var(--white) !important;
    margin: 0 !important; padding: 0 !important;
    text-shadow: 0 2px 20px rgba(0,0,0,0.4);
}
.hero-sub {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.65);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.hero-pill {
    margin-left: auto;
    padding: 0.3rem 0.8rem;
    border: 1px solid var(--gold);
    border-radius: 2px;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--gold) !important;
    font-family: 'Space Mono', monospace !important;
    align-self: flex-start;
    margin-top: 0.6rem;
    background: rgba(255,215,0,0.08);
}

/* ═══════════════════════════════════════
   SECTION LABELS
═══════════════════════════════════════ */
.section-label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold) !important;
    margin-bottom: 0.6rem;
    display: block;
}

/* ═══════════════════════════════════════
   TEXTAREA
═══════════════════════════════════════ */
[data-testid="stTextArea"] textarea {
    background: rgba(0,0,0,0.55) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 3px !important;
    color: #FFFFFF !important;
    caret-color: var(--gold) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.7 !important;
    padding: 1rem 1.2rem !important;
    resize: vertical !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(255,255,255,0.3) !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(255,215,0,0.15) !important;
    outline: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

/* ═══════════════════════════════════════
   BUTTONS
═══════════════════════════════════════ */
[data-testid="stButton"] button:focus,
[data-testid="stButton"] button:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}

[data-testid="stButton"] button {
    background: rgba(0,0,0,0.65) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 3px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    transition: background 0.2s, border-color 0.2s, color 0.2s, transform 0.1s !important;
    line-height: 1.4 !important;
    width: 100% !important;
}

[data-testid="stButton"] button p,
[data-testid="stButton"] button span,
[data-testid="stButton"] button div {
    color: #FFFFFF !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    font-size: inherit !important;
    font-family: inherit !important;
    letter-spacing: inherit !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

[data-testid="stButton"] button:hover {
    background: rgba(255,215,0,0.2) !important;
    border-color: var(--gold) !important;
    color: var(--gold) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] button:hover p,
[data-testid="stButton"] button:hover span,
[data-testid="stButton"] button:hover div {
    color: var(--gold) !important;
}
[data-testid="stButton"] button:active { transform: translateY(0) !important; }

/* Extract button */
.extract-btn-wrap [data-testid="stButton"] button {
    background: #FFFFFF !important;
    color: #E50914 !important;
    border: none !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 2.2rem !important;
    letter-spacing: 0.15em !important;
    width: auto !important;
}
.extract-btn-wrap [data-testid="stButton"] button p,
.extract-btn-wrap [data-testid="stButton"] button span,
.extract-btn-wrap [data-testid="stButton"] button div {
    color: #E50914 !important;
}
.extract-btn-wrap [data-testid="stButton"] button:hover {
    background: var(--gold) !important;
    color: #0D0D0D !important;
}
.extract-btn-wrap [data-testid="stButton"] button:hover p,
.extract-btn-wrap [data-testid="stButton"] button:hover span,
.extract-btn-wrap [data-testid="stButton"] button:hover div {
    color: #0D0D0D !important;
}

/* ═══════════════════════════════════════
   HOW IT WORKS PANEL
═══════════════════════════════════════ */
.hiw-panel {
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 4px;
    padding: 1.4rem 1.5rem;
}
.hiw-step {
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    margin-bottom: 1rem;
}
.hiw-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--gold);
    background: rgba(255,215,0,0.1);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 2px;
    padding: 0.18rem 0.45rem;
    min-width: 1.7rem;
    text-align: center;
    flex-shrink: 0;
    margin-top: 0.1rem;
}
.hiw-title { font-weight: 600; font-size: 0.88rem; color: #FFF; }
.hiw-desc  { font-size: 0.78rem; color: rgba(255,255,255,0.5); margin-top: 0.1rem; }

.fields-panel {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 3px;
    padding: 0.9rem 1rem;
    margin-top: 1.2rem;
}
.field-chip {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 2px;
    padding: 0.18rem 0.5rem;
    margin: 0.15rem 0.2rem 0.15rem 0;
    color: rgba(255,255,255,0.75) !important;
}

/* ═══════════════════════════════════════
   RESULT CARD
═══════════════════════════════════════ */
.result-card {
    background: rgba(0,0,0,0.82);
    border-radius: 4px;
    padding: 2.2rem 2.5rem;
    margin-top: 2rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--bg), var(--gold));
}
.result-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 3rem !important;
    letter-spacing: 0.03em;
    line-height: 1;
    color: #FFFFFF !important;
    margin: 0 0 0.2rem !important;
}
.result-year {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: var(--gold);
    letter-spacing: 0.12em;
}
.result-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1.4rem 0;
}
.result-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem 2rem;
    margin-bottom: 1.4rem;
}
.meta-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold) !important;
    margin-bottom: 0.3rem;
}
.meta-value { font-size: 0.92rem; color: #FFFFFF; line-height: 1.4; }
.genre-chip {
    display: inline-block;
    border: 1px solid rgba(255,215,0,0.45);
    border-radius: 2px;
    padding: 0.14rem 0.5rem;
    font-size: 0.68rem;
    font-family: 'Space Mono', monospace;
    color: var(--gold-lt) !important;
    margin: 0.15rem 0.18rem 0.15rem 0;
    letter-spacing: 0.04em;
}
.rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,215,0,0.12);
    border: 1px solid rgba(255,215,0,0.35);
    border-radius: 2px;
    padding: 0.28rem 0.65rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem;
    color: var(--gold-lt) !important;
}
.rating-star { color: var(--gold) !important; }
.rating-bar-track {
    margin-top: 0.55rem;
    height: 3px;
    background: rgba(255,255,255,0.08);
    border-radius: 2px;
    overflow: hidden;
}
.cast-list { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.2rem; }
.cast-name {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 2px;
    padding: 0.18rem 0.55rem;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.85) !important;
}
.summary-text {
    font-size: 0.93rem;
    line-height: 1.78;
    color: rgba(255,255,255,0.75) !important;
    font-style: italic;
    border-left: 2px solid var(--gold);
    padding-left: 1.1rem;
    margin-top: 0.4rem;
}

/* ═══════════════════════════════════════
   TABS
═══════════════════════════════════════ */
[data-testid="stTabs"] {
    background: transparent !important;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.12) !important;
    gap: 0.5rem;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.4) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.5rem 1rem !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 0 !important;
}

/* ═══════════════════════════════════════
   CODE BLOCK (JSON tab)
═══════════════════════════════════════ */
[data-testid="stCode"] pre,
[data-testid="stCodeBlock"] pre {
    background: rgba(0,0,0,0.7) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 3px !important;
    color: #E6E6E6 !important;
}

/* ═══════════════════════════════════════
   DOWNLOAD BUTTON
═══════════════════════════════════════ */
[data-testid="stDownloadButton"] button {
    background: rgba(255,215,0,0.12) !important;
    color: var(--gold) !important;
    border: 1px solid rgba(255,215,0,0.4) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(255,215,0,0.25) !important;
}

/* ═══════════════════════════════════════
   ERROR CARD
═══════════════════════════════════════ */
.error-card {
    background: rgba(0,0,0,0.5);
    border: 1px solid rgba(255,80,80,0.5);
    border-radius: 3px;
    padding: 1rem 1.3rem;
    color: #FF8080 !important;
    font-size: 0.85rem;
    font-family: 'Space Mono', monospace;
    margin-top: 1.5rem;
}

/* ═══════════════════════════════════════
   SPINNER
═══════════════════════════════════════ */
[data-testid="stSpinner"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    color: var(--gold) !important;
}

/* ═══════════════════════════════════════
   SUCCESS TOAST
═══════════════════════════════════════ */
.success-toast {
    background: rgba(0,120,60,0.7);
    border: 1px solid rgba(0,200,100,0.4);
    border-radius: 3px;
    padding: 0.7rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #80FFB0 !important;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)


# ── Load env & model ─────────────────────────────────────────────────────────
load_dotenv()

@st.cache_resource(show_spinner=False)
def get_model():
    from langchain_mistralai import ChatMistralAI
    return ChatMistralAI(model="mistral-small-2506")

# ── Pydantic schema ──────────────────────────────────────────────────────────
class MovieInfo(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: List[str] = []
    director: Optional[str] = None
    cast: List[str] = []
    ratings: Optional[float] = None
    summary: str = ""

parser = PydanticOutputParser(pydantic_object=MovieInfo)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Extract movie information from the paragraph.\n{format_instructions}"),
    ("human", "{paragraph}"),
])

# ── Extraction ───────────────────────────────────────────────────────────────
def extract_movie_info(paragraph: str) -> MovieInfo:
    model = get_model()
    final_prompt = prompt_template.invoke({
        "paragraph": paragraph,
        "format_instructions": parser.get_format_instructions(),
    })
    response = model.invoke(final_prompt)
    return parser.parse(response.content)

# ── Rating bar ───────────────────────────────────────────────────────────────
def rating_bar_html(rating: float) -> str:
    pct = min(rating / 10 * 100, 100)
    filled = int(round(rating / 2))
    stars = "★" * filled + "☆" * (5 - filled)
    bar_style = (
        f"width:{pct}%;height:100%;"
        "background:linear-gradient(90deg,#E50914,#FFD700);"
        "border-radius:2px;"
    )
    return (
        f'<div style="margin-top:0.3rem;">'
        f'  <div style="display:flex;align-items:center;gap:0.8rem;">'
        f'    <span style="display:inline-flex;align-items:center;gap:0.35rem;'
        f'      background:rgba(255,215,0,0.12);border:1px solid rgba(255,215,0,0.35);'
        f'      border-radius:2px;padding:0.28rem 0.65rem;font-family:Space Mono,monospace;'
        f'      font-size:0.95rem;color:#FFE566;">'
        f'      <span style="color:#FFD700;">★</span> {rating:.1f} / 10'
        f'    </span>'
        f'    <span style="font-size:0.78rem;color:rgba(255,255,255,0.3);'
        f'      font-family:Space Mono,monospace;">{stars}</span>'
        f'  </div>'
        f'  <div style="margin-top:0.55rem;height:3px;background:rgba(255,255,255,0.08);'
        f'    border-radius:2px;overflow:hidden;">'
        f'    <div style="{bar_style}"></div>'
        f'  </div>'
        f'</div>'
    )

# ── Field chips ───────────────────────────────────────────────────────────────
FIELD_NAMES = ['title', 'release_year', 'genre', 'director', 'cast', 'ratings', 'summary']
FIELDS_HTML = "".join(
    f'<span style="display:inline-block;font-family:Space Mono,monospace;font-size:0.65rem;'
    f'background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);'
    f'border-radius:2px;padding:0.18rem 0.5rem;margin:0.15rem 0.2rem 0.15rem 0;'
    f'color:rgba(255,255,255,0.75);">{f}</span>'
    for f in FIELD_NAMES
)

# ── Samples ──────────────────────────────────────────────────────────────────
SAMPLES = {
    "Inception": (
        "Christopher Nolan's 2010 sci-fi thriller Inception stars Leonardo DiCaprio as Dom Cobb, "
        "a skilled thief who enters the dreams of others to steal secrets. Joined by Joseph Gordon-Levitt, "
        "Elliot Page, and Tom Hardy, the film earned an IMDb rating of 8.8 and is celebrated for its "
        "mind-bending narrative and Hans Zimmer's iconic score."
    ),
    "Parasite": (
        "Bong Joon-ho's 2019 dark comedy thriller Parasite follows the Kim family who scheme to become "
        "employed by the wealthy Park family. Starring Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, and "
        "Choi Woo-shik, the film won four Academy Awards including Best Picture and holds a 8.5 on IMDb."
    ),
    "The Godfather": (
        "Francis Ford Coppola directed The Godfather in 1972, a crime drama epic based on Mario Puzo's "
        "novel. Marlon Brando, Al Pacino, James Caan, and Diane Keaton star in this story of the powerful "
        "Corleone mafia family. Widely considered one of the greatest films ever made, it holds a 9.2 "
        "rating on IMDb."
    ),
    "Interstellar": (
        "Released in 2014, Interstellar is a science fiction epic directed by Christopher Nolan. "
        "Matthew McConaughey, Anne Hathaway, and Jessica Chastain lead the cast in this story about "
        "astronauts who travel through a wormhole near Saturn in search of a new home for humanity. "
        "The film has a rating of 8.7 and blends hard science with emotional storytelling."
    ),
}

# ════════════════════════════════════════════════════════════════════════════
#  PAGE LAYOUT
# ════════════════════════════════════════════════════════════════════════════

# Hero
st.markdown(
    '<div class="hero-wrap">'
    '  <div>'
    '    <div class="hero-title">CineIntel</div>'
    '    <div class="hero-sub">Cinematic Intelligence Platform &nbsp;·&nbsp; Mistral LLM &nbsp;·&nbsp; Structural Extraction</div>'
    '  </div>'
    '</div>',
    unsafe_allow_html=True,
)

# Two-column layout
col_left, col_right = st.columns([5, 4], gap="large")

# ── LEFT: Input ──────────────────────────────────────────────────────────────
with col_left:
    st.markdown('<span class="section-label">Input Paragraph</span>', unsafe_allow_html=True)

    if "para_text" not in st.session_state:
        st.session_state["para_text"] = ""

    paragraph = st.text_area(
        label="paragraph",
        value=st.session_state["para_text"],
        height=200,
        placeholder=(
            "Paste any paragraph describing a movie — reviews, Wikipedia excerpts, "
            "IMDb summaries, or anything"
        ),
    )
    st.session_state["para_text"] = paragraph

    st.markdown('<span class="section-label" style="margin-top:1.1rem;display:block;">Try a sample</span>', unsafe_allow_html=True)
    sc = st.columns(4)
    for idx, (label, text) in enumerate(SAMPLES.items()):
        with sc[idx]:
            if st.button(label, key=f"sample_{label}", use_container_width=True):
                st.session_state["para_text"] = text
                st.rerun()

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    st.markdown('<div class="extract-btn-wrap">', unsafe_allow_html=True)
    extract_clicked = st.button("▶  Extract Movie Data", use_container_width=False, key="extract_btn")
    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: How it works ──────────────────────────────────────────────────────
with col_right:
    st.markdown('<span class="section-label">How It Works</span>', unsafe_allow_html=True)

    steps = [
        ("01", "Paste any movie text",      "Reviews, descriptions, Wikipedia excerpts — any free-form prose"),
        ("02", "Mistral LLM parses it",     "LangChain prompt template + Mistral-small-2506 extracts structured data"),
        ("03", "Pydantic validates output", "Type-safe MovieInfo schema guarantees reliable, structured results"),
        ("04", "Rich UI renders results",   "Visual cards, JSON export, and metadata grids displayed instantly"),
    ]
    steps_html = '<div class="hiw-panel">'
    for num, title, desc in steps:
        steps_html += (
            f'<div class="hiw-step">'
            f'  <div class="hiw-num">{num}</div>'
            f'  <div>'
            f'    <div class="hiw-title">{title}</div>'
            f'    <div class="hiw-desc">{desc}</div>'
            f'  </div>'
            f'</div>'
        )
    steps_html += (
        f'<div class="fields-panel">'
        f'  <div class="meta-label" style="margin-bottom:0.5rem;">Extracted Fields</div>'
        f'  <div>{FIELDS_HTML}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(steps_html, unsafe_allow_html=True)


# ── Extraction logic ──────────────────────────────────────────────────────────
if extract_clicked:
    current_text = st.session_state.get("para_text", "").strip()
    if not current_text:
        st.markdown('<div class="error-card">⚠ Please enter a paragraph before extracting.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Contacting Mistral · Parsing structured data · Validating schema…"):
            t0 = time.time()
            try:
                movie: MovieInfo = extract_movie_info(current_text)
                elapsed = time.time() - t0
                st.session_state["last_movie"] = movie
                st.session_state["last_elapsed"] = elapsed
                st.session_state["last_error"] = None
            except Exception as e:
                st.session_state["last_movie"] = None
                st.session_state["last_error"] = str(e)


# ── Result display ────────────────────────────────────────────────────────────
if st.session_state.get("last_error"):
    st.markdown(
        f'<div class="error-card">⚠ Extraction failed: {st.session_state["last_error"]}</div>',
        unsafe_allow_html=True,
    )

elif st.session_state.get("last_movie"):
    movie: MovieInfo = st.session_state["last_movie"]
    elapsed: float = st.session_state.get("last_elapsed", 0)
    year_str = str(movie.release_year) if movie.release_year else "—"

    st.markdown(
        f'<div class="success-toast">✓ Extraction Completed Successfully &nbsp;·&nbsp; {elapsed:.2f}s</div>',
        unsafe_allow_html=True,
    )

    tab_visual, tab_json = st.tabs(["  ◈  Visual Card  ", "  { }  JSON Export  "])

    with tab_visual:
        genres_html = "".join(
            f'<span class="genre-chip">{g}</span>' for g in movie.genre
        ) or "<span style='opacity:0.4'>—</span>"

        cast_html = "".join(
            f'<span class="cast-name">{c}</span>' for c in movie.cast
        ) if movie.cast else "<span style='opacity:0.4'>—</span>"

        rating_section = rating_bar_html(movie.ratings) if movie.ratings else (
            '<span style="color:rgba(255,255,255,0.35);font-size:0.85rem;">N/A</span>'
        )

        director_val = movie.director or "—"
        elapsed_label = f"Extracted in {elapsed:.2f}s"
        year_label = f"📅 {year_str}" if year_str != "—" else ""

        card = (
            f'<div class="result-card">'
            f'  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">'
            f'    <div>'
            f'      <div class="result-title">{movie.title}</div>'
            f'      <div class="result-year">{year_label}'
            f'        <span style="color:rgba(255,255,255,0.25);margin:0 0.4rem;">·</span>'
            f'        <span style="font-family:Space Mono,monospace;font-size:0.62rem;'
            f'          color:rgba(255,255,255,0.3);">{elapsed_label}</span>'
            f'      </div>'
            f'    </div>'
            f'    <div style="text-align:right;padding-top:0.3rem;">{genres_html}</div>'
            f'  </div>'
            f'  <hr class="result-divider"/>'
            f'  <div class="result-meta-grid">'
            f'    <div>'
            f'      <div class="meta-label">Director</div>'
            f'      <div class="meta-value">{director_val}</div>'
            f'    </div>'
            f'    <div>'
            f'      <div class="meta-label">Rating</div>'
            f'      {rating_section}'
            f'    </div>'
            f'    <div style="grid-column:span 2;">'
            f'      <div class="meta-label">Cast</div>'
            f'      <div class="cast-list">{cast_html}</div>'
            f'    </div>'
            f'  </div>'
            f'  <hr class="result-divider"/>'
            f'  <div>'
            f'    <div class="meta-label">Summary</div>'
            f'    <div class="summary-text">{movie.summary}</div>'
            f'  </div>'
            f'</div>'
        )
        st.markdown(card, unsafe_allow_html=True)

    with tab_json:
        movie_dict = {
            "title": movie.title,
            "release_year": movie.release_year,
            "genre": movie.genre,
            "director": movie.director,
            "cast": movie.cast,
            "ratings": movie.ratings,
            "summary": movie.summary,
        }
        json_str = json.dumps(movie_dict, indent=2, ensure_ascii=False)
        st.code(json_str, language="json")
        st.download_button(
            label="↓  Download JSON",
            data=json_str,
            file_name=f"{movie.title.lower().replace(' ', '_')}_info.json",
            mime="application/json",
        )


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.footer-new {
    margin-top: 3.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.8rem;
}
.footer-left {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: rgba(255,255,255,0.65);
    letter-spacing: 0.07em;
}
.footer-right {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.07em;
}
.footer-right span {
    color: rgba(255,255,255,0.65);
}
.footer-link {
    color: rgba(255,255,255,0.65) !important;
    text-decoration: none !important;
    letter-spacing: 0.1em;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    transition: color 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}
.footer-link:hover {
    color: #FFD700 !important;
}
.footer-name {
    color: rgba(255,255,255,0.65);
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
}
</style>
<div class="footer-new">
  <div class="footer-left">
    CineIntel &nbsp;·&nbsp; 2026
  </div>
  <div class="footer-right">
    <span class="footer-name">Made by Bishwajit Pattanaik</span>
    <span>·</span>
    <a class="footer-link" href="https://www.linkedin.com/in/bishwajit-pattanaik-717818320/" target="_blank">
      LinkedIn
    </a>
    <span>·</span>
    <a class="footer-link" href="https://github.com/bishwajitpattanaik" target="_blank">
      GitHub
    </a>
  </div>
</div>
""", unsafe_allow_html=True)
