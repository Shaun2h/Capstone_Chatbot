from django.test import TestCase
from guides.views import pr_filter, insert_succ,del_succ
from models.models import BaseClass
# Create your tests here.



class insertion_testcase(TestCase):
    def setUp(self):
        self.dictionary = {"company": "ASUS",
                           "region": "NA",
                           "product": "A123456B",
                           "city_ID": "A123B",
                           "target": "a.gltf",
                           "pizzabox": True,
                           "per_box": 5,
                           "seal": True
                           }

    def test_insert(self):
        self.assertTrue(BaseClass.objects.filter().count() == 0,
                        "Incorrect number of objects in data base. check other tests?")
        insert_succ(self.dictionary["company"],
                    self.dictionary["region"],
                    self.dictionary["city_ID"],
                    self.dictionary["product"],
                    self.dictionary["target"],
                    self.dictionary["pizzabox"],
                    self.dictionary["per_box"],
                    self.dictionary["seal"])
        self.assertTrue(BaseClass.objects.filter().count() == 1, "Insertion failed.")


class deletion_testcase(TestCase):
    def setUp(self):
        self.dictionary = {"company": "ASUS",
                           "region": "NA",
                           "product": "A123456B",
                           "city_ID": "A123B",
                           "target": "a.gltf",
                           "pizzabox": True,
                           "per_box": 5,
                           "seal": True
                           }
        item = BaseClass(company=self.dictionary["company"],
                         region=self.dictionary["region"],
                         city_ID=self.dictionary["city_ID"],
                         product_ID=self.dictionary["product"],
                         target=self.dictionary["target"],
                         pizzabox=self.dictionary["pizzabox"],
                         per_box=self.dictionary["per_box"],
                         sealed=self.dictionary["seal"])
        item.save()  # save.

    def test_insert(self):
        self.assertTrue(BaseClass.objects.filter().count()==1, "Incorrect number of objects in data base. check other tests?")
        del_succ(self.dictionary["region"],
                 self.dictionary["city_ID"],
                 self.dictionary["product"],
                 self.dictionary["pizzabox"],
                 self.dictionary["per_box"])
        self.assertTrue(BaseClass.objects.filter().count() == 0, "Deletion failed.")


