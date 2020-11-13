from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()
login_manager = LoginManager()
db = SQLAlchemy()