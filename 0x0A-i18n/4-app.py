#!/usr/bin/env python3
"""
App FLASK
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """
    Config class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)

app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    Best match language
    """
    locale = request.args.get('locale')
    if locale is not None and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    home route
    return: template
    """
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
