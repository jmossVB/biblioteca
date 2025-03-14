# biblioteca
Ejercicio: Documentación de un Proyecto con Tkinter, Python y PostgreSQL

📌 Descripción del Proyecto:
Deben desarrollar una aplicación de escritorio en Python utilizando Tkinter para la interfaz gráfica y PostgreSQL como base de datos. La aplicación será un sistema de gestión de biblioteca, donde los usuarios podrán registrar, buscar, actualizar y eliminar libros.

📌 Estructura del Proyecto:
El proyecto debe estar organizado en varios archivos de Python, siguiendo la estructura:

biblioteca/
│── app.py              # Archivo principal que inicia la aplicación
│── interfaz.py         # Módulo que contiene las ventanas de Tkinter ok
│── base_datos.py       # Módulo para manejar la conexión y consultas a PostgreSQL ok 
│── operaciones.py      # Módulo con funciones CRUD (Crear, Leer, Actualizar, Eliminar) ok
│── config.py           # Archivo para las configuraciones (credenciales de la BD, etc.) ok
│── README.md           # Explicación del proyecto
│── docs/
│   ├── index.html      # Documentación generada con pydoc
│   ├── base_datos.txt  # Documentación de la conexión con PostgreSQL (manual)
└── requirements.txt    # Librerías necesarias (psycopg2, tkinter, etc.) OPCIONAL

📌 Lo que deben hacer:
1️⃣ Crear la aplicación siguiendo la estructura indicada.
2️⃣ Desarrollar las funciones CRUD para gestionar libros en PostgreSQL.
3️⃣ Construir una interfaz con Tkinter que permita a los usuarios interactuar con el sistema.
4️⃣ Agregar comentarios y docstrings en cada archivo de Python explicando las funciones.
5️⃣ Generar documentación con pydoc y almacenarla en la carpeta docs/.

📌 ¿Qué deben documentar?

Explicación detallada de cada módulo y su función dentro del proyecto.
Uso de pydoc para generar documentación en HTML.

📌 Campos para el Formulario de Registro de Libros:
1️⃣ Título del libro 📖 (Texto, obligatorio)
2️⃣ Autor ✍️ (Texto, obligatorio)
3️⃣ Género 📚 (Desplegable con opciones: novela, ciencia ficción, historia, etc.)
4️⃣ Año de publicación 📅 (Número, obligatorio)
5️⃣ ISBN 🔢 (Número único, obligatorio, validado con longitud específica)
6️⃣ Editorial 🏢 (Texto, opcional)
7️⃣ Cantidad de ejemplares 📦 (Número, obligatorio, mínimo 1)

📌 Campos para la Búsqueda y Gestión:
8️⃣ Campo de búsqueda 🔍 (Permitir buscar por título, autor o ISBN)
9️⃣ Botón "Actualizar" 🔄 (Modificar datos de un libro seleccionado)
🔟 Botón "Eliminar" ❌ (Eliminar un libro de la base de datos con confirmación previa)

📌 Datos Adicionales (Opcionales):
Ubicación en la biblioteca 🏠 (Ejemplo: "Estante A-3")
Estado del libro 🏷️ (Nuevo, Usado, Dañado, etc.)
Fecha de adquisición 🗓️ (Para saber desde cuándo está en la biblioteca)

py -m pydoc -w app
python -m pydoc app







