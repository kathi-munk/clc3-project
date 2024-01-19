# CLC3 Project - From a Monolith to Microservices

## Project description
We built a small monolithic application that provides an overview over a collection of movies that we got from the open-source movie database "The Movie Database (TMDB)". Users with a user account on this website are able to maintain a watchlist, which they can fill with movies from the overview list. After watching the movies they can rate them an add them to their movie history list.

As a next step the monolithic application was restructed to work as multiple microservices. Therefore, we firstly dockerized the application, meaning that the webapp, user management, movie management and database were put into seperate docker containers and the docker images were published on Docker Hub.
Further details on how the application was restructed can be found in [From monolith to microservice](#monoToMicro).

Finally, to demonstrate that the microservices can be deployed on a cloud service, we deployed them on kubernetes using kind. A more detailed information on how to to this can be found in [How to setup microservices on kubernetes](#setupMicro).

<a name="monoToMicro"></a>

## From monolith to microservice
## Overview: Monolith Movie List Application

The **Monolith Movie List Application** is a web-based platform designed for managing movie and user data. It's built using Python and SQLite, and offers a user-friendly interface for users to interact with their movie collection. The application is comprised of several key Python modules, each dedicated to specific functions.

## Key Components

### Domain.py
- Contains data classes for Movie and User.
- **Movie**: Stores information such as ID, title, overview, release date and image path.
- **User**: Holds details including ID, username, password, and a dictionary to store movies.

### DAOs.py (Data Access Objects)
- Includes `UserDAO` and `MovieDAO` classes.
- Handles database interactions with SQLite, performing tasks like data retrieval, insertion, and updates.
  - `UserDAO`: Manages user-related data operations.
  - `MovieDAO`: Handles operations related to movie data.

### Managers.py
- Contains `UserManager` and `MovieManager` classes.
- Utilizes DAOs for database access and provides data to the UI.
  - `UserManager`: Deals with user login, watchlist, and watched movies functionalities.
  - `MovieManager`: Responsible for retrieving movie details.

### Web Application with Streamlit
- Uses Streamlit for creating a user-friendly web interface.
- Facilitates user interactions with the application, such as viewing movies, managing watchlists, and tracking watched movies.

### Database
![Database](https://github.com/kathi-munk/clc3-project/blob/main/img/db_model.png)

### Features
- **User Authentication**: Supports user login functionality.
- **Movie Management**: Users can view movies, add them to their watchlist, and mark them as watched with ratings.
- **Dynamic Data Handling**: Interacts dynamically with the SQLite database for real-time data updates.

### Monolith Architecture
![Monolith Architecture](https://github.com/kathi-munk/clc3-project/blob/main/img/Monolith.png)


## Overview: Microservices Movie Listing Application
This application is a movie listing platform developed using Python and PostgreSQL. It provides features for users to view movies, manage watchlists, track watched movies and rate movies.

### Features
- View a list of movies.
- User authentication and management.
- Add movies to a personal watchlist.
- Mark movies as watched and rate them.

### Requirements
- Python 3.x
- Flask
- psycopg2
- Streamlit
- Docker

### Database Setup
- Ensure PostgreSQL is installed.
- Create a database named `movies`.

### Backend Services
The application consists of two main Python scripts: `MovieRest.py` and `User_Rest.py`.
- `MovieRest.py`: Handles movie-related operations.
- `User_Rest.py`: Manages user authentication and their watchlist.

### Frontend
- The GUI is built with Streamlit, contained in a script named `home.py` in combination with other Py-Files.

### Docker
- The application is designed for containerization using Docker.

### Running the Application
1. Build the Docker images for the backend services and the frontend.
2. Run the Docker containers.
3. Access the Streamlit interface on the specified port.

## API Endpoints

### Movie Service
- `GET /movies`: Fetch all movies.
- `GET /movie/<int:movie_id>`: Fetch a single movie by its ID.

### User Service
- `POST /login`: Authenticate a user.
- `GET /user/<int:user_id>/watchlist`: Get a user's watchlist.
- `GET /user/<int:user_id>/watched`: Get a user's watched movies.
- `POST /user/<int:user_id>/add_movie`: Add a movie to a user's watchlist.
- `POST /user/<int:user_id>/watched_movie`: Mark a movie as watched.

## Architecture
![Microservice Architecture](https://github.com/kathi-munk/clc3-project/blob/main/img/Microservices.png)


Docker structure -> Magdalena
We created seperate Dockerfiles for Movie, User, Web and Database. In the docker-compose for each dockerfile a container is defined. The web container sends http-requests to the API containers. These are accessed via the hostname which is the same as the container name defined in the compose file. The dockerfiles are aufgebaut: using python base container, coppying needed files, install dependencies like Flask, set environment variables (which app flask should run). Start flask/streamlit on the defined port (5001, 5002). In the database docker the environments variables are the login data for the database. (evtl sollten wir die login daten von der db ins docker compose damits ned jedes mal die container neu gebaut werden müssen)

<a name="setupMicro"></a>
## How to setup microservices on kubernetes
Kind installieren, kompose installieren, ...
Kubernetes steps aufzählen

## Summary of lessons-learned
gemeinsam
