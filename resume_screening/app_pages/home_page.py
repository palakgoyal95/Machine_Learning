from pathlib import Path

import streamlit as st


HERO_IMAGE = Path(__file__).resolve().parents[1] / "assests" / "resumeai-hero.png"


def _go_to_screening():
    st.session_state["open_screening"] = True


def render():
    copy, visual = st.columns([1, 1.2], gap="large", vertical_alignment="center")
    with copy:
        st.badge("AI-assisted resume review", icon=":material/auto_awesome:", color="blue")
        st.title("Find the right fit, faster")
        st.write(
            "ResumeAI turns a resume into a clear shortlist of likely roles, "
            "relevant skills, and practical next steps."
        )
        st.button(
            "Screen a resume",
            type="primary",
            icon=":material/upload_file:",
            on_click=_go_to_screening,
        )
        st.caption("PDF in. Useful signal out. No complicated setup.")
    with visual:
        try:
            st.image(HERO_IMAGE, caption="A clearer view of every candidate", width="stretch")
        except Exception:
            # A media-serving error should not prevent the main application from loading.
            st.info("Resume screening is ready when you are.", icon=":material/auto_awesome:")

    st.space("small")
    left, right = st.columns(2, gap="medium")
    with left:
        with st.container(border=True):
            st.subheader(":material/bolt: Quick to review")
            st.write("See the likely role, match confidence, and ATS-style score in one clean view.")
    with right:
        with st.container(border=True):
            st.subheader(":material/tune: Useful details")
            st.write("Spot the skills already present and the ones worth adding before the next application.")

    st.caption("Predictions are guidance, not a final hiring decision.")
