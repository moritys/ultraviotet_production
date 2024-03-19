from django.http import HttpResponse


def production(request):
    return HttpResponse('Production')
