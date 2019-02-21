from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import requests
import re
import jdatetime


def index(request, origin, destination):
    response = requests.get('https://markazetour.ir/Systems/FlightCheapestPriceBar.aspx?Origin=THR&Destination=MHD')
    res = re.findall('\d+,000', response.text)

    time = jdatetime.datetime.now()
    iter = wbc = 7 - int(time.strftime("%w"))
    weeklist = [wbc]
    month_length = (
                jdatetime.date(int(time.year), int(time.month), 1) - jdatetime.date(int(time.year), int(time.month) - 1,
                                                                                    1)).days
    while iter + 7 < month_length:
        iter += 7
        weeklist.append(iter)

    if origin.lower() == 'tehran' and destination.lower() == 'mashad':
        return render(request, 'Charter.html',
                      {'response': res, 'origin': origin, 'destination': destination, 'wb': time.strftime("%w"),
                       'wbc': wbc, 'weekends': weeklist})
    raise Http404('Cities not supported yet')


def chart(request):
    return HttpResponse("<h1>Charter HomePage</h1>")
