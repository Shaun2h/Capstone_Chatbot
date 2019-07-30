from django.urls import path
from . import views
urlpatterns = [
    # path("", views.basic, name="Default"),
    path("", views.prID, name="Default"),
    path("spec", views.prID),
    # path("guide_response", views.guide_response),
    # this is not used since basic can fulfil the same role.
    # this path only accepts POST with correct contexts.


    # the following are for making changes to the database.
    # comment this out during showcase
    path("insert", views.insert_req, name="Default"),
    path("delete", views.del_req, name="Default"),
               ]


# where names is how you prefer to call this method. Dictates the method called in views.py in this
# module.
