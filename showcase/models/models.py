from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class BaseClass(models.Model):
    # City ID records which city is it.. based off the choice above.

    product_ID = models.CharField(max_length=50, default="")
    region = models.CharField(max_length=50, choices=(('NA', 'NA'),
                                                      ('SEA', 'SEA'),
                                                      ('EUR', 'Europe'),
                                                      ('ASIA', 'ASIA'),
                                                      ('CHINA', 'CHINA')))
    city_ID = models.IntegerField()
    target = models.CharField(max_length=300, default="")  # this saves the file name.
    pizzabox = models.BooleanField(default=False)  # is this a pizzabox instance?
    per_box = models.IntegerField(default=1, validators=[MaxValueValidator(5),
                                                         MinValueValidator(1)])
    # how many to a box?
    allowed = ["Amazon", "Asus", "Intel"]
    sealed = models.BooleanField(default=False)
    # The url is constructed based off the fields above.

    @staticmethod
    def get_company():
        return "NULL"

    def __str__(self):
        return self.get_company() + "\n Region: " + str(self.region) + "\nCityID: "\
               + str(self.city_ID) + "\nProduct ID:" + str(self.product_ID)\
               + "\nTarget url: " + str(self.target)


admin.site.register(BaseClass)


class Amazon(models.Model):
    company = models.CharField(max_length=50, default="Amazon")
    information = models.OneToOneField(BaseClass, on_delete=models.CASCADE, primary_key=True)

    @staticmethod
    def get_company():
        return "Amazon"


admin.site.register(Amazon)


class Intel(models.Model):
    company = models.CharField(max_length=50, default="Intel")
    information = models.OneToOneField(BaseClass, on_delete=models.CASCADE, primary_key=True)

    @staticmethod
    def get_company():
        return "Intel"


admin.site.register(Intel)


class Asus(models.Model):
    company = models.CharField(max_length=50, default="Asus")
    information = models.OneToOneField(BaseClass, on_delete=models.CASCADE, primary_key=True)

    @staticmethod
    def get_company():
        return "Asus"


admin.site.register(Asus)


