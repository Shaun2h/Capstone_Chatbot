from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .QuestionForm import QuestionForm, InsertForm, PrIdForm
import inspect
import models.models
# Create your views here.
all_in_model = dir(models.models)  # get all in model.py
model_classes = {}
baseclass = None
CDN_URL = "http://127.0.0.1:8000/models/"


for i in all_in_model:
    if inspect.isclass(getattr(models.models, i)) and i != "BaseClass":  # check if it is a class
        model_classes[i] = getattr(models.models, i)
    if i == "BaseClass":
        baseclass = getattr(models.models, i)  # attempt to obtain the class type


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


def prID(request):
    error = ""
    if request.method == "POST":
        question = PrIdForm(request.POST)

        if question.is_valid():
            data = question.cleaned_data
            return pr_filter(request, data["product"], data["company"])
            # exits here, returning a http response
        else:
            error = "ERROR"

    # returns a simple form allowing manual entry, or scanned entry.
    context = {"form": PrIdForm, "error_msg": error, "typing": "Information Request"}
    return HttpResponse(render(request, "request.html", context=context))


def pr_filter(request, product_ID, company):
    try:
        target_class = model_classes[company]
        main_classes = baseclass.objects.filter(product_ID=product_ID)
        requested_instance = None
        for c in main_classes:
            temp = target_class.objects.filter(information=c)
            if temp:
                requested_instance = temp
                break

        if not main_classes:
            raise models.models.models.ObjectDoesNotExist("Item does not exist")
        if not requested_instance:
            raise models.models.models.ObjectDoesNotExist("Item does not exist")
        if len(requested_instance) > 1:
            raise models.models.models.ObjectDoesNotExist("Multiple of same entry. Check Database")
        item = requested_instance[0]
        return return_guide(request, item)

    except (KeyError, models.models.models.ObjectDoesNotExist) as ex:
        return HttpResponse(str(ex))


def return_guide(request, item):
    requested_instance = item  # it's essentially a list object here.
    context = {"company": requested_instance.getEQ(),
               "region": requested_instance.information.region,
               "city": requested_instance.information.city_ID,
               "product": requested_instance.information.product_ID,
               "pizzabox": requested_instance.information.pizzabox,
               "per_box": requested_instance.information.per_box,
               "target": requested_instance.information.target,
               "sealed": requested_instance.information.sealed
               }
    list_of_views = []
    if context["sealed"]:
        # version with sealed.
        view_url = CDN_URL + context["company"] + "/" + context["region"] + "/" + context["city"] + \
                   "/" + context["product"] + "/" + context["pizzabox"] + "/" + \
                   context["per_box"] + "/"
        list_of_views.append(view_url + "sealed")

    else:
        view_url = CDN_URL + context["company"] + "/" + context["region"] + "/" + context[
            "city"] + \
                   "/" + context["product"] + "/" + context["pizzabox"] + "/" + \
                   context["per_box"] + "/"
        view_url += context["target"]
        list_of_views.append(view_url + "unsealed")

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
        target_class = model_classes[company]
        main_classes = baseclass.objects.filter(region=region, city_ID=city, product_ID=product)
        requested_instance = None
        for c in main_classes:
            temp = target_class.objects.filter(information=c)
            if temp:
                requested_instance = temp
                break
        if not main_classes:
            raise models.models.models.ObjectDoesNotExist("Item does not exist")
        if not requested_instance:
            raise models.models.models.ObjectDoesNotExist("Item does not exist")
        if len(requested_instance) > 1:
            raise models.models.models.ObjectDoesNotExist("Multiple of same entry. Check Database")
            # there should only be one of this item. If there are multiple raised from the filter,
            # check the database.

        requested_instance = requested_instance[0]  # it's essentially a list object here.

        # i need to do something to dynamically generate the list of the relevant models here..
        # i need to be able to produce the relevant descriptions here....

        return_guide(request, requested_instance)

    except (KeyError, models.models.models.ObjectDoesNotExist) as ex:
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

        target_class = model_classes[company]
        main_classes = baseclass.objects.filter(region=region, city_ID=city, product_ID=product)
        for main_class in main_classes:  # get the main classes that turned up.
            if(target_class.objects.filter(information=main_class)) > 0:
                # look through all companies.
                raise KeyError("An existing product takes up this slot. Please Remove it first.")

        attempt = baseclass(region=region, city_ID=city, product_ID=product,
                            target=url, ispizza=ispizza, per_box=per_box, sealed=seal)
        # generate the base class.

        attempt.save()  # save.
        subhead = target_class(information=attempt)
        subhead.save()
        return HttpResponse("Successfully added..." + subhead.information.target)
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
        attempt = baseclass.objects.filter(region=region, city_ID=city, product_ID=product,
                                           ispizza=ispizza, per_box=perbox)

        attempt.delete()  # save.
        return HttpResponse("Successfully REMOVED...")

    except (KeyError, models.models.models.ObjectDoesNotExist) as ex:
        print(ex)
        return HttpResponse("Failure!<br>" + str(ex))

