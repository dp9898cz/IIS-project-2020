import flask as f
import os

from .extensions import db, login_manager
from .commands import register
from .routes import main
from .models import Users

def create_app():
    app = f.Flask(__name__)
    app.config.from_pyfile("settings.py")
    
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)

    register(app)

    #login_manager.login_view = ''
    @login_manager.user_loader
    def loadUser(userID):
        return Users.query.get(userID)
    
    return app