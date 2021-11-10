from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/live")
def live():
    return render_template("live.html")

def runServer():
    app.run(debug = True, host="0.0.0.0", port=80)

if __name__ == "__main__":
    runServer()