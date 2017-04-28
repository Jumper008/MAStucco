from django.test import TestCase
from django.contrib.auth.models import User
from .models import WorkOrder, Job, PartOrder, User, Profile
from django.contrib.auth import authenticate
from datetime import datetime
from .forms import WorkOrderForm, JobForm, PartOrderForm, UserCreationForm, UserChangeForm, UserProfileForm

class AutomatedTestingSuite(TestCase):

    def setUp(self):
        #Administrator
        User.objects.create_user(username='evert', email='evert@evert.com', password='evertpassword', is_staff = True)
        #Worker
        User.objects.create_user(username='jorge', email='jorge@jorge.com', password='jorgepassword', is_staff = False)

    def test_login_existing_user(self):
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)


    def test_login_non_existing_user(self):
        response = self.client.post('/login/', {'inputUsername': 'nadie', 'inputPassword': 'nadiepassword'})
        self.assertNotEqual(response.status_code, 302)


    def test_navigation_to_order_input_worker(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'jorge', 'inputPassword': 'jorgepassword'})
        self.assertEqual(response.status_code, 302)

        #Navigation to workorders/order_input
        response = self.client.get('/workorders/order_input')
        self.assertEquals(response.status_code, 302)


    def test_navigation_to_reports_worker(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'jorge', 'inputPassword': 'jorgepassword'})
        self.assertEqual(response.status_code, 302)

        #Navigation to reports
        response = self.client.get('/reports/')
        self.assertEquals(response.status_code, 302)


    def test_navigation_to_worker_administration_worker(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'jorge', 'inputPassword': 'jorgepassword'})
        self.assertEqual(response.status_code, 302)

        #Navigation to workorders/order_input
        response = self.client.get('/workeradministration/')
        self.assertEquals(response.status_code, 302)


    def test_navigation_to_available_jobs_worker(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'jorge', 'inputPassword': 'jorgepassword'})
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username='jorge')
        Profile.objects.create(user=user, position='NA')

        #Navigation to workorders/order_input
        response = self.client.get('/workorders/')
        self.assertEquals(response.status_code, 200)

    # As a administrator

    def test_navigation_to_order_input_admin(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)

        #Navigation to workorders/order_input
        response = self.client.get('/workorders/order_input')
        self.assertEquals(response.status_code, 200)


    def test_navigation_to_reports_admin(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)

        #Navigation to reports
        response = self.client.get('/reports/')
        self.assertEquals(response.status_code, 200)


    def test_navigation_to_worker_administration_admin(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)

        #Navigation to workorders/order_input
        response = self.client.get('/workeradministration/')
        self.assertEquals(response.status_code, 200)


    def test_navigation_to_available_jobs_admin(self):
        #Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username='evert')
        Profile.objects.create(user=user, position='NA')

        #Navigation to workorders/order_input
        response = self.client.get('/workorders/')
        self.assertEquals(response.status_code, 200)


    def test_list_filtered_by_cashed(self):
        # Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/reports_cashed/')
        self.assertEqual(response.status_code, 200)

        now = datetime.now()
        user = User.objects.get(username='evert')
        Profile.objects.create(user=user, position='NA')

        workorder = WorkOrder.objects.create(date=now, customer='customerPrueba', order_by='orderPrueba',
                                             model='modelPrueba', is_cashed=True, is_taken=True, work_phase='FI',
                                             notes='notesPrueba', assigned_worker=user)

        self.assertTrue(workorder.is_cashed)

    def test_list_filtered_by_uncashed(self):
        # Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)

        now = datetime.now()
        user = User.objects.get(username='evert')
        Profile.objects.create(user=user, position='NA')

        workorder = WorkOrder.objects.create(date=now, customer='customerPrueba', order_by='orderPrueba',
                                             model='modelPrueba', is_cashed=False, is_taken=True, work_phase='FI',
                                             notes='notesPrueba', assigned_worker=user)

        self.assertFalse(workorder.is_cashed)

    # Testting Forms
    def test_search_bar(self):
        # Login with a staff user
        response = self.client.post('/login/', {'inputUsername': 'evert', 'inputPassword': 'evertpassword'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/home/', {'search_title': 'probando'})
        self.assertEqual(response.status_code, 200)

    # Valid user creation form with valid data
    def test_user_creation_valid(self):
        form = UserCreationForm(data={'first_name': 'jose', 'last_name': 'lopez', 'email': 'jose@lopez.com', 'username': 'joseivan', 'password1': 'p1', 'password2': 'p1'})
        self.assertTrue(form.is_valid())

    # Valid user creation form with invalid data
    def test_user_creation_invalid(self):
        # Diferent Passwords and email in wrong format
        form = UserCreationForm(data={'first_name': 'jose', 'last_name': 'lopez', 'email': 'jose@lopezcom', 'username': 'joseivan', 'password1': 'p1', 'password2': 'p2'})
        self.assertFalse(form.is_valid())


    # valid new worker view form with valid data
    def test_new_worker_form_view_valid(self):
        response = self.client.post("/workeradministration/new_worker",
                                    {'first_name': 'jose', 'last_name': 'lopez', 'email': 'jose@lopez.com',
                                     'username': 'joseivan', 'password1': 'p1', 'password2': 'p1', 'position': 'NA'})
        self.assertEqual(response.status_code, 302)

    # valid new worker view form with valid data
    def test_new_worker_form_view_invalid(self):
        response = self.client.post("/workeradministration/new_worker",
                                    {'first_name': 'jose', 'last_name': 'lopez', 'email': 'jose@lopez.com',
                                        'username': 'joseivan', 'password1': 'p1', 'password2': 'p1',
                                        'position': 6})
        self.assertEqual(response.status_code, 302)

    # Valid user change form with valid data
    def test_user_change_form_valid(self):
        form = UserChangeForm(data={'first_name': 'e', 'last_name': 's', 'email': 'a@b.com', 'username': 'u', 'is_active': True})
        print form.errors
        self.assertTrue(form.is_valid())

    # Valid user change form with invalid data
    def test_user_change_form_invalid(self):
        form = UserChangeForm(data={'first_name': 'e', 'last_name': 's', 'email': 'a@bcom', 'username': 'u', 'is_active': False})
        self.assertFalse(form.is_valid())

    # Valid edit worker view, form with valid data
    def test_edit_worker_view_valid(self):
        user = User.objects.get(username='evert')
        userId = user.id

        response = self.client.post("/workeradministration/info/" + str(userId),
                                    {'first_name': 'e', 'last_name': 's', 'email': 'a@b.com', 'username': 'u',
                                     'is_active': False, 'position': 'NA'})
        self.assertEqual(response.status_code, 302)

    # Valid edit worker view, form with invalid data
    def test_edit_worker_view_invalid(self):
        user = User.objects.get(username='evert')
        userId = user.id

        response = self.client.post("/workeradministration/info/" + str(userId),
                                    {'first_name': 'e', 'last_name': 's', 'email': 'a@bcom', 'username': 'u',
                                     'is_active': False, 'position': 'NA'})
        self.assertEqual(response.status_code, 302)