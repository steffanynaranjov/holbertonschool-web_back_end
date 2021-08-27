#!/usr/bin/env python3
"""
App FLASK
"""
from flask_babel import Babel
from flask import Flask, render_template, request, g


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


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """
    Best match language
    """
    locale = request.args.get('locale')
    if locale is not None and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id) -> dict:
    """ function that get a user from users """
    return users.get(user_id)


@app.before_request
def before_request():
    """ function that validate if the user exists """
    user_id = request.args.get('login_as')
    if user_id:
        user_id = int(user_id)
    g.user = get_user(user_id)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    home route
    return: template
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
