import sqlite3
import csv

#Create the Games db and games table if they don't exist and populate the
#database.
def populateDatabase():
    db_string = 'data/database/Games.db'

    try:
        db_conn = sqlite3.connect(db_string)
        db_conn.execute("DROP TABLE games")
        db_conn.execute("CREATE TABLE games(GameID INTEGER PRIMARY KEY, \
        Name VARCHAR(200), ReleaseDate VARCHAR(100), Developer VARCHAR(100), \
        Publisher VARCHAR(100), Platform VARCHAR(100), Genre VARCHAR(100), \
        Tags VARCHAR(100), PositiveRatings INTEGER, NegativeRatings INTEGER, \
        AveragePlaytime INTEGER, Price DECIMAL, Description VARCHAR(300),  \
        Image VARCHAR(100));")

        with open('data/games_clean.csv', 'r', encoding='utf8', newline='') as file:
            reader = csv.DictReader(file)
            print("Re-populating database")

            for row in reader:
                db_conn.execute("INSERT INTO games VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
                (row["GameID"], row["Name"], row["ReleaseDate"], row["Developer"], \
                row["Publisher"], row["Platform"], row["Genre"], row["Tags"], \
                row["PositiveRatings"], row["NegativeRatings"], row["AveragePlaytime"], \
                row["Price"], row["Description"], row["Image"]))
    except sqlite3.OperationalError:
        print("Database error- try restarting the server")

    print(db_conn.execute("SELECT * from games WHERE GameID=123").fetchall())
    print("Games database is ready")
    db_conn.close()
