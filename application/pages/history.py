import streamlit as st
from utils import handle_login_button, handle_logout_button, create_movie_df
from Managers import UserManager, MovieManager

st.title('History')

user_manager = UserManager()
movie_manager = MovieManager()

if 'user' not in st.session_state:
    "You need to login"
    handle_login_button(user_manager)
else:
    handle_logout_button()

    watched_tuples = user_manager.get_watched_movies(st.session_state["user"])

    movies = []
    ratings = []
    for watched_tuple in watched_tuples:
        movies.append(movie_manager.get_movie_by_id(watched_tuple[0]))
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