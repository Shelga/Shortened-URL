from flask import Flask, render_template, redirect, request

import sqlite3

app = Flask(__name__)

@app.route('/')
## index page
def index():
    return render_template("/index.html")

@app.route('/result')
## result page 
def hello():
    return 'Hello, World'