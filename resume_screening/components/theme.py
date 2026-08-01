import streamlit as st


THEMES = {
    "Light": {
        "app": "#F6F8FC",
        "surface": "#FFFFFF",
        "text": "#172033",
        "muted": "#64748B",
        "line": "#DCE3F0",
        "sidebar": "#101B36",
        "sidebar_text": "#EAF0FF",
        "shadow": "0 12px 28px rgba(31, 58, 112, 0.08)",
    },
    "Dark": {
        "app": "#0B1220",
        "surface": "#121D33",
        "text": "#E7EEF9",
        "muted": "#9AAAC2",
        "line": "#263653",
        "sidebar": "#080E1B",
        "sidebar_text": "#EAF0FF",
        "shadow": "0 14px 30px rgba(0, 0, 0, 0.26)",
    },
}


def apply_theme(mode: str) -> None:
    """Apply the user's current appearance choice without changing app behaviour."""
    palette = THEMES[mode]
    st.markdown(
        f"""
        <style>
        .stApp {{ background: {palette['app']}; color: {palette['text']}; }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p,
        .stApp li, .stApp label, .stApp [data-testid="stMarkdownContainer"] {{ color: {palette['text']}; }}
        section[data-testid="stSidebar"] {{
            background: {palette['sidebar']};
            border-right: 1px solid {palette['line']};
        }}
        section[data-testid="stSidebar"] * {{ color: {palette['sidebar_text']}; }}
        [data-testid="stSidebar"] [data-testid="stRadio"] label {{
            border-radius: 10px;
            padding: 4px 6px;
        }}
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: {palette['surface']};
            border-color: {palette['line']};
            box-shadow: {palette['shadow']};
        }}
        [data-testid="stMetric"] {{
            background: {palette['surface']};
            border: 1px solid {palette['line']};
            border-radius: 14px;
            padding: 16px;
            box-shadow: {palette['shadow']};
        }}
        [data-testid="stCaptionContainer"], .stCaption {{ color: {palette['muted']}; }}
        [data-testid="stFileUploader"] {{ background: {palette['surface']}; border-radius: 14px; }}
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {{
            background: {palette['surface']}; color: {palette['text']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
