from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.clickjacking import xframe_options_exempt


# def base(request):
#    return HttpResponse("hello")


@xframe_options_exempt
def render_model1(request, company, region, cityID, prID, ispizza, seal):
    """
    Method that returns a webpage suitable for an Iframe in the guides.
    XeoGL Version

    :param request: HTTP Request from sender
    :param company: string Company of product
    :param region: string Region for which product is bound
    :param cityID: string  City for which product is bound
    :param prID: string  Product ID number
    :param ispizza: Boolean for whether item fits into a pizza box
    :param seal: Boolean for whether the product is sealed
    :return: HTTPResponse with webpage
    """
    # this method returns the pizzabox labelling model.
    # either with or without a seal.
    # render with the babylon viewer.
    additional_path = ""  # Need to set some way to generate the model name..
    additional_path += "ispizza"
    if seal:
        additional_path += "_sealed"
    else:
        additional_path += "_unsealed"
    # should use ispizza, perbox to find the relevant item name.

    context = {"company": company, "region": region, "city": cityID, "product": prID,
               "target": additional_path}
    # context = {"target_file": unk, "question": Question.objects.all()[0]}
    # if False:
    #     Http404("Example that is never triggered.")
    return HttpResponse(render(request, "babylonview.html", context=context))


@xframe_options_exempt
def render_model2(request, company, region, cityID, prID, perbox):
    """
    Returns the babylon version of an iframe. used in the final product

    :param request: HTTP Request from sender
    :param company: string Company of product
    :param region: string Region for which product is bound
    :param cityID: string  City for which product is bound
    :param prID: string  Product ID number
    :param perbox: integer Total number of products in the box
    :return:
    """
    # This method returns the model which packs into the shipping box.
    # render with the babylon viewer.
    context = {"company": company, "region": region, "city": cityID, "product": prID,
               "target": str(perbox)}
    # context = {"target_file": unk, "question": Question.objects.all()[0]}
    # if False:
    #     Http404("Example that is never triggered.")
    return HttpResponse(render(request, "babylonview.html", context=context))
