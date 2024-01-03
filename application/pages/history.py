import streamlit as st

from utils import handle_login_button

if 'user' not in st.session_state:
    "You need to login"
    handle_login_button()
else:
    pass