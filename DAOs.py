#Here I would add the classes that access the database

class UserDAO:
    def get_user(self, username, password):
        #check in db and return dataclass User
        pass

    def get_movies(self, user_id):
        #get movies in user_movie table
        pass

    def add_movie(self, user_id, movie_id):
        #watched = False
        pass

    def watched_movie(self, user_id, movie_id, rating):
        #watched to True and add rating
        pass


class MovieDAO:
    def get_movies(self):
        #return all movies
        pass

    def get_movie_by_id(self, id):
        pass