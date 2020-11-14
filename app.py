import flask as f
import os

from appdata.extensions import db, login_manager, csrf
from appdata.commands import register
from appdata.routes import main
from appdata.models import Users

def create_app():
    app = f.Flask(__name__)
    app.config.from_pyfile("appdata/settings.py")
    
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)

    register(app)

    login_manager.login_view = 'main.login'
    @login_manager.user_loader
    def loadUser(userID):
        return Users.query.get(userID)
    
    return app