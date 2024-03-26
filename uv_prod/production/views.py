from django.shortcuts import render


def production(request):
    template_name = 'production.html'
    return render(request, template_name)
