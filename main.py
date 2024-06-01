import uvicorn
import contextlib
import logging
import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from starlette.applications import Starlette
from starlette_apispec import APISpecSchemaGenerator
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Route, Mount
from starlette.config import Config
from app.database.manager import DatabaseManager
from app.controllers import ArticlesController
from app.schemas import ArticleSchema, ResponseSchema
from app.tools.openai_service import OpenAIService
from app.responses.errors import not_found, bad_request
import docs.swagger as swagger

config = Config(".env")

ENV = os.environ.get("PYTHON_ENV")
PG_DB = config("PG_DB")
HOST = config("APP_HOST")
PORT = config("APP_PORT", cast=int)
PG_HOST = config("PG_HOST")
PG_PORT = config("PG_PORT", cast=int)
# PG_SERVICE_NAME = f"{PG_HOST}:{PG_PORT}" if ENV=="development" else config("PG_SERVICE_NAME")
PG_SERVICE_NAME = config("PG_SERVICE_NAME")
PG_USERNAME = config("PG_USERNAME")
PG_PASSWORD = config("PG_PASSWORD")
PG_DB = config("PG_DB")
DATABASE_URL = f"postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_SERVICE_NAME}/{PG_DB}"

logger = logging.getLogger(__name__)

# Initialize OpenAI service
openai_service = OpenAIService(logger)

# Setup database
dbManager = DatabaseManager(DATABASE_URL)
db = dbManager.database


@contextlib.asynccontextmanager
async def lifespan(app):
    await db.connect()
    yield
    await db.disconnect()


middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

# Setup OpenAPI specs and schemas
spec = APISpec(
    title="Test Task API",
    version="1.0",
    openapi_version="3.0.0",
    info={"description": "Test Task API Documention"},
    plugins=[MarshmallowPlugin()],
)


spec.components.schema('Article', schema=ArticleSchema)
spec.components.schema('ResponseDetails', schema=ResponseSchema)
schemas = APISpecSchemaGenerator(spec)


def schema(request):
    return schemas.OpenAPIResponse(request=request)


# Setup error handlers
exception_handlers = {
    404: not_found,
    400: bad_request,
    # 500: server_error
}

# Initialize controllers and setup routes
routes = []
for controller in [ArticlesController]:
    controller_routes = controller(
        logger, dbManager, openai_service).init_routes()

    for path, method, handler in controller_routes:
        routes.append(Route(path, endpoint=handler, methods=[method]))

routes.append(Route('/schema.yaml', endpoint=schema, include_in_schema=False))
routes.append(Mount('/docs', app=WSGIMiddleware(swagger.app)))


app = Starlette(middleware=middleware, routes=routes, lifespan=lifespan, exception_handlers=exception_handlers)

if __name__ == "__main__":
    reload = ENV=="development"
    uvicorn.run("main:app", host=HOST, port=PORT, reload=reload)