import streamlit as st
from utils import handle_login_button
from Managers import UserManager
from utils import create_movie_df

if 'username' not in st.session_state:
    "You need to login"
    handle_login_button()
else:
    user_manager = UserManager()
    movies = user_manager.get_watchlist()

    st.dataframe(
        create_movie_df(movies),
        column_config={
            "imgPath": st.column_config.ImageColumn("Poster image"),
            "title": "Title",
            "overview": "Overview",
            "release_date": "Release date"
        },
        use_container_width=True,
        hide_index=True,
    )