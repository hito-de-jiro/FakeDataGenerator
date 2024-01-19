# fake_csv/tasks.py
import os
from datetime import datetime

from app.celery import app
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from fake_csv.generator_data import run_process
from fake_csv.models import SchemaModel, ColumnModel, DatasetModel
from fake_csv.views import get_set_processing


@login_required
def create_dataset(request, pk):
    """Create dataset."""
    now = datetime.now().strftime("%d%m%Y_%H%M%S")
    parent_obj = get_object_or_404(SchemaModel, pk=pk)
    parent_id = parent_obj.id
    columns = ColumnModel.objects.filter(schema_id=parent_id)
    num_rows = request.POST['rows']
    data_dict = {column.name: [column.type, column.range_from, column.range_to] for column in columns}
    file_name = os.path.join(settings.MEDIA_ROOT, f'{parent_obj.name}_{now}.csv')
    column_separator = parent_obj.column_separator
    string_character = parent_obj.string_character
    data = DatasetModel(schema_id=parent_id)

    id_dataset = get_set_processing(data)

    # Run celery task
    run_process.delay(data,
                      id_dataset,
                      num_rows,
                      data_dict,
                      file_name,
                      column_separator,
                      string_character,
                      )

    return redirect('schema_detail', pk=pk)
