from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'pulsar/index.html')
    # return render(request, 'HTML/index.html')


# ----------------------
# def index(request):
#     return HttpResponse("<h1>Wise City Pulsar </h1>")


