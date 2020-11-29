import flask as f
import os

from appdata.extensions import db, login_manager, csrf
from appdata.commands import register_commands
from appdata.routes.main import main
from appdata.routes.dashboard import dash
from appdata.models import User

def create_app():
    app = f.Flask(__name__)
    app.config.from_pyfile("appdata/settings.py")
    
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(dash)
    csrf.exempt(dash)
    csrf.exempt(main)

    register_commands(app)

    login_manager.login_view = 'main.login'
    @login_manager.user_loader
    def loadUser(userID):
        return User.query.get(userID)

    @app.template_filter()
    def intersect(a, b):
        return len(set(a).intersection(b))
    
    return app