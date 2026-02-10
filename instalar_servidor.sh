#!/bin/bash

# ============================================
# SCRIPT DE INSTALACIÓN - SERVIDOR MYSQL
# Configuración para aceptar conexiones remotas
# ============================================

set -e

echo "========================================"
echo "  INSTALACIÓN SERVIDOR MYSQL REMOTO"
echo "========================================"

# Colores para output
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

# Solicitar contraseña para el usuario remoto
echo ""
read -sp "Ingresa la contraseña para el usuario 'cliente_remoto': " MYSQL_PASSWORD
echo ""

if [ -z "$MYSQL_PASSWORD" ]; then
    error "La contraseña no puede estar vacía"
fi

# Solicitar IP del cliente (opcional, % permite desde cualquier IP)
echo ""
read -p "IP del cliente (Enter para permitir todas las IPs): " CLIENT_IP
if [ -z "$CLIENT_IP" ]; then
    CLIENT_IP="%"
    warning "Se permitirán conexiones desde cualquier IP"
else
    info "Se permitirán conexiones solo desde: $CLIENT_IP"
fi

# 1. Actualizar repositorios
info "Actualizando repositorios..."
sudo apt update -y || error "Fallo al actualizar repositorios"

# 2. Actualizar sistema
info "Actualizando paquetes del sistema..."
sudo apt upgrade -y

# 3. Instalar MySQL Server
info "Instalando MySQL Server..."
sudo apt install mysql-server -y || error "Fallo al instalar MySQL"

# 4. Iniciar y habilitar MySQL
info "Iniciando servicio MySQL..."
sudo systemctl start mysql
sudo systemctl enable mysql

if ! sudo systemctl is-active --quiet mysql; then
    error "MySQL no se pudo iniciar"
fi
info "✓ MySQL está corriendo"

# 5. Configurar MySQL para aceptar conexiones remotas
info "Configurando MySQL para conexiones remotas..."

# Backup del archivo de configuración
sudo cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.backup

# Cambiar bind-address de 127.0.0.1 a 0.0.0.0
sudo sed -i 's/bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# Verificar el cambio
if grep -q "bind-address.*0.0.0.0" /etc/mysql/mysql.conf.d/mysqld.cnf; then
    info "✓ Configuración de bind-address actualizada"
else
    error "No se pudo actualizar bind-address"
fi

# 6. Reiniciar MySQL para aplicar cambios
info "Reiniciando MySQL..."
sudo systemctl restart mysql

# 7. Crear usuario remoto con permisos
info "Creando usuario remoto 'cliente_remoto'..."

sudo mysql <<EOF
-- Crear usuario remoto
CREATE USER IF NOT EXISTS 'cliente_remoto'@'$CLIENT_IP' IDENTIFIED BY '$MYSQL_PASSWORD';

-- Otorgar privilegios completos en la base de datos gestion_clientes
GRANT ALL PRIVILEGES ON gestion_clientes.* TO 'cliente_remoto'@'$CLIENT_IP';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Mostrar usuarios
SELECT User, Host FROM mysql.user WHERE User='cliente_remoto';
EOF

info "✓ Usuario 'cliente_remoto' creado correctamente"

# 8. Crear base de datos si existe el archivo SQL
if [ -f "crear_base_datos.sql" ]; then
    info "Creando base de datos desde crear_base_datos.sql..."
    sudo mysql < crear_base_datos.sql || warning "Problema al crear la base de datos"
    
    # Verificar
    if sudo mysql -e "USE gestion_clientes; SHOW TABLES;" &> /dev/null; then
        REGISTROS=$(sudo mysql -N -e "USE gestion_clientes; SELECT COUNT(*) FROM clientes;")
        info "✓ Base de datos creada con $REGISTROS registros"
    fi
else
    warning "No se encontró crear_base_datos.sql"
    warning "Deberás crear la base de datos manualmente"
fi

# 9. Configurar firewall (si está activo)
if sudo ufw status | grep -q "Status: active"; then
    info "Configurando firewall..."
    sudo ufw allow 3306/tcp
    info "✓ Puerto 3306 abierto en el firewall"
else
    warning "UFW no está activo. Si usas otro firewall, abre el puerto 3306"
fi

# 10. Obtener IP del servidor
SERVER_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "========================================"
echo -e "${GREEN}  ✓ SERVIDOR MYSQL CONFIGURADO${NC}"
echo "========================================"
echo ""
echo "INFORMACIÓN DE CONEXIÓN:"
echo "------------------------"
echo "  Host:     $SERVER_IP"
echo "  Puerto:   3306"
echo "  Usuario:  cliente_remoto"
echo "  Password: $MYSQL_PASSWORD"
echo "  Database: gestion_clientes"
echo ""
echo "DESDE EL CLIENTE, PRUEBA LA CONEXIÓN:"
echo "  mysql -h $SERVER_IP -u cliente_remoto -p"
echo ""
echo "PRÓXIMO PASO:"
echo "  1. Ejecutar 'instalar_cliente.sh' en tu PC local"
echo "  2. Configurar gestion_clientes.py con estos datos"
echo ""
