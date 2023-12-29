import streamlit as st
from streamlit_modal import Modal
import pandas as pd

def handle_login_button(user_manager):
    modal = Modal("Login", key="login-modal", padding=20, max_width=744)
    sidebar = st.sidebar
    login = sidebar.button("Login")

    if login:
        modal.open()

    if modal.is_open():
        with modal.container():
            show_login_modal(user_manager)


def show_login_modal(user_manager):
    # Create an empty container
    placeholder = st.empty()

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    #TODO check login
    if submit:
        user = user_manager.login()
        if user is not None:
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            placeholder.empty()
            st.success("Login successful")
        else:
            st.error("Login failed")

def create_movie_df(movies):
    titles = []
    overviews = []
    dates = []
    paths = []
    for movie in movies:
        titles.append(movie.title)
        overviews.append(movie.overview)
        dates.append(movie.release_date)
        paths.append(movie.imgPath)

    return pd.DataFrame(
        {
            "imgPath": paths,
            "title": titles,
            "overview": overviews,
            "release_date": dates
        }
    )