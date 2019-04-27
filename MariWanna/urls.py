from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    # url('search', views.search),
    url('search-similar', views.similar_search),
    url('search-custom', views.custom_search),
    url('results-similar', views.similar_results),
    url('results-custom', views.custom_results)
]