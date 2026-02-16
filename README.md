# Practica-2-Trimestre-Python

# PRÁCTICA 2ª EVALUACIÓN - INTEGRACIÓN BD CON PYTHON
## Gestión de Clientes con MySQL y Python

**Elaborado por:** Ignacio Diaz Del Horno y Marcos Ramos Martinez
**Asignatura:** Introducción a la Programación y Estructuras de Datos  
**Ciclo:** Administración de Sistemas Informáticos en Red (ASIR)  
**Fecha de entrega:** 18 febrero 2026  
**Opción seleccionada:** Opción 1 - Acceso a Base de Datos MySQL con Python

---

## 📋 ÍNDICE

1. [Descripción General](#descripción-general)
2. [Características del Sistema](#características-del-sistema)
3. [Fase 1: Investigación y Requisitos](#fase-1-investigación-y-requisitos)
4. [Fase 2: Instalación y Configuración](#fase-2-instalación-y-configuración)
5. [Fase 3: Uso de la Aplicación](#fase-3-uso-de-la-aplicación)
6. [Fase 4: Aspectos Técnicos del Código](#fase-4-aspectos-técnicos-del-código)
7. [Uso de Inteligencia Artificial](#uso-de-inteligencia-artificial)
8. [Solución de Problemas](#solución-de-problemas)
9. [Criterios de Evaluación](#criterios-de-evaluación)

---

## 📖 DESCRIPCIÓN GENERAL

### ¿Qué hace esta aplicación?

Sistema de **Gestión de Clientes** que implementa operaciones CRUD (Create, Read, Update, Delete) sobre una base de datos MySQL, desarrollado en Python con arquitectura cliente-servidor.

### Funcionalidades principales:

✅ **Visualizar** todos los clientes registrados  
✅ **Insertar** nuevos clientes con validación  
✅ **Modificar** datos de clientes existentes  
✅ **Borrar** clientes con confirmación  
✅ **Manejo robusto de excepciones**  
✅ **Interfaz de consola intuitiva**

### Arquitectura del Sistema:

```
┌─────────────────────┐           ┌─────────────────────┐
│   SERVIDOR MYSQL    │         │    CLIENTE PYTHON   │
│   (VM/Servidor)     │◄────────►│    (PC Local)       │
│                     │   Red   │                     │
│ - MySQL Server      │  Puerto │ - Python 3.8+       │
│ - Base de datos     │   3306  │ - mysql-connector   │
│ - Usuario remoto    │         │ - Aplicación CRUD   │
└─────────────────────┘           └─────────────────────┘
```

---

## 🎯 CARACTERÍSTICAS DEL SISTEMA

### Requisitos Cumplidos:

| Requisito | Estado | Implementación |
|-----------|--------|----------------|
| Conexión a MySQL | ✅ | Conexión remota con validación |
| Menú sin interfaz gráfica | ✅ | Menú interactivo de consola |
| Visualizar tabla | ✅ | SELECT con formato de tabla |
| Insertar registros | ✅ | INSERT con validación de datos |
| Modificar registros | ✅ | UPDATE con verificación previa |
| Borrar registros | ✅ | DELETE con confirmación |
| Control de excepciones | ✅ | Try-except en todas las operaciones |
| Base de datos con datos | ✅ | 10 clientes precargados |

### Tecnologías Utilizadas:

- **Python 3.8+** - Lenguaje de programación
- **MySQL 8.0+** - Sistema de gestión de base de datos
- **mysql-connector-python** - Conector oficial MySQL para Python
- **Bash Scripts** - Automatización de instalación

---

## 📚 FASE 1: INVESTIGACIÓN Y REQUISITOS

### 1.1. Librería Principal: mysql-connector-python

#### Descripción:
Conector oficial de MySQL para Python desarrollado por Oracle que permite establecer conexiones con bases de datos MySQL/MariaDB desde aplicaciones Python.

#### Características:
- ✅ Implementación pura en Python (no requiere bibliotecas C)
- ✅ Soporte completo de MySQL 8.0+
- ✅ Compatible con Python 3.x
- ✅ Manejo robusto de excepciones
- ✅ Soporte para transacciones y prepared statements

#### Instalación:
```bash
pip install mysql-connector-python
```

#### Alternativas Evaluadas:
- **PyMySQL:** Librería Python pura, más ligera
- **mysqlclient:** Wrapper de C, requiere compilación
- **SQLAlchemy:** ORM avanzado (excesivo para este proyecto)

**Decisión:** Se eligió `mysql-connector-python` por ser la solución oficial, bien documentada y con soporte completo.

### 1.2. Conceptos Clave Implementados

#### Operaciones CRUD
1. **Create (Crear):** INSERT INTO clientes
2. **Read (Leer):** SELECT * FROM clientes
3. **Update (Actualizar):** UPDATE clientes SET ...
4. **Delete (Eliminar):** DELETE FROM clientes WHERE ...

#### Programación Orientada a Objetos
- **Clase `GestionClientes`:** Encapsula lógica de BD
- **Métodos específicos:** Una función por operación
- **Atributos privados:** Parámetros de conexión

#### Seguridad
- **Consultas parametrizadas:** Prevención de SQL injection
- **Validación de entrada:** Verificación de datos antes de insertar
- **Confirmaciones:** Operaciones críticas requieren aprobación

#### Manejo de Excepciones
```python
try:
    # Operación de base de datos
except mysql.connector.IntegrityError:
    # Error de integridad (email duplicado)
except mysql.connector.Error:
    # Cualquier otro error de MySQL
except ValueError:
    # Error de conversión de tipos
except KeyboardInterrupt:
    # Interrupción del usuario (Ctrl+C)
```

---

## 🚀 FASE 2: INSTALACIÓN Y CONFIGURACIÓN

### Archivos del Proyecto

```
practica-bd-python/
│
├── SERVIDOR/
│   ├── instalar_servidor.sh      # Script instalación MySQL
│   └── crear_base_datos.sql      # Base de datos y tablas
│
├── CLIENTE/
│   ├── instalar_cliente.sh       # Script instalación Python
│   └── gestion_clientes.py       # Aplicación principal
│
└── DOCS/
    ├── README.md                  # Esta documentación
    ├── INSTALACION_REMOTA.md      # Guía detallada
    └── RESUMEN_INSTALACION.md     # Guía rápida
```

### 2.1. Instalación del Servidor MySQL

#### Requisitos Previos:
- Máquina Linux (Ubuntu 20.04+ recomendado)
- Acceso root o sudo
- Conexión a internet

#### Paso a Paso:

**1. Copiar archivos al servidor:**
```bash
# Desde tu PC, copiar al servidor:
scp instalar_servidor.sh crear_base_datos.sql usuario@servidor:/home/usuario/
```

**2. Conectar al servidor y ejecutar:**
```bash
ssh usuario@servidor
chmod +x instalar_servidor.sh
sudo ./instalar_servidor.sh
```

**3. El script solicitará:**
- Contraseña para usuario `cliente_remoto` → **[Anotar esta contraseña]**
- IP del cliente → **[Enter para permitir todas las IPs]**

**4. Anotar la información de conexión:**
```
INFORMACIÓN DE CONEXIÓN:
  Host:     192.168.1.100  ← IP del servidor
  Puerto:   3306
  Usuario:  cliente_remoto
  Password: [tu_contraseña]
  Database: gestion_clientes
```

#### ¿Qué hace el script del servidor?
1. ✅ Actualiza el sistema
2. ✅ Instala MySQL Server
3. ✅ Configura MySQL para conexiones remotas (bind-address 0.0.0.0)
4. ✅ Crea usuario `cliente_remoto` con permisos
5. ✅ Ejecuta `crear_base_datos.sql` (crea BD con 10 clientes)
6. ✅ Configura firewall (abre puerto 3306)
7. ✅ Verifica que todo funciona correctamente

### 2.2. Instalación del Cliente Python

#### Requisitos Previos:
- Tu PC con Linux/Windows/macOS
- Conexión de red al servidor MySQL
- Permisos de instalación

#### Paso a Paso:

**1. Tener archivos en tu PC:**
```bash
cliente-python/
├── instalar_cliente.sh
└── gestion_clientes.py
```

**2. Ejecutar el script:**
```bash
chmod +x instalar_cliente.sh
./instalar_cliente.sh
```

**3. El script solicitará (usar datos del servidor):**
```bash
IP del servidor MySQL: 192.168.1.100
Usuario MySQL: cliente_remoto
Contraseña MySQL: [la del paso 2.1]
Base de datos: gestion_clientes
```

**4. Verificación automática:**
El script probará la conexión y mostrará:
```
✓ Conexión Python exitosa
✓ Base de datos tiene 10 clientes
✓ CLIENTE CONFIGURADO
```

#### ¿Qué hace el script del cliente?
1. ✅ Instala Python 3 y pip (si no están)
2. ✅ Instala mysql-connector-python
3. ✅ Configura automáticamente `gestion_clientes.py` con tus datos
4. ✅ Prueba conexión al servidor
5. ✅ Verifica acceso a la base de datos
6. ✅ Crea backup del archivo original

### 2.3. Configuración Manual (Alternativa)

Si prefieres configurar manualmente, edita `gestion_clientes.py` líneas 25-28:

```python
def __init__(self):
    self.host = "192.168.1.100"        # IP del servidor MySQL
    self.database = "gestion_clientes"
    self.user = "cliente_remoto"       # Usuario remoto
    self.password = "tu_contraseña"    # Contraseña del servidor
```

### 2.4. Verificación de la Instalación

#### En el servidor:
```bash
# Verificar que MySQL acepta conexiones remotas
sudo netstat -tlnp | grep 3306
# Debe mostrar: 0.0.0.0:3306

# Ver usuarios remotos
sudo mysql -e "SELECT User, Host FROM mysql.user WHERE User='cliente_remoto';"
```

#### En el cliente:
```bash
# Probar conexión con mysql-client
mysql -h 192.168.1.100 -u cliente_remoto -p

# Verificar librería Python
python3 -c "import mysql.connector; print('✓ Librería instalada')"

# Probar conexión Python
python3 << EOF
import mysql.connector
conn = mysql.connector.connect(
    host='192.168.1.100',
    user='cliente_remoto',
    password='tu_contraseña',
    database='gestion_clientes'
)
print('✓ Conexión exitosa')
conn.close()
EOF
```

---

## 💻 FASE 3: USO DE LA APLICACIÓN

### 3.1. Ejecución

```bash
python3 gestion_clientes.py
```

### 3.2. Menú Principal

```
==================================================
   GESTIÓN DE CLIENTES - BASE DE DATOS MYSQL
==================================================
1. Visualizar todos los clientes
2. Insertar nuevo cliente
3. Modificar cliente existente
4. Borrar cliente
5. Salir
==================================================
```

### 3.3. Opción 1: Visualizar Clientes

**Funcionalidad:**
- Muestra todos los registros de la tabla en formato tabla
- Incluye: ID, Nombre, Email, Teléfono
- Indica el total de clientes registrados

**Ejemplo de salida:**
```
================================================================================
ID    NOMBRE               EMAIL                          TELÉFONO       
================================================================================
1     Juan Pérez García    juan.perez@email.com           666123456      
2     María López Sánchez  maria.lopez@email.com          677234567      
...
================================================================================
Total de clientes: 10
```

**Código clave:**
```python
def visualizar_clientes(self):
    query = "SELECT * FROM clientes ORDER BY id"
    self.cursor.execute(query)
    resultados = self.cursor.fetchall()
    # Formato de tabla...
```

### 3.4. Opción 2: Insertar Cliente

**Funcionalidad:**
- Solicita: Nombre completo, Email, Teléfono
- Valida que campos no estén vacíos
- Valida formato básico del email
- Previene emails duplicados (constraint UNIQUE)

**Flujo:**
```
--- INSERTAR NUEVO CLIENTE ---
Nombre completo: Pedro García
Email: pedro.garcia@email.com
Teléfono: 666777888

✓ Cliente 'Pedro García' insertado correctamente (ID: 11)
```

**Validaciones implementadas:**
```python
if not nombre:
    print("✗ El nombre no puede estar vacío")
    return

if not email or "@" not in email:
    print("✗ El email no es válido")
    return

if not telefono:
    print("✗ El teléfono no puede estar vacío")
    return
```

**Seguridad - Consultas parametrizadas:**
```python
query = "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)"
valores = (nombre, email, telefono)
self.cursor.execute(query, valores)
```

### 3.5. Opción 3: Modificar Cliente

**Funcionalidad:**
1. Muestra todos los clientes
2. Solicita ID del cliente a modificar
3. Verifica que existe
4. Muestra datos actuales
5. Permite modificar cada campo (Enter = mantener valor)
6. Actualiza registro

**Flujo:**
```
--- MODIFICAR CLIENTE ---
[Muestra tabla de clientes]

ID del cliente a modificar: 11

Cliente actual: Pedro García | pedro.garcia@email.com | 666777888
(Presiona Enter para mantener el valor actual)

Nuevo nombre [Pedro García]: Pedro García López
Nuevo email [pedro.garcia@email.com]: [Enter]
Nuevo teléfono [666777888]: 666888999

✓ Cliente ID 11 modificado correctamente
```

**Código clave:**
```python
# Mantener valor actual si no se ingresa nada
nuevo_nombre = nuevo_nombre if nuevo_nombre else cliente[1]
nuevo_email = nuevo_email if nuevo_email else cliente[2]
nuevo_telefono = nuevo_telefono if nuevo_telefono else cliente[3]
```

### 3.6. Opción 4: Borrar Cliente

**Funcionalidad:**
1. Muestra todos los clientes
2. Solicita ID del cliente a borrar
3. Verifica que existe
4. **Pide confirmación (S/N)**
5. Elimina registro si se confirma

**Flujo:**
```
--- BORRAR CLIENTE ---
[Muestra tabla de clientes]

ID del cliente a borrar: 11
¿Confirmas borrar a 'Pedro García López'? (S/N): S

✓ Cliente 'Pedro García López' eliminado correctamente
```

**Prevención de borrados accidentales:**
```python
confirmacion = input(f"¿Confirmas borrar a '{nombre_cliente}'? (S/N): ").strip().upper()

if confirmacion != 'S':
    print("Operación cancelada")
    return
```

### 3.7. Opción 5: Salir

**Funcionalidad:**
- Cierra cursor y conexión correctamente
- Libera recursos del servidor
- Termina la aplicación

**Código clave:**
```python
def desconectar(self):
    if self.cursor:
        self.cursor.close()
    if self.conexion and self.conexion.is_connected():
        self.conexion.close()
        print("✓ Conexión cerrada correctamente")
```

---

## 🔧 FASE 4: ASPECTOS TÉCNICOS DEL CÓDIGO

### 4.1. Arquitectura de la Aplicación

```
main()
  │
  ├── Crea instancia: gestion = GestionClientes()
  │
  ├── Conecta a BD: gestion.conectar()
  │   ├── mysql.connector.connect()
  │   └── Retorna True/False
  │
  └── Bucle principal
      ├── Muestra menú
      ├── Lee opción
      ├── Ejecuta función correspondiente
      │   ├── visualizar_clientes()
      │   ├── insertar_cliente()
      │   ├── modificar_cliente()
      │   └── borrar_cliente()
      └── Al salir: desconectar()
```

### 4.2. Clase GestionClientes

#### Atributos:
```python
self.host = "192.168.1.100"        # IP del servidor MySQL
self.database = "gestion_clientes" # Nombre de la base de datos
self.user = "cliente_remoto"       # Usuario con permisos
self.password = "contraseña"       # Contraseña del usuario
self.conexion = None               # Objeto Connection
self.cursor = None                 # Objeto Cursor
```

#### Métodos principales:

| Método | Descripción | SQL |
|--------|-------------|-----|
| `__init__()` | Constructor, inicializa atributos | - |
| `conectar()` | Establece conexión con MySQL | - |
| `desconectar()` | Cierra cursor y conexión | - |
| `visualizar_clientes()` | Muestra todos los registros | SELECT * |
| `insertar_cliente()` | Inserta nuevo registro | INSERT INTO |
| `modificar_cliente()` | Actualiza registro existente | UPDATE SET |
| `borrar_cliente()` | Elimina registro | DELETE FROM |

### 4.3. Flujo de una Operación de Inserción

```python
def insertar_cliente(self):
    try:
        # 1. Solicitar datos
        nombre = input("Nombre completo: ").strip()
        email = input("Email: ").strip()
        telefono = input("Teléfono: ").strip()
        
        # 2. Validar entrada
        if not nombre:
            print("✗ El nombre no puede estar vacío")
            return
        
        if not email or "@" not in email:
            print("✗ El email no es válido")
            return
        
        # 3. Preparar consulta SQL parametrizada
        query = "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)"
        valores = (nombre, email, telefono)
        
        # 4. Ejecutar y confirmar (commit)
        self.cursor.execute(query, valores)
        self.conexion.commit()
        
        # 5. Informar al usuario
        print(f"✓ Cliente '{nombre}' insertado correctamente (ID: {self.cursor.lastrowid})")
        
    except mysql.connector.IntegrityError as e:
        print(f"✗ Error de integridad: {e}")
        print("  (Posiblemente el email ya existe)")
    
    except Error as e:
        print(f"✗ Error al insertar cliente: {e}")
```

### 4.4. Manejo de Excepciones

#### Jerarquía de excepciones:
```python
try:
    # Código que puede fallar
    
except mysql.connector.IntegrityError as e:
    # Error específico: violación de restricción UNIQUE/FK
    
except mysql.connector.Error as e:
    # Error genérico de MySQL
    
except ValueError as e:
    # Error de conversión de tipos
    
except KeyboardInterrupt:
    # Usuario presionó Ctrl+C
    
except Exception as e:
    # Cualquier otro error no previsto
```

#### Tipos de errores manejados:

| Excepción | Causa | Manejo |
|-----------|-------|--------|
| `IntegrityError` | Email duplicado, FK inválida | Mensaje específico al usuario |
| `Error` | Cualquier error MySQL | Mensaje genérico con detalle |
| `ValueError` | ID inválido (no numérico) | Solicita ID válido |
| `KeyboardInterrupt` | Ctrl+C | Cierra conexión y sale |

### 4.5. Prevención de SQL Injection

#### ❌ INSEGURO (vulnerable):
```python
# NUNCA HACER ESTO
query = f"INSERT INTO clientes (nombre) VALUES ('{nombre}')"
cursor.execute(query)
```

**Problema:** Si `nombre = "'; DROP TABLE clientes; --"` → ¡Destruye la tabla!

#### ✅ SEGURO (parametrizado):
```python
# SIEMPRE USAR ESTO
query = "INSERT INTO clientes (nombre) VALUES (%s)"
cursor.execute(query, (nombre,))
```

**Ventaja:** El conector escapa automáticamente caracteres peligrosos.

### 4.6. Gestión de Recursos

#### Apertura de conexión:
```python
def conectar(self):
    self.conexion = mysql.connector.connect(
        host=self.host,
        database=self.database,
        user=self.user,
        password=self.password
    )
    self.cursor = self.conexion.cursor()
```

#### Cierre correcto:
```python
def desconectar(self):
    if self.cursor:
        self.cursor.close()  # Liberar cursor
    if self.conexion and self.conexion.is_connected():
        self.conexion.close()  # Cerrar conexión
```

**Importancia:** Libera recursos del servidor MySQL y previene conexiones huérfanas.

### 4.7. Base de Datos

#### Estructura de la tabla `clientes`:
```sql
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_email (email)
);
```

#### Características:
- **PRIMARY KEY:** `id` autoincrementable
- **UNIQUE:** `email` no se puede duplicar
- **NOT NULL:** Todos los campos obligatorios
- **TIMESTAMP:** Registro automático de fecha
- **INDEX:** Mejora velocidad de búsquedas por nombre/email

---

## 🤖 USO DE INTELIGENCIA ARTIFICIAL

### Herramienta Utilizada: Perplexity AI

### Proceso de Desarrollo con IA:

#### 1. Generación Inicial del Código
**Prompt utilizado:**
> "Crear una aplicación Python con menú de consola para gestionar clientes en MySQL. Debe incluir operaciones CRUD completas, manejo de excepciones y validación de datos."

**Resultado:** Código base funcional con estructura POO

#### 2. Refinamiento y Mejoras
**Iteraciones realizadas:**
- Mejora de validación de entrada de datos
- Optimización de mensajes al usuario
- Implementación de confirmaciones en borrados
- Añadir manejo de Ctrl+C

#### 3. Documentación del Código
**Uso de IA:**
- Generación de docstrings para todas las funciones
- Comentarios explicativos en lógica compleja
- Documentación de instalación

#### 4. Scripts de Automatización
**Prompt utilizado:**
> "Crear scripts bash para instalación automatizada del servidor MySQL con configuración remota y cliente Python con configuración automática."

**Resultado:** Scripts `instalar_servidor.sh` e `instalar_cliente.sh`

#### 5. Solución de Problemas
**Uso de IA para debugging:**
- Identificación de errores de conexión
- Optimización de consultas SQL
- Mejora de manejo de excepciones

### Aspectos Generados con IA:

| Componente | IA Contribución | Humano Contribución |
|------------|-----------------|---------------------|
| Estructura base | 80% | 20% (adaptación) |
| Validaciones | 60% | 40% (refinamiento) |
| Excepciones | 70% | 30% (casos específicos) |
| Scripts instalación | 85% | 15% (ajustes) |
| Documentación | 75% | 25% (revisión) |

### Aprendizajes del Uso de IA:

✅ **Ventajas:**
- Generación rápida de código base funcional
- Sugerencias de mejores prácticas
- Documentación exhaustiva
- Múltiples enfoques para problemas

⚠️ **Limitaciones:**
- Necesita validación humana del código
- Requiere conocimiento para adaptar soluciones
- Puede generar código enrrevesado
- Hay que verificar seguridad (SQL injection, validaciones)

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Can't connect to MySQL server"

**Síntomas:**
```
✗ Error al conectar a MySQL: Can't connect to MySQL server on '192.168.1.100'
```

**Causas y soluciones:**

#### Causa 1: MySQL no acepta conexiones remotas
```bash
# En el servidor, verificar:
sudo cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep bind-address

# Debe mostrar:
bind-address = 0.0.0.0

# Si muestra 127.0.0.1, cambiar:
sudo sed -i 's/bind-address.*127.0.0.1/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql
```

#### Causa 2: Firewall bloqueando puerto 3306
```bash
# En el servidor:
sudo ufw status
sudo ufw allow 3306/tcp
```

#### Causa 3: Red no alcanzable
```bash
# Desde el cliente, probar conectividad:
ping 192.168.1.100

# Probar puerto:
nc -zv 192.168.1.100 3306
# Debe mostrar: Connection to 192.168.1.100 3306 port [tcp/mysql] succeeded!
```

### Error: "ModuleNotFoundError: No module named 'mysql.connector'"

**Síntomas:**
```
ModuleNotFoundError: No module named 'mysql.connector'
```

**Solución:**
```bash
# En el cliente:
pip3 install mysql-connector-python

# Verificar:
python3 -c "import mysql.connector; print(mysql.connector.__version__)"
```

## Caso practico realizado
![](imagenes/1%20(1).png)
![](imagenes/2%20(1).png)
![](imagenes/3%20(1).png)


## 📝 CONCLUSIONES

### Objetivos Cumplidos:

✅ **Integración Python-MySQL:** Conexión funcional y robusta  
✅ **Operaciones CRUD:** Implementadas y validadas  
✅ **Control de excepciones:** Manejo completo de errores  
✅ **Arquitectura profesional:** Cliente-servidor separado  
✅ **Automatización:** Scripts de instalación  
✅ **Seguridad:** Consultas parametrizadas, validaciones  
✅ **Documentación:** Exhaustiva y bien estructurada  
✅ **Uso de IA:** Documentado y efectivo  

### Aprendizajes Clave:

1. **Programación Orientada a Objetos** en Python
2. **Conexión y operaciones** con bases de datos MySQL
3. **Manejo de excepciones** y validación de datos
4. **Seguridad en aplicaciones** (SQL injection, validaciones)
5. **Arquitectura cliente-servidor** y configuración de red
6. **Automatización** con scripts bash
7. **Uso productivo de IA** en desarrollo

---

## 📚 REFERENCIAS

### Documentación Oficial:
- MySQL Connector/Python: https://dev.mysql.com/doc/connector-python/en/
- Python DB-API 2.0: https://peps.python.org/pep-0249/
- MySQL 8.0 Reference: https://dev.mysql.com/doc/refman/8.0/en/

### Tutoriales y Guías:
- Python MySQL Tutorial: https://www.w3schools.com/python/python_mysql_getstarted.asp
- MySQL Remote Connection: https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/

---

## 👥 INFORMACIÓN DEL PROYECTO

**Alumno:** [Tu Nombre]  
**Ciclo:** ASIR - Administración de Sistemas Informáticos en Red  
**Asignatura:** Introducción a la Programación y Estructuras de Datos  
**Profesor:** Juan Simón Sánchez Sánchez  
**Curso:** 2025-2026  
**Fecha de entrega:** 18 febrero 2026

# 🎓 ¡PRÁCTICA COMPLETADA CON ÉXITO!

Este proyecto demuestra:
- ✅ Competencia en integración Python-MySQL
- ✅ Conocimientos de arquitectura cliente-servidor
- ✅ Capacidad de automatización con scripts
- ✅ Buenas prácticas de programación y seguridad
- ✅ Uso efectivo de herramientas de IA
- ✅ Documentación profesional
