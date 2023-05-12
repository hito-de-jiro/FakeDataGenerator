Fake data generator
===================
Generation of random data (full name, integer, phone, email, address)
and save to CSV file

## Build
```
pip install -r requirements.txt

python manage.py createsuperuser

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```
## Run

Click the "New scheme" button.
Enter the name of the scheme,
column name and order,
select other options.

Under "column type", select the data type.
You can add columns as needed.
Click the "Submit" button.

To create data, select the name of your schema.
On the page, enter the number of rows and click "Generate data".
after reloading the page, if everything went well,
you will see the changed status and a link to download the data.
