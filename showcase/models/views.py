from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.clickjacking import xframe_options_exempt


def base(request):
    return HttpResponse("hello")


@xframe_options_exempt
def render_model(request, company, region, cityID, prID, modelname):
    context = {"company": company, "region": region, "city": cityID, "product": prID,
               "target": modelname	}
    # context = {"target_file": unk, "question": Question.objects.all()[0]}
    # if False:
    #     Http404("Example that is never triggered.")
    return HttpResponse(render(request, "modelview.html", context=context))


@xframe_options_exempt
def render_model2(request, company, region, cityID, prID, modelname):
    context = {"company": company, "region": region, "city": cityID, "product": prID,
               "target": modelname	}
    # context = {"target_file": unk, "question": Question.objects.all()[0]}
    # if False:
    #     Http404("Example that is never triggered.")
    return HttpResponse(render(request, "babylonview.html", context=context))

