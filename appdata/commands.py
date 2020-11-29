import click, datetime
from flask.cli import with_appcontext
from flask import url_for

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

        praha = Hotel(
            name = 'Praha',
            address = 'ulice č 6',
            description = 'deshkdsfgkbiiuv',
            rooms = [
                Room(
                    number = 56,
                    night_price = 54.88,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 58,
                    night_price = 88,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 60,
                    night_price = 88,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel0.png'
        )
        brno = Hotel(
            name = 'Brno',
            address = 'ulice č 6',
            description = 'deshkdsfgkbiiuv',
            rooms = [
                Room(
                    number = 44,
                    night_price = 54.88,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 45,
                    night_price = 88,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 46,
                    night_price = 88,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel1.png'
        )
        olomouc = Hotel(
            name = 'Olomouc',
            address = 'ulice č 6',
            description = 'deshkdsfgkbiiuv',
            rooms = [
                Room(
                    number = 33,
                    night_price = 54.88,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 34,
                    night_price = 88,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 35,
                    night_price = 88,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel2.png'
        )
        hradec = Hotel(
            name = 'Hradec Králové',
            address = 'ulice č 6',
            description = 'deshkdsfgkbiiuv',
            rooms = [
                Room(
                    number = 21,
                    night_price = 54.88,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 22,
                    night_price = 88,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 23,
                    night_price = 88,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel3.png'
        )
        ostrava = Hotel(
            name = 'Ostrava',
            address = 'ulice č 6',
            description = 'deshkdsfgkbiiuv',
            rooms = [
                Room(
                    number = 11,
                    night_price = 54.88,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 12,
                    night_price = 88,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 13,
                    night_price = 88,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel4.png'
        )

        res = Reservation(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 27).date(),
                date_to = datetime.datetime(2020, 11, 30).date(),
                price = 6548,
                visit_type = 'RES',
                rooms = brno.rooms
            )
        )

        on = Ongoing(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 29).date(),
                date_to = datetime.datetime(2020, 12, 12).date(),
                price = 888,
                visit_type = 'NOW',
                rooms = praha.rooms
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
                rooms = ostrava.rooms
            ),
        )

        admin_employee.hotel = praha
        owner_employee.hotel = olomouc
        manager_employee.hotel = hradec


        db.session.add(admin_employee)
        db.session.add(owner_employee)
        db.session.add(manager_employee)
        db.session.add(test_customer)

        db.session.add(praha)
        db.session.add(brno)
        db.session.add(ostrava)
        db.session.add(hradec)
        db.session.add(olomouc)

        db.session.commit()
