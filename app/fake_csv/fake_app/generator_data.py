import csv
import os

from django.conf import settings
from faker import Faker


def generate_fake_value(fake, data_type, range_from=18, range_to=60):
    """Generate a single fake value of a given type"""
    if data_type == 'fullname':
        return fake.name()
    elif data_type == 'age':
        return fake.random_int(range_from, range_to)
    elif data_type == 'phone':
        return fake.phone_number()
    elif data_type == 'email':
        return fake.email()
    elif data_type == 'address':
        return fake.address()


def generate_fake_data(num: int, data_types: list, range_from=18, range_to=60) -> iter:
    """Generate fake data as a generator"""
    fake = Faker()

    for _ in range(int(num)):
        row = {}
        for data_type in data_types:
            row[data_type] = generate_fake_value(fake, data_type, range_from, range_to)
        yield row


def save_data(data_iter: iter, file_name: str, delimiter: str, quotechar: str, data_types: list):
    """Save created data to CSV file"""
    fieldnames = data_types
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,
                                delimiter=delimiter,
                                quotechar=quotechar,
                                )
        writer.writeheader()
        for row in data_iter:
            writer.writerow(row)

    return file_name


def run_process(num: int,
                data_types: list,
                file_name: str,
                range_from: int,
                range_to: int,
                delimiter: str,
                quotechar: str, ):
    data_iter = generate_fake_data(num=num,
                                   range_from=range_from,
                                   range_to=range_to,
                                   data_types=data_types)
    filepath = save_data(data_iter,
                         delimiter=delimiter,
                         quotechar=quotechar, file_name=file_name, data_types=data_types)

    return filepath
