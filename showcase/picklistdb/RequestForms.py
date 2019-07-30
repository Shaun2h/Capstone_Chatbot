from django import forms
from django.apps import apps

BaseClass = apps.get_model('models', 'BaseClass')   # import the model from another app in Django


class PicklistIdForm(forms.Form):
    # this is only used in the demonstration, because we only have one thing to scan,
    # and no local database to reference each of the product ids to.

    product = forms.CharField(label="Picklist ID", min_length=1, max_length=50)
    product_ID1 = forms.CharField(label="Product ID 1:", max_length=50, required=False)
    product_ID2 = forms.CharField(label="Product ID 2:", max_length=50, required=False)
    product_ID3 = forms.CharField(label="Product ID 3:", max_length=50, required=False)
    product_ID4 = forms.CharField(label="Product ID 4:", max_length=50, required=False)
    product_ID5 = forms.CharField(label="Product ID 5:", max_length=50, required=False)
    product_ID6 = forms.CharField(label="Product ID 6:", max_length=50, required=False)
    product_ID7 = forms.CharField(label="Product ID 7:", max_length=50, required=False)
    def clean_product(self):
        data = self.cleaned_data["product"]
        return data
        # if data not in models.allowed:
        #     raise ValidationError("Incorrect Product", code="Incorrect Value Entered")


class RequestPicklistID(forms.Form):
    # this is only used in the demonstration, because we only have one thing to scan,
    # and no local database to reference each of the product ids to.

    product = forms.CharField(label="Picklist ID", min_length=1, max_length=50)

    def clean_product(self):
        data = self.cleaned_data["product"]
        return data
        # if data not in models.allowed:
        #     raise ValidationError("Incorrect Product", code="Incorrect Value Entered")
