import streamlit as st
from streamlit_modal import Modal


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

    actual_username = "username"
    actual_password = "password"

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    #TODO check login
    if submit and username == actual_username and password == actual_password:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        st.success("Login successful")
    elif submit and username != actual_username and password != actual_password:
        st.error("Login failed")
    else:
        pass
