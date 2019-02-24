from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import requests
import re
import jdatetime


def my_min(first, second):
    if first == -1:
        return second
    elif second == -1:
        return first
    else:
        return min(first, second)


def prices():
    with open("links.txt") as f:
        links = f.readlines()
    links = [x.strip('\n') for x in links]
    result = []
    sites = []
    for i in range(0, 32):
        result.append(-1)
        sites.append('sln724.com')
    for link in links:
        response = requests.get('http://' + link + '/Systems/FlightCheapestPriceBar.aspx?Origin=THR&Destination=MHD')
        res = re.findall('(\d+),000', response.text)
        for i in range(0, 32):
            if i < len(res):
                temp = result[i]
                result[i] = my_min(result[i], res[i])
                if temp != result[i]:
                    sites[i] = link
    return list(zip(sites, result))


def index(request, origin, destination):
    if origin.upper() == 'THR' and destination.upper() == 'MHD':
        response = requests.get('https://markazetour.ir/Systems/FlightCheapestPriceBar.aspx?Origin=THR&Destination=MHD')
        res = re.findall('(\d+),000', response.text)
        time = jdatetime.datetime.now()
        iter = wbc = 7 - int(time.strftime("%w"))
        weeklist = [wbc]
        result = prices()
        month_length = (
                jdatetime.date(int(time.year), int(time.month), 1) - jdatetime.date(int(time.year), int(time.month) - 1,
                                                                                    1)).days
        while iter + 7 <= month_length:
            iter += 7
            weeklist.append(iter)
        while len(weeklist) <= 5:
            weeklist.append(month_length)
        w1 = {}
        w2 = {}
        w3 = {}
        w4 = {}
        w5 = {}
        w6 = {}
        for i in range(0, weeklist[0]):
            if i + time.day <= month_length:
                w1[i + time.day] = result[i - 1]
        for i in range(weeklist[0], weeklist[1]):
            if i + time.day <= month_length:
                w2[i + time.day] = result[i - 1]
        for i in range(weeklist[1], weeklist[2]):
            if i + time.day <= month_length:
                w3[i + time.day] = result[i - 1]
        for i in range(weeklist[2], weeklist[3]):
            if i + time.day <= month_length:
                w4[i + time.day] = result[i - 1]
        for i in range(weeklist[3], weeklist[4]):
            if i + time.day <= month_length:
                w5[i + time.day] = result[i - 1]
        for i in range(weeklist[4], weeklist[5]):
            if i + time.day <= month_length:
                w6[i + time.day] = result[i - 1]
        return render(request, 'Charter.html',
                      {'response': res, 'origin': origin, 'destination': destination, 'wb': time.strftime("%w"),
                       'wbc': wbc, 'w1': w1, 'w2': w2, 'w3': w3, 'w4': w4, 'w5': w5, 'w6': w6, 'mon1': 'اسفند',
                       'mon2': 'فروردین', 'domain': 'markazetour.ir'})
    raise Http404('Cities not supported yet')


def chart(request):
    return HttpResponse("<h1>Charter HomePage</h1>")
