import streamlit as st
import time

from backend.ml_model.predict import (
    extract_text_from_pdf,
    predict_resume,
)

from backend.ml_model.skills import extract_skills

st.set_page_config(
    page_title="Resume Screening",
    page_icon="📄",
    layout="wide"
)

# ------------------------------
# HEADER
# ------------------------------



# ------------------------------
# UPLOAD CARD
# ------------------------------

with st.container(border=True):

    st.markdown("## 📄 Upload Resume")

    st.markdown("""
Upload your resume in **PDF** format.

Our AI will:

- 🤖 Predict Job Role
- 📊 Calculate Confidence
- ✅ Extract Skills
- 🏆 Find Top Matching Roles
""")

    uploaded_file = st.file_uploader(
        "Choose Resume",
        type=["pdf"]
    )

# ------------------------------
# ANALYSIS
# ------------------------------

if uploaded_file is not None:

    with st.spinner("🔍 AI is analyzing your resume..."):
        time.sleep(2)

        text = extract_text_from_pdf(uploaded_file)

        result = predict_resume(text)

        skills = extract_skills(text)

    st.session_state["prediction"] = result
    st.session_state["resume_text"] = text
    st.session_state["skills"] = skills

    st.success("✅ Resume analyzed successfully!")

    st.divider()

    # ------------------------------
    # METRIC CARDS
    # ------------------------------

    predicted_role = result["predicted_role"]
    confidence = result["confidence"]
    ats_score = round(confidence)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎯 Predicted Role",
            predicted_role
        )

    with col2:
        st.metric(
            "📈 Confidence",
            f"{confidence:.2f}%"
        )

    with col3:
        st.metric(
            "📊 ATS Score",
            f"{ats_score}%"
        )

    st.divider()

    # ------------------------------
    # TOP MATCHES
    # ------------------------------

    st.subheader("🏆 Top Matching Roles")

    for item in result["top_matches"]:

        st.write(f"### {item['role']}")

        st.progress(item["confidence"]/100)

        st.write(f"Match Score : {item['confidence']}%")

    st.divider()

    # ------------------------------
    # SKILLS
    # ------------------------------

    st.subheader("💻 Detected Skills")

    if skills:

        html = ""

        for skill in skills:

            html += f"""
            <span style="
            background:#7C3AED;
            color:white;
            padding:8px 16px;
            margin:6px;
            display:inline-block;
            border-radius:25px;
            font-size:15px;
            ">
            {skill}
            </span>
            """

        st.markdown(html, unsafe_allow_html=True)

    else:

        st.warning("No skills detected.")

    st.divider()

    # ------------------------------
    # RESUME PREVIEW
    # ------------------------------

    with st.expander("📄 Resume Preview"):

        st.text_area(
            "",
            text,
            height=350
        )

    st.divider()

    # ------------------------------
    # DOWNLOAD REPORT
    # ------------------------------

    report = f"""
Resume Screening Report

Predicted Role : {predicted_role}

Confidence : {confidence:.2f}%

ATS Score : {ats_score}%

Detected Skills

{", ".join(skills)}

Top Matches

"""

    for item in result["top_matches"]:

        report += f"{item['role']} : {item['confidence']}%\n"

    st.download_button(
        "📥 Download Report",
        report,
        file_name="resume_report.txt"
    )