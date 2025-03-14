# Módulo para manejar la conexión y consultas a PostgreSQL
import psycopg2
import logging
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConexionBD:
    """
    Clase para manejar la conexión a la base de datos PostgreSQL.
    Proporciona métodos para ejecutar consultas SQL y obtener resultados de manera segura.
    """
    
    def __init__(self):
        """
        Establece la conexión a la base de datos usando psycopg2.
        """
        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT,
                application_name="Biblioteca_jmoss"
            )
            logging.info("Conexión a la base de datos establecida correctamente.")
        except Exception as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            self.conn = None
            
    def get_conexion(self):
        return self.conn
    
    def ejecutar_query(self, query, parametros=None):
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE) y realiza commit.
        
        Args:
        - query (str): La consulta SQL a ejecutar.
        - parametros (tuple, opcional): Parámetros para la consulta SQL.
        
        Returns:
        - bool: True si la consulta se ejecutó correctamente, False en caso de error.
        """
        if not self.conn:
            logging.error("No hay conexión a la base de datos.")
            return False
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, parametros)
                self.conn.commit()
                logging.info("Consulta ejecutada exitosamente.")
                return True
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error al ejecutar la consulta: {e}")
            return False
    
    def obtener_resultados(self, query, parametros=None):
        """
        Ejecuta una consulta SELECT y devuelve los resultados.
        
        Args:
        - query (str): Consulta SQL de tipo SELECT.
        - parametros (tuple, opcional): Parámetros para la consulta SQL.
        
        Returns:
        - list: Lista de tuplas con los resultados, o una lista vacía en caso de error.
        """
        if not self.conn:
            logging.error("No hay conexión a la base de datos.")
            return []
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, parametros)
                resultados = cursor.fetchall()
                return resultados
        except Exception as e:
            logging.error(f"Error al obtener resultados: {e}")
            return []
    
    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.conn:
            try:
                self.conn.close()
                logging.info("Conexión a la base de datos cerrada correctamente.")
            except Exception as e:
                logging.error(f"Error al cerrar la conexión: {e}")
