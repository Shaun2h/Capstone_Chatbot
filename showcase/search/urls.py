from django.urls import path
from . import views

urlpatterns = [path("", views.landing),
               #path("insert", views.search),
               ]
# where names is how you prefer to call this method. Dictates the method called in views.py in this
# module.
