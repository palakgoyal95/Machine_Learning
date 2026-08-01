import streamlit as st

def hero():
    st.markdown("""
    <style>
    .hero{ padding:24px; border-radius:12px; text-align:left; }
    .hero h1{ color:#E6F6F5; font-size:28px; margin:0 0 6px 0; }
    .hero p{ color:#9CA3AF; font-size:14px; margin:0; }
    </style>
    <div class="hero">
      <h1>🤖 ResumeAI</h1>
      <p>AI-powered resume screening — fast, objective, and actionable.</p>
    </div>
    """, unsafe_allow_html=True)