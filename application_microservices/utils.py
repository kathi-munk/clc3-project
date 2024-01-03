import streamlit as st
from streamlit_modal import Modal
import pandas as pd
import requests

def handle_login_button():
    modal = Modal("Login", key="login-modal", padding=20, max_width=744)
    sidebar = st.sidebar
    login = sidebar.button("Login")

    if login:
        modal.open()

    if modal.is_open():
        with modal.container():
            show_login_modal()


def show_login_modal():
    # Create an empty container
    placeholder = st.empty()

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        url = 'http://127.0.0.1:5002/login'

        # Define your payload, the data you send to the API
        payload = {
            'username': username,
            'password': password
        }

        user = requests.post(url, json=payload).json()
        if user is not None:
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            placeholder.empty()
            st.session_state["user"] = user
            st.success("Login successful")
        else:
            st.error("Login failed")


def handle_logout_button():
    sidebar = st.sidebar
    logout = sidebar.button("Logout")

    if logout:
        del st.session_state["user"]
        st.rerun()


def create_movie_df(movies):
    ids = []
    titles = []
    overviews = []
    dates = []
    paths = []
    for movie_args in movies:
        ids.append(movie_args["id"])
        titles.append(movie_args["title"])
        overviews.append(movie_args["overview"])
        dates.append(movie_args["release_date"])
        paths.append(movie_args["imgPath"])

    return pd.DataFrame(
        {
            "id": ids,
            "imgPath": paths,
            "title": titles,
            "overview": overviews,
            "release_date": dates
        }
    )
