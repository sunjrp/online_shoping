from django.shortcuts import render, redirect
from .models import *
import time
from django.db.models import Q
from django.http import HttpResponse
from datetime import timedelta, datetime
import requests
import string
import random
from random import randrange
import names
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


api_key = "fcc6fff35de0b2b9470d180bb4c76555"  #for themoviedb.org


def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        if not User.objects.filter(username=username).exists():
            user1 = User.objects.create(username=username)
            user1.set_password(password)
            user1.save()
            return render(request, 'login.html')
        else:
            error = "Error Please Check"
            return render(request, 'register.html', {'error':error})

    return render(request, 'register.html', )


def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Username or Password is INCORRECT"
            return render(request, 'login.html', {'error':error})
    else:
        return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('home.html')


def gen_movies(request):
    add_movie(100000)
    return render(request, 'home.html')


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def create_movie(size):
    movie_structure = {'title': '', 'price': '', 'rating': '', 'storyline': '', 'release_date': '', 'genre': [] }
    movie_list = []
    # for first time run you must add genre first
    if False:
        add_genres()
    d1 = datetime.strptime('1/1/2000 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')
    for item in range(1, size+1):
        movie_structure['title'] = names.get_full_name()
        movie_structure['price'] = random.randint(100, 10000)
        movie_structure['rating'] = random.randrange(0, 10)
        movie_structure['storyline'] = names.get_full_name()
        movie_structure['release_date'] = random_date(d1, d2)
        movie_structure['genre'] = []
        for i in range(2):
            movie_structure['genre'].append(random.randint(1, 9))
        movie_structure['genre'] = set(movie_structure['genre'])
        movie_list.append(movie_structure.copy())
        movie_structure.clear()
        print(item)
    return movie_list


def add_genres():
    genre_list = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Romance', 'Western']
    for genre in genre_list:
        g = Genre(name=genre)
        g.save()


def add_movie(size):
    movie_list = create_movie(size)
    for movie in movie_list:
        print(movie)
        p = Product(title=movie["title"],
                    price=movie["price"],
                    rating=str(movie["rating"]),
                    storyline=movie["storyline"],
                    release_date=movie["release_date"])
        print(p)
        p.save()
        for id in movie["genre"]:
            temp = Genre.objects.get(id=id)
            p.genre.add(temp)
            p.save()


def home(request):
    return render(request, 'home.html')


def market(request):
    genre = Genre.objects.all()
    genre_out = [""]
    for genre_obj in genre:
        if genre_obj.name != "":
            genre_out.append(genre_obj.name)
    rate = Product.  objects.all()
    rate_out = []
    for rate_obj in rate:
        if rate_obj.rating != "":
            rate_out.append(rate_obj.rating)

    return render(request, 'market.html', {'data': 'a lot of data', 'genre': genre_out, 'rating': rate_out})


def search(request):
    keyword = request.GET['keyword']
    genre = request.GET['genres']
    start_time = time.time()
    if genre:
        data = query_search(keyword, genre_select=genre)
    else:
        data = query_search(keyword)
    elapsed_time = time.time() - start_time
    return render(request, 'result.html', {'query': data, 'query_time': elapsed_time})


def query_search(keyword, movie_id=None, date_select=None, genre_select=None, tag_select=None, price_select=None):
    """search data in DB by time and keyword and return query set"""
    result = Product.objects.all()
    if date_select:
        result = result.exclude(Q(release_date__gt=date_select[0]) | Q(release_date__lt=date_select[1]))

    if movie_id:
        result = result.filter(Q(id=movie_id))

    if keyword != "":  # if have specific keyword
        result = result.filter(Q(title__icontains=keyword)).order_by('title')
        if price_select:
            result = result.exclude(Q(price__gt=price_select[0]) | Q(price__lt=price_select[1]))
        if genre_select:
            result = result.filter(Q(genre__name=genre_select))
        if tag_select:
            for word in tag_select:
                result = result.filter(Q(genre=word))
    return result


def details(request, movie_id):
    start_time = time.time()
    try:
        data = query_search("", movie_id=movie_id)[0]
    except IndexError:
        data = "Can't find this movie id"
    elapsed_time = time.time() - start_time
    return render(request, 'movie_detail.html', {'query': data, 'query_time': elapsed_time})


def add_cart(request, movie_id):
    start_time = time.time()
    data = query_search("", movie_id=movie_id)[0]
    elapsed_time = time.time() - start_time
    return render(request, 'cart.html', {'query': data, 'query_time': elapsed_time})
