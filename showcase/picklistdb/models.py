from django.db import models
from django.contrib import admin


class Picklist(models.Model):
    own_id = models.CharField(max_length=50, default="")
    product_ID1 = models.CharField(max_length=50, default="", blank=False)
    product_ID2 = models.CharField(max_length=50, default="", blank=True)
    product_ID3 = models.CharField(max_length=50, default="", blank=True)
    product_ID4 = models.CharField(max_length=50, default="", blank=True)
    product_ID5 = models.CharField(max_length=50, default="", blank=True)
    product_ID6 = models.CharField(max_length=50, default="", blank=True)
    product_ID7 = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return str(self.own_id)


admin.site.register(Picklist)