CREATE TABLE players (
    email TEXT PRIMARY KEY NOT NULL,
    nickname TEXT NOT NULL,
    pswd TEXT NOT NULL
);

CREATE TABLE scoreboard(
    emailPlayer TEXT PRIMARY KEY,
    win INTEGER,
    FOREIGN KEY (emailPlayer) REFERENCES player (email)
);