from django.conf.urls import url
from accounts.forms import QuizLoginForm

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'form.html',  # registration/login.html 파일을 대신 함 / 즉, registration/login.html은 삭제해도 무방함
        'authentication_form': QuizLoginForm,
    }),
    url(r'signup/$', 'accounts.views.signup'),
    url(r'^profile/$', 'accounts.views.profile_detail'),
    # url(r'^profile/edit/$', 'accounts.views.profile_edit'),
]
