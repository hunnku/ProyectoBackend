import unittest
import json

from src.app import app, usuarios, to_do_list

class TestUsuariosAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        usuarios.clear()
        to_do_list.clear()
    

    def test_crear_usuario_exitoso(self):
        datos_enviados = {
            "nombre": "Mario Mendoza",
            "email": "mario.mendoza@mundo.com"
        }
        
        respuesta = self.app.post('/api/usuarios', 
                                  data=json.dumps(datos_enviados),
                                  content_type='application/json')
        
        datos_respuesta = json.loads(respuesta.data)
        
        if respuesta.status_code != 201:
            print(f"Error devuelto en la api: \n {respuesta}")
        
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(datos_respuesta['nombre'], "Mario Mendoza")
        self.assertEqual(datos_respuesta['estado'], "activo")

    def test_crear_usuario_falta_email(self):
        datos_enviados = {
            "nombre": "Laura Gomez"
            # Falta el email
        }
        
        respuesta = self.app.post('/api/usuarios', 
                                  data=json.dumps(datos_enviados),
                                  content_type='application/json')
        
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(len(usuarios), 0)

    def test_crear_nueva_tarea(self):
        usuarios.append({"id": 1, "nombre": "Miguel", "email": "miguel@test.com"})
        datos_nueva_tarea = {
            "fecha": "2026-10-29 12:00:00",
            "id_usuario": 1,
            "titulo": "Grooming Profesional"
        }
        
        respuesta_tarea = self.app.post('/api/to_do_creacion',
                                  data=json.dumps(datos_nueva_tarea),
                                  content_type='application/json')
        
        datos_respuesta_tarea = json.loads(respuesta_tarea.data)

        if respuesta_tarea.status_code != 201:
            print(f"Error devuelto en la api: \n {datos_respuesta_tarea}")        
        self.assertEqual(respuesta_tarea.status_code, 201)
        self.assertEqual(datos_respuesta_tarea['titulo'], "Grooming Profesional")
        self.assertEqual(datos_respuesta_tarea['id_usuario'], 1)

    def test_obtener_todas_las_tareas(self):
        to_do_list.extend([
            {"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"},
            {"id": 2, "titulo": "Baño Premium", "estado": "cancelado", "fecha": "2026-03-30 09:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-30 08:00:00"},
            {"id": 3, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-03-30 13:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-27 09:00:00"},
            {"id": 4, "titulo": "Grooming Profesional", "estado": "pendiente", "fecha": "2026-10-30 15:00:00", "id_usuario": 1, "fecha_creacion": "2026-09-28 09:00:00"},
            {"id": 5, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-10-30 12:00:00", "id_usuario": 3, "fecha_creacion": "2026-09-29 09:00:00"}
        ])
        
        respuesta = self.app.get('/api/to_do')
        
        if respuesta.status_code != 200:
            print(f"Error devuelto en la api: \n {respuesta}") 
        self.assertEqual(respuesta.status_code, 200)
        datos_respuesta = respuesta.get_json()
        self.assertEqual(len(datos_respuesta), 5)
           
    def test_obtener_tarea_por_id(self):
        to_do_list.extend([
            {"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"},
            {"id": 2, "titulo": "Baño Premium", "estado": "cancelado", "fecha": "2026-03-30 09:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-30 08:00:00"},
            {"id": 3, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-03-30 13:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-27 09:00:00"},
            {"id": 4, "titulo": "Grooming Profesional", "estado": "pendiente", "fecha": "2026-10-30 15:00:00", "id_usuario": 1, "fecha_creacion": "2026-09-28 09:00:00"},
            {"id": 5, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-10-30 12:00:00", "id_usuario": 3, "fecha_creacion": "2026-09-29 09:00:00"}
        ])
        
        llaves_esperadas = ['estado', 'fecha', 'fecha_creacion', 'id', 'id_usuario', 'titulo']
        
        respuesta = self.app.get('/api/to_do/id/3')
        json_respuesta = json.loads(respuesta.data) 
        llaves_json_respuesta = respuesta.get_json()
        
        if respuesta.status_code != 200:
            print(f"Error devuelto en la api: \n {json_respuesta}")   
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(json_respuesta['id'], 3)
        self.assertCountEqual(llaves_json_respuesta.keys(), llaves_esperadas)

    def test_tarea_por_id_inexistente(self):
        to_do_list.extend([
            {"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"},
            {"id": 2, "titulo": "Baño Premium", "estado": "cancelado", "fecha": "2026-03-30 09:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-30 08:00:00"},
        ])

        respuesta = self.app.get('/api/to_do/id/3')
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 404)
        self.assertEqual(json_respuesta['error'], "id: 3 no esta registrado")

    def test_crear_tarea_con_usuario_inexistente(self):
        usuarios.append({"id": 1,"nombre": "Juan Pérez","email": "juan.perez@example.com","estado": "activo"})
        
        datos_nueva_tarea = {
            "fecha": "2026-10-29 12:00:00",
            "id_usuario": 100,
            "titulo": "Grooming Profesional"
        }

        respuesta = self.app.post('/api/to_do_creacion',
                                  data=json.dumps(datos_nueva_tarea),
                                  content_type='application/json')
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(json_respuesta['error'], "El usuario no existe")
           
    def test_actualizar_estado_tarea(self):
        to_do_list.append({"id": 4, "titulo": "Grooming Profesional", "estado": "pendiente", "fecha": "2026-10-30 15:00:00", "id_usuario": 1, "fecha_creacion": "2026-09-28 09:00:00"})  

        cuerpo = {"estado": "completado"}
        
        respuesta = self.app.put('/api/actualizar_tarea/4',
                                 data=json.dumps(cuerpo),
                                 content_type='application/json')

        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(json_respuesta['mensaje'], "Estado actualizado correctamente")

    def test_actualizar_estado_tarea_cancelado(self):
        to_do_list.append({"id": 2, "titulo": "Baño Premium", "estado": "cancelado", "fecha": "2026-03-30 09:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-30 08:00:00"})  

        cuerpo = {"estado": "completado"}
        
        respuesta = self.app.put('/api/actualizar_tarea/2',
                                 data=json.dumps(cuerpo),
                                 content_type='application/json')

        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(json_respuesta['error'], "Solo se pueden actualizar las tareas en estado pendiente")
       
    def test_eliminar_tarea_existente(self):
        to_do_list.append({"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"})
        
        respuesta = self.app.delete('/api/eliminar_tarea/1')
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(json_respuesta['mensaje'], "Tarea 1 eliminada correctamente")
        
    def test_lista_tareas_usuario(self):
        to_do_list.append({"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"})
        
        respuesta = self.app.get('/api/to_do/cliente/1')  
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(json_respuesta['id_usuario'], 1)
        
    def test_lista_tareas_usuario_error(self):
        to_do_list.append({"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"})
        
        respuesta = self.app.get('/api/to_do/cliente/2')  
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 404)
        self.assertEqual(json_respuesta['error'], "Usuario 2 no encontrado")   
        
    def test_lista_tarea_titulo(self):
        to_do_list.append({"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"})
        
        respuesta = self.app.get('/api/to_do/titulo/Baño Premium')
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(json_respuesta['titulo'], "Baño Premium")                    
        
    def test_lista_tarea_titulo_error(self):
        to_do_list.append({"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"})
        
        respuesta = self.app.get('/api/to_do/titulo/Baño Perro')
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 404)
        self.assertEqual(json_respuesta['error'], "Tarea Baño Perro no encontrada")           

    def test_lista_tarea_estado(self):
        to_do_list.append({"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"})
                
        respuesta = self.app.get('/api/to_do/estado/pendiente')
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(json_respuesta['estado'], "pendiente")  


    def test_listado_usuario(self):
        to_do_list.extend([
            {"id": 1, "titulo": "Baño Premium", "estado": "pendiente", "fecha": "2026-03-30 10:00:00", "id_usuario": 1, "fecha_creacion": "2026-03-25 09:00:00"},
            {"id": 2, "titulo": "Baño Premium", "estado": "cancelado", "fecha": "2026-03-30 09:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-30 08:00:00"},
            {"id": 3, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-03-30 13:00:00", "id_usuario": 2, "fecha_creacion": "2026-03-27 09:00:00"},
            {"id": 4, "titulo": "Grooming Profesional", "estado": "pendiente", "fecha": "2026-10-30 15:00:00", "id_usuario": 1, "fecha_creacion": "2026-09-28 09:00:00"},
            {"id": 5, "titulo": "Grooming Profesional", "estado": "completado", "fecha": "2026-10-30 12:00:00", "id_usuario": 3, "fecha_creacion": "2026-09-29 09:00:00"}
        ])
        
        respuesta = self.app.get('/api/usuario_id/1')
        
        json_respuesta = json.loads(respuesta.data)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(json_respuesta['id'], 1)  

if __name__ == '__main__':
    unittest.main()