# Sinhala News Platform
This is the source of sinhala news platform dissertation project.

Name: Senarath Pathiranalage Nishan Sajeewee Wickramasinghe
Student ID: Q102091977

## Instructions to Start the Application

### Pre-Requisites
Python greater than 3.11 installed. Anaconda prefererd

### How to start the application

1. Create a new anaconda environment.
    ```bash
    conda create --name sinhala-news-platform python=3.11
    ```

2. Activate anaconda environment.
    ```bash
    conda activate sinhala-news-platform
    ```

3. Install required python dependencies.
    ```bash
    pip install -r requirements.txt
    ```

4. Download models from [OneDrive](https://ssu-my.sharepoint.com/:f:/r/personal/2senan77_solent_ac_uk/Documents/Dissertation%20Project/Documentations/Final%20Report/Shared%20Models?csf=1&web=1&e=hGldD5) location.
    1. Create a new directory in project root directory called "temp" if not exists.
    2. Move the downloaded files into "temp" folder. (Make sure not to rename any folder in downloaded files)

5. Start the application.
    ```bash
    python manage.py runserver --noreload
    ```


## Development Notes
This sections is only for development purposes and please ignore if you want to run the application.

### Start the server
```bash
python manage.py runserver
```

Run server without duplicate schedulers
```bash
python manage.py runserver --noreload
```

### Migrate database changes

`python manage.py makemigrations`

then migrate using
`python manage.py migrate`


### Create superuser
A superuser login is required to login to the django admin portal
`python manage.py createsuperuser`

Admin portal url: `http://localhost:8000/admin`

Default credentials
* Username: admin
* Password: 123


### Create a new app
`python manage.py startapp <appname>`