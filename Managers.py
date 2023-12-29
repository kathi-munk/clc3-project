# Here I would add the Managers which use the DAOs to access the database
# and provide the data to the UI
from DAOs import UserDAO, MovieDAO

class UserManager:
    def __init__(self):
        self.dao = UserDAO()

    def login(self, username, password):
        #call get_user
        UserDAO.get_user(username, password)

    def get_watchlist(self, user_id):
        #get movies and filter
        allMovies = UserDAO.get_movies(user_id)
        # TODO filter
        pass

    def get_watched_movies(self, user_id):
        #get movies and filter
        pass

    def add_movie(self, user_id, movie_id):
        pass

    def watched_movie(self, user_id, movie_id, rating):
        pass

class MovieManager:
    def __init__(self):
        self.dao = MovieDAO()
    def get_movies(self):
        pass

    def get_movie_by_id(self, id):
        pass