#Here I would add the classes that access the database
import os
import sqlite3
from Domain import Movie, User

class UserDAO:
    def get_user(self, username, password):
        #check in db and return dataclass User
        conn = sqlite3.connect("../db/movies.db")
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
        conn = sqlite3.connect("../db/movies.db")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT movieId, watched FROM user_movie WHERE userId = ?", (user.id,))
            user_movies = cursor.fetchall()
            for user_movie in user_movies:
                user.movies[user_movie[0]] = user_movie[1]
            return user.movies
        
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            # Closing the connection
            if conn:
                conn.close()

    def add_movie(self, user_id, movie_id):
        #watched = False
        conn = sqlite3.connect("../db/movies.db")
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_movie (userId, movieId, watched) VALUES (?, ?, ?)", (user_id, movie_id, False))
            conn.commit()

        except sqlite3.IntegrityError as e:
            print("Movie already exists for this user or user/movie not found.", e)
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            # Closing the connection
            if conn:
                conn.close()
            

    def watched_movie(self, user_id, movie_id, rating):
        #watched to True and add rating
        conn = sqlite3.connect("../db/movies.db")
        try:
            cursor = conn.cursor()
            cursor.execute("Update user_movie SET watched = ?, rating = ? WHERE userId = ? AND movieId = ?", (True, rating, user_id, movie_id))
            conn.commit()

            # Check if the update was successful
            if cursor.rowcount == 0:
                print("No such movie found for the user or already watched.")
            else:
                print(f"Movie {movie_id} watched by user {user_id} with rating {rating}")
                conn.commit()  # Commit changes to the database

        except sqlite3.Error as error:
            print("Failed to update data in sqlite table", error)
        finally:
            # Closing the connection
            if conn:
                conn.close()
    
class MovieDAO:
    def get_movies(self):
        conn = sqlite3.connect("../db/movies.db")
        movie_list = []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movie")

            # Fetch all results from the database
            movies = cursor.fetchall()

            # Convert each movie record into a Movie object and add to the list
            for movie in movies:
                movie_obj = Movie(*movie)  # Unpack each movie tuple into the Movie constructor
                movie_list.append(movie_obj)

            return movie_list

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if conn:
                conn.close()

    def get_movie_by_id(self, id):
        # Connect to the SQLite database
        conn = sqlite3.connect("../db/movies.db")
        try:
            # Create a cursor object using the cursor() method
            cursor = conn.cursor()

            # Prepare SQL query to SELECT a movie by the given ID
            query = "SELECT * FROM movie WHERE id = ?"

            # Executing the SQL command
            cursor.execute(query, (id,))

            # Fetch one record and return result
            movie_data = cursor.fetchone()
            if movie_data:
                # Convert the movie data into a Movie object
                movie = Movie(*movie_data)
                return movie
            else:
                # Return None or raise an error if no movie was found
                return None

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            # Closing the connection
            if conn:
                conn.close()

