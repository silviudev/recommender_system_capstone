from flask import Flask, render_template, url_for, jsonify, request
from content_recommender import importTopTenFromCSV
from db_utility import populateDatabase
import sqlite3

app = Flask(__name__)
topTenDict = importTopTenFromCSV()
db_conn = ""

@app.route("/")
@app.route("/home")
def home():
    # Get the top 10 games by most positive ratings
    top_ten_games = db_conn.execute("SELECT GameId, Name, Price, Image, PositiveRatings, \
    NegativeRatings, Genre FROM games ORDER BY PositiveRatings DESC LIMIT 10").fetchall()
    return render_template("home.html", topTen=top_ten_games)

@app.route("/recommender")
def recommender():
    return render_template("recommender.html", id=request.args.get("id"))

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/api/recs")
def getRecs():
    #Get the id of the game from the request parameters
    id = int(request.args.get("id"))

    # Fetch the top ten recommendations' info from the database
    top_ten_ids = topTenDict[id]
    top_ten_list = db_conn.execute("SELECT GameId, Name, Price, Image, PositiveRatings, \
    NegativeRatings FROM games WHERE GameId=? OR GameId=? OR GameId=? OR GameId=? OR GameId=? \
    OR GameId=? OR GameId=? OR GameId=? OR GameId=? OR GameId=?", tuple(top_ten_ids)).fetchall()


    # Get all the info for the main game on the page
    main_data = db_conn.execute("SELECT * FROM games WHERE GameID=?", (id,)).fetchall()

    # Printing data for debug purposes
    #print(top_ten_list)
    #print(main_data)

    # return the main game data and top 10 recommended games' data
    # in JSON format
    return jsonify(mainData=main_data, recData=top_ten_list)

if __name__ == '__main__':
    db_conn = populateDatabase()
    app.run(debug=True)
