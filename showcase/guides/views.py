# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .QuestionForm import QuestionForm, InsertForm, PrIdForm
from models.models import BaseClass
from picklistdb.RequestForms import Forceprint5
from django.core.exceptions import ObjectDoesNotExist
from picklistdb.print import print_barcodes
from threading import Thread
import os
import random
# Create your views here.
CDN_URL = "http://127.0.0.1:8000/models/"
relevant_keys = ['Amazon', 'Asus', 'Intel']


def prID(request):
    """
    Wrapper method around pr_filter, and also prints the scanned IDs.

    :param request: HTTP request that wasa sent in
    :return: HTTP Response, depending on outcome of operation
    """
    error = ""
    if request.method == "POST":
        question = PrIdForm(request.POST)
        if "foo" in request.POST.keys() and Forceprint5(request.POST).is_valid():
            # it is from the form within the same page.
            relevant_list = []
            for idx in range(1, 6):
                relevant_list.append(request.POST["product_ID"+str(idx)])
                print(request.POST["product_ID" + str(idx)])

            thread = Thread(target=print_barcodes, kwargs=dict(list_of_ids=relevant_list,
                                                               new_cwd=os.getcwd()))
            # print the output.
            thread.start()
            return pr_filter(request, request.POST["product"])
            # begin by pushing out the same page.

        elif question.is_valid():
            data = question.cleaned_data
            try:
                data["foo"]
            except KeyError:
                return pr_filter(request, data["product"])

            # exits here, returning a http response
        else:
            error = "ERROR"

    # returns a simple form allowing manual entry, or scanned entry.
    context = {"form": PrIdForm, "error_msg": error, "typing": "Scan Pick List"}
    return HttpResponse(render(request, "request.html", context=context))


def pr_filter(request, product_ID):
    """
    Filters for a specific item in the database based off product IDs. Returns a guide if appropriate
    or the original form if the item was not found

    :param request: HTTP Request that was passed in.
    :param product_ID: string product ID
    :return: HTTPResponse, template and values depend on outcome of search.
    """
    try:
        # target_class = model_classes[company]
        requested_instance = BaseClass.objects.filter(product_ID=product_ID)

        # for c in main_classes:
        #     temp = target_class.objects.filter(information=c)
        #     if temp:
        #         requested_instance = temp
        #         break

        if not requested_instance:  # i.e it's still none..
            raise ObjectDoesNotExist("Item does not exist")
        # if not requested_instance:
        #     raise models.models.models.ObjectDoesNotExist("Item does not exist")
        if len(requested_instance) > 1:
            raise ObjectDoesNotExist("Multiple of same entry. Check Database")

        return return_guide(request, requested_instance[0])

    except (KeyError, ObjectDoesNotExist) as ex:
        context = {"form": PrIdForm, "error_msg": "Item does not exist", "typing": "Scan Pick List"}
        return HttpResponse(render(request, "request.html", context=context))


def return_guide(request, item):
    """
    Returns a html page with the guide for packing the product
    :param request: Request that was passed in.
    :param item: The instance of the object in the database that was filtered
    :return: HTTPResponse with template "guideview.html"
    """
    requested_instance = item  # it's essentially a list object here.
    if random.random() < 0.5:
        addy = "Requires Waterproofing"
    else:
        addy = "No Waterproof"
    context = {"company": requested_instance.company,
               "region": requested_instance.region,
               "city": requested_instance.city_ID,
               "product": requested_instance.product_ID,
               "pizzabox": requested_instance.pizzabox,
               "per_box": requested_instance.per_box,
               "sealed": requested_instance.sealed,
               "form": Forceprint5,
               "additional": addy,
               "additional2": "Box: BIG"
               }
    list_of_views = []

    # version with sealed.
    view_url = CDN_URL + context["company"] + "/" + context["region"] + "/" + str(context["city"]) \
               + "/" + context["product"] + "/"

    if context["sealed"] and context["pizzabox"]:
        list_of_views.append(view_url + str(context["pizzabox"]) + "/"+"1")
    elif context["pizzabox"]:
        list_of_views.append(view_url + str(context["pizzabox"]) + "/" + "0")

    list_of_views.append(view_url + str(context["per_box"]))
    context["viewlist"] = list_of_views
    print(list_of_views)
    return HttpResponse(render(request, "guideview.html", context=context))


