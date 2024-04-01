import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util 

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err 
@server.route("/upload", methods=["POST"])
def upload():
    token, err = access.login(request)
    if err:
        return err
    if not request.files:
        return "missing file"
    file = request.files["file"]
    if not file:
        return "missing file"
    if not file.filename:
        return "missing file"
    if not util.allowed_file(file.filename):
        return "invalid file type"
    if not validate(token):
        return "invalid token"
    fs.put(file, filename=file.filename)
    return "upload successful"
@server.route("/list", methods=["GET"])
def download():
    pass 

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
    

