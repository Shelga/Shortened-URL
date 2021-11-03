from flask import Flask, render_template, redirect, request
import sqlite3
import shortuuid


app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
## index page

def index():
    if request.method == "POST":
        urlToSort = request.form.get("urlToSort")

        if not urlToSort:
            return render_template("apology.html", message = "You must provide a URL")

        shotrUrl = shortuuid.uuid(urlToSort)[:8]

        connect = sqlite3.connect("project.db")
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS url_shortner(
            id INTEGER PRIMARY KEY,
            url TEXT,
            hash TEXT 
        )""")

        connect.commit()

        cursor.execute("INSERT INTO url_shortner (url, hash) VALUES (?, ?)", (urlToSort, shotrUrl))
        connect.commit()
        
        return render_template("result.html")

    if request.method == "GET":
        return render_template("/index.html")

# @app.route('/result', methods = ["GET", "POST"])
# ## result page 
# def hello():
#     return render_template("/result.html")