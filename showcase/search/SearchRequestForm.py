from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator  # , URLValidator
from django.apps import apps


BaseClass = apps.get_model('models', 'BaseClass')  # import the model from another app in Django


class SearchForm(forms.Form):
    """
    Class that holds the fields for a search request
    """
    company = forms.CharField(label="Company", min_length=1, max_length=200, required=False)
    region = forms.CharField(label="Region",
                             widget=forms.Select(choices=(("", ""), ("NA", "NA"), ("SEA", "SEA"),
                                                          ("EUR", "EUR"), ("ASIA", "ASIA"),
                                                          ("CHINA", "CHINA"))),
                             required=False
                             )
    product = forms.CharField(label="Product ID", min_length=1, max_length=200, required=False)

    def clean_company(self):
        data = self.cleaned_data["company"]
        if data not in BaseClass.allowed:
            raise ValidationError("Incorrect Company", code="Incorrect Value Entered")
        return data

    def clean_region(self):
        data = self.cleaned_data["region"]
        # if data not in models.allowed:
        #     raise ValidationError("Incorrect Region ID", code="Incorrect Value Entered")
        return data

    def clean_product(self):
        data = self.cleaned_data["product"]
        return data
        # if data not in models.allowed:
        #     raise ValidationError("Incorrect Product", code="Incorrect Value Entered")
