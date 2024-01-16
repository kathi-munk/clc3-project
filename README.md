# CLC3 Project - From a Monolith to Microservices

## Project description
We built a small monolithic application that provides an overview over a collection of movies that we got from the open-source movie database "The Movie Database (TMDB)". Users with a user account on this website are able to maintain a watchlist, which they can fill with movies from the overview list. After watching the movies they can rate them an add them to their movie history list.

As a next step the monolithic application was restructed to work as multiple microservices. Therefore, we firstly dockerized the application, meaning that the webapp, user management, movie management and database were put into seperate docker containers and the docker images were published on Docker Hub.
Further details on how the application was restructed can be found in [From monolith to microservice](#monoToMicro).

Finally, to demonstrate that the microservices can be deployed on a cloud service, we deployed them on kubernetes using kind. A more detailed information on how to to this can be found in [How to setup microservices on kubernetes](#setupMicro).

<a name="monoToMicro"></a>
## From monolith to microservice
### Database

### Monolith architecture
Grafik die Aufbau zeigt und beschreiben -> Milan

### Microservice architecture
Grafik die Aufbau zeigt und Änderungen aufzählen -> Milan

Docker structure -> Magdalena

<a name="setupMicro"></a>
## How to setup microservices on kubernetes
Kind installieren, kompose installieren, ...
Kubernetes steps aufzählen

## Summary of lessons-learned
gemeinsam