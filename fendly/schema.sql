CREATE TABLE IF NOT EXISTS "user" (
    userID INTEGER PRIMARY KEY generated always as identity,
    first_name CHAR(45) NOT NULL,
    last_name CHAR(45) NOT NULL,
    username CHAR(45) NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_details" (
    id INTEGER PRIMARY KEY generated always as identity,
    userID INTEGER UNIQUE NOT NULL,
    profile_pic TEXT NOT NULL,
    job_title TEXT NOT NULL,
    company TEXT NOT NULL,
    linkedIn_username TEXT NOT NULL,
    twitter_username TEXT NOT NULL,
    github_username TEXT NOT NULL,
    website TEXT NOT NULL,
    FOREIGN KEY (userID) REFERENCES "user" (userID) ON DELETE CASCADE ON UPDATE CASCADE
);