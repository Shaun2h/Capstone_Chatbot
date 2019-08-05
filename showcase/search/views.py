# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .SearchRequestForm import SearchForm
from models.models import BaseClass
from picklistdb.RequestForms import Forceprint5
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import random
# Create your views here.
CDN_URL = "http://127.0.0.1:8000/models/"
ProductRequestUrl = "http://127.0.0.1:8000/guides/"
relevant_keys = ['Amazon', 'Asus', 'Intel']


def landing(request):
    error = ""
    if request.method == "POST":
        question = SearchForm(request.POST)
        if question.is_valid:
            # it is from the form within the same page.
            # print the output.
            return search_request(request, request.POST)
            # begin by pushing out the same page.
            # exits here, returning a http response
        else:
            error = "Invalid data entered"

    # returns a simple form allowing manual entry, or scanned entry.
    context = {"form": SearchForm, "error_msg": error, "typing": "Search Request"}
    return HttpResponse(render(request, "request.html", context=context))


def search_request(request, entered):
    try:
        # target_class = model_classes[company]
        requested_instance = []
        print(entered)
        if entered["company"] != "" and entered["product"] != "" and entered["region"] != "":
            print(1)
            requested_instance = BaseClass.objects.filter(
                Q(company__icontains=entered["company"]) |
                Q(product_ID__icontains=entered["product"]) |
                Q(region__icontains=entered["region"]))
        elif entered["company"] != "" and entered["product"] != "":
            print(2)
            requested_instance = BaseClass.objects.filter(
                Q(company__icontains=entered["company"]) |
                Q(product_ID__icontains=entered["product"]))

        elif entered["company"] != "" and entered["region"] != "":
            print(3)
            requested_instance = BaseClass.objects.filter(
                Q(company__icontains=entered["company"]) |
                Q(region__icontains=entered["region"]))

        elif entered["product"] != "" and entered["region"] != "":
            print(4)
            requested_instance = BaseClass.objects.filter(
                Q(product_ID__icontains=entered["product"]) |
                Q(region__icontains=entered["region"]))

        elif entered["product"] != "":
            print(5)
            print("doing a thing")
            requested_instance = BaseClass.objects.filter(
                Q(region__icontains=entered["product"]))

        elif entered["region"] != "":
            print(6)
            requested_instance = BaseClass.objects.filter(
                Q(region__icontains=entered["region"]))

        elif entered["company"] != "" and entered["region"] != "":
            print(7)
            requested_instance = BaseClass.objects.filter(
                Q(company__icontains=entered["company"]))

        if len(requested_instance) < 1:
            raise ObjectDoesNotExist("Multiple of same entry. Check Database")

        return return_results(request, requested_instance)

    except (KeyError, ObjectDoesNotExist) as ex:
        context = {"form": SearchForm, "error_msg": "Item does not exist",
                   "typing": "Scan Pick List"}
        return HttpResponse(render(request, "request.html", context=context))


def return_results(request, requested_instance):
    resultslist = []
    current = random.randint(1, 7)
    for item in requested_instance:
        if random.random() < 0.5:
            addy = "Requires Waterproofing"
        else:
            addy = "No Waterproof"
        selected = "microchip" + str(current % 7)+".jpg"
        current += 1
        context = {"company": item.company,
                   "region": item.region,
                   "city": item.city_ID,
                   "product": item.product_ID,
                   "pizzabox": item.pizzabox,
                   "per_box": item.per_box,
                   "sealed": item.sealed,
                   "additional": addy,
                   "additional2": "Box: BIG",
                   "selected_picture": selected
                   }
        resultslist.append(context)

    # version with sealed.
    context = {'results': resultslist, "form": SearchForm, "typing": "Product Search",
               "target_url": ProductRequestUrl}

    return HttpResponse(render(request, "Searchresults.html", context=context))


