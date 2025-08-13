import streamlit as st
from utils import get_greeting
from state import get_current_model, get_models_list, set_current_model


def render_header():
    user_name = "Marc"
    greeting = get_greeting()

    # Greeting only (compact)
    st.markdown(
        f"<h1 style='margin:0.25rem 0 0.1rem 0'>{greeting}, {user_name}</h1>",
        unsafe_allow_html=True,
    )


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


def render_composer():
    current_model = get_current_model()

    # Keep things compact; we’ll align the arrow with a column next to the textarea
    composer_h = 72  # px; textarea height and arrow-cell height must match

    st.markdown(
        f"""
        <style>
        .block-container {{ padding-top: 0.5rem !important; padding-bottom: 0.15rem !important; }}
        [data-testid="stVerticalBlock"] {{ gap: 0.15rem !important; }}
        h1, h2, h3 {{ margin-top: 0.08rem !important; margin-bottom: 0.08rem !important; }}

        /* Remove stray margins Streamlit adds */
        .stMarkdown, .stTextArea, .stButton, .stSelectbox, .stContainer {{
            margin: 0 !important; padding: 0 !important;
        }}

        /* Arrow column: same height as textarea, perfectly centered.
           A tiny negative left margin pulls it visually closer to the prompt box. */
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

    return send_button, user_input