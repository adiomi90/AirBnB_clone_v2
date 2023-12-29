#!/usr/bin/python3
""" A script that starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def display_html():
    states = storage.all(State)
    return render_template("8-cities_by_states.html",
                           Table="States",
                           states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
