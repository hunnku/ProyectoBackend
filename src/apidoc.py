from datetime import datetime
from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields, validate

# --- Configuración de la Aplicación ---
app = Flask(__name__)
app.json.ensure_ascii = False

# --- Configuración de Flask-Smorest para Documentación ---
app.config["API_TITLE"] = "API de Tareas y Usuarios (To-Do List)"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# --- Base de Datos en Memoria (Consolidada desde app.py) ---
to_do_list = [
  {"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"},
  {"id": 2, "titulo": "Baño Premium", "estado": "cancelado", "fecha": "2026-03-30 09:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-30 08:00:00"},
  {"id": 3, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-03-30 13:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-27 09:00:00"},
  {"id": 4, "titulo": "Grooming Profesional", "estado": "pendiente", "fecha": "2026-10-30 15:00:00", "id_usuario": 1, "fecha_creacion": "2026-09-28 09:00:00"},
  {"id": 5, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-10-30 12:00:00", "id_usuario": 3, "fecha_creacion": "2026-09-29 09:00:00"}
]
usuarios = [
  {"id": 1, "nombre": "Juan Pérez", "email": "juan.perez@example.com", "estado": "activo"},
  {"id": 2, "nombre": "María García", "email": "maria.garcia@example.com", "estado": "activo"},
  {"id": 3, "nombre": "Carlos López", "email": "carlos.lopez@example.com", "estado": "activo"},
  {"id": 4, "nombre": "Miguel Diaz", "email": "miguel.diaz@example.com", "estado": "inactivo"}
]
titulos_disponibles = ["Baño Estandar", "Baño Premium", "Grooming Profesional"]
estados_permitidos = ["pendiente", "completado", "cancelado"]
estados_usuario_permitidos = ["activo", "inactivo"]

# --- Schemas de Marshmallow para Validación y Serialización ---

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    estado = fields.Str(dump_only=True, description="Estado del usuario, por defecto 'activo' al crear.")

class UserUpdateSchema(Schema):
    nombre = fields.Str()
    email = fields.Email()
    estado = fields.Str(validate=validate.OneOf(estados_usuario_permitidos))

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.OneOf(titulos_disponibles))
    estado = fields.Str(dump_only=True, description="Estado de la tarea, se asigna 'pendiente' automáticamente.")
    fecha = fields.Str(required=True, description="Fecha de ejecución de la tarea (formato: YYYY-MM-DD HH:MM:SS).")
    id_usuario = fields.Int(required=True)
    fecha_creacion = fields.Str(dump_only=True, description="Fecha de creación automática.")

class TaskUpdateSchema(Schema):
    estado = fields.Str(required=True, validate=validate.OneOf(["completado", "cancelado"]))

# --- Blueprint para Tareas ---
blp_tasks = Blueprint("Tareas", "tareas", url_prefix="/api/tareas", description="Operaciones sobre tareas (to-do)")

@blp_tasks.route("/")
class TaskList(MethodView):
    @blp_tasks.response(200, TaskSchema(many=True))
    def get(self):
        """Listar todas las tareas"""
        return to_do_list

    @blp_tasks.arguments(TaskSchema)
    @blp_tasks.response(201, TaskSchema)
    def post(self, task_data):
        """Crear una nueva tarea"""
        if not any(u["id"] == task_data["id_usuario"] for u in usuarios):
            abort(400, message="El 'id_usuario' proporcionado no existe.")
        
        if any(t["fecha"] == task_data["fecha"] for t in to_do_list):
            abort(409, message=f"Conflicto: ya existe una reserva para la fecha {task_data['fecha']}.")

        nuevo_id = max(t["id"] for t in to_do_list) + 1 if to_do_list else 1
        nueva_tarea = {
            "id": nuevo_id,
            "titulo": task_data["titulo"],
            "fecha": task_data["fecha"],
            "id_usuario": task_data["id_usuario"],
            "estado": "pendiente",
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        to_do_list.append(nueva_tarea)
        return nueva_tarea

@blp_tasks.route("/<int:task_id>")
class Task(MethodView):
    @blp_tasks.response(200, TaskSchema)
    def get(self, task_id):
        """Obtener una tarea por su ID"""
        for task in to_do_list:
            if task["id"] == task_id:
                return task
        abort(404, message=f"Tarea con ID {task_id} no encontrada.")

    @blp_tasks.arguments(TaskUpdateSchema)
    @blp_tasks.response(200, TaskSchema)
    def put(self, task_data, task_id):
        """Actualizar el estado de una tarea a 'completado' o 'cancelado'"""
        for task in to_do_list:
            if task["id"] == task_id:
                if task["estado"] != "pendiente":
                    abort(400, message="Solo se pueden actualizar tareas que están en estado 'pendiente'.")
                task["estado"] = task_data["estado"]
                return task
        abort(404, message=f"Tarea con ID {task_id} no encontrada.")
        
    @blp_tasks.response(204)
    def delete(self, task_id):
        """Eliminar una tarea por su ID"""
        global to_do_list
        if not any(t["id"] == task_id for t in to_do_list):
            abort(404, message=f"Tarea con ID {task_id} no encontrada.")
        
        to_do_list = [task for task in to_do_list if task["id"] != task_id]
        return ""

# --- Endpoints de Búsqueda para Tareas ---
@blp_tasks.route("/cliente/<int:user_id>")
class TasksByUser(MethodView):
    @blp_tasks.response(200, TaskSchema(many=True))
    def get(self, user_id):
        """Listar todas las tareas de un usuario específico"""
        tasks = [task for task in to_do_list if task["id_usuario"] == user_id]
        if not tasks:
            abort(404, message=f"No se encontraron tareas para el usuario con ID {user_id}.")
        return tasks

@blp_tasks.route("/estado/<string:estado>")
class TasksByStatus(MethodView):
    @blp_tasks.response(200, TaskSchema(many=True))
    def get(self, estado):
        """Listar tareas por estado (pendiente, completado, cancelado)"""
        if estado not in estados_permitidos:
            abort(400, message=f"Estado no válido. Use uno de: {', '.join(estados_permitidos)}")
        
        tasks = [task for task in to_do_list if task["estado"] == estado]
        if not tasks:
            abort(404, message=f"No se encontraron tareas con el estado '{estado}'.")
        return tasks
        
# --- Blueprint para Usuarios ---
blp_users = Blueprint("Usuarios", "usuarios", url_prefix="/api/usuarios", description="Operaciones sobre usuarios")

@blp_users.route("/")
class UserList(MethodView):
    @blp_users.response(200, UserSchema(many=True))
    def get(self):
        """Listar todos los usuarios"""
        return usuarios

    @blp_users.arguments(UserSchema(only=("nombre", "email")))
    @blp_users.response(201, UserSchema)
    def post(self, user_data):
        """Crear un nuevo usuario"""
        nuevo_id = max(u["id"] for u in usuarios) + 1 if usuarios else 1
        nuevo_usuario = {
            "id": nuevo_id,
            "nombre": user_data["nombre"],
            "email": user_data["email"],
            "estado": "activo"
        }
        usuarios.append(nuevo_usuario)
        return nuevo_usuario

@blp_users.route("/<int:user_id>")
class User(MethodView):
    @blp_users.response(200, UserSchema)
    def get(self, user_id):
        """Obtener un usuario por su ID"""
        for user in usuarios:
            if user["id"] == user_id:
                return user
        abort(404, message=f"Usuario con ID {user_id} no encontrado.")

    @blp_users.arguments(UserUpdateSchema)
    @blp_users.response(200, UserSchema)
    def put(self, user_data, user_id):
        """Actualizar nombre, email o estado de un usuario"""
        for user in usuarios:
            if user["id"] == user_id:
                user.update(user_data)
                return user
        abort(404, message=f"Usuario con ID {user_id} no encontrado.")

# --- Endpoints de Búsqueda para Usuarios ---
@blp_users.route("/nombre/<string:nombre>")
class UserByName(MethodView):
    @blp_users.response(200, UserSchema)
    def get(self, nombre):
        """Buscar un usuario por su nombre (búsqueda exacta, insensible a mayúsculas)"""
        for user in usuarios:
            if user["nombre"].lower() == nombre.lower():
                return user
        abort(404, message=f"Usuario con nombre '{nombre}' no encontrado.")

@blp_users.route("/estado/<string:estado>")
class UsersByStatus(MethodView):
    @blp_users.response(200, UserSchema(many=True))
    def get(self, estado):
        """Listar usuarios por estado (activo, inactivo)"""
        if estado not in estados_usuario_permitidos:
            abort(400, message=f"Estado no válido. Use uno de: {', '.join(estados_usuario_permitidos)}")
            
        users = [user for user in usuarios if user["estado"] == estado]
        if not users:
            abort(404, message=f"No se encontraron usuarios con el estado '{estado}'.")
        return users

# --- Registro de Blueprints en la API ---
api.register_blueprint(blp_tasks)
api.register_blueprint(blp_users)


# --- Ejecución de la aplicación ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)

