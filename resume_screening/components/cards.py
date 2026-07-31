import streamlit as st

def metric_card(title,value,color):

    st.markdown(f"""

    <div style="

    background:#1E293B;

    border-radius:20px;

    padding:25px;

    border-left:6px solid {color};

    box-shadow:0 10px 30px rgba(0,0,0,.3);

    ">

    <h4 style="color:#CBD5E1;">{title}</h4>

    <h1 style="color:white;">{value}</h1>

    </div>

    """,unsafe_allow_html=True)