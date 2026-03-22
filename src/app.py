from datetime import datetime
from flask import Flask, jsonify, request, render_template
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields


app = Flask(__name__)

# Desactivar JSON_AS_ASCII
app.json.ensure_ascii = False

to_do_list = [
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

titulos_disponibles = [
  {
    "id": 1,
    "titulo": "Baño Estandar"
  },
  {
    "id": 2,
    "titulo": "Baño Premium"
  },
  {
    "id": 3,
    "titulo": "Grooming Profesional"
  }
]

listado_estados = [
  {
    "id": 1,
    "estado": "pendiente"
  },
  {
    "id": 2,
    "estado": "completado"
  },
  {
    "id": 3,
    "estado": "cancelado"
  }
]


#################################################################
#           Metodos GET para la lista de tareas                 #
#################################################################

# Metodo GET para obtener el listado de to do
@app.route('/api/to_do', methods=['GET'])
def to_do():
    return jsonify(to_do_list), 200

# Extra el listado de tareas por usuario
@app.route('/api/to_do/cliente/<int:id_usuario>', methods=['GET']) # 'int' en minúsculas
def get_to_do(id_usuario):
    for usuario in to_do_list:
        if usuario['id_usuario'] == id_usuario:
            # Devolvemos el diccionario 'usuario', no solo el ID
            return jsonify(usuario), 200
    return jsonify({"error": f"Usuario {id_usuario} no encontrado"}), 404

# Extrae el listado de tareas por titulo 
@app.route('/api/to_do/titulo/<string:titulo>', methods=['GET'])
def get_to_do_by_titulo(titulo):
    for tarea in to_do_list:
        if tarea['titulo'] == titulo:
            return jsonify(tarea), 200
    return jsonify({"error": f"Tarea {titulo} no encontrada"}), 404

# Extrae el listado de tareas por estado
@app.route('/api/to_do/estado/<string:estado>', methods=['GET'])
def get_to_do_by_estado(estado):
    for estados in to_do_list:
        if estados['estado'] == estado:
            return jsonify(estados), 200
    return jsonify({"error": f"Estado {estado} no encontrada"}), 404

# Extrae el listado de tareas por fecha de ejecucion
@app.route('/api/to_do/fecha/<string:fecha>', methods=['GET'])
def get_to_do_by_fecha(fecha):
    for registro in to_do_list:
      fecha_en_lista = registro['fecha'][0:10]
      if fecha_en_lista == fecha:
        return jsonify(registro), 200
    return jsonify({"error": f"Fecha {fecha} no encontrada"}), 404

# Extrae el listado de tareas por fecha de creacion
@app.route('/api/to_do/fecha_creacion/<string:fecha_creacion>', methods=['GET'])
def get_to_do_by_fecha_creacion(fecha_creacion):
    for registro in to_do_list:
      fecha_en_lista = registro['fecha_creacion'][0:10]
      if fecha_en_lista == fecha_creacion:
        return jsonify(registro), 200
    return jsonify({"error": f"Fecha de creacion {fecha_creacion} no encontrada"}), 404

# Extrae la tarea por id de creacion
@app.route('/api/to_do/id/<int:id>', methods=['GET'])
def get_to_do_id(id):
  for i in to_do_list:
    if i['id'] == id:
      return jsonify(i), 200
  return jsonify({"error": f"id: {id} no esta registrado"}), 404

#################################################################
#           Metodos POST para la lista de tareas                #
#################################################################

@app.route('/api/to_do_creacion', methods=['POST'])
def creacion_tarea():
    nuevo_registro = request.get_json()
    
    usuario_existe = any(u.get('id') == nuevo_registro.get('id_usuario') for u in usuarios)
    if not usuario_existe:
        return jsonify({"error": "El usuario no existe"}), 400

    titulo_ingresado = nuevo_registro.get('titulo')
    
    titulo_es_valido = any(i.get('titulo') == titulo_ingresado for i in titulos_disponibles)
    
    if not titulo_es_valido:
        return jsonify({"error": "Título no válido"}), 400

    nuevo_registro['estado'] = "pendiente"
    nuevo_registro['fecha_creacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    nuevo_id = len(to_do_list) + 1
    nuevo_registro['id'] = nuevo_id
    
    to_do_list.append(nuevo_registro)
    
    return jsonify(nuevo_registro), 201
        
        
#################################################################
#           Metodos PUT para la lista de tareas                 #
#################################################################       
        
# Put para actualizar el estado de la tarea
@app.route('/api/actualizar_tarea/<int:id>', methods=['PUT'])
def actualiza_estado(id):
    datos_cliente = request.get_json()
    
    if not datos_cliente or 'estado' not in datos_cliente:
        return jsonify({"error": "Debes enviar el campo 'estado' en el JSON"}), 400
        
    nuevo_estado = datos_cliente.get('estado').lower()
    estados_permitidos = ['cancelado', 'completado']
    
    if nuevo_estado not in estados_permitidos:
        return jsonify({"error": f"Estado inválido. Desde pendiente solo puedes pasar a: {estados_permitidos}"}), 400
    
    for tarea in to_do_list:
        if tarea.get('id') == id:
            if tarea.get('estado') != 'pendiente':
                return jsonify({"error": "Solo se pueden actualizar las tareas en estado pendiente"}), 400
                
            tarea["estado"] = nuevo_estado
            
            return jsonify({
                "mensaje": "Estado actualizado correctamente", 
                "tarea": tarea
            }), 200
            
    return jsonify({"error": f"No se encontró ninguna tarea con el ID {id}"}), 404
        
        
        
        
        
        
        
        
        
        
        
           
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    return jsonify(usuarios), 200


@app.route('/registro_to_do')
def registro_to_do():
    return "<p>Registro de baño</p>"

@app.route('/registro_usuario')
def registro_usuario():
    return "<p>Registro de usuario</p>"



if __name__ == '__main__':
    app.run(debug=True)