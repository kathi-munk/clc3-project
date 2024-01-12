import requests
import streamlit as st
from utils import handle_login_button, handle_logout_button, create_movie_df

st.title('History')


if 'user' not in st.session_state:
    "You need to login"
    handle_login_button()
else:
    handle_logout_button()

    watched_tuples = requests.get(f'http://user-api:5002/user/{st.session_state["user"]["id"]}/watched').json()

    movies = []
    ratings = []
    for watched_tuple in watched_tuples:
        movies.append(requests.get(f"http://movie-api:5001/movie/{watched_tuple[0]}").json())
        ratings.append(watched_tuple[1])
    movie_df = create_movie_df(movies)

    movie_df['rating'] = ratings
    movie_df = st.dataframe(
        movie_df,
        column_config={
            "rating": st.column_config.NumberColumn(
                "Movie rating",
                format="%d ⭐",
            ),
            "imgPath": st.column_config.ImageColumn("Poster image"),
            "title": "Title",
            "overview": "Overview",
            "release_date": "Release date"
        },
        use_container_width=True,
        hide_index=True,
        column_order=("rating", "imgPath", "title", "overview", "release_date")
    )