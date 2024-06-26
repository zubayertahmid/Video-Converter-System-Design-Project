import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

#config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
print(server.config["MYSQL_HOST"]) 

server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing Credentials", 401
    #database check for usename and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM users WHERE username = %s", ([auth.username])
        )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        if auth.username != email or auth.password != password:
            return "Invalid Credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("SECRET_KEY"), True)
    else:
        return "Invalid Credentials", 401
    
@server.route("/validate", methods=["POST"])
def validate():
    token = request.headers.get("Authorization")
    if not token:
        return "Missing Authorization Header", 401
    
    token = token.split(" ")[1]
    try:
        decoded = jwt.decode(
            token, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "Not authorized", 403
def createJWT(username, secret, is_admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "is_admin": is_admin,
        },
        secret,
        algorithm="HS256",
    )
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)