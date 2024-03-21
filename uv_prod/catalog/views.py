from django.shortcuts import render


def product_list(request):
    template_name = 'catalog.html'
    return render(request, template_name)
