import sqlite3 as sql

def insertUser(email,nickname,pswd):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO players (email, nickname, pswd) VALUES (?,?)", (email,pswd))
    con.commit()
    con.close()

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT email, nickname, pswd FROM players")
	users = cur.fetchall()
	con.close()
	return users