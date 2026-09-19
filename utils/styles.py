"""
styles.py
Loads the custom CSS stylesheet into the Streamlit app.
"""

import os
import streamlit as st

CSS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "assets", "styles.css")


def load_css():
    try:
        with open(CSS_PATH, "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fail silently in the UI; the app still functions without custom styling.
        pass
