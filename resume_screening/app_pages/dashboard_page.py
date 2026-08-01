import plotly.express as px
import streamlit as st


def render():
    st.title("Resume insights")
    st.write("A closer look at the latest screening result.")

    if "prediction" not in st.session_state:
        st.info("Upload a resume first and the insights will show up here.", icon=":material/upload_file:")
        return

    result = st.session_state["prediction"]
    skills = st.session_state.get("skills", [])
    matches = result["top_matches"]
    confidence = result["confidence"]
    ats = st.session_state.get("ats")

    metrics = st.columns(3)
    metrics[0].metric("Best-fit role", result["predicted_role"])
    metrics[1].metric("Match confidence", f"{confidence:.1f}%")
    metrics[2].metric(
        "ATS score",
        f"{ats['score']}%" if ats else "Not calculated",
        help="Separate from model confidence; it uses job-description matching when a description is supplied.",
    )

    left, right = st.columns([3, 2], gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Role match comparison")
            chart = px.bar(
                matches,
                x="confidence",
                y="role",
                orientation="h",
                text_auto=".1f",
                labels={"confidence": "Match confidence (%)", "role": "Role"},
            )
            chart.update_layout(height=320, margin=dict(l=0, r=20, t=20, b=0), showlegend=False)
            chart.update_traces(marker_color="#2563EB", texttemplate="%{x:.1f}%", textposition="outside")
            st.plotly_chart(chart, width="stretch")

    with right:
        with st.container(border=True):
            st.subheader("Skills found")
            if skills:
                for skill in skills:
                    st.badge(skill, icon=":material/check:", color="green")
            else:
                st.warning("No skills matched our current library for this resume yet.", icon=":material/manage_search:")
                st.caption("Try a text-based PDF or a resume that names its tools and technologies.")

    required = ["Python", "SQL", "Git", "Docker", "AWS", "React", "Django"]
    missing = [skill for skill in required if skill.casefold() not in {item.casefold() for item in skills}]
    with st.container(border=True):
        st.subheader("Good next additions")
        if missing:
            st.write("These common skills could make the profile more rounded:")
            for skill in missing:
                st.badge(skill, icon=":material/add:", color="orange")
        else:
            st.success("This profile already covers the core skills in this checklist.", icon=":material/check_circle:")

    with st.expander("Review extracted resume text", icon=":material/article:"):
        st.text_area(
            "Resume text",
            st.session_state.get("resume_text", "")[:4000],
            height=300,
            label_visibility="collapsed",
        )
