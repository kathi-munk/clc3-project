import psycopg2
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

    def __repr__(self):
        return f"User({self.id}, '{self.username}', '{self.movies}')"

class UserDAO:
    def __init__(self):
        self.conn_params = {
            "dbname": "your_dbname",
            "user": "your_username",
            "password": "your_password",
            "host": "your_host"
        }

    def get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def get_user(self, username, password):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
            user_data = cursor.fetchone()
            if user_data:
                user = User(*user_data)
                return user
            else:
                return None
        except psycopg2.Error as error:
            print("Failed to read data from table", error)
        finally:
            if conn:
                conn.close()

    def get_movies(self, user: User):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT movieId, watched, rating FROM user_movie WHERE userId = %s", (user.id,))
            user_movies = cursor.fetchall()
            for user_movie in user_movies:
                user.movies[user_movie[0]] = (user_movie[1], user_movie[2])
            return user.movies
        except psycopg2.Error as error:
            print("Failed to read data from table", error)
        finally:
            if conn:
                conn.close()

    def add_movie(self, user_id, movie_id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_movie (userId, movieId, watched) VALUES (%s, %s, %s)", (user_id, movie_id, False))
            conn.commit()
        except psycopg2.IntegrityError as e:
            print("Movie already exists for this user or user/movie not found.", e)
        except psycopg2.Error as error:
            print("Failed to insert data into table", error)
        finally:
            if conn:
                conn.close()

    def watched_movie(self, user_id, movie_id, rating):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("Update user_movie SET watched = %s, rating = %s WHERE userId = %s AND movieId = %s", (True, rating, user_id, movie_id))
            if cursor.rowcount == 0:
                print("No such movie found for the user or already watched.")
            else:
                print(f"Movie {movie_id} watched by user {user_id} with rating {rating}")
                conn.commit()
        except psycopg2.Error as error:
            print("Failed to update data in table", error)
        finally:
            if conn:
                conn.close()

    def get_user_by_id(self, user_id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                user = User(*user_data)
                user.movies = self.get_movies(user)
                return user
            else:
                return None
        except psycopg2.Error as error:
            print("Failed to read data from table", error)
        finally:
            if conn:
                conn.close()

class UserManager:
    def __init__(self):
        self.dao = UserDAO()

    def login(self, username, password):
        return self.dao.get_user(username, password)

    def get_watchlist(self, user):
        allMovies = self.dao.get_movies(user)
        watchlist = [k for k, v in allMovies.items() if not v[0]]
        return watchlist

    def get_watched_movies(self, user):
        allMovies = self.dao.get_movies(user)
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
        return jsonify(user.__dict__)
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/user/<int:user_id>/watchlist', methods=['GET'])
def get_watchlist(user_id):
    user = user_manager.get_user_by_id(user_id)
    if user:
        watchlist = user_manager.get_watchlist(user)
        return jsonify(watchlist)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/user/<int:user_id>/watched', methods=['GET'])
def get_watched_movies(user_id):
    user = user_manager.get_user_by_id(user_id)
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
