# CLC3 Project - From a Monolith to Microservices

## Project description
We built a small monolithic web application that provides an overview over a collection of movies that we got from the open-source movie database "The Movie Database (TMDB)". Users with a user account on this website are able to maintain a watchlist, which they can fill with movies from the overview list. After watching the movies they can rate them an add them to their movie history list.

As a next step the monolithic application was restructed to work as multiple microservices. Therefore, we firstly dockerized the application, meaning that the webapp, user management, movie management and database were put into seperate docker containers and the docker images were published on Docker Hub.
Further details on how the application was restructed can be found in down below.

Finally, to demonstrate that the microservices can be deployed on a cloud service, we deployed them on kubernetes using kind.

## Requirements
- Python 3.10
- Python packages defined in requirements.txt
- Docker
- kubectl
- [kind](https://kind.sigs.k8s.io/)

## Monolith 
### Architecture
![Monolith Architecture](https://github.com/kathi-munk/clc3-project/blob/main/img/Monolith.png)

The application was built with Python and SQLite, and offers a user-friendly interface for users to interact with their movie collection. The application is built of multiple python "modules", each dedicated to specific functions.

### Key Components
#### Domain.py
- Contains data classes for Movie and User.
- **Movie**: Stores information such as ID, title, overview, release date and image path.
- **User**: Holds details including ID, username, password, and a dictionary to store movies.

#### DAOs.py (Data Access Objects)
- Includes `UserDAO` and `MovieDAO` classes.
- Handles database interactions with SQLite, performing tasks like data retrieval, insertion, and updates.
  - `UserDAO`: Manages user-related data operations.
  - `MovieDAO`: Handles operations related to movie data.

#### Managers.py
- Contains `UserManager` and `MovieManager` classes.
- Utilizes DAOs for database access and provides data to the UI.
  - `UserManager`: Deals with user login, watchlist, and watched movies functionalities.
  - `MovieManager`: Responsible for retrieving movie details.

#### Web Application with Streamlit
- Uses Streamlit for creating a user-friendly web interface.
- Facilitates user interactions with the application, such as viewing movies, managing watchlists, and tracking watched movies.

#### Database
<img src="img/db_model.png" alt="Database" width="300" height="auto">


For the Monolith we opted for a sqlite database since it was easier to start with. However, for the microservices architecture we chose a PostgreSQL database to enable external access via a dedicated port.

----Featuresteil würd ich entfernen
#### Features
- **User Authentication**: Supports user login functionality.
- **Movie Management**: Users can view movies, add them to their watchlist, and mark them as watched with ratings.
- **Dynamic Data Handling**: Interacts dynamically with the SQLite database for real-time data updates.

## Microservices 
### Architecture
![Microservice Architecture](https://github.com/kathi-munk/clc3-project/blob/main/img/Microservices.png)

### Database change
Instead of a SQLLite database a PostgreSQL database is now used, as these can be access via HTTP and the goal was to put the database into its own container and access it there.

### Backend Services
The application consists of two main Python scripts: `MovieRest.py` and `User_Rest.py`.
- `MovieRest.py`: Handles movie-related operations.
- `User_Rest.py`: Manages user authentication and their watchlist.


### API Endpoints

#### Movie Service
- `GET /movies`: Fetch all movies.
- `GET /movie/<int:movie_id>`: Fetch a single movie by its ID.

#### User Service
- `POST /login`: Authenticate a user.
- `GET /user/<int:user_id>/watchlist`: Get a user's watchlist.
- `GET /user/<int:user_id>/watched`: Get a user's watched movies.
- `POST /user/<int:user_id>/add_movie`: Add a movie to a user's watchlist.
- `POST /user/<int:user_id>/watched_movie`: Mark a movie as watched.


## Dockerization
For  Movie, User, Web and Database seperate Dockerfiles were created. The docker-compose defines a container for each dockerfile. The Web container establishes HTTP connections with the API containers, utilizing hostnames matching the container names defined in the compose file.
The dockerfiles follow this structure: 
- using python as base image
- copying needed files
- install dependencies e.g. Flask
- set environment variables (e.g. which app flask should run)
- starting flask/streamlit on the defined port (e.g. 5001 = movies-rest)
In the database container the environments variables are the login data for the database. <span style="color: red;">(? To avoid repeated container rebuilding, we might consider incorporating the database login information directly into the docker-compose file.?)</span>

Here's the overview of the launched containers and their associated ports:
![Docker Structure](https://github.com/kathi-munk/clc3-project/blob/main/img/dockercontainer_structure.png)

### Running the microservice in docker
1. Build the Docker images for the backend services and the frontend.
2. Run the Docker containers.
3. Access the Streamlit interface on the specified port.

## Microservices on Kubernetes
To run the microservices on Kubernetes we built on the before explained docker-compose.

To convert the docker-compose into the Kubernetes configuration files, `konvert compose` was used to built the deployment and service YAML files. These configuration files can be found in the kubernetes folder.

To finally setup and start the application in Kubernetes the following steps need to be done:
- open the repository in the CLI 
- change into the microservice/kubernetes folder (`cd microservice\kubernetes`)
- create a Kubernetes cluster: `kind create cluster`
- apply the configuration files: `kubectl apply -f .`
- check that deployments were created: `kubectl get deployments`
- check that services were created: `kubectl get svc`
- open port to web application: `kubectl port-forward service/web-application 8501:8501`
- open application in `127.0.0.1:8501`



## Summary of lessons-learned
gemeinsam
