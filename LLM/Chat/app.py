import streamlit as st
from state import init_state, new_chat, send_message
from ui_widgets import (
    render_header,
    render_history,
    render_messages,
    render_composer,
)
from services.ollama_client import list_models_safe
from utils import inject_css

# Page config MUST be the first Streamlit call
st.set_page_config(
    page_title="Chat UI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main() -> None:
    # Init state + global CSS
    init_state()
    inject_css()

    # ---- Layout: hamburger column (anchored left) + collapsible panel + main ----
    panel_open = st.session_state.get("sidebar_open", True)

    ham_w = 0.04                          # slim column for the hamburger on the far left
    panel_w = 0.22 if panel_open else 0.0001  # slide-out panel (hidden when closed)
    main_w = 1 - ham_w - panel_w

    ham_col, panel_col, main_col = st.columns([ham_w, panel_w, main_w], gap="small")

    # ---------- HAMBURGER (far left) ----------
    with ham_col:
        st.markdown('<div class="hamburger-wrap">', unsafe_allow_html=True)
        if st.button("☰", key="hamburger_toggle", help="Toggle menu", use_container_width=True):
            st.session_state.sidebar_open = not panel_open
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- SLIDE-OUT PANEL (only when open) ----------
    if panel_open:
        with panel_col:
            st.header("Menu")

            if st.button("➕ New", use_container_width=True, type="primary", key="panel_new"):
                new_chat()
                st.rerun()

            models = list_models_safe()

            # Ensure there's always a valid model in session state
            if (
                "current_model" not in st.session_state
                or st.session_state.current_model not in models
            ):
                st.session_state.current_model = models[0] if models else ""

            selected_model = st.selectbox(
                "Model",
                options=models,
                index=(
                    models.index(st.session_state.current_model)
                    if st.session_state.current_model in models and models
                    else 0
                ),
                help="Ollama models installed locally.",
                key="model_select",
            )
            st.session_state.current_model = selected_model

            render_history()

    # ---------- MAIN AREA ----------
    with main_col:
        render_header(name="Marc")
        render_messages()
        render_composer(on_send=send_message)

if __name__ == "__main__":
    main()