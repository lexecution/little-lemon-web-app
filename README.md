# little lemon web application

the back end for the little lemon restaurant

`littlelemon/` is the django project and `restaurant/` is the app (models, serializers, views, urls). the home page template lives in `templates/`, its css and images in `static/`, and the unit tests in `tests/`.

## setup

you need python 3.12 or newer, a mysql server on `127.0.0.1:3306`, & git. 

**1. create a virtual environment and install the requirements**

```bash
python -m venv venv

# macos / linux
source venv/bin/activate
# windows (cmd)
venv\scripts\activate

pip install -r requirements.txt
```

**2. create the database**

```sql
create database littlelemon character set utf8mb4;
```

the settings assume user `root`, an empty password, host `127.0.0.1` and port `3306`.

**3. migrate and create an admin user**

```bash
python manage.py migrate
python manage.py createsuperuser
```

**4. run the server**

```bash
python manage.py runserver
```

go to http://127.0.0.1:8000/ and you'll be redirected to the home page at `/restaurant/`. you can add menu items from the admin site at `/admin/` or thru the api.

## endpoints

a menu item has a `title`, a `price` and an `inventory` count. a booking has a `name`, `no_of_guests` (at least 1) and a `booking_date`.

| method | path | token needed | what it does |
| --- | --- | --- | --- |
| get | `/restaurant/` | no | home page |
| get | `/restaurant/menu/` | no | list menu items |
| post | `/restaurant/menu/` | yes | create a menu item |
| get | `/restaurant/menu/<id>` | no | get one menu item |
| put, patch | `/restaurant/menu/<id>` | yes | update a menu item |
| delete | `/restaurant/menu/<id>` | yes | delete a menu item |
| get, post | `/restaurant/booking/tables/` | yes | list or create bookings |
| get, put, patch, delete | `/restaurant/booking/tables/<id>/` | yes | work with one booking |
| post | `/auth/users/` | no | register |
| get | `/auth/users/me/` | yes | current user |
| post | `/auth/token/login/` | no | log in, returns `auth_token` |
| post | `/auth/token/logout/` | yes | log out and drop the token |
| post | `/restaurant/api-token-auth/` | no | plain drf login, returns `token` |
| get | `/admin/` | superuser | django admin |

anyone can read the menu, but changing it needs a token. the booking api needs a token for every request. send it as `authorization: token <token>` or `authorization: bearer <token>`.

## trying the api

```bash
# register
curl -x post http://127.0.0.1:8000/auth/users/ \
  -h "content-type: application/json" \
  -d '{"username": "lemon", "email": "lemon@example.com", "password": "str0ng-lemon-pass!"}'

# log in (returns {"auth_token": "<token>"})
curl -x post http://127.0.0.1:8000/auth/token/login/ \
  -h "content-type: application/json" \
  -d '{"username": "lex", "password": "str0ng-lemon-pass!"}'

# book a table
curl -x post http://127.0.0.1:8000/restaurant/booking/tables/ \
  -h "authorization: token <token>" -h "content-type: application/json" \
  -d '{"name": "adrian", "no_of_guests": 4, "booking_date": "2026-12-24t19:30:00z"}'

# log out
curl -x post http://127.0.0.1:8000/auth/token/logout/ \
  -h "authorization: token <token>"
```

## tests

```bash
python manage.py test
```
