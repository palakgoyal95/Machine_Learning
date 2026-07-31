import streamlit as st

def hero():

    st.markdown("""
    <style>

    .hero{

        background:linear-gradient(135deg,#7C3AED,#2563EB);

        border-radius:25px;

        padding:45px;

        text-align:center;

        box-shadow:0px 20px 50px rgba(124,58,237,.35);

        margin-bottom:30px;

    }

    .hero h1{

        color:white;

        font-size:56px;

        margin-bottom:10px;

    }

    .hero p{

        color:#E5E7EB;

        font-size:22px;

    }

    </style>

    <div class="hero">

        <h1>🤖 ResumeAI</h1>

        <p>AI Powered Resume Screening Platform</p>

    </div>

    """,unsafe_allow_html=True)