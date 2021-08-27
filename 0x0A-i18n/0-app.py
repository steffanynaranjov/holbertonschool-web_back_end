#!/usr/bin/env python3
""" app main """

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def basic_app():
    """ this is a basic app """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)
