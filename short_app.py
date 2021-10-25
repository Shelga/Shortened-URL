from flask import Flask

app = Flask(__name__)

@app.route('/')
## index page
def index():
    return 'Index Page'

@app.route('/result')
## result page 
def hello():
    return 'Hello, World'