def asked(request, company, region, city, product):
    """
    DEPRECATED.

    :param request: original http request
    :param company: string Company of product
    :param region: string Region for which product is bound
    :param city: string  City for which product is bound
    :param product: string  Product ID number
    :return: returns a guide from the guides class if a valid object is found. If not, return a
    Http response with exception.
    """
    try:
        requested_instance = BaseClass.objects.filter(company=company,
                                                      region=region, city_ID=city,
                                                      product_ID=product)

        if len(requested_instance < 1):
            raise ObjectDoesNotExist("Item does not exist")
        if len(requested_instance) > 1:
            raise ObjectDoesNotExist("Multiple of same entry. Check Database")
            # there should only be one of this item. If there are multiple raised from the filter,
            # check the database.
        requested_instance = requested_instance[0]  # it's essentially a list object here.
        # i need to do something to dynamically generate the list of the relevant models here..
        # i need to be able to produce the relevant descriptions here....
        return_guide(request, requested_instance)

    except (KeyError, ObjectDoesNotExist) as ex:
        return HttpResponse(str(ex))


# Methods for insertion and deletion of data into database. These should be commented out before
# showcase.


def insert_req(request):
    """
    GET or POST requests that are sent to the server are received in this method.

    This method is for requesting an insertion of an item from the database
    If the method is a POST request, it is forwarded to the method insert_succ.
    If not, a basic http response with the request form is sent

    :param request: Accepts the HTTP Request sent in.
    :return: If method is not POST, returns a HTTPResponse with the request form.
    """
    error = ""
    if request.method == "POST":
        insertreq = InsertForm(request.POST)
        if insertreq.is_valid():
            data = insertreq.cleaned_data
            return insert_succ(data["company"], data["region"], data["city"], data["product"],
                               data["urlline"], data["ispizza"], data["per_box"], data["issealed"])
        else:
            error = "ERROR"
            form = insertreq
    else:
        form = InsertForm
    context = {"form": form, "error_msg": error, "notice": "INSERTION", "typing": "Insert Request"}
    return HttpResponse(render(request, "request.html", context=context))


def insert_succ(company, region, city, product, url, ispizza, per_box, seal):
    """
    Creates a new instance of a product and saves it in the database. Raises an error upon failure

    This method will also check for duplicates of the same item, ensuring no two same products are
    added. The check requirements can be configured by changing the filter below.

    :param company: string Company of product
    :param region: string Region for which product is bound
    :param city: string  City for which product is bound
    :param product: string  Product ID number
    :param url: string File name for 3D model file. Field is generally unused and can be left as empty strings
    :param ispizza: Boolean for whether item fits into a pizza box
    :param per_box: Integer for number of products per box
    :param seal: Boolean for whether the product is sealed
    :return: HTTP Response with an explanation. Unformatted.
    """

    try:
        main_classes = BaseClass.objects.filter(region=region, city_ID=city, product_ID=product)
        if len(main_classes) > 0:  # is a duplicate in the area?
            raise KeyError("An existing product takes up this slot. Please Remove it first.")

        attempt = BaseClass(company=company, region=region, city_ID=city, product_ID=product,
                            target=url, pizzabox=ispizza, per_box=per_box, sealed=seal)
        # generate the base class.
        attempt.save()  # save.
        return HttpResponse("Successfully added..." + attempt.company)

    except KeyError as ex:
        print(ex)
        return HttpResponse("Failure!<br>" + str(ex))


def del_req(request):
    """
    GET or POST requests that are sent to the server are received in this method.

    This method is for requesting a deletion of an item from the database
    If the method is a POST request, it is forwarded to the method del_succ.
    If not, a basic http response with the request form is sent

    :param request: Accepts the HTTP Request sent in.
    :return: If method is not POST, returns a HTTPResponse with the request form.
    """
    error = ""
    if request.method == "POST":
        insertreq = QuestionForm(request.POST)
        if insertreq.is_valid():
            data = insertreq.cleaned_data
            return del_succ(data["region"], data["city"], data["product"], data["ispizza"],
                            data["per_box"])
            # optionally, add: data["company"]
        else:
            error = "ERROR"
            form = insertreq
    else:
        form = QuestionForm
    context = {"form": form, "error_msg": error, "notice": "DELETION", "typing": "Delete Request"}
    return HttpResponse(render(request, "request.html", context=context))


def del_succ(region, city, product, ispizza, perbox):
    """
    Deletes an entry from the database.

    :param region: string  Region for which product is bound
    :param city:  string City for which product is bound
    :param product: string
    :param ispizza: Boolean
    :param perbox: Integer
    :return: HttpResponse, unformatted string of operation result. Exceptions are provided on failure
    """
    # optionally add company to arguments.

    try:
        # target_class = model_classes[company]  # in case. you need to reference the actual class.
        attempt = BaseClass.objects.filter(region=region, city_ID=city, product_ID=product,
                                           pizzabox=ispizza, per_box=perbox)
        if not attempt.count():
            return HttpResponseNotFound("Entry does not exist:" + product)
        else:
            attempt.delete()  # save.
        return HttpResponse("Successfully REMOVED...")

    except (KeyError, ObjectDoesNotExist) as ex:
        print(ex)
        return HttpResponse("Failure!<br>" + str(ex))

