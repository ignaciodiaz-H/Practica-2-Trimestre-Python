#!/bin/bash

# ============================================
# SCRIPT DE INSTALACIÓN - CLIENTE PYTHON
# Instalación de Python y librerías para conectar a MySQL remoto
# ============================================

set -e

echo "========================================"
echo "  INSTALACIÓN CLIENTE PYTHON"
echo "========================================"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Solicitar datos del servidor MySQL
echo ""
info "Configuración de conexión al servidor MySQL"
echo ""
read -p "IP del servidor MySQL: " SERVER_IP
read -p "Usuario MySQL (default: cliente_remoto): " MYSQL_USER
MYSQL_USER=${MYSQL_USER:-cliente_remoto}
read -sp "Contraseña MySQL: " MYSQL_PASSWORD
echo ""
read -p "Base de datos (default: gestion_clientes): " MYSQL_DB
MYSQL_DB=${MYSQL_DB:-gestion_clientes}

if [ -z "$SERVER_IP" ] || [ -z "$MYSQL_PASSWORD" ]; then
    error "Debes proporcionar IP del servidor y contraseña"
fi

# 1. Actualizar repositorios
info "Actualizando repositorios..."
sudo apt update -y || error "Fallo al actualizar repositorios"

# 2. Instalar Python3 y pip si no están
info "Verificando Python3 y Pip..."
# Instalamos ambos por seguridad, si ya existen, apt no hará nada.
sudo apt install -y python3 python3-pip python3-full || error "Fallo al instalar dependencias de Python"

PYTHON_VERSION=$(python3 --version)
PIP_VERSION=$(pip3 --version)
info "✓ Python: $PYTHON_VERSION"
info "✓ Pip: $PIP_VERSION"

# 3. Instalar librería MySQL Connector
info "Instalando mysql-connector-python..."
pip3 install mysql-connector-python --break-system-packages || error "Fallo al instalar..."

# Verificar instalación
if python3 -c "import mysql.connector" 2>/dev/null; then
    info "✓ mysql-connector-python instalado correctamente"
else
    error "No se pudo verificar la instalación de mysql-connector-python"
fi

# 4. Instalar cliente MySQL (opcional, para pruebas)
info "Instalando cliente MySQL para pruebas..."
sudo apt install mysql-client -y || warning "No se pudo instalar mysql-client (opcional)"

# 5. Probar conexión al servidor
info "Probando conexión al servidor MySQL..."
if command -v mysql &> /dev/null; then
    if mysql -h "$SERVER_IP" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1;" &> /dev/null; then
        info "✓ Conexión exitosa al servidor MySQL"
    else
        warning "No se pudo conectar al servidor. Verifica:"
        echo "  - El servidor está accesible en $SERVER_IP"
        echo "  - El puerto 3306 está abierto"
        echo "  - Las credenciales son correctas"
    fi
else
    warning "mysql-client no disponible, saltando prueba de conexión"
fi

# 6. Configurar archivo Python automáticamente
if [ -f "gestion_clientes.py" ]; then
    info "Configurando gestion_clientes.py con los datos del servidor..."
    
    # Crear backup
    cp gestion_clientes.py gestion_clientes.py.backup
    
    # Actualizar parámetros de conexión
    sed -i "s/self.host = \"localhost\"/self.host = \"$SERVER_IP\"/" gestion_clientes.py
    sed -i "s/self.user = \"root\"/self.user = \"$MYSQL_USER\"/" gestion_clientes.py
    sed -i "s/self.password = \"\"/self.password = \"$MYSQL_PASSWORD\"/" gestion_clientes.py
    sed -i "s/self.database = \"gestion_clientes\"/self.database = \"$MYSQL_DB\"/" gestion_clientes.py
    
    info "✓ Archivo gestion_clientes.py configurado"
    info "  (Backup guardado en gestion_clientes.py.backup)"
else
    warning "No se encontró gestion_clientes.py"
    warning "Deberás configurarlo manualmente con estos datos:"
    echo ""
    echo "  self.host = \"$SERVER_IP\""
    echo "  self.database = \"$MYSQL_DB\""
    echo "  self.user = \"$MYSQL_USER\""
    echo "  self.password = \"$MYSQL_PASSWORD\""
fi

# 7. Probar conexión con Python
info "Probando conexión con Python..."
python3 << EOF
import mysql.connector
try:
    conexion = mysql.connector.connect(
        host="$SERVER_IP",
        database="$MYSQL_DB",
        user="$MYSQL_USER",
        password="$MYSQL_PASSWORD"
    )
    if conexion.is_connected():
        print("${GREEN}[INFO]${NC} ✓ Conexión Python exitosa")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes;")
        count = cursor.fetchone()[0]
        print(f"${GREEN}[INFO]${NC} ✓ Base de datos tiene {count} clientes")
        conexion.close()
except Exception as e:
    print(f"${RED}[ERROR]${NC} No se pudo conectar: {e}")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    info "✓ Prueba de conexión Python exitosa"
else
    error "Fallo la prueba de conexión Python"
fi

echo ""
echo "========================================"
echo -e "${GREEN}  ✓ CLIENTE CONFIGURADO${NC}"
echo "========================================"
echo ""
echo "CONFIGURACIÓN DE CONEXIÓN:"
echo "--------------------------"
echo "  Servidor: $SERVER_IP:3306"
echo "  Usuario:  $MYSQL_USER"
echo "  Database: $MYSQL_DB"
echo ""
echo "PRÓXIMO PASO:"
echo "  python3 gestion_clientes.py"
echo ""
