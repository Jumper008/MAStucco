import os
import django
from datetime import datetime


def populate():
    #adding workers
    gimenez=add_user('Gimenez', 'password1')
    gimenez.set_password('password1')
    villa=add_user('Villa', 'password2')
    hermosillo=add_user('Hermosillo', 'password3')
    corona=add_user('Corona', 'password4')
    delgado=add_user('Delgado', 'password5')
    dominguez=add_user('Dominguez', 'password6')

    d1 = datetime(2016, 8, 2, 10, 30, 50)
    d2 = datetime(2017, 2, 24, 22, 30, 50)
    d3 = datetime(2016, 10, 12, 12, 30, 50)
    d4 = datetime(2017, 2, 26, 17, 30, 50)
    d5 = datetime(2016, 12, 20, 13, 30, 50)
    d6 = datetime(2017, 1, 30, 9, 30, 50)
    d7 = datetime(2016, 12, 12, 15, 30, 50)
    #Adding work orders
    add_workorder(d1, 'Daniel Perez', 'Jorge Salazar', 'modelo1', False, True, 'AD', 'Hello! this is a dummy work order!',
                  gimenez)
    add_workorder(d2, 'Eugenio Guerra', 'Eduardo Moreira', 'modelo1', True, False, 'FI', 'Hello! this is a dummy work order!',
                  delgado)
    add_workorder(d3, 'Maria Guerra', 'Diego Perez', 'modelo3', True, False, 'FI', 'Hello! this is a dummy work order!',
                  villa)
    add_workorder(d4, 'Eduardo Guillen', 'Javier Valdez', 'modelo2', True, True, 'AD', 'Hello! this is a dummy work order!',
                  gimenez)
    add_workorder(d5, 'Alejandro Gonzalez', 'Ivan Lopez', 'modelo3', False, False, 'FI', 'Hello! this is a dummy work order!',
                  hermosillo)
    add_workorder(d6, 'Elisa Garza', 'Emiliano Morris', 'modelo3', True, False, 'FI', 'Hello! this is a dummy work order!',
                  hermosillo)
    add_workorder(d7, 'Laura Chavez', 'Antonio Varela', 'modelo1', False, True, 'AD', 'Hello! this is a dummy work order!',
                  corona)
    add_workorder(d2, 'Perla Ruiz', 'Andres Alvarez', 'modelo2', True, False, 'AD', 'Hello! this is a dummy work order!',
                  dominguez)
    add_workorder(d1, 'Pedro Solis', 'Raul Ramirez', 'modelo1', False, True, 'AD', 'Hello! this is a dummy work order!',
                  villa)
    add_workorder(d6, 'Mario Moncada', 'Alejandro Pinson', 'modelo2', False, False, 'AD', 'Hello! this is a dummy work order!',
                  delgado)

    # Print out what we have added to the user.
    for u in User.objects.all():
        print "The following users has been added: " + u.username

    # Print out what we have added to the user.
    for wo in WorkOrder.objects.all():
        print "The following work orders has been added: " + wo.customer


def add_user(name, password):
    u = User.objects.get_or_create(username=name, password=password)[0]
    return u

def add_workorder(date, customer, order_by, model, is_cashed, is_taken, work_phase, notes, assigned_worker):
    u = WorkOrder.objects.get_or_create(date=date, customer=customer, order_by=order_by, model=model, is_cashed=is_cashed,
                                   is_taken=is_taken, work_phase=work_phase, notes=notes,
                                   assigned_worker=assigned_worker)
    return u


# Start execution here!
if __name__ == '__main__':
    print "Starting WAMAStucco population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MAStucco.settings')
    django.setup()
    from WAMAStucco.models import WorkOrder
    from django.contrib.auth.models import User
    populate()