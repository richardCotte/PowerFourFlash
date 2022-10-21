CREATE TABLE player (
    email TEXT PRIMARY KEY,
    pseudo TEXT,
    pass TEXT
);

CREATE TABLE scoreboard(
    emailPlayer TEXT PRIMARY KEY,
    win INTEGER,
    FOREIGN KEY (emailPlayer) REFERENCES player (email)
);