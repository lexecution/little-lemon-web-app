api paths to test (base url http://127.0.0.1:8000)

public
/restaurant/                    home page
/restaurant/menu/               GET menu list
/restaurant/menu/1              GET one item
/auth/users/                    POST register {"username","email","password"}
/auth/token/login/              POST login, returns auth_token
/restaurant/api-token-auth/     POST login (DRF), returns token

w/ header auth: Token <token>  (Insomnia: Bearer Token also works)
/restaurant/booking/tables/     GET list, POST create
/restaurant/booking/tables/1/   GET, PUT, PATCH, DELETE
/restaurant/menu/               POST create item
/restaurant/menu/1              PUT, PATCH, DELETE
/auth/users/me/                 GET current user
/auth/token/logout/             POST logout

/admin/                         superuser only
