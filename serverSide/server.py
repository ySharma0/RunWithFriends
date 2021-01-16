from flask import Flask, jsonify
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

cloud_config= {
        'secure_connect_bundle': '<<secure-connect-Exercisewithfriends.zip'
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

@app.route("/", methods = ["POST"])
def index():
    return "index"