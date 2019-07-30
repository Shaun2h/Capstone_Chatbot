from django.shortcuts import render
from .RequestForms import PicklistIdForm, RequestPicklistID
from django.http import HttpResponse, HttpResponseNotFound
from picklistdb.models import Picklist
from .models import Picklist
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

CDN_URL = "http://127.0.0.1:8000/picklists/"


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
    context = {"form": RequestPicklistID, "error_msg": error, "typing": "Picklist Request"}
    return HttpResponse(render(request, "request.html", context=context))


def pick_response(request, picklistid):
    try:
        main_classes = Picklist.objects.filter(own_id=picklistid)
        requested_instance = main_classes.count()
        if not main_classes:
            raise ObjectDoesNotExist("Item does not exist")
        if not requested_instance:
            raise ObjectDoesNotExist("Item does not exist")
        if requested_instance > 1:
            raise ObjectDoesNotExist("Multiple of same entry. Check Database")
        return return_guide(request, requested_instance)

    except (KeyError, ObjectDoesNotExist) as ex:
        return HttpResponse(str(ex))


def return_guide(request, item):
    # do something here to the picklist... do i print it or something??
    return HttpResponse("done!")




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

        attempt = Picklist(own_id=input_id, product_ID1=product_ID1, product_ID2=product_ID2,
                           product_ID3=product_ID3, product_ID4=product_ID4, product_ID5=product_ID5
                           , product_ID6=product_ID6, product_ID7=product_ID7
                           )
        # generate the base class.

        attempt.save()  # save.

        return HttpResponse("Successfully added Picklist:"+ input_id)
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

    except (KeyError, models.models.ObjectDoesNotExist) as ex:
        print(ex)
        return HttpResponse("Failure!<br>" + str(ex))

