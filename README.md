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
- Celery: ``` $ docker-compose exec celery bash ```
- Rabbitmq: ``` $ docker-compose exec rabbit bash ```
- Postgres:  ``` $ docker-compose exec db bash ```
### Run tests
```
$ cd customers-API
$ docker-compose -f test.yml build
$ docker-compose -f test.yml run test_api
```

