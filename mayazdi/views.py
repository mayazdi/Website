from django.http import HttpResponse


def default(requset):
    return HttpResponse("<h1>Home</h1>")


def post(request):
    return HttpResponse("<h1>Post</h1>")
