How to start the server
```bash
python manage.py runserver
```


How to migrate database changes

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
