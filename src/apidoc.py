from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields

app = Flask(__name__)

# Configuración de Swagger UI
app.config["API_TITLE"] = "Library API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# 1. Definimos el Esquema (lo que Swagger usará para la documentación)
class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)

# 2. Creamos un Blueprint (Organización)
blp = Blueprint("books", __name__, description="Operaciones con libros")

# Datos en memoria (Simulación de DB)
books = []

@blp.route("/book")
class Books(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        """Lista todos los libros"""
        return books

    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, new_data):
        """Agrega un nuevo libro"""
        new_data["id"] = len(books) + 1
        books.append(new_data)
        return new_data

api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)