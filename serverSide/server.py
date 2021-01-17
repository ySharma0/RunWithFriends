from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
import hashlib

cloud_config= {
        'secure_connect_bundle': 'secure-connect-exercisewithfriends.zip'
}


# check for env variables
if not os.getenv("DATABASE_USERNAME"):
    raise RuntimeError("DATABASE_USERNAME is not set")
if not os.getenv("DATABASE_PASSWORD"):
    raise RuntimeError("DATABASE_PASSWORD is not set")


# setup database
usrname = os.getenv("DATABASE_USERNAME")
pswrd = os.getenv("DATABASE_PASSWORD")
auth_provider = PlainTextAuthProvider(usrname, pswrd)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()


app = Flask(__name__)


#Check if user exists method:
def checkUser(username):
    checkIfUserExistsQuery = "SELECT username FROM 'Exercisewithfriends'.user"
    if(session.execute(checkIfUserExistsQuery) != None):
        return True
    else:
        return False

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def index():
    return "index"
# LOGIN API
# @app.route("/login", methods =["POST"])
# def login():
#     login_params = request.get_json()
#     usrname = str(login_params["username"]).upper()
#     pswd = str(login_params["password"])
#     passwordHash = hashlib.sha256()
#     passwordHash.update(pswd.encode('utf8'))
#     hashedPassword = str(passwordHash.hexdigest())

#     if session.execute(session.prepare( """ select count(*) from "Exercisewithfriends".user WHERE username=? and password=? ALLOW FILTERING; """), [usrname, hashedPassword]).one()[0] == 1:
#         userID = session.execute(session.prepare( """ select userinfo_id from "Exercisewithfriends".user WHERE username=?; """), [usrname]).one()[0]
#         return jsonify({"userinfo_id":userID}),200
#     else:
#         return jsonify({"error":"unsuccesful"}),200
        
@app.route("/signup", methods = ["POST"])
def signup():
    signup_params = request.get_json()
    username = str(signup_params["username"]).upper()
    password = str(signup_params["password"])
    firstName = str(signup_params["firstName"]).capitalize()
    lastName = str(signup_params["lastName"]).capitalize()
    email = str(signup_params["email"]).upper()
    age = int(signup_params["age"])
    gender = str(signup_params["gender"]).upper()
    country = str(signup_params["country"]).upper()
    passwordHash = hashlib.sha256()
    passwordHash.update(password.encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest())
    placeholderFriendslist = set()

    if( checkUser == True):
        return "error, username already exists"
    else:
        
        session.execute(session.prepare("""INSERT INTO "Exercisewithfriends".user (username,password,userinfo_id) VALUES(?,?,uuid())"""),[username, hashedPassword])
        # Get id of just created user:
        userID = session.execute(session.prepare( """ select userinfo_id from "Exercisewithfriends".user WHERE username=?; """), [username]).one()[0]
        # update user info:
        session.execute(session.prepare("""insert into "Exercisewithfriends".user_info (id, age, country, email, first_name, friend_list, gender, last_name) values (?,?,?,?,?,?,?,?)"""),[userID,age,country,email,firstName,placeholderFriendslist,gender,lastName])
        return jsonify({"sucess":"user created"}),200

@app.route("/addfriend", methods = ["POST"])
def addfriend():
    addfriend_params = request.get_json()
    username = str(addfriend_params["username"]).upper()
    friend = str(addfriend_params["friend"]).upper()
    if(checkUser(username) == False):
        return jsonify({"error":"user does not exist"})
    else:
        userId = None
        getFriendsListQuery = "SELECT friends_list FROM 'Exercisewithfriends'.user_info WHERE user_id=" + userId
        getUserIdQuery = "SELECT userinfo_id FROM 'Exercisewithfriends'.user WHERE username="+username
        addFriendQuery = """UPDATE friends_list FROM 'Exercisewithfriends'.user_info SET friends_list = [?] + friends_list WHERE userId = ?"""
        # Get userId from username:
        userId = session.execute(getUserIdQuery).one()
        # check if users are already friends:
        friends = session.execute(getFriendsListQuery).one()
        if friends != None:
            if friend in friends:
                return jsonify({"error":"friend already added"})
        else:
            # Add friend to list:
            session.execute(session.prepare(addFriendQuery),[friend,userId])
            return({"success":"Added friend"}),200