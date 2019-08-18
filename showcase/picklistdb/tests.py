from django.test import TestCase
from picklistdb.models import Picklist
from picklistdb.views import del_succ, insert_succ
from picklistdb.RequestForms import PicklistIdForm
# Create your tests here.


class InsertTestcase(TestCase):
    def setUp(self):
        self.initial_dict = {"product": "ABCDEFG1",
                             "product_ID1": "ITEM1",
                             "product_ID2": "ITEM2",
                             "product_ID3": "ITEM3",
                             "product_ID4": "ITEM4",
                             "product_ID5": "ITEM5",
                             "product_ID6": "ITEM6",
                             "product_ID7": "ITEM7",
                             "product_ID8": "ITEM8",
                             "product_ID9": "ITEM9",
                             "product_ID10": "ITEM10"
                             }
        self.form = PicklistIdForm(data=self.initial_dict)

    def test_insert(self):
        if self.form.is_valid():

            insert_succ(self.form.cleaned_data)
            #print("Validated form.")
            main_classes = Picklist.objects.filter(own_id=self.initial_dict["product"])
            outlist = main_classes[0].req_list()
            comparison = sorted(["ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7",
                                 "ITEM8",
                          "ITEM9",
                          "ITEM10"])
            self.assertTrue(sorted(outlist) == comparison, "Picklist Insertion Successful")
            main_classes.delete()
        else:
            #print(self.form.errors)
            self.assertFalse(True, "Failed to validate data!")


class deleteTestcase(TestCase):
    def setUp(self):
        item = Picklist(own_id="ABCDEFG1", product_ID1="ITEM1", product_ID2="ITEM2",
                        product_ID3="ITEM3", product_ID4="ITEM4",
                        product_ID5="ITEM5", product_ID6="ITEM6",
                        product_ID7="ITEM7", product_ID8="ITEM8",
                        product_ID9="ITEM9", product_ID10="ITEM10")
        item.save()  # save.

    def test_insert(self):
        attempt = Picklist.objects.filter(own_id="ABCDEFG1")
        dictionary = {"product": "ABCDEFG1",
                             "product_ID1": "ITEM1",
                             "product_ID2": "ITEM2",
                             "product_ID3": "ITEM3",
                             "product_ID4": "ITEM4",
                             "product_ID5": "ITEM5",
                             "product_ID6": "ITEM6",
                             "product_ID7": "ITEM7",
                             "product_ID8": "ITEM8",
                             "product_ID9": "ITEM9",
                             "product_ID10": "ITEM10"
                             }
        form = PicklistIdForm(data=dictionary)
        form.is_valid()
        del_succ(form.cleaned_data)
        #print("deleted form")
        self.assertTrue(Picklist.objects.filter(own_id="ABCDEFG1").count() == 0,
                        "Picklist deletion Successful")

