DROP DATABASE IF exists when2raid;
CREATE DATABASE when2raid;
-- Creación de tablas
USE when2raid;
CREATE TABLE usuarios (
    nombre_usuario VARCHAR(16) PRIMARY KEY,
    passwd_usuario VARCHAR(16) NOT NULL,
    nombre_completo VARCHAR(32)
) ENGINE=INNODB;
CREATE TABLE tipos (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(64) NOT NULL,
    descripcion_tipo VARCHAR (128),
    max_tipo INT
) ENGINE=INNODB;
CREATE TABLE actividades (
    id_actividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre_actividad VARCHAR(64) NOT NULL,
    descripcion_actividad VARCHAR (128),
    tipo_actividad INT,
    privacidad BOOLEAN NOT NULL,
    passwd_actividad VARCHAR(16),
    apuntados_actividad INT NOT NULL,
    usuarios_actividad JSON NOT NULL,
    limite_actividad INT,
    FOREIGN KEY (tipo_actividad) REFERENCES tipos(id_tipo)
) ENGINE=INNODB;
CREATE TABLE horas_disponibles (
    id_actividad INT PRIMARY KEY,
    usuario_actividad VARCHAR(16),
    dia1 CHAR(26) NOT NULL,
    dia2 CHAR(26) NOT NULL,
    dia3 CHAR(26) NOT NULL,
    dia4 CHAR(26) NOT NULL,
    dia5 CHAR(26) NOT NULL,
    dia6 CHAR(26) NOT NULL,
    dia7 CHAR(26) NOT NULL,
    FOREIGN KEY (id_actividad) REFERENCES actividades(id_actividad),
    FOREIGN KEY (usuario_actividad) REFERENCES usuarios(nombre_usuario)
) ENGINE=INNODB;
CREATE TABLE log_actividades (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_actividad INT NOT NULL,
    usuario VARCHAR(16) DEFAULT USER(),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    accion VARCHAR(64) NOT NULL,
    FOREIGN KEY (id_actividad) REFERENCES actividades(id_actividad)
) ENGINE=INNODB;
CREATE TABLE log_usuarios (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(16) DEFAULT USER(),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    accion VARCHAR(64) NOT NULL
) ENGINE=INNODB;
-- Creación de triggers
DELIMITER //
CREATE TRIGGER log_insert_actividad
    AFTER INSERT ON actividades
    FOR EACH ROW
BEGIN
    INSERT INTO log_actividades VALUES (NEW.id_actividad,CURRENT_TIMESTAMP(),'Actividad Creada');
END; //
DELIMITER ;
DELIMITER //
CREATE TRIGGER log_insert_usuario
    AFTER INSERT ON usuarios
    FOR EACH ROW
BEGIN
    INSERT INTO log_usuarios VALUES (NEW.nombre_usuario,CURRENT_TIMESTAMP(),'Usuario Creado');
END; //
DELIMITER ;
-- Creación de usario limitado
DROP USER IF EXISTS 'usario_limitado'@'when2raid-devtest.cl0s6yiusrsj.us-east-1.rds.amazonaws.com' IDENTIFIED BY 'creador_usuario';
CREATE USER 'usario_limitado'@'when2raid-devtest.cl0s6yiusrsj.us-east-1.rds.amazonaws.com' IDENTIFIED BY 'creador_usuario';
GRANT INSERT ON when2raid.log_insert_usuario TO 'usario_limitado'@'when2raid-devtest.cl0s6yiusrsj.us-east-1.rds.amazonaws.com';
GRANT SELECT ON when2raid.usuarios TO 'usario_limitado'@'when2raid-devtest.cl0s6yiusrsj.us-east-1.rds.amazonaws.com';
GRANT CREATE USER ON *.* TO 'usario_limitado'@'when2raid-devtest.cl0s6yiusrsj.us-east-1.rds.amazonaws.com';

DROP USER IF EXISTS 'usuario_final'@'when2raid-devtest.cl0s6yiusrsj.us-east-1.rds.amazonaws.com';
CREATE USER 'usuario_final'@'when2raid-devtest.cl0s6yiusrsj.us-east-1.rds.amazonaws.com' IDENTIFIED BY 'userFinal';