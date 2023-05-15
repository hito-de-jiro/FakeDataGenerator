Fake data generator
===================
Generation of random data (full name, integer, phone, email, address)
and save to CSV file<br>
Used Django framework

## Copy project
```
git clone https://github.com/hito-de-jiro/FakeDataGenerator.git
```

## Preparation
Install Python venv
```
pip install virtualenv
virtualenv venv
```
Activate venv (windows)
```
venv\Scripts\activate.bat
```

## Build
Install dependencies of project
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

## Usage

Click the "New scheme" button. Enter the name of the scheme, column name and order, select other options.

Under "column type", select the data type.
You can press button "Add column" and add columns as needed.
Click the "Submit" button.

To create data, select the name of your schema.
On the page, enter the number of rows and click "Generate data".
after reloading the page, if everything went well,
you will see the changed status (green "Ready") and a link to download the data.