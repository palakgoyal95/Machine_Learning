import pandas as pd
import streamlit as st


def _confidence_label(confidence: float) -> str:
    if confidence >= 80:
        return "Strong pattern match"
    if confidence >= 55:
        return "Moderate pattern match"
    return "Low pattern match"


def render():
    st.title("Resume insights")
    st.write("Understand the latest screening result at a glance.")

    if "prediction" not in st.session_state:
        st.info("Upload a resume first and the insights will appear here.", icon=":material/upload_file:")
        return

    result = st.session_state["prediction"]
    skills = st.session_state.get("skills", [])
    matches = result.get("top_matches", [])
    confidence = float(result.get("confidence", 0))
    ats = st.session_state.get("ats")
    second_confidence = matches[1]["confidence"] if len(matches) > 1 else 0
    role_gap = max(confidence - second_confidence, 0)

    st.caption(
        "These insights describe patterns in the uploaded document. They are not a hiring recommendation or an assessment of a person."
    )

    metrics = st.columns(4, border=True)
    metrics[0].metric("Best-fit role", result["predicted_role"])
    metrics[1].metric("Match confidence", f"{confidence:.1f}%", _confidence_label(confidence))
    metrics[2].metric("Role lead", f"{role_gap:.1f} pts", "Over the next best match")
    metrics[3].metric("Recognised skills", len(skills), "From the current skill library")

    left, right = st.columns([3, 2], gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Role match comparison")
            if matches:
                match_frame = pd.DataFrame(matches).rename(
                    columns={"role": "Role", "confidence": "Match confidence"}
                )
                st.bar_chart(match_frame, x="Role", y="Match confidence", color="#2563EB")
                st.dataframe(
                    match_frame,
                    hide_index=True,
                    column_config={
                        "Match confidence": st.column_config.ProgressColumn(
                            "Match confidence", min_value=0, max_value=100, format="%.1f%%"
                        )
                    },
                )
            else:
                st.warning("No role matches are available for this document.", icon=":material/manage_search:")

    with right:
        with st.container(border=True):
            st.subheader("What the confidence means")
            st.write(f"**{_confidence_label(confidence)}**")
            st.write(
                "Confidence is the model's probability estimate for the best-fit role after comparing the resume's wording with patterns in its training data."
            )
            if len(matches) > 1:
                st.caption(
                    f"The leading role is {role_gap:.1f} percentage points ahead of {matches[1]['role']}."
                )
            st.info(
                "Use this as a starting point for review, especially when the leading roles are close together.",
                icon=":material/info:",
            )

    skills_col, ats_col = st.columns([3, 2], gap="large")
    with skills_col:
        with st.container(border=True):
            st.subheader("Skills recognised")
            if skills:
                st.caption(f"{len(skills)} skills matched the current skill library.")
                for skill in skills:
                    st.badge(skill, icon=":material/check:", color="green")
            else:
                st.warning("No skills matched the current library for this resume yet.", icon=":material/manage_search:")
                st.caption("Try a text-based PDF or clearly name tools and technologies in the resume.")

    with ats_col:
        with st.container(border=True):
            st.subheader("ATS readiness")
            if not ats:
                st.info("ATS readiness was not calculated for this result.", icon=":material/info:")
            else:
                st.metric("ATS score", f"{ats['score']}%")
                if ats["has_job_description"]:
                    st.caption("Based on resume readiness, required-skill coverage, and job-description keywords.")
                else:
                    st.caption("Based on resume readability, sections, recognised skills, and contact details.")

    if ats and ats["has_job_description"]:
        with st.container(border=True):
            st.subheader("Job-description skill coverage")
            required_skills = ats["details"]["required_skills"]
            matched_skills = ats["matched_skills"]
            coverage = (len(matched_skills) / required_skills * 100) if required_skills else 0
            st.progress(coverage / 100, text=f"{len(matched_skills)} of {required_skills} recognised required skills matched")
            if ats["missing_skills"]:
                st.write("**Skills to verify or add when accurate**")
                for skill in ats["missing_skills"]:
                    st.badge(skill, icon=":material/add:", color="orange")
            elif required_skills:
                st.success("All recognised required skills were found in this resume.", icon=":material/check_circle:")
            else:
                st.info("No recognised skills were found in the job description to compare.", icon=":material/info:")
    elif ats:
        with st.container(border=True):
            st.subheader("Make this insight more specific")
            st.write("Add a job description on the screening page to compare its recognised requirements with the resume.")

    with st.expander("Review extracted resume text", icon=":material/article:"):
        st.text_area(
            "Resume text",
            st.session_state.get("resume_text", "")[:4000],
            height=300,
            label_visibility="collapsed",
            disabled=True,
        )
