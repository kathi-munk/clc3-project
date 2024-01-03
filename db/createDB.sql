-- Removed CREATE DATABASE command

-- movie table
CREATE TABLE movie (
    id          SERIAL PRIMARY KEY,
    title         TEXT NOT NULL,
    overview      TEXT NOT NULL,
    release_date  DATE NOT NULL,
    imgPath       TEXT NOT NULL
);

-- users table
CREATE TABLE users(
    id          SERIAL PRIMARY KEY,
    username     TEXT NOT NULL,
    password TEXT NOT NULL,
    UNIQUE(username)
);

-- user_movie table
CREATE TABLE user_movie(
    userId      INTEGER NOT NULL,
    movieId     INTEGER NOT NULL,
    watched     BOOLEAN NOT NULL,
    rating      INTEGER,
    PRIMARY KEY (userId, movieId),
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- video table
CREATE TABLE video(
    id          SERIAL PRIMARY KEY,
    movieId     INTEGER NOT NULL,
    name        TEXT NOT NULL,
    path        TEXT NOT NULL,
    type        TEXT NOT NULL,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE ON UPDATE CASCADE
);


