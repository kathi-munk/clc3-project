CREATE DATABASE clc_moviedb;

CREATE TABLE movie (
    id				INT(11)			NOT NULL,
	title			VARCHAR(150) 	NOT NULL,
	overview		VARCHAR(500)	NOT NULL,
	release_date	DATE			NOT NULL,
	imgPath			VARCHAR(100)	NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE user_movie(
    userId      INT(11)     NOT NULL,
    movieId     INT(11)     NOT NULL,
    watched     BOOLEAN     NOT NULL,
    rating      INT(11),
    PRIMARY KEY (userId, movieId)
);

CREATE TABLE users(
     id           INT(11) NOT NULL auto_increment,
     username     VARCHAR(255) NOT NULL,
     passwordhash CHAR(40) NOT NULL,
     PRIMARY KEY (id),
     UNIQUE KEY username (username)
);

CREATE TABLE video(
    id          INT(11)         NOT NULL auto_increment,
    movieId     INT(11)         NOT NULL,
    name		VARCHAR(150) 	NOT NULL,
    path		VARCHAR(100)	NOT NULL,
    type        VARCHAR(100)    NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE user_movie ADD CONSTRAINT user_movie_fk1 FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE user_movie ADD CONSTRAINT user_movie_fk2 FOREIGN KEY (movieId) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE video ADD CONSTRAINT video_mvfk_1 FOREIGN KEY (movieId) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;