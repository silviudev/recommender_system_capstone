from flask import Flask, render_template, url_for, jsonify, request, flash, redirect
from content_recommender import importTopTenFromCSV
from db_utility import populateDatabase, checkUserDB
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user
from models.user_model import User
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '6649d7dbabb36bf6b6e02f23088b6571'
topTenDict = importTopTenFromCSV()
db_conn = ""
user_db_conn = ""
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#HOME ROUTE
@app.route("/")
@app.route("/home")
def home():
    # Get the top 10 games by most positive ratings
    top_ten_games = db_conn.execute("SELECT GameId, Name, Price, Image, PositiveRatings, \
    NegativeRatings, Genre FROM games ORDER BY PositiveRatings DESC LIMIT 10").fetchall()
    return render_template("home.html", topTen=top_ten_games)

#ABOUT ROUTE
@app.route("/about")
def about():
    return render_template("about.html")

#REGISTER ROUTE
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password and create the user in the database
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        try:
            user_db_conn.execute("INSERT INTO Users (Username, Email, Password) \
            VALUES (?,?,?)", (form.username.data.lower(), form.email.data.lower(), hashed_pass))
            flash(f'Account created for {form.username.data}! You can now log in', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            if "Users.Email" in str(e):
                flash(f'Email is already in use', 'danger')
            elif "Users.Username" in str(e):
                flash(f'Username is already in use', 'danger')
    elif request.method == 'POST' and form.errors:
        # Flash error messages for every error in the form
        for error in form.errors:
            for e in form.errors[error]:
                flash(f"{error.capitalize()} error, {e}", 'danger')
    return render_template("register.html", form=form)

#LOGIN ROUTE
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = None
        user_data = user_db_conn.execute("SELECT * FROM Users WHERE Username = ?",
        (form.username.data.lower(),)).fetchall()
        if user_data:
            user = User(user_data[0][0], user_data[0][1], user_data[0][2], user_data[0][3], user_data[0][4])
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successful for user {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash("Login failed- please check username and password", 'danger')
    elif request.method == 'POST' and form.errors:
        for error in form.errors:
            for str in form.errors[error]:
                flash(f"{error.capitalize()} error, {str}", 'danger')
    return render_template("login.html", form=form)

#LOG OUT ROUTE
@app.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out!", 'success')
    return redirect(url_for('home'))

#RECOMMENDER ROUTE
@app.route("/recommender")
def recommender():
    return render_template("recommender.html", id=request.args.get("id"))

#ANALYTICS ROUTE
@app.route("/analytics")
def analytics():
    #If user not manager redirect home
    if(not current_user.is_authenticated or current_user.type != 'Manager'):
        flash("Access denied-only Manager accounts can access this page", 'danger')
        return redirect(url_for('home'))
    return render_template("analytics.html")

#ACCOUNT PAGE ROUTE
@app.route("/account")
def account():
    #If user not logged in redirect to login
    if(not current_user.is_authenticated):
        flash("Error- must be logged in to access this page", 'danger')
        return redirect(url_for('login'))
    return render_template("account.html")

#GAME SEARCH ROUTE
@app.route("/search")
def search():
    search_terms = request.args.get("data")

    #Get the games where the name matches the search term, up to 100
    search_results =  db_conn.execute("SELECT GameId, Name, Price, Image, \
    Genre FROM games WHERE Name LIKE ? LIMIT 100", ("%" + search_terms + "%",)).fetchall()
    return render_template("search.html", results=search_results, terms=search_terms, num=len(search_results))

#API ROUTE FOR GETTING TOP TEN RECOMMENDATIONS
@app.route("/api/recs")
def getRecs():
    #Get the id of the game from the request parameters
    id = int(request.args.get("id"))

    # Fetch the top ten recommendations' info from the database
    top_ten_tuples = topTenDict[id]

    top_ten_ids = []
    top_ten_sims = []

    for str in top_ten_tuples:
        tup = eval(str)
        top_ten_sims.append(tup[0])
        top_ten_ids.append(tup[1])


    top_ten_list = db_conn.execute("SELECT GameId, Name, Price, Image, PositiveRatings, \
    NegativeRatings FROM games WHERE GameId=? OR GameId=? OR GameId=? OR GameId=? OR GameId=? \
    OR GameId=? OR GameId=? OR GameId=? OR GameId=? OR GameId=?", tuple(top_ten_ids)).fetchall()

    # Get all the info for the main game on the page
    main_data = db_conn.execute("SELECT * FROM games WHERE GameID=?", (id,)).fetchall()

    # return the main game data and top 10 recommended games' data
    # in JSON format
    return jsonify(mainData=main_data, recData=top_ten_list, simData=top_ten_sims)

#API ROUTE FOR POSTING RECOMMENDER OPINION
@app.route("/api/opinion", methods=['GET', 'POST'])
def postOpinion():
    if(current_user.is_authenticated):
        user_id = int(current_user.id)
        game_id = int(request.args.get("id"))
        opinion = request.args.get("opinion")
        if(opinion == "Great!"):
            opinion = 3
        elif opinion == "Okay":
            opinion = 2
        else:
            opinion = 1
        user_db_conn.execute("REPLACE INTO RecommenderOpinions VALUES (?,?,?)",
        (user_id, game_id, opinion))
    return ""

#Function for loading the user to the login managaer
@login_manager.user_loader
def load_user(user_id):
    user_data = user_db_conn.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,)).fetchall()
    return User(user_data[0][0], user_data[0][1], user_data[0][2], user_data[0][3], user_data[0][4])

# Run app in debug mode and check/populate databases
if __name__ == '__main__':
    user_db_conn = checkUserDB(bcrypt)
    db_conn = populateDatabase()
    app.run(debug=True)
