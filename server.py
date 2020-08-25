from flask import Flask, request, Response, send_file
from flask import jsonify

import time
from flask_cors import CORS
import json

from werkzeug.utils import secure_filename

import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="new_schema")


# Initialize the Flask application
app = Flask(__name__)
CORS(app=app)


current_user_id = 1000
#Account Registration
@app.route('/app/user', methods=['POST'])
def auth():
    r = request.json

    # print(r["username"])
    # print(r["password"])
    # return jsonify({"userid":12334})

    cur = db.cursor()

    current_user_id = current_user_id +1
    sql = "INSERT INTO users (username, passwordd, usersid) VALUES (%s, %s, %s)"
    val = (r["username"],r["password"],current_user_id)
    cur.execute(sql, val)
    db.commit()
    cur.execute("CREATE TABLE current_user_id (website VARCHAR(255),username VARCHAR(255), password VARCHAR(255))")
    return jsonify({"'status': 'account created'"})





#login
@app.route('/app/user/auth', methods=['POST'])
def login():
    r = request.json
    cur = db.cursor()
    cur.execute("SELECT passwordd,usersid FROM users where username=\"%s\" ",r["username"])
    myresult = cur.fetchall()
    if(myresult[0]==r["password"]):
        return jsonify({'status': "success",'userid': myresult[1]})



# #username and password list
@app.route('/app/sites/list/?user={userId}', methods=['GET'])
def listdetails(userId):
    r = request.json
    data = """{[]}"""
    cur.execute("SELECT * FROM %s")
    myresult = cur.fetchall()
    j = json.loads(data)
    for x in myresult:
        y = {"website": x[0]}
        y = {"username": x[1]}
        y = {"password": x[2]}
        data.append(y)
    return y
        
        

# #save new username and password
@app.route('/app/sites?user={userId}', methods=['POST'])
def savenew(userId):
    r = request.json
    sql = "INSERT INTO %s (website, username, password) VALUES (%s, %s, %s)"
    val = (userId,r["username"],r["password"],current_user_id)
    cur.execute(sql, val)
    db.commit()

    return jsonify({'status': "success"})


app.run(port=5000,host="0.0.0.0")

