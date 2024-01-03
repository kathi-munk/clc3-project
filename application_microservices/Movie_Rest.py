import sqlite3
from flask import Flask, jsonify, request
from dataclasses import dataclass


app = Flask(__name__)


@dataclass
class Movie:
    def __init__(self, id, title, overview, release_date, imgPath):
        self.id = id
        self.title = title
        self.overview = overview
        self.release_date = release_date
        self.imgPath = imgPath

    def __repr__(self):
        return f"Movie({self.id}, '{self.title}', '{self.overview}', '{self.release_date}', '{self.imgPath}')"


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

class MovieManager:
    def __init__(self):
        self.dao = MovieDAO()

    def get_movies(self):
        return self.dao.get_movies()

    def get_movie_by_id(self, id):
        return self.dao.get_movie_by_id(id)


# Initialize MovieManager
movie_manager = MovieManager()

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = movie_manager.get_movies()
    return jsonify([movie.__dict__ for movie in movies])  # Convert list of movie objects to list of dictionaries

@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = movie_manager.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie.__dict__)  # Convert the movie object to a dictionary
    else:
        return jsonify({"error": "Movie not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application

