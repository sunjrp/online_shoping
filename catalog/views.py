from django.shortcuts import render
from .models import *
import time
from django.db.models import Q
from django.http import HttpResponse
import requests
import string
import random
# Create your views here.


api_key = "fcc6fff35de0b2b9470d180bb4c76555"  #for themoviedb.org


def request_movies_genre():
    url_tv = f"https://api.themoviedb.org/3/genre/tv/list?api_key={api_key}"
    url_movie = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}"
    for url in [url_tv, url_movie]:
        response = requests.get(url)
        load = response.json()
        print(load)
        for genre in load["genres"]:
            print(genre)
            p = Genre(id=genre["id"], name=genre["name"])
            p.save()


def request_movies_all():
    alphabet_list = list(string.ascii_lowercase)
    print(alphabet_list)
    for alphabet in alphabet_list:
        for page in range(1,3):
            url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={alphabet}&page={page}"
            response = requests.get(url)
            load = response.json()
            for movie in load["results"]:
                try:
                    poster_path = movie["poster_path"]
                    img_url = f"https://image.tmdb.org/t/p/original{poster_path}"
                    p = Product(title=movie["title"],
                                id=movie["id"],
                                price=str(random.randint(0, 10000)),
                                rating=str(movie["vote_average"]),
                                storyline=movie["overview"],
                                thumbnail_url=img_url,
                                release_date=movie["release_date"])
                    p.save()
                    print(p)
                    if movie["genre_ids"]:
                        for id_num in movie["genre_ids"]:
                            print(id_num)
                            movie_genres = Genre(id=id_num)
                            movie_genres.save()
                            p.genre.add(movie_genres)
                except:
                    pass


def home(request):
    return render(request, 'home.html')


def market(request):
    return render(request, 'market.html', {'data': 'a lot of data'})


def search(request):
    keyword = request.GET['keyword']
    start_time = time.time()
    data = query_search(keyword)
    elapsed_time = time.time() - start_time
    return render(request, 'result.html', {'query': data, 'query_time': elapsed_time})


def query_search(keyword, movie_id=None, date_select=None, type_select=None, tag_select=None, price_select=None):
    """search data in DB by time and keyword and return query set"""
    if type_select is None:
        type_select = []
    result = Product.objects.all()
    if date_select:
        result = result.exclude(Q(release_date__gt=date_select[0]) | Q(release_date__lt=date_select[1]))

    if movie_id:
        result = result.filter(Q(id=movie_id))

    if keyword != "":  # if have specific keyword
        result = result.filter(Q(title__startswith=keyword))
        if price_select:
            result = result.exclude(Q(price__gt=price_select[0]) | Q(price__lt=price_select[1]))
        if type_select:
            for word in type_select:
                result = result.filter(Q(MovieType__type=word))
        if tag_select:
            for word in tag_select:
                result = result.filter(Q(MovieType__type=word))
    return result


def details(request, movie_id):
    print(movie_id)
    start_time = time.time()
    data = query_search("", movie_id=movie_id)[0]
    elapsed_time = time.time() - start_time
    return render(request, 'movie_detail.html', {'query': data, 'query_time': elapsed_time})
