import psycopg2
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
    def __init__(self):
        self.conn_params = {
            "dbname": "movies",
            "user": "myuser",
            "password": "mypassword",
            "host":"database"
        }

    def get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def get_movies(self):
        conn = self.get_connection()
        movie_list = []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movie")
            movies = cursor.fetchall()

            for movie in movies:
                movie_obj = Movie(*movie)
                movie_list.append(movie_obj)

            return movie_list

        except psycopg2.Error as error:
            print("Failed to read data from table", error)
        finally:
            if conn:
                conn.close()

    def get_movie_by_id(self, id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM movie WHERE id = %s"
            cursor.execute(query, (id,))
            movie_data = cursor.fetchone()
            if movie_data:
                movie = Movie(*movie_data)
                return movie
            else:
                return None

        except psycopg2.Error as error:
            print("Failed to read data from table", error)
        finally:
            if conn:
                conn.close()

class MovieManager:
    def __init__(self):
        self.dao = MovieDAO()

    def get_movies(self):
        return self.dao.get_movies()

    def get_movie_by_id(self, id):
        return self.dao.get_movie_by_id(id)

movie_manager = MovieManager()

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = movie_manager.get_movies()
    return jsonify([movie.__dict__ for movie in movies])

@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = movie_manager.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie.__dict__)
    else:
        return jsonify({"error": "Movie not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)


