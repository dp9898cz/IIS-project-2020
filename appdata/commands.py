import click, datetime
from flask.cli import with_appcontext

from appdata.extensions import db
from appdata.models import Hotel, User, Customer, Employee, Reservation, Visit, Ongoing, Past, Room


def register_commands(app):
    @app.cli.command(name='create_db', help="Create empty database.")
    def create_db():
        db.create_all()

    @app.cli.command(name='fill_db', help='Fill up DB with sample data')
    def fill_db():

        admin_employee = Employee(
            user=User(
                login='admin',
                unhashed_password='admin',
                isEmployee=True,
                name='Admin',
                surname='Admin'
            ),
            isAdmin=True,
            isOwner=True,
            email='test@test.com'
        )

        owner_employee = Employee(
            user=User(
                login='owner',
                unhashed_password='owner',
                isEmployee=True,
                name='Owner',
                surname='Owner'
            ),
            isOwner=True,
            email='test@test.com'
        )
        manager_employee = Employee(
            user=User(
                login='manager',
                unhashed_password='manager',
                isEmployee=True,
                name='Manager',
                surname='Manager'
            ),
            email='test@test.com'
        )
        test_customer = Customer(
            user=User(
                login='test',
                unhashed_password='test',
                name='Customer',
                surname='One'
            ),
            email='test@test.com'
        )

        test_hotel = Hotel(
            name = 'MyHotel',
            address = 'ulice č',
            description = 'deshkdsfgkbiiuv',
            rooms = [
                Room(
                    number = 565,
                    night_price = 54.88,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 566,
                    night_price = 88,
                    room_type = 'PREM',
                    number_of_beds = 3
                )
            ]
        )

        test_hotel_2 = Hotel(
            name = 'MyHotel_2',
            address = 'ulice č 2',
            description = 'deshkdsfgkbidfDiuv',
            rooms = [
                Room(
                    number = 565,
                    night_price = 54.88,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 566,
                    night_price = 88,
                    room_type = 'PREM',
                    number_of_beds = 3
                )
            ]
        )

        another_room = Room(
            number = 569,
            night_price = 48,
            room_type = 'BUSS',
            number_of_beds = 3,
            hotel = test_hotel
        )

        res = Reservation(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 27).date(),
                date_to = datetime.datetime(2020, 11, 30).date(),
                price = 6548,
                visit_type = 'RES',
                rooms = test_hotel.rooms
            )
        )

        on = Ongoing(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 29).date(),
                date_to = datetime.datetime(2020, 12, 12).date(),
                price = 888,
                visit_type = 'NOW',
                rooms = [
                    another_room
                ]
            ),
            key_customer = True
        )

        past = Past(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 20).date(),
                date_to = datetime.datetime(2020, 11, 25).date(),
                price = 68448.888,
                visit_type = 'PAS',
                rooms = [
                    another_room
                ]
            ),
        )

        db.session.add(admin_employee)
        db.session.add(test_hotel_2)
        db.session.add(owner_employee)
        db.session.add(manager_employee)
        db.session.add(test_customer)

        db.session.commit()
