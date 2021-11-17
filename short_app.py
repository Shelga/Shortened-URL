from flask import Flask, redirect, request, jsonify
import sqlite3
from hashfunction import get_hash

import requests 


app = Flask(__name__)


@app.route('/', methods = ["POST"])
def get_url():
    if request.method == "POST":
        ## Receive URL
        urlToSort = request.form.get("urlToSort")
       
        ## Calling the hash function from the module
        shotrUrl = get_hash(urlToSort)

        ## Create taable and save long url and hash
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
        
        ## Create short URL 
        varToJson = f"{request.root_url}/result/" + shotrUrl

        jsonobj = jsonify({'short URL': varToJson})
  
        return jsonobj


@app.route('/result/<varToJson>', methods = ["GET"])
def show_result(varToJson):
    
    ## Get hash from short URL 
    varToJson = varToJson

    connect = sqlite3.connect("project.db")
    cursor = connect.cursor()

    longUrl= cursor.execute('SELECT url FROM url_shortner WHERE hash = ?', (varToJson,))

    longUrl = cursor.fetchone()

    ## Redirect to long URL
    return redirect(longUrl[0], 302)


if __name__ == '__main__':
    app.run()

