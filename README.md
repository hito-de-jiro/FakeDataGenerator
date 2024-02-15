Fake data generator
===================
Generation of random data (full name, integer, phone, email, address)
and save to CSV file.<br>
Used Django, Docker, PostgreSQL, Celery, Redis, Flower.<br>
_By default, the program works with_ _**threads**_.<br> 
For Celery, Postgres, and Docker, you need to uncomment some code.<br> 
Read the docs for the **Docker build**.

## How to clone the repository?
To clone the repository, run the following command.
```shell
git clone https://github.com/hito-de-jiro/FakeDataGenerator.git
```
## Preparation
Install Python venv.
```shell
pip install virtualenv
virtualenv venv
```
Activate venv (windows).
```shell
venv\Scripts\activate
```
## Build
1. Install dependencies of project.
   ```shell
   pip install -r requirements.txt
   ```
2. Go to application folder.
   ```shell
   cd app
   ```
3. Make and apply project migrations.
   ```shell
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create superuser.
   ```shell
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '12345')"
   ```
   Will be created superuser  with these data:<br>
   login: admin<br>
   mail: admin@example.com<br> 
   password: 12345

5. Run server.
```shell
python manage.py runserver
```

## Usage

Click the "New scheme" button. Enter the name of the scheme, column name and order, select other options.
Under "column type", select the data type.
You can press button "Add column" and add columns as needed.
Click the "Submit" button.
To create data, select the name of your schema.
On the page, enter the number of rows and click "Generate data".
Tasks in progress have three statuses: **Wait**, **Running**, **Ready**.
After completing the task, if everything went well,
You will see the status changed to "**Ready**" and a link to **download** data.

## Docker build

1. Copy project
    ```shell
    git clone https://github.com/hito-de-jiro/FakeDataGenerator.git
    ```
2. By default, the program works with threads. To use Celery you need to uncomment the code in the following files:
   ```
   app/__init__.py
   app/settings.py
   fake_csv/generator_data.py
   fake_csv/tasks.py
   ```
3. Build
    ```shell
    docker-compose up -d --build
    ```
4. Create a superuser:<br>
   
   ```shell
   docker compose run --rm django python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '12345')"
   ```
   Will be created superuser  with these data:<br>
   - login: admin<br>
   - mail: admin@example.com<br> 
   - password: 12345<br><br>

5. And start
    ```shell
   docker compose up
   ```
6. Stop the application:
    ```shell
    docker compose stop
    ```
<br>
The app is available at the [link](http://127.0.0.1:8000/)<br>
To monitor tasks, **Flower** is used, available at [link](http://127.0.0.1:5555/)