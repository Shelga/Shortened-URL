from flask import Flask, redirect, request, jsonify
import sqlite3
import shortuuid


app = Flask(__name__)



@app.route('/', methods = ["POST"])
## index page
def get_url():
    if request.method == "POST":
        urlToSort = request.form.get("urlToSort")
       
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
        
        varToJson = f"{request.root_url}/result/" + shotrUrl

        jsonobj = jsonify({'short URL': varToJson})
  
        return jsonobj





@app.route('/result/<varToJson>', methods = ["GET"])
def show_result(varToJson):
    
    varToJson = varToJson
    print("varToJson", varToJson)

    connect = sqlite3.connect("project.db")
    cursor = connect.cursor()

    # longUrl= cursor.execute('SELECT url FROM url_shortner WHERE hash = "LKEWWrV5";')
    longUrl= cursor.execute('SELECT url FROM url_shortner WHERE hash = ?', (varToJson,))

    longUrl = cursor.fetchone()
    print("longUrl", longUrl)


    # return "Hello"
  

    return redirect(longUrl[0], 302)


if __name__ == '__main__':
    app.run()

