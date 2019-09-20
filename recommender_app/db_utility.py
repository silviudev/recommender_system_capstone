import sqlite3
import csv

# Create the Games db and games table in RAM and populate the
# database.
def populateDatabase():
    try:
        db_conn = sqlite3.connect(":memory:", check_same_thread=False)
        db_conn.isolation_level = None
        db_conn.execute("CREATE TABLE games(GameID INTEGER PRIMARY KEY, \
        Name VARCHAR(200), ReleaseDate VARCHAR(100), Developer VARCHAR(100), \
        Publisher VARCHAR(100), Platform VARCHAR(100), Genre VARCHAR(100), \
        Tags VARCHAR(100), PositiveRatings INTEGER, NegativeRatings INTEGER, \
        AveragePlaytime INTEGER, Price DECIMAL, Description VARCHAR(300),  \
        Image VARCHAR(100));")

        with open('data/games_clean.csv', 'r', encoding='utf8', newline='') as file:
            reader = csv.DictReader(file)
            print("Re-populating games database")

            for row in reader:
                db_conn.execute("INSERT INTO games VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
                (row["GameID"], row["Name"], row["ReleaseDate"], row["Developer"], \
                row["Publisher"], row["Platform"], row["Genre"], row["Tags"], \
                row["PositiveRatings"], row["NegativeRatings"], row["AveragePlaytime"], \
                row["Price"], row["Description"], row["Image"]))
    except sqlite3.OperationalError:
        print("Database error- try restarting the server")

    print("Games database is ready")
    return db_conn

# Check to see if the Users and Recommender tables exist in the Users database
# and create them if not.
def checkUserDB(bcrypt):
    try:
        user_db_conn = sqlite3.connect("data/database/Users.db", check_same_thread=False)
        user_db_conn.isolation_level = None
        user_db_conn.execute("CREATE TABLE IF NOT EXISTS Users(UserID INTEGER PRIMARY KEY AUTOINCREMENT, \
        Username VARCHAR(20) UNIQUE, Email VARCHAR(200) UNIQUE, Password VARCHAR(200), AccountType VARCHAR(10) \
        DEFAULT 'Customer')")
        user_db_conn.execute("CREATE TABLE IF NOT EXISTS RecommenderOpinions (UserID INTEGER, \
        GameID INTEGER, Opinion TINYINT, FOREIGN KEY(UserID) REFERENCES Users(UserID), PRIMARY KEY(UserID, GameID))")
        # Create the special Manager account if doesn't exist
        if not user_db_conn.execute("SELECT * FROM Users WHERE username='manager' and AccountType='Manager'").fetchall():
            manager_pass = "test"
            special_pass = bcrypt.generate_password_hash(manager_pass).decode("UTF-8")
            user_db_conn.execute("INSERT INTO Users (Username, Email, Password, AccountType) \
            VALUES ('manager', 'management@awesomegames.com', ?, 'Manager')", (special_pass,))
    except sqlite3.OperationalError as e:
        print("Database error- try restarting the server")
        print("Error description " + str(e))
    print("Users database is ready")
    return user_db_conn
