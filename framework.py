from services import *
from flask import Flask, session, redirect, url_for
import views
from functools import wraps
import configs

app = Flask(__name__)

# initial data
base_troops=query_troops()
base_specialisms=query_specialisms()
base_items=query_items()

def init(app):
    """
    init configs and register routes
    """
    app.config.from_object('configs')
    app.register_blueprint(views.views, url_prefix="")


def _login_required(f):
    """
    decorator function to check if user has logged in
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("current_user", None) != None:
            return f(*args, **kwargs)   
        return redirect(url_for('views.login'))
    return decorated_function


if __name__=="__main__":
    init(app)
    app.run()
