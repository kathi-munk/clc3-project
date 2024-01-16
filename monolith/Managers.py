# Here I would add the Managers which use the DAOs to access the database
# and provide the data to the UI
from DAOs import UserDAO, MovieDAO

class UserManager:
    def __init__(self):
        self.dao = UserDAO()

    def login(self, username, password):
        #call get_user
        user = self.dao.get_user(username, password)
        return user

    def get_watchlist(self, user):
        #get movies and filter
        allMovies = self.dao.get_movies(user)
        watchlist = [k for k, v in allMovies.items() if not v[0]]
        return watchlist

    def get_watched_movies(self, user_id):
        #get movies and filter
        allMovies = self.dao.get_movies(user_id)
        watched = [(k, v[1]) for k, v in allMovies.items() if v[0]]
        return watched

    def add_movie(self, user_id, movie_id):
        self.dao.add_movie(user_id, movie_id)

    def watched_movie(self, user_id, movie_id, rating):
        self.dao.watched_movie(user_id, movie_id, rating)

class MovieManager:
    def __init__(self):
        self.dao = MovieDAO()

    def get_movies(self):
        return self.dao.get_movies()

    def get_movie_by_id(self, id):
        return self.dao.get_movie_by_id(id)