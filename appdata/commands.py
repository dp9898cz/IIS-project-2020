import click
from flask.cli import with_appcontext

from appdata.extensions import db
from appdata.models import Users, Hotel

def register_commands(app):
    @app.cli.command(name='create_db', help="Create empty database.")
    def create_db():
        db.create_all()

    @app.cli.command(name='fill_db', help='Fill up DB with sample data')
    def fill_db():
        pass
    