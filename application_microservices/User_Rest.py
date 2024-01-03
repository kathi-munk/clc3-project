import sqlite3
from flask import Flask, jsonify, request
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class User:
    id: int
    username: str
    password: str
    movies: dict

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.movies = {}

    def __repr__(self): # printing
        return f"User({self.id}, '{self.username}', '{self.movies}')"


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
            cursor.execute("SELECT movieId, watched, rating FROM user_movie WHERE userId = ?", (user.id,))
            user_movies = cursor.fetchall()
            for user_movie in user_movies:
                user.movies[user_movie[0]] = (user_movie[1], user_movie[2])
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

    def get_user_by_id(self, user_id):
        conn = sqlite3.connect("../db/movies.db")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                # Convert the user data into a User object
                user = User(*user_data)
                user.movies = self.get_movies(user)  # Assume get_movies() populates user movies
                return user
            else:
                # Return None if no user was found
                return None
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if conn:
                conn.close()

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

    def get_user_by_id(self,user_id):
        return self.dao.get_user_by_id(user_id)


user_manager = UserManager()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = user_manager.login(data['username'], data['password'])
    if user:
        return jsonify(user)  # Convert the user object to a string for JSON response
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/user/<int:user_id>/watchlist', methods=['GET'])
def get_watchlist(user_id):
    user = user_manager.get_user_by_id(user_id)  # Assume a method to get user by ID
    if user:
        watchlist = user_manager.get_watchlist(user)
        return jsonify(watchlist)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/user/<int:user_id>/watched', methods=['GET'])
def get_watched_movies(user_id):
    user = user_manager.get_user_by_id(user_id)  # Assume a method to get user by ID
    if user:
        watched = user_manager.get_watched_movies(user)
        return jsonify(watched)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/user/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    movie_id = request.json['movie_id']
    user_manager.add_movie(user_id, movie_id)
    return jsonify({"success": "Movie added to watchlist"})

@app.route('/user/<int:user_id>/watched_movie', methods=['POST'])
def watched_movie(user_id):
    movie_id = request.json['movie_id']
    rating = request.json['rating']
    user_manager.watched_movie(user_id, movie_id, rating)
    return jsonify({"success": "Movie marked as watched"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
