from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from home.views import *
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm,password_reset_complete,logout
from django.contrib.auth.forms import PasswordResetForm
admin.autodiscover()

urlpatterns = [
    url(r'^unsubscribe/$', login_required(Unsubscribe), name="unsubscribe"),
    url(r'^support/$', login_required(Support),  name="support"),
    url(r'^logout/$', logout, {'next_page': '/'}, name="logout_page"),
    url(r'^signup/entity/social/(?P<pk_entity>\d{1,1000000})$', login_required(TrialSocial), name='signup_page_trial_social'),
    url(r'^signup/entity/(?P<pk_entity>\d{1,1000000})$', SignupTrialView, name='signup_page_trial'),
    url(r'^signup/$', SignupView.as_view(), name='signup_page'),
    url(r'^terms/and/privacity/$', TermsAndPrivacityView.as_view(), name='terms_and_privacity'),
    url(r'^signup/email_sent/(?P<email>.{1,254})$', SignupEmailSentView.as_view(), name='signup_email_sent_page'),
    url(r'^signup/verify/yes/$', SignupVerified.as_view(), name='signup_verified_page'),
    url(r'^signup/verify/not/$', SignupNotVerified.as_view(), name='signup_not_verified_page'),
    url(r'^signup/verify/$', SignupVerifyView.as_view(), name='signup_verify'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login_page'),
    url(r'^password/reset/$', password_reset,{'template_name':'home_password_reset.html',
                                              'email_template_name':'email/home_reset_password.txt',
                                              'html_email_template_name':'email/home_reset_password.html',
                                              'subject_template_name':'email/home_reset_password_subject.txt',
                                              'password_reset_form': PasswordResetForm,
                                              'from_email': settings.EMAIL_HOST_USER,
                                              }, name='password_reset_page'),
    url(r'^password/reset/done/$', password_reset_done,{'template_name':'home_password_reset_email_sent.html'},name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'home_password_reset_verified.html'}, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'home_password_reset_success.html'},
        name='password_reset_complete'),
    url(r'', include('social_django.urls', namespace='social')),
]
