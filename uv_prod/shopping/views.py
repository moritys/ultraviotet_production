from django.shortcuts import render
import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook

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


def generate_excel_report(request):
    documents = Document.objects.all().order_by('number')
    total_components_quantities = {}

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%Y|%H:%M")

    for document in documents:
        if document_is_new(document):
            document_components_quantities = calculate_components_for_document(document)
            for component, quantities in document_components_quantities.items():
                if component not in total_components_quantities:
                    total_components_quantities[component] = {
                        'calculated': 0,
                        'stock': quantities['stock']
                    }
                total_components_quantities[component]['calculated'] += quantities['calculated']

    data = {
        'Component': [],
        'Part Number': [],
        'Order': [],
        'In stock': [],
    }

    for component, quantities in total_components_quantities.items():
        data['Component'].append(component.name)
        data['Part Number'].append(component.part_number)
        data['Order'].append(quantities['calculated'])
        data['In stock'].append(quantities['stock'])

    # Создание таблицы с Pandas и запись в Excel
    df = pd.DataFrame(data)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=components_report_{formatted_datetime}.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name='Components Report'
        )

    workbook = writer.book
    worksheet = workbook['Components Report']

    for column_cells in worksheet.columns:
        max_length = 0
        column = column_cells[0].column_letter

        for cell in column_cells:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except Exception:
                pass

        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column].width = adjusted_width

    writer.close()

    return response
