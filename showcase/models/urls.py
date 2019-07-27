from django.urls import path
from . import views
urlpatterns = [
    path("", views.base),
    path("<slug:company>/<slug:region>/<int:cityID>/<int:prID>/<slug:modelname>",
         views.render_model2,
         name="Model Request")
               ]
# where names is how you prefer to call this method. Dictates the method called in views.py in this
# module.
