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
                unhashed_password='iis2020',
                isEmployee=True,
                name='Admin',
                surname='Admin'
            ),
            isAdmin=True,
            isOwner=True,
            email='admin@rentel.com'
        )

        owner_employee = Employee(
            user=User(
                login='owner',
                unhashed_password='iis2020',
                isEmployee=True,
                name='Owner',
                surname='Owner'
            ),
            isOwner=True,
            email='owner@rentel.com'
        )
        manager_employee = Employee(
            user=User(
                login='manager',
                unhashed_password='iis2020',
                isEmployee=True,
                name='Manager',
                surname='Manager'
            ),
            email='manager@rentel.com'
        )
        
        test_customer = Customer(
            user=User(
                login='uzivatel',
                unhashed_password='iis2020',
                name='Daniel',
                surname='Nový'
            ),
            email='test@test.com'
        )

        
        praha = Hotel(
            name = 'Praha',
            address = 'ulice č 6',
            description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam erat volutpat. Aenean vel massa quis mauris vehicula lacinia. Aliquam id dolor. Vivamus ac leo pretium faucibus. Praesent vitae arcu tempor neque lacinia pretium. Etiam quis quam. Curabitur ligula sapien, pulvinar a vestibulum quis, facilisis vel sapien. Maecenas ipsum velit, consectetuer eu lobortis ut, dictum at dui. Mauris tincidunt sem sed arcu. Nunc auctor. Mauris metus. Nullam feugiat, turpis at pulvinar vulputate, erat libero tristique tellus, nec bibendum odio risus sit amet ante. Proin in tellus sit amet nibh dignissim sagittis. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Etiam neque. Suspendisse sagittis ultrices augue. Aliquam erat volutpat. Duis viverra diam non justo. Maecenas aliquet accumsan leo. Nunc tincidunt ante vitae massa. Curabitur sagittis hendrerit ante. Nam sed tellus id magna elementum tincidunt. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. In rutrum. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Proin mattis lacinia justo. Mauris elementum mauris vitae tortor. Aliquam erat volutpat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Proin mattis lacinia justo. Nunc dapibus tortor vel mi dapibus sollicitudin. Cras pede libero, dapibus nec, pretium sit amet, tempor quis. Pellentesque pretium lectus id turpis. Donec iaculis gravida nulla. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur bibendum justo non orci. Maecenas fermentum, sem in pharetra pellentesque, velit turpis volutpat ante, in pharetra metus odio a lectus. Etiam dictum tincidunt diam. Maecenas libero. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis. Fusce tellus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Etiam bibendum elit eget erat. Donec ipsum massa, ullamcorper in, auctor et, scelerisque sed, est. Sed convallis magna eu sem. Mauris dolor felis, sagittis at, luctus sed, aliquam non, tellus. Aliquam erat volutpat. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer in sapien. Integer vulputate sem a nibh rutrum consequat. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Cras elementum. Praesent vitae arcu tempor neque lacinia pretium.',
            rooms = [
                Room(
                    number = 56,
                    night_price = 990,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 58,
                    night_price = 1336,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 60,
                    night_price = 1990,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel0.png'
        )
        brno = Hotel(
            name = 'Brno',
            address = 'Komenského 42, Brno',
            description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam erat volutpat. Aenean vel massa quis mauris vehicula lacinia. Aliquam id dolor. Vivamus ac leo pretium faucibus. Praesent vitae arcu tempor neque lacinia pretium. Etiam quis quam. Curabitur ligula sapien, pulvinar a vestibulum quis, facilisis vel sapien. Maecenas ipsum velit, consectetuer eu lobortis ut, dictum at dui. Mauris tincidunt sem sed arcu. Nunc auctor. Mauris metus. Nullam feugiat, turpis at pulvinar vulputate, erat libero tristique tellus, nec bibendum odio risus sit amet ante. Proin in tellus sit amet nibh dignissim sagittis. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Etiam neque. Suspendisse sagittis ultrices augue. Aliquam erat volutpat. Duis viverra diam non justo. Maecenas aliquet accumsan leo. Nunc tincidunt ante vitae massa. Curabitur sagittis hendrerit ante. Nam sed tellus id magna elementum tincidunt. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. In rutrum. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Proin mattis lacinia justo. Mauris elementum mauris vitae tortor. Aliquam erat volutpat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Proin mattis lacinia justo. Nunc dapibus tortor vel mi dapibus sollicitudin. Cras pede libero, dapibus nec, pretium sit amet, tempor quis. Pellentesque pretium lectus id turpis. Donec iaculis gravida nulla. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur bibendum justo non orci. Maecenas fermentum, sem in pharetra pellentesque, velit turpis volutpat ante, in pharetra metus odio a lectus. Etiam dictum tincidunt diam. Maecenas libero. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis. Fusce tellus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Etiam bibendum elit eget erat. Donec ipsum massa, ullamcorper in, auctor et, scelerisque sed, est. Sed convallis magna eu sem. Mauris dolor felis, sagittis at, luctus sed, aliquam non, tellus. Aliquam erat volutpat. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer in sapien. Integer vulputate sem a nibh rutrum consequat. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Cras elementum. Praesent vitae arcu tempor neque lacinia pretium.',
            rooms = [
                Room(
                    number = 44,
                    night_price = 990,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 45,
                    night_price = 1258,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 46,
                    night_price = 1687,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel1.png'
        )
        olomouc = Hotel(
            name = 'Olomouc',
            address = 'Nová 9, Olomouc',
            description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam erat volutpat. Aenean vel massa quis mauris vehicula lacinia. Aliquam id dolor. Vivamus ac leo pretium faucibus. Praesent vitae arcu tempor neque lacinia pretium. Etiam quis quam. Curabitur ligula sapien, pulvinar a vestibulum quis, facilisis vel sapien. Maecenas ipsum velit, consectetuer eu lobortis ut, dictum at dui. Mauris tincidunt sem sed arcu. Nunc auctor. Mauris metus. Nullam feugiat, turpis at pulvinar vulputate, erat libero tristique tellus, nec bibendum odio risus sit amet ante. Proin in tellus sit amet nibh dignissim sagittis. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Etiam neque. Suspendisse sagittis ultrices augue. Aliquam erat volutpat. Duis viverra diam non justo. Maecenas aliquet accumsan leo. Nunc tincidunt ante vitae massa. Curabitur sagittis hendrerit ante. Nam sed tellus id magna elementum tincidunt. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. In rutrum. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Proin mattis lacinia justo. Mauris elementum mauris vitae tortor. Aliquam erat volutpat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Proin mattis lacinia justo. Nunc dapibus tortor vel mi dapibus sollicitudin. Cras pede libero, dapibus nec, pretium sit amet, tempor quis. Pellentesque pretium lectus id turpis. Donec iaculis gravida nulla. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur bibendum justo non orci. Maecenas fermentum, sem in pharetra pellentesque, velit turpis volutpat ante, in pharetra metus odio a lectus. Etiam dictum tincidunt diam. Maecenas libero. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis. Fusce tellus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Etiam bibendum elit eget erat. Donec ipsum massa, ullamcorper in, auctor et, scelerisque sed, est. Sed convallis magna eu sem. Mauris dolor felis, sagittis at, luctus sed, aliquam non, tellus. Aliquam erat volutpat. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer in sapien. Integer vulputate sem a nibh rutrum consequat. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Cras elementum. Praesent vitae arcu tempor neque lacinia pretium.',
            rooms = [
                Room(
                    number = 33,
                    night_price = 889,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 34,
                    night_price = 1200,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 35,
                    night_price = 1600,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel2.png'
        )
        hradec = Hotel(
            name = 'Hradec Králové',
            address = 'Nádražní 6, Hradec Králové',
            description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam erat volutpat. Aenean vel massa quis mauris vehicula lacinia. Aliquam id dolor. Vivamus ac leo pretium faucibus. Praesent vitae arcu tempor neque lacinia pretium. Etiam quis quam. Curabitur ligula sapien, pulvinar a vestibulum quis, facilisis vel sapien. Maecenas ipsum velit, consectetuer eu lobortis ut, dictum at dui. Mauris tincidunt sem sed arcu. Nunc auctor. Mauris metus. Nullam feugiat, turpis at pulvinar vulputate, erat libero tristique tellus, nec bibendum odio risus sit amet ante. Proin in tellus sit amet nibh dignissim sagittis. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Etiam neque. Suspendisse sagittis ultrices augue. Aliquam erat volutpat. Duis viverra diam non justo. Maecenas aliquet accumsan leo. Nunc tincidunt ante vitae massa. Curabitur sagittis hendrerit ante. Nam sed tellus id magna elementum tincidunt. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. In rutrum. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Proin mattis lacinia justo. Mauris elementum mauris vitae tortor. Aliquam erat volutpat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Proin mattis lacinia justo. Nunc dapibus tortor vel mi dapibus sollicitudin. Cras pede libero, dapibus nec, pretium sit amet, tempor quis. Pellentesque pretium lectus id turpis. Donec iaculis gravida nulla. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur bibendum justo non orci. Maecenas fermentum, sem in pharetra pellentesque, velit turpis volutpat ante, in pharetra metus odio a lectus. Etiam dictum tincidunt diam. Maecenas libero. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis. Fusce tellus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Etiam bibendum elit eget erat. Donec ipsum massa, ullamcorper in, auctor et, scelerisque sed, est. Sed convallis magna eu sem. Mauris dolor felis, sagittis at, luctus sed, aliquam non, tellus. Aliquam erat volutpat. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer in sapien. Integer vulputate sem a nibh rutrum consequat. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Cras elementum. Praesent vitae arcu tempor neque lacinia pretium.',
            rooms = [
                Room(
                    number = 21,
                    night_price = 790,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 22,
                    night_price = 990,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 23,
                    night_price = 880,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel3.png'
        )
        ostrava = Hotel(
            name = 'Ostrava',
            address = 'U kapličky 165, Ostrava',
            description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam erat volutpat. Aenean vel massa quis mauris vehicula lacinia. Aliquam id dolor. Vivamus ac leo pretium faucibus. Praesent vitae arcu tempor neque lacinia pretium. Etiam quis quam. Curabitur ligula sapien, pulvinar a vestibulum quis, facilisis vel sapien. Maecenas ipsum velit, consectetuer eu lobortis ut, dictum at dui. Mauris tincidunt sem sed arcu. Nunc auctor. Mauris metus. Nullam feugiat, turpis at pulvinar vulputate, erat libero tristique tellus, nec bibendum odio risus sit amet ante. Proin in tellus sit amet nibh dignissim sagittis. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Etiam neque. Suspendisse sagittis ultrices augue. Aliquam erat volutpat. Duis viverra diam non justo. Maecenas aliquet accumsan leo. Nunc tincidunt ante vitae massa. Curabitur sagittis hendrerit ante. Nam sed tellus id magna elementum tincidunt. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. In rutrum. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Proin mattis lacinia justo. Mauris elementum mauris vitae tortor. Aliquam erat volutpat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Proin mattis lacinia justo. Nunc dapibus tortor vel mi dapibus sollicitudin. Cras pede libero, dapibus nec, pretium sit amet, tempor quis. Pellentesque pretium lectus id turpis. Donec iaculis gravida nulla. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur bibendum justo non orci. Maecenas fermentum, sem in pharetra pellentesque, velit turpis volutpat ante, in pharetra metus odio a lectus. Etiam dictum tincidunt diam. Maecenas libero. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis. Fusce tellus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Etiam bibendum elit eget erat. Donec ipsum massa, ullamcorper in, auctor et, scelerisque sed, est. Sed convallis magna eu sem. Mauris dolor felis, sagittis at, luctus sed, aliquam non, tellus. Aliquam erat volutpat. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer in sapien. Integer vulputate sem a nibh rutrum consequat. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Cras elementum. Praesent vitae arcu tempor neque lacinia pretium.',
            rooms = [
                Room(
                    number = 11,
                    night_price = 890,
                    room_type = 'ECON',
                    number_of_beds = 2
                ),
                Room(
                    number = 12,
                    night_price = 1600,
                    room_type = 'BUSS',
                    number_of_beds = 3
                ),
                Room(
                    number = 13,
                    night_price = 990,
                    room_type = 'PREM',
                    number_of_beds = 2
                )
            ],
            picture = 'hotel4.png'
        )

        res = Reservation(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2021, 2, 1).date(),
                date_to = datetime.datetime(2021, 2, 5).date(),
                price = 990,
                visit_type = 'RES',
                rooms = [brno.rooms[0]]
            ),
            is_paid_princ = True,
            is_paid_visit = True
        )
        res = Reservation(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 2, 5).date(),
                date_to = datetime.datetime(2020, 2, 11).date(),
                price = 890,
                visit_type = 'RES',
                rooms = [hradec.rooms[0]]
            ),
            is_paid_princ = True
        )

        on = Ongoing(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 29).date(),
                date_to = datetime.datetime(2021, 1, 30).date(),
                price = 990,
                visit_type = 'NOW',
                rooms = [praha.rooms[0]]
            ),
            key_customer = True
        )

        past = Past(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 20).date(),
                date_to = datetime.datetime(2020, 11, 25).date(),
                price = 990,
                visit_type = 'PAS',
                rooms = [ostrava.rooms[1]]
            ),
        )
        past1 = Past(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 10).date(),
                date_to = datetime.datetime(2020, 11, 20).date(),
                price = 1200,
                visit_type = 'PAS',
                rooms = [olomouc.rooms[1]]
            ),
        )
        past2 = Past(
            visit = Visit(
                customer = test_customer,
                date_from = datetime.datetime(2020, 11, 5).date(),
                date_to = datetime.datetime(2020, 11, 10).date(),
                price = 1100,
                visit_type = 'PAS',
                rooms = [praha.rooms[2]]
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
