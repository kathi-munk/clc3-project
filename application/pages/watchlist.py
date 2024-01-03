import streamlit as st
from utils import handle_login_button, create_movie_df
from Managers import UserManager, MovieManager


if 'user' not in st.session_state:
    "You need to login"
    handle_login_button()
else:
    user_manager = UserManager()
    movie_manager = MovieManager()
    watchlist_ids = user_manager.get_watchlist(st.session_state["user"])

    movies = []
    for id in watchlist_ids:
        movies.append(movie_manager.get_movie_by_id(id))
    movie_df = create_movie_df(movies)

    movie_df['add'] = False
    movie_df = st.data_editor(
        movie_df,
        column_config={
            "add": st.column_config.CheckboxColumn(
                "Select for watched list",
                default=False,
            ),
            "imgPath": st.column_config.ImageColumn("Poster image"),
            "title": "Title",
            "overview": "Overview",
            "release_date": "Release date"
        },
        use_container_width=True,
        hide_index=True,
        column_order=("add", "imgPath", "title", "overview", "release_date")
    )

    add_watched = st.button("Add to watched list")

    if add_watched:
        ids = movie_df[movie_df["add"]]["id"]
        for id in ids:
            user_manager.watched_movie(st.session_state["user"].id, id, 1)

        movie_df['add'] = False