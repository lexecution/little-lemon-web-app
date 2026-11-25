# Little Lemon – Web Application & REST APIs

Back-end for the **Little Lemon** restaurant, built with **Django** and **Django REST Framework** on a **MySQL** database. It serves a static HTML home page and exposes two APIs: a **Menu API** (ordering food) and a **Table Booking API** (reserving a table for a date and number of guests). User registration and token authentication are provided by **Djoser**.

## Features

| Requirement | Where it lives |
| --- | --- |
| Django serves static HTML content | `templates/index.html`, `static/`, route `/restaurant/` |
| Back end connected to MySQL | `DATABASES` in `littlelemon/settings.py` (`mysqlclient` driver) |
| Menu API (CRUD) | `restaurant/views.py` → `MenuItemsView`, `SingleMenuItemView` |
| Table Booking API (CRUD) | `restaurant/views.py` → `BookingViewSet` (DRF router) |
| User registration & authentication | Djoser + DRF token authentication |
| Unit tests | `tests/test_models.py`, `tests/test_views.py` |
| Testable with Insomnia | See [Testing with Insomnia](#testing-with-insomnia) |

## Project structure

```
LittleLemon/
├── manage.py
├── requirements.txt
├── README.md             <- this file
├── Readme.txt            <- API paths for peer review
├── .gitignore
├── .env.example          <- optional environment variables
├── littlelemon/          <- Django project package
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── restaurant/           <- Django app
│   ├── admin.py          <- registers Menu and Booking in the admin
│   ├── authentication.py <- also accepts "Authorization: Bearer <token>"
│   ├── models.py         <- Menu and Booking models
│   ├── serializers.py    <- MenuSerializer, BookingSerializer
│   ├── views.py          <- index view, Menu views, BookingViewSet
│   ├── urls.py
│   └── migrations/
├── templates/
│   └── index.html        <- home page
├── static/
│   ├── css/style.css
│   └── img/              <- logos, photos, favicon
└── tests/
    ├── test_models.py
    └── test_views.py
```

## Prerequisites

* Python 3.12+ (developed and tested on 3.12 with Django 6.1 and Django 5.2 LTS; on older Python versions `pip` resolves to Django 5.2 LTS)
* A running **MySQL** server (MariaDB also works) on `127.0.0.1:3306`
* Git

## Setup

### 1. Create a virtual environment and install dependencies

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate
# Windows (cmd)
venv\Scripts\activate

pip install -r requirements.txt
```

> **`mysqlclient` build errors?** On Linux install the MySQL client headers first
> (Debian/Ubuntu: `sudo apt install pkg-config libmysqlclient-dev build-essential python3-dev`).
> On macOS: `brew install mysql pkg-config`. Windows normally installs a pre-built wheel.

### 2. Create the database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE LittleLemon CHARACTER SET utf8mb4;
```

The default settings expect: database `LittleLemon`, user `root`, empty password, host `127.0.0.1`, port `3306`.
If your credentials differ, set the environment variables listed in `.env.example`
(`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) instead of editing the code.

### 3. Run the migrations and create an admin user

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start the server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> – it redirects to the home page at <http://127.0.0.1:8000/restaurant/>.

Optionally add some data from the admin site at <http://127.0.0.1:8000/admin/> (log in with the superuser) or through the APIs below.

## Data model

| Model | Fields |
| --- | --- |
| `Menu` | `id`, `title` (varchar 255), `price` (decimal 10,2), `inventory` (int) |
| `Booking` | `id`, `name` (varchar 255), `no_of_guests` (int, ≥ 1), `booking_date` (datetime) |

## API reference

Base URL: `http://127.0.0.1:8000`

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `/restaurant/` | – | Home page (HTML) |
| GET | `/restaurant/menu/` | – | List menu items |
| POST | `/restaurant/menu/` | Token | Create a menu item |
| GET | `/restaurant/menu/<id>` | – | Retrieve one menu item |
| PUT / PATCH | `/restaurant/menu/<id>` | Token | Update a menu item |
| DELETE | `/restaurant/menu/<id>` | Token | Delete a menu item |
| GET | `/restaurant/booking/tables/` | Token | List bookings |
| POST | `/restaurant/booking/tables/` | Token | Create a booking |
| GET / PUT / PATCH / DELETE | `/restaurant/booking/tables/<id>/` | Token | Retrieve, update or delete a booking |
| POST | `/auth/users/` | – | **Register** a new user |
| GET | `/auth/users/me/` | Token | Current user |
| POST | `/auth/token/login/` | – | **Login** (Djoser) → `auth_token` |
| POST | `/auth/token/logout/` | Token | **Logout** (invalidates the token) |
| POST | `/restaurant/api-token-auth/` | – | Obtain a token (plain DRF view) → `token` |
| – | `/admin/` | Superuser | Django admin |

The menu can be **read** by anyone, but creating, changing or deleting menu items requires a token.
The booking API is **fully protected**: every request needs a token.

### Authentication flow

```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "lex", "email": "lex@example.com", "password": "Str0ng-lemon-pass!"}'

# 2. Log in – returns {"auth_token": "<token>"}
curl -X POST http://127.0.0.1:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "lex", "password": "Str0ng-lemon-pass!"}'

# 3. Call a protected endpoint
curl http://127.0.0.1:8000/restaurant/booking/tables/ \
  -H "Authorization: Token <token>"

curl -X POST http://127.0.0.1:8000/restaurant/booking/tables/ \
  -H "Authorization: Token <token>" -H "Content-Type: application/json" \
  -d '{"name": "Adrian", "no_of_guests": 4, "booking_date": "2026-12-24T19:30:00Z"}'

# 4. Log out
curl -X POST http://127.0.0.1:8000/auth/token/logout/ \
  -H "Authorization: Token <token>"
```

The API accepts both `Authorization: Token <token>` (DRF default) and `Authorization: Bearer <token>`.

## Testing with Insomnia

1. Install [Insomnia](https://insomnia.rest/download) and start the Django server.
2. **Get a token** – create a `POST` request to `http://127.0.0.1:8000/auth/token/login/` (or `/restaurant/api-token-auth/`), body type **JSON**:
   `{"username": "<your user>", "password": "<your password>"}`. Copy the token from the response.
3. **Menu API** – `GET http://127.0.0.1:8000/restaurant/menu/` lists the items. To change data, open the **Auth** tab, choose **Bearer Token**, paste the token, then:
   * `POST /restaurant/menu/` with `{"title": "Burger", "price": "75.60", "inventory": 10}` creates an item.
   * `PUT /restaurant/menu/<id>` with the full updated JSON modifies it.
   * `DELETE /restaurant/menu/<id>` removes it. Issue the `GET` again to confirm.
4. **Booking API** – with the Bearer token set, `GET`/`POST` `http://127.0.0.1:8000/restaurant/booking/tables/`.
   Without a token the API answers `401 Unauthorized`.

## Running the tests

```bash
python manage.py test
```

Django creates (and afterwards removes) a temporary `test_LittleLemon` database, so the MySQL user needs permission to create databases (`root` has it). The suite covers the models, the home page, the Menu API (including permissions), the Booking API (CRUD and authentication) and registration / login / logout.

## Publishing the project to GitHub

```bash
git init
git add .
git commit -m "Little Lemon web application"
git branch -M main
git remote add origin https://github.com/<your-user>/LittleLemon.git
git push -u origin main
```

## Notes

* `settings.py` ships with a development-only `SECRET_KEY` and `DEBUG=True`. For any real deployment set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS`.
* Static files are served by Django's development server from the project-level `static/` folder. Run `python manage.py collectstatic` (output goes to `staticfiles/`, which is git-ignored) when deploying.
