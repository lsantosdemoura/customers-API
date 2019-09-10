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

```
$ python manage.py createsuperuser --username test --email test@example.com
$ python manage.py drf_create_token test
Generated token 634688774ca38570ceed5e552a697617031ddab3 for user test
$ curl http://127.0.0.1:8000/api/customers -H 'Authorization: Token 634688774ca38570ceed5e552a697617031ddab3'
```
Or with httpie
```
http post http://127.0.0.1:8000/api-token-auth/ username=test password=test123

```
