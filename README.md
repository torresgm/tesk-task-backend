Note: before starting, add the OpenAI API key on the `.env` and `.env.local`, as `OPENAI_API_KEY`. (`.env.local` is used in the docker environement)


## Setup DB using Docker:

### • Starts postgres db in docker (runs in the background):
`docker-compose up -d db`

### • Stops postgres db container in docker:
`docker-compose stop db`

## Running using Docker:

### • Build/re-build and start docker containers, and leave it running (setups postgres database and starts the server):
`docker-compose up -d --build`

### • Start docker containers and leave it running (runs postgres database and starts the server):
`docker-compose up -d`

(see [Docker](https://docs.docker.com/) for more references)

## Running locally:

⚠️ make sure postgres db is running (see above on how to run)

### run db migration to latest:
`alembic upgrade head`

### start the server:
`python main.py`

### alternatively, run script to migrate db and start the server:
`bash run.sh`

## Access the API docs:
<http:localhost:8000/docs>

----
## Migrations:

### create migration:
`alembic revision -m [migration_name]`

example: `alembic revision -m Add a column`

### migrate to latest:
`alembic upgrade head`

### rollback to specific migration:
`alembic downgrade [+N]`

example: `alembic downgrade -1`

### view migration history:
`alembic history`

### migrate specific migration:
`alembic upgrade [identifier]`

### rollback specific migration:
`alembic downgrade [identifier]`

(see [Alembic](https://alembic.sqlalchemy.org/en/latest/) for more references)


----

## File/Folder Structure:

```
📦app
 ┣ 📂controllers
 ┣ 📂database
 ┣ 📂responses
 ┣ 📂schemas
 ┣ 📂services
 ┣ 📂tools
📦docs
📦migrations
```

| Directory            |                  Description                    |
|----------------------|:-----------------------------------------------:|
| `app/controllers`    |   Contains controllers - passes the user input, and decides how to output the response   |
| `app/database`       |   Contains gateway between the service and <br> database, the layer that accesses the database and does the operations             |
| `app/responses`      |   Contains HTTP response utils                  |
| `app/schemas`        |   Contains model schemas                        |
| `app/services`       |   Contains services where controller and repository middleware, gathers data from controller, performs   validation <br> and business logic, and calls repositories for database manipulation   |
|   `app/tools`        |   Contains services for external libraries      |
|   `docs`             |   Contains Swagger UI API documentation setup   |
| `migrations`         |   Contains migration files                      |


----

### Docs References: 

- [Docker](https://docs.docker.com/)
- [Starlette](https://www.starlette.io/)
- [Swagger](https://swagger.io/docs/specification/about/)