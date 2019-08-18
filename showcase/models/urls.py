from django.urls import path
from . import views
urlpatterns = [
    path("<slug:company>/<slug:region>/<slug:cityID>/<slug:prID>/<slug:ispizza>/<int:seal>",
         views.render_model1,
         name="Model Request"),

               ]
# where names is how you prefer to call this method. Dictates the method called in views.py in this
# module.
