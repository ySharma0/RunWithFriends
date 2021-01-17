from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
import hashlib
import uuid
import json

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
    if(session.execute(session.prepare( """SELECT username FROM "Exercisewithfriends".user WHERE username = ?"""),[username]).one() != None):
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

    if( checkUser(username) == True):
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
    userid = uuid.UUID(addfriend_params["userid"])
    friend = str(addfriend_params["friend"]).upper()
    if(checkUser(friend) == False):
        return jsonify({"error":"user does not exist"})
    else:
        addfriendQuerry = """update "Exercisewithfriends".user_info set friend_list = friend_list + {'""" + friend + """'} where id= ? ;"""
        session.execute(session.prepare(addfriendQuerry),[userid])
        return({"success":"Added friend"}), 200


@app.route("/removefriend", methods = ["POST"])
def removefriend():
    removefriend_params = request.get_json()
    userid = uuid.UUID(removefriend_params["userid"])
    friend = str(removefriend_params["friend"]).upper()
    if(checkUser(friend) == False):
        return jsonify({"error":"user does not exist"})
    else:
        removefriendQuerry = """update "Exercisewithfriends".user_info set friend_list = friend_list + {'""" + friend + """'} where id= ? ;"""
        session.execute(session.prepare(removefriendQuerry),[userid])
        return({"success":"removed friend"}), 200

@app.route("/getfriends", methods = ["POST"])
def getfriends():
    getfriends_params = request.get_json()
    userid = uuid.UUID(getfriends_params["userid"])
    friends = session.execute(session.prepare("""SELECT friend_list FROM "Exercisewithfriends".user_info WHERE id = ?"""),[userid]).one()[0]
    return json.dumps({"friends":list(friends)}),200


@app.route("/getuserinfo", methods = ["POST"])
def getuserinfo():
    getuserinfo_params = request.get_json()
    userid = uuid.UUID(getuserinfo_params["userid"])
    userinfo = session.execute(session.prepare("""SELECT * FROM "Exercisewithfriends".user_info WHERE id = ?"""),[userid]).one()
    return jsonify({"user_id":userinfo[0],
                    "age":userinfo[1],
                    "country":userinfo[2],
                    "email":userinfo[3],
                    "first_name":userinfo[4],
                    "gender":userinfo[6],
                    "last_name":userinfo[7]})