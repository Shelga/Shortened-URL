from flask import Flask, render_template, redirect, request, url_for, jsonify
import sqlite3
import shortuuid
import socketserver
import socket

app = Flask(__name__)



    

# original_socket_bind = socketserver.TCPServer.server_bind
# def socket_bind_wrapper(self):
#     ret = original_socket_bind(self)
#     print("Socket running at {}:{}".format(*self.socket.getsockname()))
#     # Recover original implementation
#     socketserver.TCPServer.server_bind = original_socket_bind
#     return ret

# @app.route("/")
# def hello():
#     return 'Hello, world! running on {}'.format(request.Host)

# socketserver.TCPServer.server_bind = socket_bind_wrapper   #Hook the wrapper
# app.run(port=0, debug=True)


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
    connect = sqlite3.connect("project.db")
    cursor = connect.cursor()

    longUrl= cursor.execute(f'SELECT url FROM url_shortner WHERE hash == {varToJson};')
    print(longUrl)

    return longUrl





if __name__ == '__main__':
    app.run()

