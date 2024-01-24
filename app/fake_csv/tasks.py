# fake_csv/tasks.py
import threading
import time

from fake_csv.generator_data import run_process
from fake_csv.models import DatasetModel


def create_dataset_task(
        parent_id,
        num_rows,
        data_dict,
        file_name,
        column_separator,
        string_character):
    """Create dataset."""
    # set status -- Wait
    data = DatasetModel(schema_id=parent_id)
    data.status = 'Wait'
    data.save()
    pk_dataset = data.id

    # use celery, comment for threading
    # run_process.delay(
    #     pk_dataset=pk_dataset,
    #     num_rows=num_rows,
    #     data_dict=data_dict,
    #     file_name=file_name,
    #     column_separator=column_separator,
    #     string_character=string_character,
    # )
    # use threads, comment for celery

    thr = threading.Thread(target=run_process, args=(
        pk_dataset,
        num_rows,
        data_dict,
        file_name,
        column_separator,
        string_character,
    ), daemon=True)
    time.sleep(3)
    thr.start()
