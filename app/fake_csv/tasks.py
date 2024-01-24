# fake_csv/tasks.py
import threading

from fake_csv.generator_data import run_process


def create_dataset_task(
        parent_id,
        num_rows,
        data_dict,
        file_name,
        column_separator,
        string_character, ):
    """Create dataset."""
    # use celery, comment for threading
    # run_process.delay(
    #     parent_id=parent_id,
    #     num_rows=num_rows,
    #     data_dict=data_dict,
    #     file_name=file_name,
    #     column_separator=column_separator,
    #     string_character=string_character,
    # )
    # use threads, comment for celery
    thr = threading.Thread(target=run_process, args=(
        parent_id,
        num_rows,
        data_dict,
        file_name,
        column_separator,
        string_character,
    ), daemon=True)

    thr.start()
