# Módulo con funciones CRUD (Crear, Leer, Actualizar, Eliminar)
import psycopg2
from base_datos import ConexionBD
import logging

conn = ConexionBD()

def leer_libro_por_id(conn, ncodlib):
    """
    Obtiene los detalles de un libro por su ID.

    Parámetros:
    - conn: objeto de conexión a la base de datos.
    - ncodlib: ID del libro a buscar.

    Retorna:
    - Un diccionario con los detalles del libro si existe, o None si no se encuentra.
    """
    conexion = conn.get_conexion()
    if not conexion:
        logging.error("No se pudo obtener la conexión a la base de datos.")
        return None

    try:
        with conexion.cursor() as cur:
            cur.execute(
                """ SELECT ncodlib, ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje 
                    FROM libros WHERE ncodlib = %s""",
                (ncodlib,)
            )
            libro = cur.fetchone()

        if libro:
            return {
                "ncodlib": libro[0],
                "ctitlib": libro[1],
                "cautlib": libro[2],
                "cgenlib": libro[3],
                "nanopublib": libro[4],
                "ccodisbn": libro[5].strip(),  # Eliminamos espacios en ISBN si existen
                "cedilib": libro[6] if libro[6] else "",
                "ncaneje": libro[7]
            }
        else:
            logging.warning(f"No se encontró ningún libro con ID {ncodlib}")
            return None
    except Exception as e:
        logging.error(f"Error al obtener libro por ID: {e}")
        return None

def existe_libro_por_isbn(conn, ccodisbn):
    """
    Verifica si un libro con el mismo ISBN ya existe en la base de datos.

    Parámetros:
    - conn: conexión a la base de datos
    - ccodisbn: código ISBN a verificar

    Retorna:
    - True si el libro ya existe, False si no.
    """
    conexion = conn.get_conexion()
    if not conexion:
        logging.error("No se pudo obtener la conexión a la base de datos.")
        return False  # No podemos verificar, asumimos que no existe

    try:
        with conexion.cursor() as cur:
            cur.execute("SELECT 1 FROM libros WHERE ccodisbn = %s", (ccodisbn,))
            return cur.fetchone() is not None  # Si hay resultado, el ISBN ya existe
    except Exception as e:
        logging.error(f"Error al verificar ISBN: {e}")
        return False  # Si hay error, asumimos que no existe

# Función para crear un nuevo libro en la base de datos
def crear_libro(conn, ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje):
    """
    Inserta un nuevo libro en la base de datos.

    Parámetros:
    - conn: objeto de conexión a la base de datos.
    - ctitlib: Título del libro.
    - cautlib: Autor del libro.
    - cgenlib: Género del libro.
    - nanopublib: Año de publicación del libro.
    - ccodisbn: ISBN del libro (debe tener 13 caracteres).
    - cedilib: Editorial del libro (opcional).
    - ncaneje: Cantidad de ejemplares del libro.
    """
    conexion = conn.get_conexion()  # Obtener la conexión real
    if not conexion:
        logging.error("No se pudo obtener la conexión a la base de datos.")
        return
    
    try:
        with conexion.cursor() as cur:
            cur.execute(
                """
                INSERT INTO libros (ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje),
            )
        conexion.commit()
        logging.info("Libro agregado correctamente")
    except psycopg2.IntegrityError as e:
        conexion.rollback()
        logging.error(f"Error al agregar libro: {e}")
    except Exception as e:
        conexion.rollback()
        logging.error(f"Error inesperado: {e}")

# Función para leer (listar) todos los libros de la base de datos
def leer_libros(conn):
    """
    Obtiene todos los libros almacenados en la base de datos.

    Parámetros:
    - conn: objeto de conexión a la base de datos.

    Retorna:
    - Una lista de diccionarios con los detalles de los libros.
    """
    query = "SELECT * FROM libros order by ncodlib asc"
    return conn.obtener_resultados(query)

# Función para actualizar un libro en la base de datos
def actualizar_libro(conn, ncodlib, ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje):
    """
    Actualiza los detalles de un libro en la base de datos.

    Parámetros:
    - conn: objeto de conexión a la base de datos.
    - ncodlib: ID del libro a actualizar.
    - ctitlib: Nuevo título del libro.
    - cautlib: Nuevo autor del libro.
    - cgenlib: Nuevo género del libro.
    - nanopublib: Nuevo año de publicación del libro.
    - ccodisbn: Nuevo ISBN del libro (debe tener 13 caracteres).
    - cedilib: Nueva editorial del libro (opcional).
    - ncaneje: Nueva cantidad de ejemplares del libro.
    """
    query = """
            UPDATE  libros
            SET     ctitlib = %s, 
                    cautlib = %s, 
                    cgenlib = %s, 
                    nanopublib = %s, 
                    ccodisbn = %s, 
                    cedilib = %s, 
                    ncaneje = %s
            WHERE   ncodlib = %s
            """
    parametros = (ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje, ncodlib)
    conn.ejecutar_query(query, parametros)

# Función para eliminar un libro en la base de datos
def eliminar_libro(conn, ncodlib):
    """
    Elimina un libro de la base de datos.

    Parámetros:
    - conn: objeto de conexión a la base de datos.
    - ncodlib: ID del libro a eliminar.
    """
    query = """
            DELETE 
            FROM    libros
            WHERE   ncodlib = %s
            """
    conn.ejecutar_query(query, (ncodlib,))