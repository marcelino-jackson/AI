from __future__ import annotations
import streamlit as st
from datetime import datetime

PRIMARY_MAX_WIDTH = 920
USER_BG = "#1f2937"      # slate-800
ASSIST_BG = "#111827"    # gray-900
BORDER = "#2a2f3a"

def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        /* Layout width */
        .block-container {{
            max-width: {PRIMARY_MAX_WIDTH}px;
            margin: 0 auto;
        }}

        /* Hide toolbar (Deploy, etc.) */
        [data-testid="stToolbar"],
        header [data-testid="stHeaderActionElements"] {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* Sidebar width */
        section[data-testid="stSidebar"] {{
            width: 16rem !important;
        }}

        /* Chat bubbles */
        [data-testid="stChatMessage"] {{
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 10px 14px;
            margin: 8px 0 16px 0;
            background: {ASSIST_BG};
        }}
        [data-testid="stChatMessage-user"] {{
            background: {USER_BG};
        }}

        /* Timestamp inline */
        .msg-ts {{
            float: right;
            opacity: 0.6;
            font-size: 0.8rem;
        }}

        /* ===========================================
           PROMPT (chat input) — rectangular box
           =========================================== */

        /* Outer container of st.chat_input */
        div[data-testid="stChatInput"] > div {{
            display: flex;
            align-items: center;            /* vertical center icon/text/send */
            min-height: 96px;               /* bigger than default */
            padding: 0 14px;
            width: 100% !important;

            /* Force rectangular corners */
            border-radius: 8px !important;
            overflow: hidden;               /* clip inner rounded corners */
            border: 1px solid rgba(255,255,255,0.15);
            background-color: rgba(255,255,255,0.04);
            box-shadow: none !important;
        }}

        /* Some inner BaseWeb wrappers add their own radius—neutralize them */
        div[data-testid="stChatInput"] [data-baseweb],
        div[data-testid="stChatInput"] [data-baseweb] * {{
            border-radius: 0 !important;
        }}

        /* The immediate input wrappers sometimes carry rounded corners */
        div[data-testid="stChatInput"] [data-baseweb="base-input"],
        div[data-testid="stChatInput"] [data-baseweb="textarea"],
        div[data-testid="stChatInput"] div[role="textbox"] {{
            border-radius: 0 !important;
            background: transparent !important;
        }}

        /* Textarea styling (keep user text left-aligned) */
        div[data-testid="stChatInput"] textarea {{
            min-height: 72px !important;    /* tall inner area so it looks balanced */
            padding-top: 0;
            padding-bottom: 0;
            margin: 0;
            font-size: 1.0rem;
            line-height: 1.5rem;
            text-align: left;
            resize: none;
            background-color: transparent;
        }}

        /* Keep placeholder left-aligned */
        div[data-testid="stChatInput"] textarea::placeholder {{
            text-align: left;
        }}

        /* Focus state (subtle) */
        div[data-testid="stChatInput"] > div:focus-within {{
            border-color: rgba(255,255,255,0.25);
            box-shadow: 0 0 0 2px rgba(255,255,255,0.08);
        }}

        /* Ensure any buttons inside chat_input (send, etc.) are centered */
        div[data-testid="stChatInput"] button {{
            align-self: center;
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
