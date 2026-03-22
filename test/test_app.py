import unittest
import json

from src.app import app, usuarios, to_do_list

class TestUsuariosAPI(unittest.TestCase):
    
    # El método setUp se ejecuta ANTES de cada prueba
    def setUp(self):
        # Creamos un cliente de pruebas para simular peticiones (como Postman pero en código)
        self.app = app.test_client()
        self.app.testing = True
        
        usuarios.clear()

    def test_crear_usuario_exitoso(self):
        # 1. Preparamos los datos (El Body del POST)
        datos_enviados = {
            "nombre": "Mario Mendoza",
            "email": "mario.mendoza@mundo.com"
        }
        
        # 2. Ejecutamos la acción (Hacemos el POST simulado)
        respuesta = self.app.post('/api/usuarios', 
                                  data=json.dumps(datos_enviados),
                                  content_type='application/json')
        
        # Convertimos la respuesta de JSON a diccionario de Python
        datos_respuesta = json.loads(respuesta.data)
        
        # 3. Validaciones (Asserts): Aquí comprobamos si el código hizo su trabajo
        
        # Validamos que el código HTTP sea 201 (Creado)
        self.assertEqual(respuesta.status_code, 201)
        
        # Validamos que el nombre sea el que enviamos
        self.assertEqual(datos_respuesta['nombre'], "Mario Mendoza")
        
        # Validamos tu regla de negocio: ¿Se forzó el estado a 'activo'?
        self.assertEqual(datos_respuesta['estado'], "activo")
        
        # Validamos que la lista 'usuarios' ahora tenga 1 elemento
        self.assertEqual(len(usuarios), 1)


    def test_crear_usuario_falta_email(self):
        # 1. Preparamos datos INCOMPLETOS a propósito
        datos_enviados = {
            "nombre": "Laura Gomez"
            # Falta el email
        }
        
        # 2. Ejecutamos la acción
        respuesta = self.app.post('/api/usuarios', 
                                  data=json.dumps(datos_enviados),
                                  content_type='application/json')
        
        # 3. Validaciones
        # Validamos que la API rechace la petición con un error 400 (Bad Request)
        self.assertEqual(respuesta.status_code, 400)
        
        # Validamos que la lista siga vacía (no se guardó nada por el error)
        self.assertEqual(len(usuarios), 0)

if __name__ == '__main__':
    unittest.main()