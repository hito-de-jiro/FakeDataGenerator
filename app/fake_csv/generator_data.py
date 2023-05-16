import csv

from faker import Faker


def generate_fake_value(fake, data_type, range_from, range_to):
    """Generate a single fake value of a given type"""
    if data_type == 'fullname':
        return fake.name()

    elif data_type == 'integer':
        if range_from and range_to is not None:
            return fake.random_int(range_from, range_to)
        else:
            return None

    elif data_type == 'phone':
        return fake.phone_number()
    elif data_type == 'email':
        return fake.email()
    elif data_type == 'address':
        return fake.address()


def generate_fake_data(num: int, data_dict: dict) -> iter:
    """Generate fake data as a generator"""
    fake = Faker()

    for _ in range(int(num)):
        row = {}
        for name, data in data_dict.items():
            row[name] = generate_fake_value(fake, data[0], data[1], data[2])

        yield row


def save_data(data_iter: iter, file_name: str, delimiter: str, quotechar: str,
              data_dict: dict):
    """Save created data to CSV file"""
    fieldnames = data_dict.keys()

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
                data_dict: dict,
                file_name: str,
                delimiter: str,
                quotechar: str):
    """Starting the creation process"""
    data_iter = generate_fake_data(num=num,
                                   data_dict=data_dict)
    save_data(data_iter,
              delimiter=delimiter,
              quotechar=quotechar,
              file_name=file_name,
              data_dict=data_dict
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
