import click, datetime
from flask.cli import with_appcontext

from appdata.extensions import db
from appdata.models import Hotel, User, Customer, Employee, Reservation, Visit, Ongoing, Past


def register_commands(app):
    @app.cli.command(name='create_db', help="Create empty database.")
    def create_db():
        db.create_all()

    @app.cli.command(name='fill_db', help='Fill up DB with sample data')
    def fill_db():

        admin_employee = Employee(
            user=User(
                login='admin',
                unhashed_password='admin'
            ),
            isAdmin=True,
            isOwner=True
        )

        owner_employee = Employee(
            user=User(
                login='owner',
                unhashed_password='owner'
            ),
            isOwner=True
        )
        manager_employee = Employee(
            user=User(
                login='manager',
                unhashed_password='manager'
            )
        )
        test_customer = Customer(
            user=User(
                login='test',
                unhashed_password='test'
            ),
            email='test@test.com'
        )

        res = Reservation(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime.now(),
                date_to = datetime.datetime.now(),
                price = 6548
            )
        )

        db.session.add(admin_employee)
        db.session.add(owner_employee)
        db.session.add(manager_employee)
        db.session.add(test_customer)

        db.session.commit()
