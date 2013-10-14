import os
from flask import Flask, render_template
import json

app = Flask(__name__)

file=open('data.json')
data=json.load(file)
file.close()

@app.route("/", methods=['GET'])
def index():
    global data
    return render_template('index.html', data=data)

if 'DYNO' not in os.environ:
	app.debug = True
	app.run()