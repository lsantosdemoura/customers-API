# Customers API
API for creating, reading, updating and deleting customers and their favorite products

---
## REQUIREMENTS
- [docker-compose](https://docs.docker.com/compose/install/)

---

## USAGE
### Run the project
```
$ git clone https://github.com/lsantosdemoura/customers-API.git
$ cd customers-API
# You can build and start docker at once
$ docker-compose up --build
```
#### You can access all images' bashes:
- The project itself: ``` $ docker-compose exec web bash ```
- Postgres:  ``` $ docker-compose exec db bash ```
### Run tests
```
$ cd customers-API
$ docker-compose -f test.yml build
$ docker-compose -f test.yml run test_api
```
### You need to create an authentication token
```
$ python manage.py createsuperuser --username test --email test@example.com
$ python manage.py drf_create_token test
Generated token 9c474c3d334a6b073b62cc76622a60fb4d19464f for user test
$ http http://localhost:8000/api/favorites/ 'Authorization: Token 9c474c3d334a6b073b62cc76622a60fb4d19464f'
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 522
Content-Type: application/json
Date: Tue, 10 Sep 2019 16:13:28 GMT
Server: WSGIServer/0.2 CPython/3.7.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "customer": "test@test.com",
        "product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
        "url": "http://localhost:8000/api/favorites/1/"
    },
    {
        "customer": "test@test.com",
        "product_id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f",
        "url": "http://localhost:8000/api/favorites/2/"
    },
    {
        "customer": "test@test.com",
        "product_id": "f6c094e1-f27d-677b-4187-cf6a5acd03aa",
        "url": "http://localhost:8000/api/favorites/3/"
    },
    {
        "customer": "test2@test.com",
        "product_id": "f6c094e1-f27d-677b-4187-cf6a5acd03aa",
        "url": "http://localhost:8000/api/favorites/7/"
    }
]
```
### Without authentication
```
$ http http://localhost:8000/api/favorites/
HTTP/1.1 401 Unauthorized
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 58
Content-Type: application/json
Date: Tue, 10 Sep 2019 16:14:44 GMT
Server: WSGIServer/0.2 CPython/3.7.4
Vary: Accept, Cookie
WWW-Authenticate: Basic realm="api"
X-Frame-Options: SAMEORIGIN

{
    "detail": "Authentication credentials were not provided."
}

```

### You can also make a request on this endpoint to get your token
```
http post http://127.0.0.1:8000/api-token-auth/ username=test password=test123
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Date: Tue, 10 Sep 2019 16:17:25 GMT
Server: WSGIServer/0.2 CPython/3.7.4
Vary: Cookie
X-Frame-Options: SAMEORIGIN

{
    "token": "9c474c3d334a6b073b62cc76622a60fb4d19464f"
}

```
### You can create a Customer
```
http post http://127.0.0.1:8000/customers/ name:='"test5"' email:='"test5@test.com"' 'Authorization: Token 9c474c3d334a6b073b62cc76622a60fb4d19464f'

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 90
Content-Type: application/json
Date: Tue, 10 Sep 2019 16:26:00 GMT
Server: WSGIServer/0.2 CPython/3.7.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "email": "test5@test.com",
    "name": "test5",
    "url": "http://127.0.0.1:8000/api/customers/8/"
}

```
You can also delete, list, and patch a Customer


### You can create a Favorite list sending a product id
```
http post http://127.0.0.1:8000/favorites/ customer_email:='"test12@test.com"' product_id:='"f8cb4a82-910e-6654-1240-d994c2997d2c"' 'Authorization: Token 9c474c3d334a6b073b62cc76622a60fb4d19464f'

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 129
Content-Type: application/json
Date: Tue, 10 Sep 2019 16:31:06 GMT
Server: WSGIServer/0.2 CPython/3.7.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "customer": "test5@test.com",
    "product_id": "f8cb4a82-910e-6654-1240-d994c2997d2c",
    "url": "http://127.0.0.1:8000/api/favorites/9/"
}
```


### And you can get the details from a customer
```
http http://127.0.0.1:8000/api/customers/8/ 'Authorization: Token 9c474c3d334a6b073b62cc76622a60fb4d19464f'

HTTP/1.1 200 OK
Allow: GET, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 627
Content-Type: application/json
Date: Tue, 10 Sep 2019 16:32:33 GMT
Server: WSGIServer/0.2 CPython/3.7.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "email": "test5@test.com",
    "favorites": [
        {
            "image": "http://challenge-api.luizalabs.com/images/f8cb4a82-910e-6654-1240-d994c2997d2c.jpg",
            "price": 667.8,
            "product_id": "f8cb4a82-910e-6654-1240-d994c2997d2c",
            "reviewScore": null,
            "title": "Cadeira para Auto Burigotto Matrix p/ Crianças",
            "url": "http://127.0.0.1:8000/api/favorites/8/"
        },
    ],
    "name": "test5"
}

```
