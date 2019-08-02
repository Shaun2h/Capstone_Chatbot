from django.shortcuts import render
from .RequestForms import PicklistIdForm, RequestPicklistID, Forceprint5, Forceprint3
from django.http import HttpResponse, HttpResponseNotFound
from .models import Picklist
from django.core.exceptions import ObjectDoesNotExist
from threading import Thread
import os
# Create your views here.
from picklistdb.print import print_barcodes
CDN_URL = "http://127.0.0.1:8000/picklists/"


def request_print3(request):
    error = ""
    context = {"form": Forceprint3, "error_msg": error, "typing": "Print Shipping Labels"}
    if request.method == "POST":
        question = Forceprint3(request.POST)

        if question.is_valid():
            data = question.cleaned_data
            printing_list = []
            for key in data.keys():
                if len(data[key]) > 0:
                    printing_list.append(data[key])
                    printing_list.append(data[key])
                    printing_list.append(data[key])
            print_request_int(request, printing_list)  # obtain picklist id.
            # exits here, returning a http response
        else:
            context["error"] = "ERROR"
            context["form"] = Forceprint3(request.POST)
            return HttpResponse(render(request, "request.html", context=context))

    # returns a simple form allowing manual entry, or scanned entry.
    return HttpResponse(render(request, "request.html", context=context))


def request_print5(request):
    error = ""
    context = {"form": Forceprint5, "error_msg": error, "typing": "Print Product Labels"}
    if request.method == "POST":
        question = Forceprint5(request.POST)

        if question.is_valid():
            data = question.cleaned_data
            printing_list = []
            for key in data.keys():
                if len(data[key]) > 0:
                    printing_list.append(data[key])
                    printing_list.append(data[key])
            print_request_int(request, printing_list)  # obtain picklist id.
            # exits here, returning a http response
        else:
            context["error"] = "ERROR"
            context["form"] = Forceprint5(request.POST)
            return HttpResponse(render(request, "request.html", context=context))

    # returns a simple form allowing manual entry, or scanned entry.
    return HttpResponse(render(request, "request.html", context=context))


def print_request_int(request, data):
    error = ""
    try:

        thread = Thread(target=print_barcodes, kwargs=dict(list_of_ids=data,
                                                           new_cwd=os.getcwd()))
        # print the output.
        thread.start()
        context = {"form": Forceprint5, "error_msg": error, "typing": "Request a print"}
        # return HttpResponse(render(request, "request.html", context=context))

    except (KeyError, ObjectDoesNotExist) as ex:
        pass
        # return HttpResponse(str(ex)) # fail to do anything.


def request_pick(request):
    error = ""
    if request.method == "POST":
        question = RequestPicklistID(request.POST)

        if question.is_valid():
            data = question.cleaned_data
            return pick_response(request, data["product"])  # obtain picklist id.
            # exits here, returning a http response
        else:
            error = "ERROR"

    # returns a simple form allowing manual entry, or scanned entry.
    context = {"form": RequestPicklistID, "error_msg": error, "typing": "Request Picklist"}
    return HttpResponse(render(request, "request.html", context=context))


def pick_response(request, picklistid):
    try:
        main_classes = Picklist.objects.filter(own_id=picklistid)
        count = main_classes.count()
        if not main_classes:
            raise ObjectDoesNotExist("Item does not exist")
        if not count:
            raise ObjectDoesNotExist("Item does not exist")
        if count > 1:
            raise ObjectDoesNotExist("Multiple of same entry. Check Database")
        error = ""
        context = {"form": RequestPicklistID, "error_msg": error, "typing": "Request Picklist "}
        printing_list = main_classes[0].req_list()
        thread = Thread(target=print_barcodes, kwargs=dict(list_of_ids=printing_list,
                                                           new_cwd=os.getcwd()))
        # print the output.
        thread.start()

        return HttpResponse(render(request, "request.html", context=context))

    except (KeyError, ObjectDoesNotExist) as ex:
        return HttpResponse(str(ex))


def insert_req(request):
    error = ""
    if request.method == "POST":
        insertreq = PicklistIdForm(request.POST)
        if insertreq.is_valid():
            data = insertreq.cleaned_data
            return insert_succ(data)
        else:
            error = "ERROR"
            form = insertreq
    else:
        form = PicklistIdForm
    context = {"form": form, "error_msg": error, "notice": "INSERTION", "typing": "Insert Request"}
    return HttpResponse(render(request, "request.html", context=context))


def insert_succ(data):
    try:
        input_id = data["product"]
        product_ID1 = data["product_ID1"]
        product_ID2 = data["product_ID2"]
        product_ID3 = data["product_ID3"]
        product_ID4 = data["product_ID4"]
        product_ID5 = data["product_ID5"]
        product_ID6 = data["product_ID6"]
        product_ID7 = data["product_ID7"]
        product_ID8 = data["product_ID8"]
        product_ID9 = data["product_ID9"]
        product_ID10 = data["product_ID10"]

        attempt = Picklist(own_id=input_id, product_ID1=product_ID1, product_ID2=product_ID2,
                           product_ID3=product_ID3, product_ID4=product_ID4,
                           product_ID5=product_ID5, product_ID6=product_ID6,
                           product_ID7=product_ID7, product_ID8=product_ID8,
                           product_ID9=product_ID9, product_ID10=product_ID10)

        # generate the base class.

        attempt.save()  # save.

        return HttpResponse("Successfully added Picklist:" + input_id)
    except KeyError as ex:
        print(ex)
        return HttpResponse("Failure!<br>" + str(ex))


def del_req(request):
    error = ""
    if request.method == "POST":
        insertreq = RequestPicklistID(request.POST)
        if insertreq.is_valid():
            data = insertreq.cleaned_data
            return del_succ(data)
            # optionally, add: data["company"]
        else:
            error = "ERROR"
            form = insertreq
    else:
        form = RequestPicklistID
    context = {"form": form, "error_msg": error, "notice": "DELETION", "typing": "Delete Request"}
    return HttpResponse(render(request, "request.html", context=context))


def del_succ(data):
    # optionally add company to arguments.

    try:
        input_id = data["product"]
        # target_class = model_classes[company]  # in case. you need to reference the actual class.
        attempt = Picklist.objects.filter(own_id=input_id)
        if not attempt.count():  # does not exist
            return HttpResponseNotFound("Entry does not exist:" + input_id)
        else:
            attempt.delete()  # save.
            return HttpResponse("Successfully removed Picklist:" + input_id)

    except (KeyError, ObjectDoesNotExist) as ex:
        print(ex)
        return HttpResponse("Failure!<br>" + str(ex))

