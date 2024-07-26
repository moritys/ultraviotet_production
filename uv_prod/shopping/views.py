from django.shortcuts import render

from .utils import calculate_components_for_document, document_is_new
from production.models import Document


def shopping(request):
    template_name = 'shopping.html'

    documents = Document.objects.all().order_by('number')
    document_components_quantities = {}

    for document in documents:
        if document_is_new(document):
            document_components_quantities[document] = calculate_components_for_document(document)

    context = {
        'document_components_quantities': document_components_quantities
    }

    return render(request, template_name, context)
