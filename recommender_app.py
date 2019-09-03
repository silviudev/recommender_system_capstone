from flask import Flask, render_template, url_for, jsonify, request
from content_recommender import importTopTenFromCSV
from db_utility import populateDatabase

app = Flask(__name__)
topTenDict = importTopTenFromCSV()

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/recommender")
def recommender():
    return render_template("recommender.html")

@app.route("/api/recs")
def getRecs():
    id = int(request.args.get("id", 0))
    return jsonify(topTenDict[id])


if __name__ == '__main__':
    populateDatabase()
    app.run(debug=True)
