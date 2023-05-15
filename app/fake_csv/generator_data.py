import csv

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


def generate_fake_data(num: int, name_type_dict: dict, range_from=18, range_to=60) -> iter:
    """Generate fake data as a generator"""
    fake = Faker()

    for _ in range(int(num)):
        row = {}
        for data_name, data_type in name_type_dict.items():
            row[data_name] = generate_fake_value(fake, data_type, range_from, range_to)
        yield row


def save_data(data_iter: iter, file_name: str, delimiter: str, quotechar: str,
              name_type_dict: dict):
    """Save created data to CSV file"""
    fieldnames = name_type_dict.keys()
    with open(file_name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,
                                delimiter=delimiter,
                                quotechar=quotechar,
                                )
        writer.writeheader()
        for row in data_iter:
            writer.writerow(row)


def run_process(data,
                id_dataset,
                num: int,
                name_type_dict: dict,
                file_name: str,
                range_from: int,
                range_to: int,
                delimiter: str,
                quotechar: str):
    """Starting the creation process"""
    data_iter = generate_fake_data(num=num,
                                   range_from=range_from,
                                   range_to=range_to,
                                   name_type_dict=name_type_dict)
    save_data(data_iter,
              delimiter=delimiter,
              quotechar=quotechar,
              file_name=file_name,
              name_type_dict=name_type_dict,
              )

    get_set_ready(data,
                  id_dataset,
                  file_name)


def get_set_ready(data, id_dataset, file_name):
    """Set the status of the finished file"""
    if id_dataset:
        data.status = 'Ready'
        data.file = file_name
        data.save()
