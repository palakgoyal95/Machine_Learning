import streamlit as st

import plotly.express as px

st.set_page_config(page_title="AI Dashboard", layout="wide")

st.title("📊 AI Resume Dashboard")

if "prediction" not in st.session_state:
    st.warning("⚠ Please upload a resume first.")
    st.stop()

result = st.session_state["prediction"]
skills = st.session_state.get("skills", [])

predicted_role = result["predicted_role"]
confidence = result["confidence"]
top_matches = result["top_matches"]

ats_score = min(100, round(confidence))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Predicted Role",
        predicted_role
    )

with col2:
    st.metric(
        "Confidence",
        f"{confidence:.2f}%"
    )

with col3:
    st.metric(
        "ATS Score",
        f"{ats_score}%"
    )

st.divider()

st.subheader("🏆 Top Matching Roles")

for role in top_matches:

    st.write(f"### {role['role']}")

    st.progress(role["confidence"] / 100)

    st.write(f"{role['confidence']} % Match")

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("✅ Detected Skills")

    if skills:

        for skill in skills:
            st.success(skill)

    else:

        st.info("No skills detected.")

with right:

    st.subheader("❌ Missing Skills")

    required = [
        "Python",
        "SQL",
        "Git",
        "Docker",
        "AWS",
        "React",
        "Django"
    ]

    missing = [
        skill
        for skill in required
        if skill not in skills
    ]

    if missing:

        for skill in missing:
            st.error(skill)

    else:

        st.success("No missing skills 🎉")

st.divider()

st.subheader("📄 Resume Preview")

st.text_area(
    "",
    st.session_state["resume_text"][:4000],
    height=300
)

fig = px.bar(
    x=["Backend","Python","Data"],
    y=[95,90,80]
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("💡 AI Suggestions")

st.success("✔ Add Docker")

st.success("✔ Add AWS")

st.success("✔ Mention REST APIs")

st.success("✔ Add measurable achievements")