from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.clickjacking import xframe_options_exempt


def base(request):
    return HttpResponse("hello")

"""
@xframe_options_exempt
def render_model(request, company, region, cityID, prID, modelname):
    # old method. renders using a 3d viewer
    context = {"company": company, "region": region, "city": cityID, "product": prID,
               "target": modelname	}
    # context = {"target_file": unk, "question": Question.objects.all()[0]}
    # if False:
    #     Http404("Example that is never triggered.")
    return HttpResponse(render(request, "modelview.html", context=context))
"""


@xframe_options_exempt
def render_model(request, company, region, cityID, prID, ispizza, perbox, seal):
    # render with the babylon viewer.

    additional_path = ""  # Need to set some way to generate the model name..
    if ispizza:
        additional_path += "ispizza_"
    additional_path += str(perbox)
    sealed = bool(seal)
    if sealed:
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

