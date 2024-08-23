from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to the demo scrapper"

if __name__ == "__main__":
    app.run(debut=True)

from controller import *