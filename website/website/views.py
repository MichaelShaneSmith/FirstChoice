from django.http import HttpResponse


def data(request):
    return HttpResponse("Hello, world. This is a test.")
