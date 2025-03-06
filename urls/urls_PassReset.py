from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy

urlpatterns = [
    path('password-reset/', 
         PasswordResetView.as_view(
             template_name='pass_reset/password_reset_form.html',
             email_template_name='pass_reset/password_reset_email.html',
             html_email_template_name = 'pass_reset/password_reset_email.html',
             subject_template_name='pass_reset/password_reset_subject.txt',
             success_url=reverse_lazy('password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/', 
         PasswordResetDoneView.as_view(
                template_name='pass_reset/password_reset_done.html'
               
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(
             template_name='pass_reset/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/', 
         PasswordResetCompleteView.as_view(
             template_name='pass_reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]