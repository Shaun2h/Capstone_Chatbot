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
    product_ID8 = models.CharField(max_length=50, default="", blank=True)
    product_ID9 = models.CharField(max_length=50, default="", blank=True)
    product_ID10 = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return str(self.own_id)

    def req_list(self):
        attributes = [a for a in dir(Picklist) if not a.startswith('__')
                      and a.startswith("product_")]
        return_list = []
        for item in attributes:
            if len(item) > 0:
                print(item)
                return_list.append(getattr(self, item)) # access the relevant attributes.
        print(return_list)
        return return_list


admin.site.register(Picklist)
