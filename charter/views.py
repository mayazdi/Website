from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import requests
import re
import jdatetime


def index(request, origin, destination):
    if origin.upper() == 'THR' and destination.upper() == 'MHD':
        response = requests.get('https://markazetour.ir/Systems/FlightCheapestPriceBar.aspx?Origin=THR&Destination=MHD')
        res = re.findall('(\d+),000', response.text)
        time = jdatetime.datetime.now()
        iter = wbc = 7 - int(time.strftime("%w"))
        weeklist = [wbc]
        month_length = (
            jdatetime.date(int(time.year), int(time.month), 1) - jdatetime.date(int(time.year), int(time.month) - 1,
                                                                                1)).days
        while iter + 7 <= month_length:
            iter += 7
            weeklist.append(iter)
        if len(weeklist) == 5:
            weeklist.append(month_length)
        w1 = {}
        w2 = {}
        w3 = {}
        w4 = {}
        w5 = {}
        w6 = {}
        for i in range(1, weeklist[0] + 1):
            w1[i] = res[i - 1]
        for i in range(weeklist[0] + 1, weeklist[1] + 1):
            w2[i] = res[i - 1]
        for i in range(weeklist[1] + 1, weeklist[2] + 1):
            w3[i] = res[i - 1]
        for i in range(weeklist[2] + 1, weeklist[3] + 1):
            w4[i] = res[i - 1]
        for i in range(weeklist[3] + 1, weeklist[4] + 1):
            w5[i] = res[i - 1]
        for i in range(weeklist[4] + 1, weeklist[5] + 1):
            w6[i] = res[i - 1]
        return render(request, 'Charter.html',
                      {'response': res, 'origin': origin, 'destination': destination, 'wb': time.strftime("%w"),
                       'wbc': wbc, 'w1': w1, 'w2': w2, 'w3': w3, 'w4': w4, 'w5': w5, 'w6': w6})
    raise Http404('Cities not supported yet')


def chart(request):
    return HttpResponse("<h1>Charter HomePage</h1>")
