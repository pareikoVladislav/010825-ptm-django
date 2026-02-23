from django.http import HttpResponse


def index(request):
    return HttpResponse(
        "HELLOW, WORLD!!!!!!!!"
    )


def home_page(request):
    return HttpResponse(
        "HOME PAGE"
    )
