from django.urls import path
from . import views
urlpatterns = [path("", views.request_pick),
               path("insert", views.insert_req),
               path("delete", views.del_req)
               ]
# where names is how you prefer to call this method. Dictates the method called in views.py in this
# module.
