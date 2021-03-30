from django.shortcuts import render
from .models import *
import time
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'home.html')


def market(request):
    return render(request, 'market.html', {'data': 'a lot of data'})


def search(request):
    keyword = request.GET['keyword']
    print(keyword)
    start_time = time.time()
    data = query_search(keyword)
    print(data)
    elapsed_time = time.time() - start_time
    return render(request, 'result.html', {'query': data, 'query_time': elapsed_time})


def query_search(keyword, date_select=None, type_select=None, tag_select=None, price_select=None):
    """search data in DB by time and keyword and return query set"""
    if type_select is None:
        type_select = []
    result = Movie.objects.all()

    if date_select:
        result = result.exclude(Q(release_date__gt=date_select[0]) | Q(release_date__lt=date_select[1]))

    if keyword != "":  # if have specific keyword
        result = result.filter(Q(name__startswith=keyword))
        if price_select:
            result = result.exclude(Q(price__gt=price_select[0]) | Q(price__lt=price_select[1]))
        if type_select:
            for word in type_select:
                result = result.filter(Q(MovieType__type=word))
        if tag_select:
            for word in tag_select:
                result = result.filter(Q(MovieType__type=word))

    return result
