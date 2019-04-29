from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('', views.home),
    # url('search', views.search),
    url('login', views.login),
    url('perform-signin', views.perform_signin),
    url('failed-authentication', views.failed_authentication),
    url('create-account', views.create_account),
    url('enter-user', views.enter_user),
    url('logout', views.logout),
    url('search-similar', views.similar_search),
    url('search-custom', views.custom_search),
    url('results-similar', views.similar_results),
    url('results-custom', views.custom_results)
]