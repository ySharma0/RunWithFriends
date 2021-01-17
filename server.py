from flask import Flask, jsonify, request, render_template
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
import hashlib
import uuid
import json

cloud_config = {
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


# CLIENT:
@app.route("/")
def index():
    return render_template("index.html")


# Check if user exists method:
def checkUser(username):
    if(session.execute(session.prepare("""SELECT username FROM "Exercisewithfriends".user WHERE username = ?"""), [username]).one() != None):
        return True
    else:
        return False


# LOGIN API
@app.route("/login", methods=["POST"])
def login():
    login_params = request.get_json()
    usrname = str(login_params["username"]).upper()
    pswd = str(login_params["password"])
    passwordHash = hashlib.sha256()
    passwordHash.update(pswd.encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest())

    if session.execute(session.prepare(""" select count(*) from "Exercisewithfriends".user WHERE username=? and password=? ALLOW FILTERING; """), [usrname, hashedPassword]).one()[0] == 1:
        userID = session.execute(session.prepare(
            """ select userinfo_id from "Exercisewithfriends".user WHERE username=?; """), [usrname]).one()[0]
        return jsonify({"userinfo_id": userID}), 200
    else:
        return jsonify({"error": "unsuccesful"}), 200


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if(request.method == "GET"):
        return render_template("signup.html")

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

    if(checkUser(username) == True):
        return jsonify({"error": "username already exists"})
    else:

        session.execute(session.prepare(
            """INSERT INTO "Exercisewithfriends".user (username,password,userinfo_id) VALUES(?,?,uuid())"""), [username, hashedPassword])
        # Get id of just created user:
        userID = session.execute(session.prepare(
            """ select userinfo_id from "Exercisewithfriends".user WHERE username=?; """), [username]).one()[0]
        # update user info:
        session.execute(session.prepare("""insert into "Exercisewithfriends".user_info (id, age, country, email, first_name, friend_list, gender, last_name) values (?,?,?,?,?,?,?,?)"""), [
                        userID, age, country, email, firstName, placeholderFriendslist, gender, lastName])
        return jsonify({"success": "user created"}), 200


@app.route("/addfriend", methods=["POST", "GET"])
def addfriend():
    if(request.method == "GET"):
        return render_template("addfriend.html")
    addfriend_params = request.get_json()
    userid = uuid.UUID(addfriend_params["userid"])
    friend = str(addfriend_params["friend"]).upper()
    if(checkUser(friend) == False):
        return jsonify({"error": "user does not exist"})
    else:
        addfriendQuerry = """update "Exercisewithfriends".user_info set friend_list = friend_list + {'""" + \
            friend + """'} where id= ? ;"""
        session.execute(session.prepare(addfriendQuerry), [userid])
        return({"success": "Added friend"}), 200


@app.route("/removefriend", methods=["POST", "GET"])
def removefriend():
    if(request.method == "GET"):
        return render_template("removefriend.html")
    removefriend_params = request.get_json()
    userid = uuid.UUID(removefriend_params["userid"])
    friend = str(removefriend_params["friend"]).upper()
    if(checkUser(friend) == False):
        return jsonify({"error": "user does not exist"})
    else:
        removefriendQuerry = """update "Exercisewithfriends".user_info set friend_list = friend_list + {'""" + \
            friend + """'} where id= ? ;"""
        session.execute(session.prepare(removefriendQuerry), [userid])
        return({"success": "removed friend"}), 200


@app.route("/getfriends", methods=["POST"])
def getfriends():
    getfriends_params = request.get_json()
    userid = uuid.UUID(getfriends_params["userid"])
    friends = session.execute(session.prepare(
        """SELECT friend_list FROM "Exercisewithfriends".user_info WHERE id = ?"""), [userid]).one()[0]
    return json.dumps({"friends": list(friends)}), 200


@app.route("/getuserinfo", methods=["POST"])
def getuserinfo():
    getuserinfo_params = request.get_json()
    userid = uuid.UUID(getuserinfo_params["userid"])
    userinfo = session.execute(session.prepare(
        """SELECT * FROM "Exercisewithfriends".user_info WHERE id = ?"""), [userid]).one()
    return jsonify({"user_id": userinfo[0],
                    "age": userinfo[1],
                    "country": userinfo[2],
                    "email": userinfo[3],
                    "first_name": userinfo[4],
                    "gender": userinfo[6],
                    "last_name": userinfo[7]})


@app.route("/updateuserinfo", methods=["POST"])
def updateuserinfo():
    updateuserinfo_params = request.get_json()
    userid = uuid.UUID(updateuserinfo_params["userid"])
    firstName = updateuserinfo_params["first_name"]
    lastName = updateuserinfo_params["last_name"]
    email = updateuserinfo_params["email"]
    age = updateuserinfo_params["age"]
    gender = updateuserinfo_params["gender"]
    country = updateuserinfo_params["country"]
    session.execute(session.prepare("""UPDATE "Exercisewithfriends".user_info SET first_name=?, last_name=?, email=?,age=?,gender=?,country=? WHERE id = ?"""), [
                    firstName, lastName, email, age, gender, country, userid])
    return jsonify({"success": "updated"})


@app.route("/createchallenge", methods=["POST"])
def createchallenge():
    create_params = request.get_json()
    userid = uuid.UUID(create_params["userid"])
    owner = session.execute(session.prepare(
        """SELECT username FROM "Exercisewithfriends".user WHERE userinfo_id = ? ALLOW FILTERING"""), [userid]).one()[0]
    join_code = str(create_params["join_code"])
    isOngoing = True
    workout = create_params["workout"]
    name = str(create_params["name"])
    scores = {owner: 0}

    if(session.execute(session.prepare("""SELECT count(*) FROM "Exercisewithfriends".challenge WHERE join_code = ?"""), [join_code]).one()[0]):
        return jsonify({"error": "join code already exists"})
    else:
        qparams = [name, join_code, isOngoing, owner, workout, scores]
        session.execute(session.prepare(
            """INSERT INTO "Exercisewithfriends".challenge ( name,join_code, isOngoing , owner , workout, scores) VALUES (?,?,?,?, ?, ?);"""), qparams)
        return jsonify({"success": "challenge created"}), 200


@app.route("/joinchallenge", methods=["POST", "GET"])
def joinchallenge():
    if(request.method == "GET"):
        return render_template("joinchallenge.html")

    join_params = request.get_json()
    userid = uuid.UUID(join_params["userid"])
    username = session.execute(session.prepare(
        """SELECT username FROM "Exercisewithfriends".user WHERE userinfo_id = ? ALLOW FILTERING"""), [userid]).one()[0]
    join_code = str(join_params["join_code"])

    if(not session.execute(session.prepare("""SELECT count(*) FROM "Exercisewithfriends".challenge WHERE join_code = ?"""), [join_code]).one()[0]):
        return jsonify({"error": "join code does not exist"})
    else:
        session.execute(session.prepare(
            """UPDATE "Exercisewithfriends".challenge SET scores = scores + {'""" + username + """': 0} WHERE join_code = ?"""), [join_code])
        session.execute(session.prepare(
            """UPDATE "Exercisewithfriends".user_info SET challenge_list = challenge_list + {'""" + join_code + """'} WHERE id = ?"""), [userid])
        return jsonify({"success": "challenge joined"}), 200


@app.route("/getallchallenge", methods=["POST"])
def getallchallenge():
    join_params = request.get_json()
    userid = uuid.UUID(join_params["userid"])
    challenges = session.execute(session.prepare(
        """SELECT challenge_list FROM "Exercisewithfriends".user_info WHERE id = ? """), [userid]).one()[0]
    x = {}
    for i in challenges:
        x[i] = session.execute(session.prepare(
            """SELECT name FROM "Exercisewithfriends".challenge WHERE join_code = ?"""), [i]).one()[0]
    return jsonify(x)


@app.route("/getchallengeinfo", methods=["POST"])
def getchallengeinfo():
    join_params = request.get_json()
    join_code = str(join_params["join_code"])
    if(not session.execute(session.prepare("""SELECT count(*) FROM "Exercisewithfriends".challenge WHERE join_code = ?"""), [join_code]).one()[0]):
        return jsonify({"error": "join code does not exist"})
    else:
        challenge_info = session.execute(session.prepare(
            """SELECT * FROM "Exercisewithfriends".challenge WHERE join_code = ?"""), [join_code]).one()
        y = ["join_code", "isongoing", "name", "owner"]
        x = {}
        for i in range(len(challenge_info)-2):
            x[y[i]] = challenge_info[i]
        y = list(challenge_info[4].keys())
        y2 = list(challenge_info[4].values())
        x["scores"] = {}
        x["workout"] = {}
        for i in range(len(y)):
            x["scores"][y[i]] = y2[i]
        y = list(challenge_info[5].keys())
        y2 = list(challenge_info[5].values())
        for i in range(len(y)):
            x["workout"][y[i]] = y2[i]

        return jsonify(x)
