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
        conn = sqlite3.connect("db/movies.db")
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
        conn = sqlite3.connect("db/movies.db")
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

