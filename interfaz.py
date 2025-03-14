# Módulo que contiene las ventanas de Tkinter para la gestión de libros en la biblioteca.

import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from operaciones import crear_libro, leer_libros, actualizar_libro, eliminar_libro, existe_libro_por_isbn, leer_libro_por_id
from base_datos import ConexionBD

# Establecer conexión con la base de datos
conn = ConexionBD()

class BibliotecaApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("Biblioteca - CRUD")

def agregar_libro():
    """
    Función que recoge los datos del formulario, valida la entrada y agrega un nuevo libro a la base de datos.
    
    1. Obtiene los datos del formulario.
    2. Valida que los campos obligatorios estén completos y sean correctos.
    3. Si todo es válido, se llama a la función `crear_libro` para agregarlo a la base de datos.
    """
    # Obtener los datos de los campos de texto
    ctitlib = entry_titulo.get()
    cautlib = entry_autor.get()
    cgenlib = combo_genero.get()
    nanopublib = entry_anio.get()
    ccodisbn = entry_isbn.get()
    cedilib = entry_editorial.get()
    ncaneje = entry_edicion.get()

    # Validar que los campos obligatorios no estén vacíos
    if not ctitlib or not cautlib or not cgenlib or not nanopublib or not ccodisbn or not ncaneje:
        messagebox.showwarning("Error", "Los campos Título, Autor, Género, Año de publicación, ISBN y Cantidad de ejemplares son obligatorios.")
        return

    # Validar que el ISBN tenga 13 caracteres
    if len(ccodisbn) != 13:
        messagebox.showwarning("Error", "El ISBN debe tener 13 caracteres.")
        return

    # Validar que la cantidad de ejemplares sea un número mayor o igual a 1
    try:
        ncaneje = int(ncaneje)
        if ncaneje < 1:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Error", "La cantidad de ejemplares debe ser un número mayor o igual a 1.")
        return

    # Validar que el año de publicación sea un número
    try:
        nanopublib = int(nanopublib)
    except ValueError:
        messagebox.showwarning("Error", "El año de publicación debe ser un número.")
        return
    
    # validación: Verificar si el ISBN ya existe**
    if existe_libro_por_isbn(conn, ccodisbn):
        messagebox.showerror("Error", f"Ya existe un libro con el ISBN {ccodisbn}.")
        return  # No intentamos agregarlo

    # Si todo es válido, creamos el libro
    # Intentar agregar el libro
    try:
        crear_libro(conn, ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje)
        messagebox.showinfo("Éxito", "Libro agregado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el libro:\n{e}")
    actualizar_lista()  # Actualizamos la lista de libros en la interfaz

def actualizar_lista():
    """
    Función que actualiza la lista de libros en la interfaz.
    
    Elimina todos los elementos de la lista y luego inserta los libros obtenidos desde la base de datos.
    """
    listBox.delete(0, tk.END)  # Eliminar elementos previos de la lista
    for libro in leer_libros(conn):  # Leer todos los libros desde la base de datos
        listBox.insert(tk.END, f"{libro[0]} - {libro[1]}")

def eliminar_seleccionado():
    """
    Función para eliminar un libro seleccionado de la lista con confirmación previa.

    1. Obtiene la selección del usuario en la lista.
    2. Muestra un mensaje de confirmación.
    3. Si el usuario acepta, elimina el libro correspondiente de la base de datos.
    4. Actualiza la lista después de la eliminación.
    """
    seleccion = listBox.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Debe seleccionar un libro para eliminar.")
        return

    libro_seleccionado = listBox.get(seleccion)
    id_libro = libro_seleccionado.split(" - ")[0]  # Obtener el ID del libro

    # Mensaje de confirmación
    confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el libro con ID {id_libro}?")
    if not confirmar:
        return  # Si el usuario cancela, no hacemos nada

    # Eliminación del libro
    try:
        eliminar_libro(conn, id_libro)
        messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
        actualizar_lista()  # Refrescar la lista
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el libro:\n{e}")
        actualizar_lista()  # Actualizar la lista de libros después de la eliminación

