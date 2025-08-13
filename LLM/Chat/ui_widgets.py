import streamlit as st
from utils import get_greeting
from state import get_current_model, get_models_list, set_current_model


# ---------- Header ----------

def render_header():
    user_name = "Marc"
    greeting = get_greeting()
    st.markdown(
        f"<h1 style='margin:0.25rem 0 0.1rem 0'>{greeting}, {user_name}</h1>",
        unsafe_allow_html=True,
    )


# ---------- Sidebar ----------

def render_sidebar():
    with st.sidebar:
        if st.button("+ New", key="new_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.write("**Model**")
        models = get_models_list()
        current_model = get_current_model()

        if not models:
            st.error("No models available")
        else:
            selected_model = st.selectbox(
                "Choose model",
                options=models,
                index=models.index(current_model) if current_model in models else 0,
                key="model_selector",
            )
            if selected_model != current_model:
                set_current_model(selected_model)
                st.rerun()

        st.write("**History**")
        st.write("No past chats yet.")


# ---------- Chat messages ----------

def render_chat_messages():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            model_used = message.get("model", "Unknown")

            if role == "user":
                st.markdown(
                    f'<div class="chat-message user" style="margin:0.08rem 0">{content}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="chat-message assistant" style="margin:0.08rem 0">
                    <div class="model-badge">🤖 {model_used}</div>
                    <div class="message-content">{content}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )


# ---------- Progress UI (determinate/indeterminate) ----------

def _render_progress(show: bool, text: str = "Working…"):
    if not show:
        return

    progress = st.session_state.get("gen_progress")
    status = text or st.session_state.get("gen_status", "Working…")

    st.markdown(
        """
        <style>
        .progress-row {
            display: flex; align-items: center; gap: .6rem;
            margin: .35rem 0 .1rem 0;
        }
        .progress-track {
            position: relative; flex: 1 1 auto; height: 6px;
            background: rgba(255,255,255,.08); border-radius: 999px; overflow: hidden;
            min-width: 140px;
        }
        .progress-fill {
            position: absolute; left: 0; top: 0; height: 100%;
            background: linear-gradient(90deg, rgba(255,255,255,.25), rgba(255,255,255,.6));
            border-radius: 999px;
            transition: width .25s ease;
        }
        .dots { display: inline-flex; align-items: center; gap: .25rem; height: 10px; }
        .dot {
            width: 6px; height: 6px; border-radius: 50%;
            background: rgba(255,255,255,.55);
            animation: bounce 1s infinite ease-in-out;
        }
        .dot:nth-child(2){ animation-delay: .12s; }
        .dot:nth-child(3){ animation-delay: .24s; }
        .dot:nth-child(4){ animation-delay: .36s; }
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: .7; }
          40% { transform: translateY(-5px); opacity: 1; }
        }
        .progress-text { font-size: .85rem; opacity: .75; white-space: nowrap; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if isinstance(progress, (int, float)):
        pct = max(0, min(100, int(progress)))
        st.markdown(
            f"""
            <div class="progress-row">
              <div class="progress-track">
                <div class="progress-fill" style="width:{pct}%"></div>
              </div>
              <div class="progress-text">{status} {pct}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="progress-row">
              <div class="dots">
                <span class="dot"></span><span class="dot"></span>
                <span class="dot"></span><span class="dot"></span>
              </div>
              <div class="progress-text">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------- Attachment helpers ----------

def _init_upload_state():
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []  # list of dicts: {name, type, size, data}


def _file_emoji(mime: str, name: str) -> str:
    if mime:
        if mime.startswith("image/"):
            return "🖼️"
        if mime.startswith("text/"):
            return "📄"
        if mime in ("application/pdf",):
            return "📕"
        if "excel" in mime or name.lower().endswith((".xls", ".xlsx", ".csv")):
            return "📊"
        if "json" in mime or name.lower().endswith(".json"):
            return "🔣"
        if "zip" in mime or name.lower().endswith((".zip", ".tar", ".gz", ".7z")):
            return "🧩"
    # default
    return "📎"


def _render_attachment_chips():
    """Show uploaded-file chips inside the composer area with remove buttons."""
    _init_upload_state()
    files = st.session_state.uploaded_files

    # CSS for chips row
    st.markdown(
        """
        <style>
        .attach-row { display:flex; flex-wrap:wrap; gap:.35rem; margin:.1rem 0 .2rem 0; }
        .chip {
            display:inline-flex; align-items:center; gap:.4rem;
            padding:.2rem .5rem; border-radius:999px;
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.1);
            font-size:.85rem;
        }
        .chip .x { margin-left:.15rem; opacity:.7; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Render chips and deletion buttons
    if files:
        st.markdown('<div class="attach-row">', unsafe_allow_html=True)
        to_remove = []
        for idx, f in enumerate(files):
            col_chip, col_x = st.columns([10, 1])
            with col_chip:
                st.markdown(
                    f"<div class='chip'>{_file_emoji(f['type'], f['name'])} {f['name']}</div>",
                    unsafe_allow_html=True,
                )
            with col_x:
                if st.button("✕", key=f"rm_{idx}", help=f"Remove {f['name']}"):
                    to_remove.append(idx)
        st.markdown("</div>", unsafe_allow_html=True)

        # Apply removals
        for i in reversed(to_remove):
            del st.session_state.uploaded_files[i]


# ---------- Composer (with file upload & chips) ----------

def render_composer():
    current_model = get_current_model()

    composer_h = 72  # px; textarea height and arrow-cell height must match

    st.markdown(
        f"""
        <style>
        .block-container {{ padding-top: 0.5rem !important; padding-bottom: 0.15rem !important; }}
        [data-testid="stVerticalBlock"] {{ gap: 0.15rem !important; }}
        h1, h2, h3 {{ margin-top: 0.08rem !important; margin-bottom: 0.08rem !important; }}
        .stMarkdown, .stTextArea, .stButton, .stSelectbox, .stContainer {{
            margin: 0 !important; padding: 0 !important;
        }}
        .arrow-cell {{
            height: {composer_h}px;
            display: flex; align-items: center; justify-content: center;
            margin-left: -6px;
        }}
        .arrow-cell .stButton > button {{
            width: 36px; height: 36px; border-radius: 50%; padding: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Prompting line directly under greeting (tight)
    if current_model:
        st.markdown(f"### Prompting {current_model}...")
    else:
        st.markdown("### Prompting (no model selected)...")

    # ---- Attachments bar (chips) + uploader ----
    _init_upload_state()
    # Uploader: allow multiple files; we immediately persist them to session_state
    new_files = st.file_uploader(
        label="Attach files",
        type=None,
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Attach files for the LLM to use",
        key="uploader_input",
    )
    if new_files:
        for uf in new_files:
            data = uf.read()
            meta = {"name": uf.name, "type": uf.type, "size": len(data), "data": data}
            # de-duplicate by name+size
            if not any(m["name"] == meta["name"] and m["size"] == meta["size"] for m in st.session_state.uploaded_files):
                st.session_state.uploaded_files.append(meta)

    # Show chips for anything attached
    _render_attachment_chips()

    # Two columns: textarea + arrow; arrow is center-right of the prompt row
    input_col, arrow_col = st.columns([18, 2], gap="small")

    with input_col:
        user_input = st.text_area(
            label="Message",
            height=composer_h,
            key="user_input",
            placeholder="Type your prompt here...",
            label_visibility="collapsed",
        )

    with arrow_col:
        st.markdown('<div class="arrow-cell">', unsafe_allow_html=True)
        send_button = st.button(
            "➤",
            key="arrow_send_btn",
            help="Send message",
            use_container_width=False,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # When sending, expose attachments to the rest of the app
    if send_button:
        st.session_state["is_generating"] = True
        st.session_state["gen_status"] = "Queued…"
        # Attachments made available for app.py / model client:
        st.session_state["attached_files"] = st.session_state.uploaded_files.copy()
        if "gen_progress" in st.session_state:
            del st.session_state["gen_progress"]

    # Progress indicator right below composer/results
    _render_progress(
        show=st.session_state.get("is_generating", False),
        text=st.session_state.get("gen_status", "Working…"),
    )

    return send_button, user_input