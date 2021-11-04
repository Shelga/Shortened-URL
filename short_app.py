from flask import Flask, render_template, redirect, request, url_for, jsonify
import sqlite3
import shortuuid
import socket

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

        print(request.environ['SERVER_NAME'])

        # jsonobj = jsonify({'short URL': shotrUrl})
        # return jsonobj

        return 'Hello, world! running on %s' % request.Host
        
    if request.method == "GET":
        ## get hash for url
        # ...
        return redirect(url_for('app.show_result', hash=hash))



@app.route('/result/<hash>', methods = ["GET"])
## result page 
def show_result(hash):
    pass



if __== '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port)