def datos_libro_seleccionado(event=None):  # Se agrega 'event=None' para evitar el error
    """
    Carga los datos del libro seleccionado en los campos de entrada consultando la BD.
    """
    seleccion = listBox.curselection()
    if not seleccion:
        return  # Si no hay selección, no hacer nada

    libro_seleccionado = listBox.get(seleccion)  # Obtener el texto del libro seleccionado
    id_libro = int(libro_seleccionado.split(" - ")[0])  # Extraer el ID del libro

    libro = leer_libro_por_id(conn, id_libro)  # Buscar en la BD

    if libro:
        entry_titulo.delete(0, tk.END)
        entry_titulo.insert(0, libro["ctitlib"])

        entry_autor.delete(0, tk.END)
        entry_autor.insert(0, libro["cautlib"])

        combo_genero.set(libro["cgenlib"])  # Establecer el valor del ComboBox

        entry_anio.delete(0, tk.END)
        entry_anio.insert(0, str(libro["nanopublib"]))

        entry_isbn.delete(0, tk.END)
        entry_isbn.insert(0, libro["ccodisbn"])  # ISBN sin espacios

        entry_editorial.delete(0, tk.END)
        entry_editorial.insert(0, libro["cedilib"])

        entry_edicion.delete(0, tk.END)
        entry_edicion.insert(0, str(libro["ncaneje"]))

    else:
        logging.warning("No se encontraron datos para el libro seleccionado.")

def actualza_libro():
    """
    Toma los valores editados de los campos de entrada y actualiza el libro en la BD.
    """
    seleccion = listBox.curselection()
    if not seleccion:
        logging.warning("No hay libro seleccionado para actualizar.")
        return

    libro_seleccionado = listBox.get(seleccion)  # Obtener el texto del libro seleccionado
    ncodlib = int(libro_seleccionado.split(" - ")[0])  # Extraer el ID del libro

    # Obtener valores de los campos
    ctitlib = entry_titulo.get()
    cautlib = entry_autor.get()
    cgenlib = combo_genero.get()
    nanopublib = int(entry_anio.get()) if entry_anio.get().isdigit() else None
    ccodisbn = entry_isbn.get()
    cedilib = entry_editorial.get()
    ncaneje = int(entry_edicion.get()) if entry_edicion.get().isdigit() else None

    if not all([ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje]):
        logging.warning("Todos los campos son obligatorios.")
        return

    # Llamamos a la función que actualiza en la BD
    actualizar_libro(conn, ncodlib, ctitlib, cautlib, cgenlib, nanopublib, ccodisbn, cedilib, ncaneje)
    
    logging.info("Libro actualizado correctamente.")
    # Actualizar lista en la interfaz
    actualizar_lista() # Actualizamos la lista de libros en la interfaz

# Crear ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Biblioteca - CRUD")

# Campos de entrada para los datos del libro
tk.Label(ventana, text="Título del libro ").pack()
entry_titulo = tk.Entry(ventana)
entry_titulo.pack()

tk.Label(ventana, text="Autor ").pack()
entry_autor = tk.Entry(ventana)
entry_autor.pack()

tk.Label(ventana, text="Género ").pack()
combo_genero = ttk.Combobox(ventana, values=["novela", "ciencia ficción", "historia", "biografía", "fantasía", "drama"])
combo_genero.pack()

tk.Label(ventana, text="Año de publicación ").pack()
entry_anio = tk.Entry(ventana)
entry_anio.pack()

tk.Label(ventana, text="ISBN ").pack()
entry_isbn = tk.Entry(ventana)
entry_isbn.pack()

tk.Label(ventana, text="Editorial  (Opcional)").pack()
entry_editorial = tk.Entry(ventana)
entry_editorial.pack()

tk.Label(ventana, text="Cantidad de ejemplares ").pack()
entry_edicion = tk.Entry(ventana)
entry_edicion.pack()

# Botones para las acciones de CRUD (Agregar, Eliminar, Actualizar)
tk.Button(ventana, text="Agregar Libro", command=agregar_libro).pack()
tk.Button(ventana, text="Eliminar Libro", command=eliminar_seleccionado).pack()
tk.Button(ventana, text="Actualizar Libro", command=actualza_libro).pack()

# Lista para mostrar los libros
listBox = tk.Listbox(ventana)
listBox.pack()
actualizar_lista()  # Actualizamos la lista de libros cuando se inicia la ventana

# Asociar evento de selección con la función que cargará los datos del libro seleccionado
listBox.bind("<<ListboxSelect>>", datos_libro_seleccionado)

# Botón para cerrar la aplicación
btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit, bg="red", fg="white")
btn_salir.pack()

# Ejecutar el loop de la interfaz gráfica
ventana.mainloop()