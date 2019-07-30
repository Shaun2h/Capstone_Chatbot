# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .QuestionForm import QuestionForm, InsertForm, PrIdForm
from models.models import BaseClass
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
CDN_URL = "http://127.0.0.1:8000/models/"
relevant_keys = ['Amazon', 'Asus', 'Intel']

"""
def basic(request):
    error = ""
    if request.method == "POST":
        question = QuestionForm(request.POST)

        if question.is_valid():
            data = question.cleaned_data
            return asked(request, data["company"], data["region"], data["city"], data["product"])
            # exits here, returning a http response
        else:
            error = "ERROR"

    # returns a simple form allowing manual entry, or scanned entry.
    context = {"form": QuestionForm, "error_msg": error}
    return HttpResponse(render(request, "request.html", context=context))

    # return a http response, set to 405.
    # out = HttpResponse(error)
    # out.status_code = 405
    # return out
"""


def prID(request):
    error = ""
    if request.method == "POST":
        question = PrIdForm(request.POST)

        if question.is_valid():
            data = question.cleaned_data
            return pr_filter(request, data["product"])
            # exits here, returning a http response
        else:
            error = "ERROR"

    # returns a simple form allowing manual entry, or scanned entry.
    context = {"form": PrIdForm, "error_msg": error, "typing": "Information Request"}
    return HttpResponse(render(request, "request.html", context=context))


def pr_filter(request, product_ID):
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
        return HttpResponse(str(ex))


def return_guide(request, item):
    requested_instance = item  # it's essentially a list object here.
    context = {"company": requested_instance.company,
               "region": requested_instance.region,
               "city": requested_instance.city_ID,
               "product": requested_instance.product_ID,
               "pizzabox": requested_instance.pizzabox,
               "per_box": requested_instance.per_box,
               "target": requested_instance.target,
               "sealed": requested_instance.sealed
               }
    list_of_views = []
    if context["sealed"]:
        # version with sealed.
        view_url = CDN_URL + context["company"] + "/" + context["region"] + "/" \
                   + str(context["city"])\
                   + "/" + context["product"] + "/" + str(context["pizzabox"]) + "/" + \
                   str(context["per_box"]) + "/"
        list_of_views.append(view_url + "1")

    else:
        view_url = CDN_URL + context["company"] + "/" + context["region"] + "/" \
                   + str(context["city"])\
                   + "/" + context["product"] + "/" + str(context["pizzabox"]) + "/" + \
                   str(context["per_box"]) + "/"
        list_of_views.append(view_url + "0")
    context["viewlist"] = list_of_views
    print(list_of_views)
    return HttpResponse(render(request, "guideview.html", context=context))


""" # another method for handling the responses. Since one method alone is anough...
def guide_response(request):  # main method to handle the incoming request. If correct
    error = "Make Req."
    if request.method == "POST":
        question = QuestionForm(request.POST)
        if question.is_valid():
            data = question.cleaned_data
            return asked(request, data["company"], data["region"], data["city"], data["product"])
        else:
            error = "ERROR"
    context = {"form": QuestionForm, "error_msg": error}
    return HttpResponse(render(request, "form.html", context=context))
"""


def asked(request, company, region, city, product):
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

