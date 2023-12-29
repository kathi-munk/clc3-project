import streamlit as st
from st_pages import Page, show_pages

from Managers import MovieManager, UserManager
from utils import handle_login_button, create_movie_df

st.set_page_config(layout="wide")

show_pages(
    [
        Page("home.py", "Home"),
        Page("pages/watchlist.py", "Watchlist"),
        Page("pages/history.py", "History"),
    ]
)

movie_manager = MovieManager()
user_manager = UserManager()

if 'username' not in st.session_state:
    handle_login_button(user_manager)

movies = movie_manager.get_movies()

st.dataframe(
    create_movie_df(movies),
    column_config={
        "imgPath": st.column_config.ImageColumn("Poster image"),
        "title": "Title",
        "overview":  "Overview",
        "release_date":  "Release date"
    },
    use_container_width = True,
    hide_index=True,
)
