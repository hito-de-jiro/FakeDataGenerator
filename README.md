Fake data generator
===================
Generation of random data (full name, integer, phone, email, address)
and save to CSV file

## Preparation
Install venv
```
pip install virtualenv
virtualenv venv
```
activate venv (..\venv\Scripts>activate bla-bla-bla)

## Build

Go to ROOT folder and install dependencies (..\app>pip install -r requirements.txt) 
```
pip install -r requirements.txt
```

Make and apply project migrations
```
python manage.py makemigrations
python manage.py migrate
```
Create superuser
```
python manage.py createsuperuser
```

Run server
```
python manage.py runserver
```
## How to create data

Click the "New scheme" button.<br>
Enter the name of the scheme,<br>
column name and order,<br>
select other options.
---
Under "column type", select the data type.<br>
You can press button "Add column" and add columns as needed.<br>
Click the "Submit" button.
---
To create data, select the name of your schema.<br>
On the page, enter the number of rows and click "Generate data".<br>
after reloading the page, if everything went well,<br>
you will see the changed status (green "Ready") and a link to download the data.
