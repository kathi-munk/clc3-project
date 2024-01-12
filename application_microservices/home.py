import streamlit as st
from st_pages import Page, show_pages
import requests

from utils import handle_login_button, handle_logout_button, create_movie_df

st.set_page_config(layout="wide")

show_pages(
    [
        Page("home.py", "Home", ":house:"),
        Page("pages/watchlist.py", "Watchlist"),
        Page("pages/history.py", "History"),
    ]
)

st.title('Movie list')

movie_df = create_movie_df(requests.get("http://movie-api:5001/movies").json())

if 'user' not in st.session_state:
    handle_login_button()

    st.dataframe(
        movie_df,
        column_config={
            "imgPath": st.column_config.ImageColumn("Poster image"),
            "title": "Title",
            "overview":  "Overview",
            "release_date":  "Release date"
        },
        use_container_width=True,
        hide_index=True,
        column_order=("add", "imgPath", "title", "overview", "release_date")
    )

else:
    handle_logout_button()

    movie_df['add'] = False
    movie_df = st.data_editor(
        movie_df,
        column_config={
            "add": st.column_config.CheckboxColumn(
                "Select for watchlist",
                default=False,
            ),
            "imgPath": st.column_config.ImageColumn("Poster image"),
            "title": "Title",
            "overview": "Overview",
            "release_date": "Release date"
        },
        use_container_width=True,
        hide_index=True,
        column_order=("add", "imgPath", "title", "overview", "release_date"),
        disabled=("imgPath", "title", "overview", "release_date")
    )

    add_watchlist = st.button("Add to watchlist")

    if add_watchlist:
        ids = movie_df[movie_df["add"]]["id"]
        url = f'http://user-api:5002/user/{st.session_state["user"]["id"]}/add_movie'
        for id in ids:
            # Define your payload, the data you send to the API
            payload = {
                'movie_id': id,
            }
            requests.post(url, json=payload)

        st.rerun()
