import streamlit as st
from pathlib import Path

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="ResumeAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------
# LOAD CSS
# ------------------------
css_path = Path("styles/style.css")

if css_path.exists():
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

# ------------------------
# SIDEBAR HEADER
# ------------------------

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-logo">

<h1>🤖 ResumeAI</h1>

<p>AI Resume Screening</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("---")

# ------------------------
# HERO SECTION
# ------------------------

st.markdown(
    """
<div class="hero">

<h1>🤖 ResumeAI</h1>

<h3>AI Powered Resume Screening Platform</h3>

<p>
Upload your resume and receive AI-powered ATS analysis,
job prediction, skill extraction and career recommendations.
</p>

</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ------------------------
# FEATURES
# ------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
<div class="feature-card">

<h2>📄</h2>

<h4>Upload Resume</h4>

<p>Upload PDF Resume</p>

</div>
""",
        unsafe_allow_html=True,
    )

with col2:

    st.markdown(
        """
<div class="feature-card">

<h2>🤖</h2>

<h4>AI Prediction</h4>

<p>Predict Job Role</p>

</div>
""",
        unsafe_allow_html=True,
    )

with col3:

    st.markdown(
        """
<div class="feature-card">

<h2>📊</h2>

<h4>ATS Analysis</h4>

<p>AI Resume Score</p>

</div>
""",
        unsafe_allow_html=True,
    )

st.write("")

st.info("👈 Select **Resume Screening** from the sidebar to upload your resume.")