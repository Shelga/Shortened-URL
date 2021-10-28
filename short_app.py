from flask import Flask, render_template, redirect, request

import sqlite3

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
## index page
def index():
    if request.method == "POST":
        pass
    if request.method == "GET":
        return render_template("/index.html")

@app.route('/result')
## result page 
def hello():
    return render_template("/result.html")