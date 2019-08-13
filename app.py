import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY")
app.config["MONGO_DBNAME"]="CookBook"
app.config["MONGO_URI"]=os.getenv("MONGO_URI")

mongo=PyMongo(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route('/sign_in')
def sign_in():
    # Release the session variables
    # session.pop('logged_in', None)
    # session.pop('user', None)
    return render_template('login.html')   
   
@app.route('/login',methods=['GET','POST'])
def login():
    users=mongo.db.users
    username=request.form['user']
    #Search for the inserted username in the DB
    user=users.find_one({"user":username})
    #Is user in the DB check if passwords match
    if user:
        password=user['password']
        if request.form['password']==password:
            session['user']=username
            session['logged_in']=True
            return redirect(url_for('home'))
        else:
            flash('Wrong password')    
            return redirect(url_for('sign_in'))
    else:        
        flash('Wrong username')    
        return redirect(url_for('sign_in'))  
# New user registration template.
@app.route('/new_user')
def new_user():
    return render_template('new_user.html')  

# New user registration submit
@app.route('/new_user/register', methods=['GET','POST'])
def register():
    user={}
    users=mongo.db.users
    username=request.form['user']
    # Checks if the user name is in use 
    if users.find_one({"user":username}):
        flash('Username not valid, already taken.')
        return redirect(url_for('new_user'))
    else: 
        # User name valid as new user, redirecting to the login page
        user["user"]=username
        user["password"]=request.form['password']
        users.insert_one(user)
        flash('User created. You can now login.')
        return redirect(url_for('sign_in'))
            
@app.route("/recipes")
def recipes():
    return render_template("recipes.html")
    
@app.route("/favourites")
def favourites():
    return render_template("favourites.html")
    
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)