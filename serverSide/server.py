from flask import Flask, jsonify
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
import hashlib

cloud_config= {
        'secure_connect_bundle': 'secure-connect-Exercisewithfriends.zip'
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

@app.route("/login", methods["POST"])
def login():
    login_params = request.get_json()
    usrname = str(login_params["username"]).upper()
    pswd = str(login_params["password"])
    passwordHash = hashlib.sha256()
    passwordHash.update(pswd.encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest())

    if session.execute(session.prepare( """ select count(*) from "Exercisewithfriends".user WHERE username=? and password=? ALLOW FILTERING; """), [usrname, hashedPassword]).one()[0] == 1:
        userID = session.execute(session.prepare( """ select userinfo_id from "Exercisewithfriends".user WHERE username=?; """), [usrname]).one()[0]
        return jsonify({"userinfo_id":userID}),200
    else:
        return jsonify({"error":"unsuccesful"}),200

@app.route("/", methods = ["POST"])
def index():
    return "index"