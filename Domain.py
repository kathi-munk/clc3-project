# Here I would put the movie and user dataclasses
from dataclasses import dataclass


@dataclass
class Movie:
    pass

@dataclass
class User:
    id: int
    username: str
    passwordhash: str
    movies: list
    
    def __repr__(self): # printing 
        return f"User({self.id}, '{self.username}', '{self.movies}')"