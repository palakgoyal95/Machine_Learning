import streamlit as st


def render():
    st.title("About ResumeAI")
    st.write("A lightweight assistant for making resume review feel less repetitive and more consistent.")

    with st.container(border=True):
        st.subheader("Built with")
        st.markdown("- Streamlit\n- Python\n- Scikit-learn\n- Resume text extraction and skill matching")

    st.info(
        "Use the results as a starting point for review—not as an automated hiring decision.",
        icon=":material/info:",
    )
