#Here I would add the classes that access the database
import sqlite3
from Domain import Movie, User

class UserDAO:
    def get_user(self, username, password):
        #check in db and return dataclass User
        conn = sqlite3.connect("db/movies.db")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()
            if user_data:
                # Convert the movie data into a Movie object
                user = User(*user_data)
                return user
            else:
                # Return None or raise an error if no movie was found
                return None
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            # Closing the connection
            if conn:
                conn.close()

    def get_movies(self, user:User):
        #get movies in user_movie table
        conn = sqlite3.connect("db/movies.db")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT movieId FROM user_movie WHERE id = ?", (user.id,))
            user_movies = cursor.fetchall()
            for user_movie in user_movies:
                user.movies.append(user_movie)
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            # Closing the connection
            if conn:
                conn.close()

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