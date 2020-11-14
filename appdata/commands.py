import click
from flask.cli import with_appcontext

from appdata.extensions import db
from appdata.models import Users, Hotel

def register(app):

    @app.cli.command(name='create_db', help="create_db command")
    def create_db():
        db.create_all()