#!/usr/bin/env python3
"""
GESTIÓN DE CLIENTES - Base de Datos MySQL
Aplicación de consola para realizar operaciones CRUD sobre una tabla de clientes

Autor: Práctica 2ªEV - ASIR
Fecha: Febrero 2026
"""

import mysql.connector
from mysql.connector import Error
import sys

class GestionClientes:
    """
    Clase para gestionar las operaciones CRUD sobre la tabla de clientes
    """
    
    def __init__(self):
        self.host = "100.52.14.160"
        self.database = "gestion_clientes"
        self.user = "cliente_remoto"
        self.password = "asir"
        self.conexion = None
        self.cursor = None
    
    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor()
                return True
        except Error as e:
            print(f"✗ Error al conectar a MySQL: {e}")
            return False
    
    def desconectar(self):
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
        Muestra los registros incluyendo la columna fecha_registro
        """
        try:
            # Seleccionamos las 5 columnas que existen en tu tabla SQL
            query = "SELECT id, nombre, email, telefono, fecha_registro FROM clientes ORDER BY id"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            
            if not resultados:
                print("\n⚠ No hay clientes registrados")
                return
            
            print("\n" + "="*105)
            print(f"{'ID':<5} {'NOMBRE':<25} {'EMAIL':<30} {'TELÉFONO':<15} {'REGISTRO':<20}")
            print("="*105)
            
            for fila in resultados:
                # Ahora desempaquetamos los 5 valores (incluyendo la fecha)
                id_c, nombre, email, tel, fecha = fila
                # Convertimos la fecha a string para que no de error al imprimir
                fecha_str = str(fecha)
                print(f"{id_c:<5} {nombre:<25} {email:<30} {tel:<15} {fecha_str:<20}")
            
            print("="*105)
            print(f"Total: {len(resultados)} clientes")
            
        except Error as e:
            print(f"✗ Error al visualizar: {e}")

    def insertar_cliente(self):
        try:
            print("\n--- INSERTAR NUEVO CLIENTE ---")
            nombre = input("Nombre completo: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()
            
            if not nombre or "@" not in email:
                print("✗ Datos inválidos")
                return

            query = "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (nombre, email, telefono))
            self.conexion.commit()
            print(f"✓ Cliente insertado (ID: {self.cursor.lastrowid})")
        except Error as e:
            print(f"✗ Error: {e}")

    def modificar_cliente(self):
        try:
            id_cliente = int(input("\nID del cliente a modificar: "))
            # Buscamos primero para ver qué hay
            self.cursor.execute("SELECT nombre, email, telefono FROM clientes WHERE id = %s", (id_cliente,))
            actual = self.cursor.fetchone()
            
            if not actual:
                print("✗ No existe ese ID")
                return

            print(f"Editando: {actual[0]}")
            n_nombre = input(f"Nuevo nombre [{actual[0]}]: ") or actual[0]
            n_email = input(f"Nuevo email [{actual[1]}]: ") or actual[1]
            n_tel = input(f"Nuevo teléfono [{actual[2]}]: ") or actual[2]

            query = "UPDATE clientes SET nombre=%s, email=%s, telefono=%s WHERE id=%s"
            self.cursor.execute(query, (n_nombre, n_email, n_tel, id_cliente))
            self.conexion.commit()
            print("✓ Cliente actualizado")
        except Exception as e:
            print(f"✗ Error: {e}")

    def borrar_cliente(self):
        try:
            id_cliente = int(input("\nID del cliente a borrar: "))
            confirmar = input(f"¿Seguro que quieres borrar el ID {id_cliente}? (s/n): ")
            if confirmar.lower() == 's':
                self.cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
                self.conexion.commit()
                print("✓ Registro eliminado")
        except Exception as e:
            print(f"✗ Error: {e}")

def mostrar_menu():
    print("\n" + "·"*50)
    print("  MENÚ GESTIÓN DE CLIENTES (ASIR)")
    print("·"*50)
    print("1. Listar clientes")
    print("2. Añadir cliente")
    print("3. Modificar cliente")
    print("4. Eliminar cliente")
    print("5. Salir")
    print("·"*50)

def main():
    gestion = GestionClientes()
    if not gestion.conectar():
        print("Error crítico: No hay conexión con el servidor MySQL")
        sys.exit(1)
    
    print("✓ Conectado a 100.52.14.160")

    while True:
        mostrar_menu()
        opcion = input("Selecciona (1-5): ")
        
        if opcion == '1':
            gestion.visualizar_clientes()
        elif opcion == '2':
            gestion.insertar_cliente()
        elif opcion == '3':
            gestion.modificar_cliente()
        elif opcion == '4':
            gestion.borrar_cliente()
        elif opcion == '5':
            gestion.desconectar()
            break
        else:
            print("Opción no válida")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()