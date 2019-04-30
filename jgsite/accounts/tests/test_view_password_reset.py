from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
#from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase

#During test running, each outgoing email is saved in django.core.mail.outbox. 
#This is a simple list of all EmailMessage instances that have been sent. The 
#outbox attribute is a special attribute that is created only when the locmem 
#email backend is used. It doesn’t normally exist as part of the django.core.mail 
#module and you can’t import it directly. The code below shows how to access 
#this attribute correctly.

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.get(url)
 
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
 
    def test_view_function(self):
        view = resolve('/accounts/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)
 
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
 
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)
 
    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf and email
        '''
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


# class SuccessfulPasswordResetTests(TestCase):
#     def setUp(self):
#         email = 'john@doe.com'
#         User.objects.create_user(username='john', email=email, password='123abcdef')
#         url = reverse('password_reset')
#         self.client.post(url, {'email': email})
#      
#     def test_redirection(self):
#         url = reverse('password_reset_done')
#         self.assertRedirects(self.response, url)
#      
#     def test_send_password_reset_email(self):
#         self.assertEqual(1, len(mail.outbox))
#      
#      
# class InvalidPasswordResetTests(TestCase):
#     def setUp(self):
#         url = reverse('accounts:password_reset')
#         self.client.post(url, {'email': 'donotexist@email.com'})
#   
#     def test_redirection(self):
#         '''
#         Even invalid emails in the database should
#         redirect the user to password_reset_done view
#         '''
#         url = reverse('accounts:password_reset_done')
#         self.assertRedirects(self.response, url)
#   
#     def test_no_reset_email_sent(self):
#         self.assertEqual(0, len(mail.outbox))


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='john@doe.com', password='123abcdef')

        '''
        create a valid password reset token
        based on how django creates the token internally:
        https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py#L280
        '''
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/confirm/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf and two password fields
        '''
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='john@doe.com', password='123abcdef')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        '''
        invalidate the token by changing the password
        '''
        user.set_password('abcdef123')
        user.save()

        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('accounts:password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))

class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)        