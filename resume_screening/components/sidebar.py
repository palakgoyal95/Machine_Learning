from streamlit_option_menu import option_menu
import streamlit as st


def show_sidebar():
    with st.sidebar:

        st.markdown("""
        <div style="
        text-align:center;
        padding:20px;
        ">
            <h1 style="color:#8B5CF6;margin-bottom:5px;">
                🤖 ResumeAI
            </h1>

            <p style="color:#94A3B8;">
                AI Resume Screening
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        selected = option_menu(
            menu_title=None,

            options=[
                "Home",
                "Resume Screening",
                "Dashboard",
                "About"
            ],

            icons=[
                "house-fill",
                "file-earmark-arrow-up-fill",
                "bar-chart-fill",
                "info-circle-fill"
            ],

            menu_icon="cast",

            default_index=0,

            styles={

                "container": {
                    "padding": "5px",
                    "background-color": "#1E293B",
                    "border-radius": "15px",
                },

                "icon": {
                    "color": "#8B5CF6",
                    "font-size": "20px",
                },

                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "8px",
                    "padding": "12px",
                    "border-radius": "10px",
                    "--hover-color": "#334155",
                    "color": "white",
                },

                "nav-link-selected": {
                    "background-color": "#7C3AED",
                    "color": "white",
                },
            },
        )

        st.markdown("---")

        st.markdown(
            "<p style='text-align:center;color:gray;'>ResumeAI v2.0</p>",
            unsafe_allow_html=True,
        )

        return selected