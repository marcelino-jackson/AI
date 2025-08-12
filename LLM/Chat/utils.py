from __future__ import annotations
import streamlit as st
from datetime import datetime

PRIMARY_MAX_WIDTH = 1200
USER_BG = "#1f2937"
ASSIST_BG = "#111827"
BORDER = "#2a2f3a"

def inject_css() -> None:
    """Global styling for hamburger, boxes, headers, prompt, and sidebar spacing."""
    st.markdown(
        f"""
        <style>
        /* Center main content */
        .block-container {{
            max-width: {PRIMARY_MAX_WIDTH}px;
            margin: 0 auto;
        }}

        /* Hide Streamlit toolbar (Deploy, etc.) */
        [data-testid="stToolbar"],
        header [data-testid="stHeaderActionElements"] {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* ======== Sidebar padding & spacing ======== */
        section[data-testid="stSidebar"] > div:first-child {{
            padding-right: 16px;               /* keep controls away from main column */
        }}
        section[data-testid="stSidebar"] .stButton {{
            margin-bottom: 20px !important;    /* gap after + New button */
        }}
        section[data-testid="stSidebar"] label {{
            margin-top: 8px !important;        /* space before "Model" label */
            margin-bottom: 6px !important;
        }}
        section[data-testid="stSidebar"] [data-baseweb="select"] {{
            margin-bottom: 24px !important;    /* space before History */
        }}
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] [data-baseweb="select"] {{
            width: 100% !important;
            box-sizing: border-box;
        }}

        /* ======== Chat bubbles ======== */
        [data-testid="stChatMessage"] {{
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 14px 16px;
            margin: 8px 0 16px 0;
            background: {ASSIST_BG};
        }}
        [data-testid="stChatMessage-user"] {{
            background: {USER_BG};
        }}

        /* ======== Single-row section headers (Prompting / Results) ======== */
        [data-testid="stChatMessage"] .section-header {{
            width: 100%;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 12px;
        }}
        [data-testid="stChatMessage"] .section-title {{
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: 0.2px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        [data-testid="stChatMessage"] .section-meta {{
            margin-left: auto;
            opacity: 0.7;
            font-size: 0.95rem;
            white-space: nowrap;
        }}
        [data-testid="stChatMessage"] .model-chip {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.06);
            font-weight: 600;
            font-size: 0.95rem;
            line-height: 1.2;
        }}
        [data-testid="stChatMessage"] p {{
            margin-top: 0.15rem;
        }}

        /* ======== Prompt (chat input) — rectangular and aligned ======== */
        /* IMPORTANT: remove the previous negative margin so it doesn't overlap the sidebar */
        div[data-testid="stChatInput"] {{
            margin-left: 0;                     /* was -72px */
            width: 100% !important;             /* no overflow into sidebar */
        }}
        div[data-testid="stChatInput"] > div {{
            display: flex;
            align-items: center;
            min-height: 116px;
            padding: 0 16px;
            width: 100% !important;

            border-radius: 8px !important;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.15);
            background-color: rgba(255,255,255,0.04);
            box-shadow: none !important;
        }}
        div[data-testid="stChatInput"] [data-baseweb],
        div[data-testid="stChatInput"] [data-baseweb] * {{
            border-radius: 0 !important;
        }}
        div[data-testid="stChatInput"] textarea {{
            min-height: 92px !important;
            padding-top: 0;
            padding-bottom: 0;
            margin: 0;
            font-size: 1.05rem;
            line-height: 1.6rem;
            text-align: left;
            resize: none;
            background-color: transparent;
        }}
        div[data-testid="stChatInput"] textarea::placeholder {{
            text-align: left;
        }}
        div[data-testid="stChatInput"] button {{
            align-self: center;
        }}

        /* ======== Hamburger column ======== */
        .hamburger-wrap {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            align-items: center;
            padding-top: 8px;
        }}
        .hamburger-wrap .stButton > button {{
            width: 44px;
            height: 44px;
            border-radius: 10px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            font-size: 18px;
            line-height: 1;
        }}
        .hamburger-wrap .stButton > button:hover {{
            background: rgba(255,255,255,0.10);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def greeting_for_now(name: str) -> str:
    hour = datetime.now().hour
    if hour < 12:
        g = "Good morning"
    elif hour < 18:
        g = "Good afternoon"
    else:
        g = "Good evening"
    return f"{g}, {name}"