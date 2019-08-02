from django.urls import path
from . import views
urlpatterns = [path("", views.request_print3),
               path("insert", views.insert_req),
               path("delete", views.del_req),
               path("print5", views.request_print5),
               path("print3", views.request_print3)
               ]
# where names is how you prefer to call this method. Dictates the method called in views.py in this
# module.
