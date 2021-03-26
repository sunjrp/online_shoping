from django.shortcuts import render
from .models import Catalog,ItemTag
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'home.html')


def market(request):
    return render(request, 'market.html', {'data': 'a lot of data'})


def search(request):
    keyword = request.GET['keyword']
    db = request.GET['db']
    print(keyword, db)
    if db == "SQL":
        data = Catalog.objects.all()
    else:
        data = None
    return render(request, 'result.html', {'query': data})
