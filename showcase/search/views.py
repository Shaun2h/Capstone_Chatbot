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
    context = {"form": SearchForm, "error_msg": error, "typing": "Scan Pick List"}
    return HttpResponse(render(request, "request.html", context=context))


def search_request(request, entered):
    try:
        # target_class = model_classes[company]
        requested_instance = []
        print(entered)
        if entered["company"] != [""] and entered["product"] != [""] and entered["region"] != [""]:
            requested_instance = BaseClass.objects.filter(
                Q(company__icontains=entered["company"]) |
                Q(product_ID__icontains=entered["product"]) |
                Q(region__icontains=entered["region"]))
        elif entered["company"] != [""] and entered["product"] != [""]:
            requested_instance = BaseClass.objects.filter(
                Q(company__icontains=entered["company"]) |
                Q(product_ID__icontains=entered["product"]))

        elif entered["company"] != [""] and entered["region"] != [""]:
            requested_instance = BaseClass.objects.filter(
                Q(company__icontains=entered["company"]) |
                Q(region__icontains=entered["region"]))

        elif entered["product"] != [""] and entered["region"] != [""]:
            requested_instance = BaseClass.objects.filter(
                Q(product_ID__icontains=entered["product"]) |
                Q(region__icontains=entered["region"]))

        elif entered["product"] != [""]:
            requested_instance = BaseClass.objects.filter(
                Q(region__icontains=entered["region"]))

        elif entered["region"] != [""]:
            requested_instance = BaseClass.objects.filter(
                Q(region__icontains=entered["region"]))

        elif entered["company"] != [""] and entered["region"] != [""]:
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
    for item in requested_instance:
        if random.random() < 0.5:
            addy = "Requires Waterproofing"
        else:
            addy = "No Waterproof"
        context = {"company": item.company,
                   "region": item.region,
                   "city": item.city_ID,
                   "product": item.product_ID,
                   "pizzabox": item.pizzabox,
                   "per_box": item.per_box,
                   "sealed": item.sealed,
                   "additional": addy,
                   "additional2": "Box: BIG"
                   }
        resultslist.append(context)

    # version with sealed.
    context = {'results': resultslist, "form": SearchForm}

    return HttpResponse(render(request, "Searchresults.html", context=context))


