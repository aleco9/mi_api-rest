# API Usuarios

API REST para administrar usuarios desarrollada con Flask y Postgres.

## Instrucciones para levantar la API

1. Clona este repositorio.
2. Instala las dependencias usando `pip install -r requirements.txt`.
3. Configura la base de datos Postgres y ejecuta los scripts SQL para crear la tabla y (opcionalmente) inicializar con datos.
4. Ejecuta la API con `python app.py`.
5. La API estará disponible en `http://localhost:5000`.

## Endpoints

- POST `/usuarios`: Crea un nuevo usuario.
- GET `/usuarios`: Lista todos los usuarios.
- GET `/usuarios/:id_usuario`: Obtiene detalles de un usuario específico.
- PUT `/usuarios/:id_usuario`: Actualiza un usuario.
- DELETE `/usuarios/:id_usuario`: Elimina un usuario.
- GET `/usuarios/promedio-edad`: Devuelve el promedio de edad de los usuarios.
- GET `/estado`: Muestra el estado y versión de la API.
