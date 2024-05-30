-- Plantilla par la base de datos general, debe funcionar en local y en la nube
-- Puede cambiar...
DROP DATABASE IF exists when2raid;
CREATE DATABASE when2raid;
-- Creación de tablas
USE when2raid;
CREATE TABLE usuarios (
    nombre_usuario VARCHAR(16) PRIMARY KEY,
    passwd_usuario VARCHAR(64) NOT NULL,
    nombre_completo VARCHAR(32)
) ENGINE=INNODB;
CREATE TABLE tipos (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(64) NOT NULL
) ENGINE=INNODB;
CREATE TABLE actividades (
    id_actividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre_actividad VARCHAR(64) NOT NULL,
    descripcion_actividad VARCHAR (128),
    tipo_actividad INT,
    passwd_actividad VARCHAR(64),
    fecha DATE NOT NULL,
    autor VARCHAR(16) NOT NULL,
    FOREIGN KEY (tipo_actividad) REFERENCES tipos(id_tipo),
    FOREIGN KEY (autor) REFERENCES usuarios(nombre_usuario)
) ENGINE=INNODB;
CREATE TABLE horas_disponibles (
    id_actividad INT NOT NULL,
    id_usuario VARCHAR(16) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_final TIME NOT NULL,
    FOREIGN KEY (id_actividad) REFERENCES actividades(id_actividad),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(nombre_usuario)
) ENGINE=INNODB;
CREATE TABLE log_actividades (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_actividad INT NOT NULL,
    usuario VARCHAR(16),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
) ENGINE=INNODB;
CREATE TABLE log_usuarios (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(16) DEFAULT USER(),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
) ENGINE=INNODB;
-- Creación de triggers
DELIMITER //
CREATE TRIGGER log_insert_actividad
    AFTER INSERT ON actividades
    FOR EACH ROW
BEGIN
    INSERT INTO log_actividades (id_actividad,usuario,fecha) VALUES (NEW.id_actividad,NEW.autor,CURRENT_TIMESTAMP());
END //
CREATE TRIGGER log_insert_usuario
    AFTER INSERT ON usuarios
    FOR EACH ROW
BEGIN
    INSERT INTO log_usuarios (nombre_usuario,fecha) VALUES (NEW.nombre_usuario,CURRENT_TIMESTAMP());
END //
DELIMITER ;
-- Creación de usario limitado
DROP USER IF EXISTS 'usuario_limitado'@'%';
CREATE USER 'usuario_limitado'@'%' IDENTIFIED BY '';
-- Roles del usuario creador/comprobador de usuarios
REVOKE ALL PRIVILEGES ON *.* FROM 'usuario_limitado'@'%'; 
GRANT SELECT, INSERT, UPDATE, DELETE ON when2raid.usuarios TO 'usuario_limitado'@'%';
GRANT INSERT ON when2raid.log_usuarios TO 'usuario_limitado'@'%';
GRANT CREATE USER ON *.* TO 'usuario_limitado'@'%';
-- Creación del usuario final
DROP USER IF EXISTS 'usuario_final'@'%';
CREATE USER 'usuario_final'@'%' IDENTIFIED BY '';
REVOKE ALL PRIVILEGES ON *.* FROM 'usuario_final'@'%'; 
GRANT SELECT, UPDATE ON when2raid.usuarios TO 'usuario_final'@'%';
GRANT SELECT, UPDATE, INSERT, DELETE ON when2raid.actividades TO 'usuario_final'@'%';
GRANT SELECT ON when2raid.tipos TO 'usuario_final'@'%';
GRANT SELECT ON when2raid.log_actividades TO 'usuario_final'@'%';
GRANT SELECT, UPDATE, INSERT, DELETE ON when2raid.horas_disponibles TO 'usuario_final'@'%';

FLUSH PRIVILEGES;

INSERT INTO when2raid.tipos (nombre_tipo) VALUES
    ("The Epic of Alexander (Ultimate)"),
    ("The Unending Coil of Bahamut (Ultimate)"),
    ("The Weapon's Refrain (Ultimate)"),
    ("Dragonsong's Reprise (Ultimate)"),
    ("The Omega Protocol (Ultimate)"),
    ("Futures Rewritten (Ultimate)"),
    ("The Binding Coil of Bahamut"),
    ("The Second Coil of Bahamut"),
    ("The Second Coil of Bahamut (Savage)"),
    ("The Final Coil of Bahamut"),
    ("Alexander: Gordias"),
    ("Alexander: Gordias (Savage)"),
    ("Alexander: Midas"),
    ("Alexander: Midas (Savage)"),
    ("Alexander: The Creator"),
    ("Alexander: The Creator (Savage)"),
    ("Omega: Deltascape"),
    ("Omega: Deltascape (Savage)"),
    ("Omega: Sigmascape"),
    ("Omega: Sigmascape (Savage)"),
    ("Omega: Alphascape"),
    ("Omega: Alphascape (Savage)"),
    ("Eden's Gate"),
    ("Eden's Gate (Savage)"),
    ("Eden's Verse"),
    ("Eden's Verse (Savage)"),
    ("Eden's Promise"),
    ("Eden's Promise (Savage)"),
    ("Pandaemonium: Asphodelos"),
    ("Pandaemonium: Asphodelos (Savage)"),
    ("Pandaemonium: Abyssos"),
    ("Pandaemonium: Abyssos (Savage)"),
    ("Pandaemonium: Anabaseios"),
    ("Pandaemonium: Anabaseios (Savage)	");

INSERT INTO when2raid.usuarios VALUES 
    ('alex','4135aa9dc1b842a653dea846903ddb95bfb8c5a10c504a7fa16e10bc31d1fdf0','alex'),
    ('pepe','7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834','pepe'),
    ('test','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','test');

INSERT INTO when2raid.actividades VALUES
    (1,'Early Omega Prog','hello world prog',5,'7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834','2024-05-31','alex'),
    (2,'Tea Kill Party','Fate B into kill',1,NULL,'2024-06-04','pepe');

INSERT INTO when2raid.horas_disponibles VALUES
    (1,'alex','22:30:00','23:55:00'),
    (2,'pepe','18:45:00','21:35:00'),
    (2,'alex','19:30:00','22:00:00');