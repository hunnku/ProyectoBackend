from flask import Flask, jsonify, request


app = Flask(__name__)

to_do = [
  {
    "id": 1,
    "titulo": "Baño Premium",
    "estado": "pendiente",
    "fecha": "2026-03-30 10:00:00",
    "id_usuario": 1,
    "fecha_creacion": "2026-03-25 09:00:00" 
  },
  {
    "id": 2,
    "titulo": "Baño Premium",
    "estado": "cancelado",
    "fecha": "2026-03-30 09:00:00",
    "id_usuario": 2,
    "fecha_creacion": "2026-03-30 08:00:00"
  },
  {
    "id": 3,
    "titulo": "Grooming Profesional",
    "estado": "completado",
    "fecha": "2026-03-30 13:00:00",
    "id_usuario": 2,
    "fecha_creacion": "2026-03-27 09:00:00"
  },
  {
    "id": 4,
    "titulo": "Grooming Profesional",
    "estado": "pendiente",
    "fecha": "2026-10-30 15:00:00",
    "id_usuario": 1,
    "fecha_creacion": "2026-09-28 09:00:00"
  },
  {
    "id": 5,
    "titulo": "Grooming Profesional",
    "estado": "completado",
    "fecha": "2026-10-30 12:00:00",
    "id_usuario": 3,
    "fecha_creacion": "2026-09-29 09:00:00"
  }
]

usuarios = [
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan.perez@example.com"
  },
  {
    "id": 2,
    "nombre": "María García",
    "email": "maria.garcia@example.com"
  },
  {
    "id": 3,
    "nombre": "Carlos López",
    "email": "carlos.lopez@example.com"
  }
]


@app.route('/registro_to_do')
def registro_to_do():
    return "<p>Registro de baño</p>"

@app.route('/registro_usuario')
def registro_usuario():
    return "<p>Registro de usuario</p>"

@app.route('/to_do')
def to_do():
    return "<p>Listado de to do</p>"


if __name__ == '__main__':
    app.run(debug=True)