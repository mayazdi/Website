from django.http import HttpResponse
from django.shortcuts import render
import requests
import re


def index(request):
    response = requests.get('https://markazetour.ir/Systems/FlightCheapestPriceBar.aspx?Origin=THR&Destination=MHD')
    res3 = re.findall('\d+,000', response.text)
    return render(request, 'Charter.html', {'response':res3})


def chart(request):
    return HttpResponse("<h1>Charter HomePage</h1>")
