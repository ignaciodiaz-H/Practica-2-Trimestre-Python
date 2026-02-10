"""
GESTIÓN DE CLIENTES - Base de Datos MySQL
Aplicación de consola para realizar operaciones CRUD sobre una tabla de clientes

Autor: Práctica 2ªEV - ASIR
Fecha: Febrero 2026
Librería requerida: mysql-connector-python
"""

import mysql.connector
from mysql.connector import Error
import sys


class GestionClientes:
    """
    Clase para gestionar las operaciones CRUD sobre la tabla de clientes
    """
    
    def __init__(self):
        """
        Constructor de la clase. Inicializa los parámetros de conexión
        """
        self.host = "localhost"
        self.database = "gestion_clientes"
        self.user = "root"  # Cambiar según tu configuración
        self.password = ""  # Cambiar según tu configuración
        self.conexion = None
        self.cursor = None
    
    def conectar(self):
        """
        Establece la conexión con la base de datos MySQL
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor()
                print("✓ Conexión exitosa a la base de datos")
                return True
                
        except Error as e:
            print(f"✗ Error al conectar a MySQL: {e}")
            print("\nAsegúrate de:")
            print("  1. Tener MySQL en ejecución")
            print("  2. Haber creado la base de datos 'gestion_clientes'")
            print("  3. Verificar usuario y contraseña")
            return False
    
    def desconectar(self):
        """
        Cierra la conexión con la base de datos
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion and self.conexion.is_connected():
                self.conexion.close()
                print("✓ Conexión cerrada correctamente")
        except Error as e:
            print(f"✗ Error al cerrar la conexión: {e}")
    
    def visualizar_clientes(self):
        """
        Muestra todos los registros de la tabla clientes
        """
        try:
            query = "SELECT * FROM clientes ORDER BY id"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            
            if not resultados:
                print("\n⚠ No hay clientes registrados en la base de datos")
                return
            
            print("\n" + "="*80)
            print(f"{'ID':<5} {'NOMBRE':<20} {'EMAIL':<30} {'TELÉFONO':<15}")
            print("="*80)
            
            for fila in resultados:
                id_cliente, nombre, email, telefono = fila
                print(f"{id_cliente:<5} {nombre:<20} {email:<30} {telefono:<15}")
            
            print("="*80)
            print(f"Total de clientes: {len(resultados)}")
            
        except Error as e:
            print(f"✗ Error al visualizar clientes: {e}")
    
    def insertar_cliente(self):
        """
        Inserta un nuevo cliente en la base de datos
        """
        try:
            print("\n--- INSERTAR NUEVO CLIENTE ---")
            
            # Solicitar datos con validación
            nombre = input("Nombre completo: ").strip()
            if not nombre:
                print("✗ El nombre no puede estar vacío")
                return
            
            email = input("Email: ").strip()
            if not email or "@" not in email:
                print("✗ El email no es válido")
                return
            
            telefono = input("Teléfono: ").strip()
            if not telefono:
                print("✗ El teléfono no puede estar vacío")
                return
            
            # Preparar query con parámetros (previene SQL injection)
            query = "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)"
            valores = (nombre, email, telefono)
            
            self.cursor.execute(query, valores)
            self.conexion.commit()
            
            print(f"✓ Cliente '{nombre}' insertado correctamente (ID: {self.cursor.lastrowid})")
            
        except mysql.connector.IntegrityError as e:
            print(f"✗ Error de integridad: {e}")
            print("  (Posiblemente el email ya existe)")
        except Error as e:
            print(f"✗ Error al insertar cliente: {e}")
    
    def modificar_cliente(self):
        """
        Modifica los datos de un cliente existente
        """
        try:
            print("\n--- MODIFICAR CLIENTE ---")
            
            # Mostrar clientes actuales
            self.visualizar_clientes()
            
            # Solicitar ID del cliente a modificar
            try:
                id_cliente = int(input("\nID del cliente a modificar (0 para cancelar): "))
                if id_cliente == 0:
                    print("Operación cancelada")
                    return
            except ValueError:
                print("✗ ID inválido. Debe ser un número")
                return
            
            # Verificar que el cliente existe
            query_verificar = "SELECT * FROM clientes WHERE id = %s"
            self.cursor.execute(query_verificar, (id_cliente,))
            cliente = self.cursor.fetchone()
            
            if not cliente:
                print(f"✗ No existe un cliente con ID {id_cliente}")
                return
            
            print(f"\nCliente actual: {cliente[1]} | {cliente[2]} | {cliente[3]}")
            print("(Presiona Enter para mantener el valor actual)")
            
            # Solicitar nuevos datos
            nuevo_nombre = input(f"Nuevo nombre [{cliente[1]}]: ").strip()
            nuevo_email = input(f"Nuevo email [{cliente[2]}]: ").strip()
            nuevo_telefono = input(f"Nuevo teléfono [{cliente[3]}]: ").strip()
            
            # Usar valores actuales si no se ingresa nada
            nuevo_nombre = nuevo_nombre if nuevo_nombre else cliente[1]
            nuevo_email = nuevo_email if nuevo_email else cliente[2]
            nuevo_telefono = nuevo_telefono if nuevo_telefono else cliente[3]
            
            # Validar email si se modificó
            if nuevo_email != cliente[2] and "@" not in nuevo_email:
                print("✗ El email no es válido")
                return
            
            # Actualizar registro
            query = "UPDATE clientes SET nombre=%s, email=%s, telefono=%s WHERE id=%s"
            valores = (nuevo_nombre, nuevo_email, nuevo_telefono, id_cliente)
            
            self.cursor.execute(query, valores)
            self.conexion.commit()
            
            print(f"✓ Cliente ID {id_cliente} modificado correctamente")
            
        except mysql.connector.IntegrityError as e:
            print(f"✗ Error de integridad: {e}")
        except Error as e:
            print(f"✗ Error al modificar cliente: {e}")
    
    def borrar_cliente(self):
        """
        Elimina un cliente de la base de datos
        """
        try:
            print("\n--- BORRAR CLIENTE ---")
            
            # Mostrar clientes actuales
            self.visualizar_clientes()
            
            # Solicitar ID del cliente a borrar
            try:
                id_cliente = int(input("\nID del cliente a borrar (0 para cancelar): "))
                if id_cliente == 0:
                    print("Operación cancelada")
                    return
            except ValueError:
                print("✗ ID inválido. Debe ser un número")
                return
            
            # Verificar que el cliente existe
            query_verificar = "SELECT nombre FROM clientes WHERE id = %s"
            self.cursor.execute(query_verificar, (id_cliente,))
            resultado = self.cursor.fetchone()
            
            if not resultado:
                print(f"✗ No existe un cliente con ID {id_cliente}")
                return
            
            nombre_cliente = resultado[0]
            
            # Confirmación de borrado
            confirmacion = input(f"¿Confirmas borrar a '{nombre_cliente}'? (S/N): ").strip().upper()
            
            if confirmacion != 'S':
                print("Operación cancelada")
                return
            
            # Eliminar registro
            query = "DELETE FROM clientes WHERE id = %s"
            self.cursor.execute(query, (id_cliente,))
            self.conexion.commit()
            
            print(f"✓ Cliente '{nombre_cliente}' eliminado correctamente")
            
        except Error as e:
            print(f"✗ Error al borrar cliente: {e}")


