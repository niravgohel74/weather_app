from django.shortcuts import render
import requests
from .models import *
from .forms import CityForm
import os

api_key = os.getenv('SECRET_API_KEY')

# 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6b558fe3982f97c8a25227d68abb0c96'

# Create your views here.
def index(request):
    url = api_key
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        if 'main' in r:
            city_weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }
            data.append(city_weather)
        else:
            print("Error")

    context = {'data':data,'form':form}
    return render(request, 'index.html', context)