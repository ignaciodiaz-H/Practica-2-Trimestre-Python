-- ============================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Práctica 2ªEV - Integración BD con Python
-- ============================================

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS gestion_clientes
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE gestion_clientes;

-- Eliminar la tabla si existe (para poder recrearla)
DROP TABLE IF EXISTS clientes;

-- Crear la tabla de clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar datos de ejemplo
INSERT INTO clientes (nombre, email, telefono) VALUES
('Juan Pérez García', 'juan.perez@email.com', '666123456'),
('María López Sánchez', 'maria.lopez@email.com', '677234567'),
('Carlos Rodríguez Martín', 'carlos.rodriguez@email.com', '688345678'),
('Ana Fernández Díaz', 'ana.fernandez@email.com', '699456789'),
('Pedro Gómez Ruiz', 'pedro.gomez@email.com', '611567890'),
('Laura Martínez Torres', 'laura.martinez@email.com', '622678901'),
('David Sánchez Moreno', 'david.sanchez@email.com', '633789012'),
('Elena García Jiménez', 'elena.garcia@email.com', '644890123'),
('Miguel Hernández Álvarez', 'miguel.hernandez@email.com', '655901234'),
('Sara Ruiz Navarro', 'sara.ruiz@email.com', '666012345');

-- Verificar que los datos se insertaron correctamente
SELECT * FROM clientes;

-- Mostrar información de la tabla
DESCRIBE clientes;

-- ============================================
-- FIN DEL SCRIPT
-- ============================================
