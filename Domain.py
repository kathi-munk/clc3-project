# Here I would put the movie and user dataclasses
from dataclasses import dataclass


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


@dataclass
class User:
    id: int
    username: str
    passwordhash: str
    movies: dict
    
    def __repr__(self): # printing 
        return f"User({self.id}, '{self.username}', '{self.movies}')"