from django.urls import path
from . import views
urlpatterns = [
    path("", views.base),
    path("<slug:company>/<slug:region>/<int:cityID>/<slug:prID>/<slug:ispizza>/<int:perbox>/<int:seal>",
         views.render_model,
         name="Model Request")
               ]
# where names is how you prefer to call this method. Dictates the method called in views.py in this
# module.
