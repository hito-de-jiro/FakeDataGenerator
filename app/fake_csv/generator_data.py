# fake_csv/generator_data.py
import csv
import os

from django.conf import settings
from faker import Faker

# from app.celery import app  # to use Celery it is necessary to uncomment
from fake_csv.models import DatasetModel


def generate_fake_value(fake, data_type, range_from=0, range_to=0):
    """Generate a single fake value of a given type"""
    if data_type == 'fullname':
        return fake.name()

    elif data_type == 'integer':
        return fake.random_int(range_from, range_to)

    elif data_type == 'phone':
        return fake.phone_number()
    elif data_type == 'email':
        return fake.email()
    elif data_type == 'address':
        return fake.address().replace('\n', ' ')


def generate_fake_data(num_rows: int, data_dict: dict) -> iter:
    """Generate fake data as a generator"""
    fake = Faker()

    for _ in range(int(num_rows)):
        row = {}
        for name, data in data_dict.items():
            row[name] = generate_fake_value(fake, data[0], data[1], data[2])

        yield row


def save_data(
        pk_dataset: int,
        data_iter: iter,
        file_name: str,
        delimiter: str,
        quotechar: str,
        data_dict: dict):
    """Save created data to CSV file"""
    # Create and save csv file
    fieldnames = data_dict.keys()
    with open(os.path.join(settings.MEDIA_ROOT, file_name), 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=fieldnames,
            delimiter=delimiter,
            quotechar=quotechar,
        )
        writer.writeheader()
        for row in data_iter:
            writer.writerow(row)
    # File is ready, status in database changed to 'Ready'
    status = 'Ready'
    set_status(file_name, pk_dataset, status)


def set_status(file_name, pk_dataset, status):
    data = DatasetModel.objects.get(id=pk_dataset)
    data.status = status
    data.file = file_name
    data.save()


# @app.task()  # to use Celery it is necessary to uncomment
def run_process(
        pk_dataset: int,
        num_rows: int,
        data_dict: dict,
        file_name: str,
        delimiter: str,
        quotechar: str):
    """Starting the creation process"""
    status = 'Running'
    set_status(file_name, pk_dataset, status)
    data_iter = generate_fake_data(num_rows=num_rows,
                                   data_dict=data_dict)
    save_data(
        pk_dataset,
        data_iter,
        delimiter=delimiter,
        quotechar=quotechar,
        file_name=file_name,
        data_dict=data_dict)
