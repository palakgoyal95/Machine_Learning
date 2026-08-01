import time

import streamlit as st

from backend.ml_model.predict import extract_text_from_pdf, predict_resume
from backend.ml_model.skills import extract_skills
from backend.ml_model.ats import calculate_ats_score


def render():
    st.title("Screen a resume")
    st.write("Upload a PDF and we’ll surface the likely role, match strength, and skills in a few seconds.")

    with st.container(border=True):
        st.subheader("Upload a resume", divider=False)
        uploaded_file = st.file_uploader(
            "Resume PDF",
            type=["pdf"],
            help="Your file is used to generate this screening result.",
        )
        job_description = st.text_area(
            "Job description (optional, for a role-specific ATS score)",
            placeholder="Paste the role requirements, responsibilities, and required skills.",
            key="job_description",
            height=160,
        )

    if uploaded_file is None:
        st.caption("PDF files only · Results will appear here after analysis.")
        return

    with st.spinner("Reading the resume and finding the best matches…"):
        time.sleep(2)
        text = extract_text_from_pdf(uploaded_file)
        result = predict_resume(text)
        skills = extract_skills(text)
        ats = calculate_ats_score(text, job_description)

    st.session_state["prediction"] = result
    st.session_state["resume_text"] = text
    st.session_state["skills"] = skills
    st.session_state["ats"] = ats

    predicted_role = result["predicted_role"]
    confidence = result["confidence"]
    ats_score = ats["score"]

    st.success("Analysis complete — here’s the quick read.", icon=":material/check_circle:")
    metrics = st.columns(3)
    metrics[0].metric("Best-fit role", predicted_role)
    metrics[1].metric("Match confidence", f"{confidence:.1f}%")
    metrics[2].metric(
        "ATS score",
        f"{ats_score}%",
        help="A transparent resume-readiness and job-description match score. It is separate from model confidence.",
    )

    with st.expander("How the ATS score is calculated", icon=":material/info:"):
        if ats["has_job_description"]:
            st.write("20% resume readiness, 55% required-skill coverage, and 25% job-description keyword coverage.")
            st.write(f"Matched required skills: {len(ats['matched_skills'])} of {ats['details']['required_skills']}.")
            if ats["missing_skills"]:
                st.caption(f"Skills to consider adding when accurate: {', '.join(ats['missing_skills'])}.")
        else:
            st.write("No job description was provided, so this score reflects resume readiness only: readable content, standard sections, recognised skills, and contact details.")
        st.caption("It does not use name, age, gender, location, or any other protected characteristic.")

    left, right = st.columns([3, 2], gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Top role matches")
            for item in result["top_matches"]:
                st.write(f"**{item['role']}**")
                st.progress(item["confidence"] / 100, text=f"{item['confidence']:.1f}% match")

    with right:
        with st.container(border=True):
            st.subheader("Skills found")
            if skills:
                for skill in skills:
                    st.badge(skill, icon=":material/check:", color="blue")
            else:
                st.warning(
                    "No skills matched our current library yet. This can happen with image-only PDFs, "
                    "unusual formatting, or specialised domain terms.",
                    icon=":material/manage_search:",
                )
                st.caption("Tip: upload a text-based PDF, or include tools and technologies in the resume text.")

    with st.expander("Review extracted resume text", icon=":material/article:"):
        st.text_area("Resume text", text, height=320, label_visibility="collapsed")

    report = (
        "ResumeAI screening report\n\n"
        f"Best-fit role: {predicted_role}\n"
        f"Match confidence: {confidence:.2f}%\n"
        f"ATS score: {ats_score}%\n"
        f"ATS basis: {'Job-description match and resume readiness' if ats['has_job_description'] else 'Resume readiness (no job description supplied)'}\n\n"
        f"Skills found: {', '.join(skills) or 'None'}\n\n"
        "Top matches\n"
        + "\n".join(f"- {item['role']}: {item['confidence']:.2f}%" for item in result["top_matches"])
    )
    st.download_button(
        "Download report",
        report,
        file_name="resumeai_report.txt",
        icon=":material/download:",
    )
