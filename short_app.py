#!/usr/bin/env python3

from flask import Flask, redirect, request, jsonify
import sqlite3
import os
from hashfunction import get_hash
import requests 
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app = Flask(__name__)

## take environment variables from .env.
load_dotenv()
key = os.getenv('DATABASE_URL1')
app.config['SQLALCHEMY_DATABASE_URI1'] = key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Urls(db.Model):
    __tablename__ = 'url_shortner'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(120), unique=True, nullable=False)
 
    def __init__(self, url, hash):
        self.url = url
        self.hash = hash

    def __repr__(self):
        return self.url

db.create_all()

@app.route('/', methods = ["POST"])
def get_url():
    if request.method == "POST":
        # Receive URL
        urlToSort = request.form.get("urlToSort")

        try:
            res = requests.get(urlToSort)
            correct_url = True
        except:
            return "Please enter a valid URL. Perhaps you miss http:// or https://"

        if correct_url:
            
            ## Calling the hash function from the module
            shotrUrl = get_hash(urlToSort)

            ## Create taable and save long url and hash
            new_url = Urls(url=urlToSort, hash=shotrUrl)
            db.session.add(new_url)
            db.session.commit()
            
            ## Create short URL 
            varToJson = f"{request.root_url}/result/" + shotrUrl

            jsonobj = jsonify({'short URL': varToJson})
    
            return jsonobj


@app.route('/result/<varToJson>', methods = ["GET"])
def show_result(varToJson):
    
    ## Get hash from short URL 
    varToJson = varToJson

    Urls.query.all()
    longUrl = Urls.query.filter_by(hash=varToJson).all()

    ## Redirect to long URL
    return redirect(str(longUrl[0]), 302)


# @app.route('/', methods = ["POST"])
# def get_url():
#     if request.method == "POST":
#         # Receive URL
#         urlToSort = request.form.get("urlToSort")

#         try:
#             res = requests.get(urlToSort)
#             correct_url = True
#         except:
#             return "Please enter a valid URL. Perhaps you miss http:// or https://"

#         if correct_url:
            
#             ## Calling the hash function from the module
#             shotrUrl = get_hash(urlToSort)

#             ## Create taable and save long url and hash
#             connect = sqlite3.connect("project.db")
#             cursor = connect.cursor()
#             cursor.execute("""CREATE TABLE IF NOT EXISTS url_shortner(
#                 id INTEGER PRIMARY KEY,
#                 url TEXT,
#                 hash TEXT 
#             )""")
#             connect.commit()

#             cursor.execute("INSERT INTO url_shortner (url, hash) VALUES (?, ?)", (urlToSort, shotrUrl))
#             connect.commit()
            
#             ## Create short URL 
#             varToJson = f"{request.root_url}/result/" + shotrUrl

#             jsonobj = jsonify({'short URL': varToJson})
    
#             return jsonobj


# @app.route('/result/<varToJson>', methods = ["GET"])
# def show_result(varToJson):
    
#     ## Get hash from short URL 
#     varToJson = varToJson

#     connect = sqlite3.connect("project.db")
#     cursor = connect.cursor()

#     longUrl= cursor.execute('SELECT url FROM url_shortner WHERE hash = ?', (varToJson,))

#     longUrl = cursor.fetchone()

#     ## Redirect to long URL

#     return redirect(longUrl[0], 302)
    


if __name__ == '__main__':
    print("APP IS STARTING")
    print("_______________")
    print(f"PORT IS: {os.environ['SHORT_URL_PORT']}")
    app.run(host='0.0.0.0', port=int(os.environ['SHORT_URL_PORT']))

