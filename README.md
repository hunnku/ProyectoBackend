# Documentación de la API

Este documento describe los endpoints disponibles en la API de Tareas y Usuarios.

## Cómo ejecutar la aplicación

1.  Asegúrate de tener todas las dependencias instaladas:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ejecuta el servidor de desarrollo de Flask:
    ```bash
    python src/app.py
    ```
3.  La API estará disponible en `http://127.0.0.1:5000`.

---

## Endpoints de Tareas (`to-do`)

La URL base para estos endpoints es `http://127.0.0.1:5000`.

### GET

-   **Listar todas las tareas**
    ```http
    GET /api/to_do
    ```
-   **Obtener tarea por ID**
    ```http
    GET /api/to_do/id/<int:id>
    ```
-   **Obtener tareas por ID de usuario**
    ```http
    GET /api/to_do/cliente/<int:id_usuario>
    ```
-   **Obtener tarea por título**
    ```http
    GET /api/to_do/titulo/<string:titulo>
    ```
-   **Obtener tarea por estado**
    ```http
    GET /api/to_do/estado/<string:estado>
    ```
-   **Obtener tarea por fecha de ejecución (YYYY-MM-DD)**
    ```http
    GET /api/to_do/fecha/<string:fecha>
    ```
-   **Obtener tarea por fecha de creación (YYYY-MM-DD)**
    ```http
    GET /api/to_do/fecha_creacion/<string:fecha_creacion>
    ```

### POST

-   **Crear una nueva tarea**
    ```http
    POST /api/to_do_creacion
    ```
    **Cuerpo (Body) de ejemplo:**
    ```json
    {
      "titulo": "Baño Premium",
      "fecha": "2026-04-15 11:00:00",
      "id_usuario": 1
    }
    ```

### PUT

-   **Actualizar el estado de una tarea**
    ```http
    PUT /api/actualizar_tarea/<int:id>
    ```
    **Cuerpo (Body) de ejemplo:**
    ```json
    {
      "estado": "completado"
    }
    ```

### DELETE

-   **Eliminar una tarea**
    ```http
    DELETE /api/eliminar_tarea/<int:id>
    ```

---

## Endpoints de Usuarios

### GET

-   **Listar todos los usuarios**
    ```http
    GET /api/usuarios
    ```
-   **Obtener usuario por ID**
    ```http
    GET /api/usuario_id/<int:id>
    ```
-   **Obtener usuario por nombre**
    ```http
    GET /api/usuario_nombre/<string:nombre>
    ```
-   **Obtener usuarios por estado**
    ```http
    GET /api/usuario_estado/<string:estado>
    ```

### POST

-   **Crear un nuevo usuario**
    ```http
    POST /api/usuarios
    ```
    **Cuerpo (Body) de ejemplo:**
    ```json
    {
      "nombre": "Nuevo Usuario",
      "email": "nuevo.usuario@example.com"
    }
    ```

### PUT

-   **Actualizar un usuario**
    ```http
    PUT /api/usuarios/<int:id>
    ```
    **Cuerpo (Body) de ejemplo:**
    ```json
    {
      "nombre": "Nombre Actualizado",
      "email": "email.actualizado@example.com",
      "estado": "inactivo"
    }
    ```
