import requests
import streamlit as st
from utils import handle_login_button, handle_logout_button, create_movie_df

st.title('Watchlist')

if 'user' not in st.session_state:
    "You need to login"
    handle_login_button()
else:
    handle_logout_button()

    watchlist_ids = requests.get(f'http://user-api:5002/user/{st.session_state["user"]["id"]}/watchlist').json()

    movies = []
    for id in watchlist_ids:
        movies.append(requests.get(f"http://movie-api:5001/movie/{id}").json())
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
        url = f'http://user-api:5002/user/{st.session_state["user"]["id"]}/watched_movie'
        for i in range(len(ids)):
            payload = {
                'movie_id': ids[i],
                'rating': ratings[i],
            }
            requests.post(url, json=payload)

        movie_df['add'] = False
        movie_df['rating'] = 0
        st.rerun()
