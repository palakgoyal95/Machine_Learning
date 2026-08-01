import streamlit as st


def show_sidebar():
    """Render app-level navigation and lightweight context."""
    with st.sidebar:
        st.title(":material/auto_awesome: ResumeAI")
        st.caption("Clearer hiring decisions, one resume at a time.")

        selected = st.radio(
            "Navigate",
            options=["Home", "Screen resume", "Insights", "About"],
            format_func=lambda page: {
                "Home": ":material/home: Home",
                "Screen resume": ":material/upload_file: Screen resume",
                "Insights": ":material/insights: Insights",
                "About": ":material/info: About",
            }[page],
            label_visibility="collapsed",
            key="navigation",
        )

        st.space("medium")
        st.caption("APPEARANCE")
        st.radio(
            "Color mode",
            options=["Light", "Dark"],
            horizontal=True,
            label_visibility="collapsed",
            key="color_mode",
            format_func=lambda mode: f":material/{'light_mode' if mode == 'Light' else 'dark_mode'}: {mode}",
        )

        st.space("medium")
        st.caption("HOW IT WORKS")
        st.write("Upload a PDF, review the match, then explore skills and recommendations.")
        st.space("small")
        st.caption("ResumeAI · v2.0")

    return selected
