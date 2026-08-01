import streamlit as st

from app_pages import about_page, dashboard_page, home_page, screening_page
from components.sidebar import show_sidebar
from components.theme import apply_theme


st.set_page_config(
    page_title="ResumeAI",
    page_icon=":material/auto_awesome:",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
    "Home": home_page.render,
    "Screen resume": screening_page.render,
    "Insights": dashboard_page.render,
    "About": about_page.render,
}

if "color_mode" not in st.session_state:
    st.session_state["color_mode"] = "Light"

# Button callbacks set this neutral intent flag. Resolve it before the
# navigation widget is created; Streamlit does not permit changing a widget's
# own session-state key later in the same render.
if st.session_state.pop("open_screening", False):
    st.session_state["navigation"] = "Screen resume"

apply_theme(st.session_state["color_mode"])
selected_page = show_sidebar()
PAGES.get(selected_page, home_page.render)()
