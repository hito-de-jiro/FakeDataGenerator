# fake_csv/tasks.py
import threading

from fake_csv.generator_data import run_process


def create_dataset_task(
        pk_dataset: int,
        num_rows: int,
        data_dict: dict,
        file_name: str,
        column_separator: str,
        string_character: str):
    # Use threading
    thr = threading.Thread(target=run_process, args=(
        pk_dataset,
        num_rows,
        data_dict,
        file_name,
        column_separator,
        string_character,
    ), daemon=True)

    thr.start()
    # for Celery it is necessary to uncomment
    # run_process.delay(
    #     pk_dataset,
    #     num_rows,
    #     data_dict,
    #     file_name,
    #     column_separator,
    #     string_character,
    # )