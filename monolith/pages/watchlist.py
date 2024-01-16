import streamlit as st
from utils import handle_login_button, handle_logout_button, create_movie_df
from Managers import UserManager, MovieManager

st.title('Watchlist')

user_manager = UserManager()
movie_manager = MovieManager()

if 'user' not in st.session_state:
    "You need to login"
    handle_login_button(user_manager)
else:
    handle_logout_button()

    watchlist_ids = user_manager.get_watchlist(st.session_state["user"])

    movies = []
    for id in watchlist_ids:
        movies.append(movie_manager.get_movie_by_id(id))
    movie_df = create_movie_df(movies)

    movie_df['add'] = False
    movie_df['rating'] = 0
    movie_df = st.data_editor(
        movie_df,
        column_config={
            "add": st.column_config.CheckboxColumn(
                "Select for watched list",
                default=False,
            ),
            "rating": st.column_config.SelectboxColumn(
                "Movie rating",
                width="medium",
                options=[
                    1, 2, 3, 4, 5
                ],
                required=False,
            ),
            "imgPath": st.column_config.ImageColumn("Poster image"),
            "title": "Title",
            "overview": "Overview",
            "release_date": "Release date"
        },
        use_container_width=True,
        hide_index=True,
        column_order=("add", "rating", "imgPath", "title", "overview", "release_date"),
        disabled=("imgPath", "title", "overview", "release_date")
    )

    add_watched = st.button("Add to watched list")

    if add_watched:
        ids = movie_df[movie_df["add"]]["id"].tolist()
        ratings = movie_df[movie_df["add"]]["rating"].tolist()
        for i in range(len(ids)):
            user_manager.watched_movie(st.session_state["user"].id, ids[i], ratings[i])

        movie_df['add'] = False
        movie_df['rating'] = 0
        st.rerun()
