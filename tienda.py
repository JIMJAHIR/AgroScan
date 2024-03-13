import mysql
import mysql.connector
from cnx import DB_CONFIG

#Esta función sirve para listar los productos
def listar_productos():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT idproductos, imagen, nombre, precio, categoria FROM productos"
        print("Ejecutando consulta SQL:", query)
        cursor.execute(query)
        result = cursor.fetchall()
        productos = []
        for fila in result:
            productos.append(fila)
        return productos
    except mysql.connector.Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

#Esta función sirve para poder adaptar lo obtenido a algo mas manejable para el html
def convertir():
    objetos = listar_productos()
    productos = []
    for producto in objetos:
        id = producto[0]
        img = producto[1]
        nombre = producto[2]
        precio = producto[3] + " x Unidad"
        cat = producto[4]
        result = [id,img,nombre,precio,cat]
        productos.append(result)
    return productos

def producto_id(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT idproductos, imagen, nombre, precio, categoria FROM productos WHERE idproductos = %s"
        print("Ejecutando consulta SQL:", query)
        cursor.execute(query,(id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def listar_categoria(categoria):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT idproductos, imagen, nombre, precio, categoria FROM productos WHERE categoria = %s"
        print("Ejecutando consulta SQL:", query)
        cursor.execute(query,(categoria,))
        result = cursor.fetchall()
        productos = []
        for fila in result:
            productos.append(fila)
        return productos
    except mysql.connector.Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

class carrito:
    def __init__(self):
        self.items = []
    
    def agregar(self, id):
        item = producto_id(id)
        self.items.append(item)

    def eliminar(self, id):
        item = producto_id(id)
        self.items.remove(item)

    def mostrar_carrito(self):
        return self.items
