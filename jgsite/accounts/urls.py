from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('password/change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html',
            success_url = reverse_lazy('accounts:password_change_done')
        ), 
        name='password_change'),
    path('password/change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ), 
        name='password_change_done'),
    
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url = reverse_lazy('accounts:password_reset_done'),
        ),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url = reverse_lazy('accounts:password_reset_complete'),
        ),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'),    
    
]