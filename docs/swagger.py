from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
app = Flask(__name__)

# Configure Swagger UI
SWAGGER_URL = '/docs'
API_URL = '/schema.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Tesk Task API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix="/")