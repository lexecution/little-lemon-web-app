LITTLE LEMON - API PATHS TO TEST
================================

Base URL (local development server): http://127.0.0.1:8000
Start the server with:  python manage.py runserver
(See README.md for the full set-up: virtualenv, MySQL, migrations.)

Public paths (no token needed)
------------------------------
1   /restaurant/                      Home page (static HTML served by Django)
2   /restaurant/menu/                 Menu API   - GET list
3   /restaurant/menu/1                Menu API   - GET one item (use any existing id)
4   /auth/users/                      Registration - POST {"username", "email", "password"}
5   /auth/token/login/                Login      - POST {"username", "password"} -> auth_token
6   /restaurant/api-token-auth/       Login (DRF) - POST {"username", "password"} -> token

Token-protected paths
---------------------
Send the token in the header   Authorization: Token <token>
(Insomnia: Auth tab -> "Bearer Token" also works with the same token.)

7   /restaurant/booking/tables/       Table booking API - GET list, POST create
8   /restaurant/booking/tables/1/     Table booking API - GET, PUT, PATCH, DELETE one booking
9   /restaurant/menu/                 Menu API   - POST create a menu item
10  /restaurant/menu/1                Menu API   - PUT / PATCH / DELETE one menu item
11  /auth/users/me/                   Current user - GET
12  /auth/token/logout/               Logout     - POST (invalidates the token)

Admin
-----
13  /admin/                           Django admin (requires a superuser: python manage.py createsuperuser)

Example JSON bodies
-------------------
Register   POST /auth/users/
           {"username": "lex", "email": "lex@example.com", "password": "Str0ng-lemon-pass!"}

Menu item  POST /restaurant/menu/
           {"title": "Greek Salad", "price": "12.50", "inventory": 20}

Booking    POST /restaurant/booking/tables/
           {"name": "Adrian", "no_of_guests": 4, "booking_date": "2026-12-24T19:30:00Z"}

Run the automated tests with:  python manage.py test
