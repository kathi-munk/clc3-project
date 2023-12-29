import streamlit as st
from st_pages import Page, show_pages

from utils import show_login_modal, handle_login_button

st.set_page_config(layout="wide")

show_pages(
    [
        Page("home.py", "Home"),
        Page("pages/watchlist.py", "Watchlist"),
        Page("pages/history.py", "History"),
    ]
)



if 'username' not in st.session_state:
    handle_login_button()