from django.urls import path
from . import views
from django.views.generic import TemplateView, RedirectView
from django.conf.urls import url, include

app_name = 'usuarios'

urlpatterns = [
    path('', views.index, name='index'),
]