-- Removed CREATE DATABASE command

-- movie table
CREATE TABLE movie (
    id            INTEGER PRIMARY KEY,
    title         TEXT NOT NULL,
    overview      TEXT NOT NULL,
    release_date  DATE NOT NULL,
    imgPath       TEXT NOT NULL
);

-- user_movie table
CREATE TABLE user_movie(
    userId      INTEGER NOT NULL,
    movieId     INTEGER NOT NULL,
    watched     BOOLEAN NOT NULL,
    rating      INTEGER,
    PRIMARY KEY (userId, movieId),
    FOREIGN KEY (userId) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- users table
CREATE TABLE user(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    username     TEXT NOT NULL,
    password TEXT NOT NULL,
    UNIQUE(username)
);

-- video table
CREATE TABLE video(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    movieId     INTEGER NOT NULL,
    name        TEXT NOT NULL,
    path        TEXT NOT NULL,
    type        TEXT NOT NULL,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE ON UPDATE CASCADE
);


