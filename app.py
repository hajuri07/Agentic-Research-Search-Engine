import streamlit as st
import requests
import json
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Search",
    page_icon="🔍",
    layout="centered",
)

# ── Gold / dark theme styles ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* ── Global dark background ── */
html, body, [class*="css"], .stApp {
    font-family: 'Syne', sans-serif;
    background-color: #0e0e0e !important;
    color: #f0e6c8 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem;
    max-width: 760px;
    background-color: #0e0e0e !important;
}

/* Input box */
.stTextInput > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid #c9a84c !important;
    color: #f0e6c8 !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input::placeholder { color: #7a6a44 !important; }
.stTextInput > div > div > input:focus {
    box-shadow: 0 0 0 2px #c9a84c55 !important;
    border-color: #f0c040 !important;
}

/* Primary button → gold */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #c9a84c, #f0c040) !important;
    color: #0e0e0e !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    letter-spacing: 0.3px;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #f0c040, #ffe680) !important;
    transform: translateY(-1px);
}

/* Toggle */
.stToggle label { color: #c9a84c !important; font-size: 0.85rem; }

/* ── Header ── */
.app-header {
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin-bottom: 2rem;
}
.app-title {
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #f0c040, #c9a84c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.app-subtitle {
    font-size: 0.8rem;
    color: #7a6a44;
    font-weight: 400;
}

/* ── Status badge ── */
.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    padding: 3px 10px;
    border-radius: 4px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-blue  { background: #1a2a4a; color: #6ab0ff; border: 1px solid #2a4a7a; }
.badge-green { background: #0d2a1a; color: #4cdb80; border: 1px solid #1a5a30; }
.badge-gray  { background: #1e1e1e; color: #aaa;    border: 1px solid #333; }
.badge-amber { background: #2a1e00; color: #f0c040; border: 1px solid #5a4000; }

/* ── Tool chip ── */
.tool-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1a1500;
    border: 1px solid #c9a84c55;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.78rem;
    color: #c9a84c;
    font-family: 'IBM Plex Mono', monospace;
    margin: 0.5rem 0 1rem;
}

/* ── Result card ── */
.result-card {
    border: 1px solid #2a2200;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    background: #141100;
    transition: border-color .2s, box-shadow .2s;
}
.result-card:hover {
    border-color: #c9a84c;
    box-shadow: 0 0 12px #c9a84c22;
}
.result-title {
    font-weight: 700;
    font-size: 0.92rem;
    color: #f0d980;
    margin-bottom: 5px;
    line-height: 1.4;
}
.result-snippet {
    font-size: 0.8rem;
    color: #b0a080;
    line-height: 1.6;
    margin-bottom: 7px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.result-url {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #c9a84c;
    text-decoration: none;
    opacity: 0.8;
    word-break: break-all;
}
.result-url:hover { opacity: 1; text-decoration: underline; }

/* ── Summary box ── */
.summary-box {
    background: #100e00;
    border-left: 3px solid #c9a84c;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin-top: 1.5rem;
    font-size: 0.875rem;
    line-height: 1.75;
    color: #e0d0a0;
}
.summary-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    color: #c9a84c;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

/* ── Divider ── */
.slim-divider {
    border: none;
    border-top: 1px solid #2a2200;
    margin: 1.2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def render_markdown_as_html(text: str) -> str:
    """Convert basic markdown to HTML for clean rendering inside st.markdown."""
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # bullet list items (- or *)
    lines = text.split('\n')
    html_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('* ') or stripped.startswith('- '):
            html_lines.append(f"&bull; {stripped[2:]}<br>")
        elif stripped.startswith(('1.','2.','3.','4.','5.','6.','7.','8.','9.')):
            # numbered list
            parts = stripped.split('.', 1)
            html_lines.append(f"<strong>{parts[0]}.</strong>{parts[1] if len(parts)>1 else ''}<br>")
        elif stripped == '':
            html_lines.append('<br>')
        else:
            html_lines.append(stripped + ' ')
    return ''.join(html_lines)


BASE_URL = "https://agentic-research-search-engine.onrender.com/"


# ── App layout ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <span class="app-title">🔍 Research Search</span>
  <span class="app-subtitle">powered by FastAPI + LLM</span>
</div>
""", unsafe_allow_html=True)

query = st.text_input(
    label="",
    placeholder="e.g. latest research papers on transformers...",
    label_visibility="collapsed",
)

col1, col2 = st.columns([1, 5])
with col1:
    search_btn = st.button("Search", use_container_width=True, type="primary")
with col2:
    use_stream = st.toggle("Stream results", value=True)

st.markdown('<hr class="slim-divider">', unsafe_allow_html=True)

# ── Search execution ──────────────────────────────────────────────────────────
if search_btn and query.strip():

    # ── STREAMING mode ────────────────────────────────────────────────────────
    if use_stream:
        status_slot   = st.empty()
        tool_slot     = st.empty()
        results_slot  = st.empty()
        summary_slot  = st.empty()

        collected_results = []
        result_html_parts = []

        try:
            with requests.get(
                f"{BASE_URL}/search-stream",
                params={"query": query},
                stream=True,
                timeout=60,
            ) as resp:
                resp.raise_for_status()

                for raw_line in resp.iter_lines():
                    if not raw_line:
                        continue
                    try:
                        chunk = json.loads(raw_line)
                    except json.JSONDecodeError:
                        continue

                    status = chunk.get("status", "")

                    # — status badges —
                    if status == "started":
                        status_slot.markdown(
                            '<span class="badge badge-blue">⏳ starting</span>',
                            unsafe_allow_html=True,
                        )

                    elif status == "tool_selected":
                        tool = chunk.get("tool", "unknown")
                        status_slot.markdown(
                            '<span class="badge badge-blue">🔧 fetching results</span>',
                            unsafe_allow_html=True,
                        )
                        tool_slot.markdown(
                            f'<div class="tool-chip">🛠 tool &nbsp;→&nbsp; <strong>{tool}</strong></div>',
                            unsafe_allow_html=True,
                        )

                    elif status == "processing":
                        status_slot.markdown(
                            '<span class="badge badge-amber">⚙️ processing</span>',
                            unsafe_allow_html=True,
                        )

                    elif status == "summary":
                        status_slot.markdown(
                            '<span class="badge badge-green">✅ done</span>',
                            unsafe_allow_html=True,
                        )
                        raw_summary = chunk.get("summary", "")
                        clean_summary = render_markdown_as_html(raw_summary)
                        summary_slot.markdown(f"""
<div class="summary-box">
  <div class="summary-label">Summary</div>
  {clean_summary}
</div>
""", unsafe_allow_html=True)

                    elif status == "done":
                        pass  # badge already green

                    # — result card (no status key) —
                    elif "title" in chunk:
                        collected_results.append(chunk)
                        title   = chunk.get("title", "Untitled")
                        snippet = chunk.get("content", "")[:220]
                        url     = chunk.get("url", "")

                        result_html_parts.append(f"""
<div class="result-card">
  <div class="result-title">{title}</div>
  <div class="result-snippet">{snippet}{'…' if len(chunk.get('content',''))>220 else ''}</div>
  {'<a class="result-url" href="'+url+'" target="_blank">'+url+'</a>' if url else ''}
</div>""")
                        results_slot.markdown(
                            "".join(result_html_parts),
                            unsafe_allow_html=True,
                        )

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to FastAPI. Is it running on localhost:8000?")
        except Exception as e:
            st.error(f"❌ Error: {e}")

    # ── NON-STREAMING mode ────────────────────────────────────────────────────
    else:
        with st.spinner("Searching..."):
            try:
                resp = requests.get(
                    f"{BASE_URL}/search",
                    params={"query": query},
                    timeout=60,
                )
                data = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI. Is it running on localhost:8000?")
                st.stop()
            except Exception as e:
                st.error(f"❌ {e}")
                st.stop()

        if data.get("status") == "error":
            st.error(f"API error: {data.get('message')}")
            st.stop()

        # tool chip
        tool = data.get("tool_used", "unknown")
        st.markdown(
            f'<div class="tool-chip">🛠 tool &nbsp;→&nbsp; <strong>{tool}</strong></div>',
            unsafe_allow_html=True,
        )

        # result cards
        results = data.get("results", [])
        if results:
            cards_html = []
            for item in results:
                if not isinstance(item, dict):
                    continue
                title   = item.get("title", "Untitled")
                snippet = item.get("content", "")[:220]
                url     = item.get("url", "")
                cards_html.append(f"""
<div class="result-card">
  <div class="result-title">{title}</div>
  <div class="result-snippet">{snippet}{'…' if len(item.get('content',''))>220 else ''}</div>
  {'<a class="result-url" href="'+url+'" target="_blank">'+url+'</a>' if url else ''}
</div>""")
            st.markdown("".join(cards_html), unsafe_allow_html=True)
        else:
            st.info("No results found.")

        # summary
        raw_summary = data.get("summary", "")
        if raw_summary:
            clean_summary = render_markdown_as_html(raw_summary)
            st.markdown(f"""
<div class="summary-box">
  <div class="summary-label">Summary</div>
  {clean_summary}
</div>
""", unsafe_allow_html=True)

elif search_btn and not query.strip():
    st.warning("Please enter a search query.")