def mostrar_menu():
    """
    Muestra el menú principal de la aplicación
    """
    print("\n" + "="*50)
    print("   GESTIÓN DE CLIENTES - BASE DE DATOS MYSQL")
    print("="*50)
    print("1. Visualizar todos los clientes")
    print("2. Insertar nuevo cliente")
    print("3. Modificar cliente existente")
    print("4. Borrar cliente")
    print("5. Salir")
    print("="*50)


def main():
    """
    Función principal que ejecuta el programa
    """
    print("\n" + "="*50)
    print("   SISTEMA DE GESTIÓN DE CLIENTES")
    print("="*50)
    
    # Crear instancia de la clase
    gestion = GestionClientes()
    
    # Intentar conectar a la base de datos
    if not gestion.conectar():
        print("\n✗ No se pudo establecer conexión con la base de datos")
        print("Saliendo del programa...")
        sys.exit(1)
    
    # Bucle principal del programa
    while True:
        try:
            mostrar_menu()
            opcion = input("\nSelecciona una opción (1-5): ").strip()
            
            if opcion == '1':
                gestion.visualizar_clientes()
            
            elif opcion == '2':
                gestion.insertar_cliente()
            
            elif opcion == '3':
                gestion.modificar_cliente()
            
            elif opcion == '4':
                gestion.borrar_cliente()
            
            elif opcion == '5':
                print("\nCerrando aplicación...")
                gestion.desconectar()
                print("¡Hasta pronto!")
                break
            
            else:
                print("✗ Opción inválida. Por favor selecciona 1-5")
            
            # Pausa para que el usuario vea los mensajes
            input("\nPresiona Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\nInterrupción detectada...")
            gestion.desconectar()
            print("Saliendo del programa...")
            break
        
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")
            input("Presiona Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
