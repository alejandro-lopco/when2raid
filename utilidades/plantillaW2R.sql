-- Plantilla par la base de datos general, debe funcionar en local y en la nube
-- Puede cambiar...
DROP DATABASE IF exists when2raid;
CREATE DATABASE when2raid;
-- Creación de tablas
USE when2raid;
CREATE TABLE usuarios (
    nombre_usuario VARCHAR(16) PRIMARY KEY,
    passwd_usuario VARCHAR(64) NOT NULL
) ENGINE=INNODB;
CREATE TABLE tipos (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(64) NOT NULL,
    desc_tipo VARCHAR(1024) NOT NULL
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
    nombre_usuario VARCHAR(16),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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

INSERT INTO when2raid.tipos (nombre_tipo,desc_tipo) VALUES
    ('The Epic of Alexander (Ultimate)',CONCAT_WS('\n\n','Expansión: ShadowBringers','Parche de salida: 5.1','Sync Item Level: 475','Nivel: 80')),
    ('The Unending Coil of Bahamut (Ultimate)',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.1','Sync Item Level: 345','Nivel: 70')),
    ('The Weapon\'s Refrain (Ultimate)',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.3','Sync Item Level: 375','Nivel: 70')),
    ('Dragonsong\'s Reprise (Ultimate)',CONCAT_WS('\n\n','Expansión: EndWalker','Parche de salida: 6.1','Sync Item Level: 605','Nivel: 90')),
    ('The Omega Protocol (Ultimate)',CONCAT_WS('\n\n','Expansión: EndWalker','Parche de salida: 6.3','Sync Item Level: 635','Nivel: 90')),
    ('Futures Rewritten (Ultimate)',CONCAT_WS('\n\n','Expansión: DawnTrail','Parche de salida: 7.1','Sync Item Level: 705','Nivel: 100')),
    ('The Binding Coil of Bahamut',CONCAT_WS('\n\n','Expansión: A Realm Reborn','Parche de salida: 2.0','Sync Item Level: 82','Nivel: 50')),
    ('The Second Coil of Bahamut',CONCAT_WS('\n\n','Expansión: A Realm Reborn','Parche de salida: 2.2','Item Level Mínimo: 90','Item Level Máximo: 105','Nivel: 50')),
    ('The Second Coil of Bahamut (Savage)',CONCAT_WS('\n\n','Expansión: A Realm Reborn','Parche de salida: 2.2','Sync Item Level: 105','Nivel: 50')),
    ('The Final Coil of Bahamut',CONCAT_WS('\n\n','Expansión: A Realm Reborn','Parche de salida: 2.4','Item Level Mínimo: 110','Item Level Máximo: 123','Nivel: 50')),
    ('Alexander Gordias',CONCAT_WS('\n\n','Expansión: HeavensWard','Parche de salida: 3.0','Sync Item Level: 170','Nivel: 60')),
    ('Alexander Gordias (Savage)',CONCAT_WS('\n\n','Expansión: HeavensWard','Parche de salida: 3.0','Item Level Mínimo: 190','Item Level Máximo: 205','Nivel: 60')),
    ('Alexander Midas',CONCAT_WS('\n\n','Expansión: HeavensWard','Parche de salida: 3.2','Sync Item Level: 200','Nivel: 60')),
    ('Alexander Midas (Savage)',CONCAT_WS('\n\n','Expansión: HeavensWard','Parche de salida: 3.2','Item Level Mínimo: 215','Item Level Máximo: 225','Nivel: 60')),
    ('Alexander The Creator',CONCAT_WS('\n\n','Expansión: HeavensWard','Parche de salida: 3.4','Sync Item Level: 230','Nivel: 60')),
    ('Alexander The Creator (Savage)',CONCAT_WS('\n\n','Expansión: HeavensWard','Parche de salida: 3.4','Item Level Mínimo: 245','Item Level Máximo: 255','Nivel: 60')),
    ('Omega Deltascape',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.0','Sync Item Level: 295','Nivel: 70')),
    ('Omega Deltascape (Savage)',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.0','Item Level Mínimo: 310','Item Level Máximo: 320','Nivel: 70')),
    ('Omega Sigmascape',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.2','Sync Item Level: 325','Nivel: 70')),
    ('Omega Sigmascape (Savage)',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.2','Item Level Mínimo: 340','Item Level Máximo: 350','Nivel: 70')),
    ('Omega Alphascape',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.4','Sync Item Level: 355','Nivel: 70')),
    ('Omega Alphascape (Savage)',CONCAT_WS('\n\n','Expansión: StormBlood','Parche de salida: 4.4','Item Level Mínimo: 370','Item Level Máximo: 380','Nivel: 70')),
    ('Eden\'s Gate',CONCAT_WS('\n\n','Expansión: ShadowBringers','Parche de salida: 5.0','Sync Item Level : 425','Nivel: 80')),
    ('Eden\'s Gate (Savage)',CONCAT_WS('\n\n','Expansión: ShadowBringers','Parche de salida: 5.0','Item Level Mínimo: 440','Item Level Máximo: 450','Nivel: 80')),
    ('Eden\'s Verse',CONCAT_WS('\n\n','Expansión: ShadowBringers','Parche de salida: 5.2','Sync Item Level: 455','Nivel: 80')),
    ('Eden\'s Verse (Savage)',CONCAT_WS('\n\n','Expansión: ShadowBringers','Parche de salida: 5.2','Item Level Mínimo: 470','Item Level Máximo: 480','Nivel: 80')),
    ('Eden\'s Promise',CONCAT_WS('\n\n','Expansión: ShadowBringers','Parche de salida: 5.4','Sync Item Level: 485','Nivel: 80')),
    ('Eden\'s Promise (Savage)',CONCAT_WS('\n\n','Expansión: ShadowBringers','Parche de salida: 5.4','Item Level Mínimo: 500','Item Level Máximo: 510','Nivel: 80')),
    ('Pandaemonium Asphodelos',CONCAT_WS('\n\n','Expansión: EndWalker','Parche de salida: 6.0','Sync Item Level: 565','Nivel: 90')),
    ('Pandaemonium Asphodelos (Savage)',CONCAT_WS('\n\n','Expansión: ','Parche de salida: 6.0','Item Level Mínimo: 570','Item Level Máximo: 580','Nivel: 90')),
    ('Pandaemonium Abyssos',CONCAT_WS('\n\n','Expansión: EndWalker','Parche de salida: 6.2','Sync Item Level: 585','Nivel: 90')),
    ('Pandaemonium Abyssos (Savage)',CONCAT_WS('\n\n','Expansión: EndWalker','Parche de salida: 6.2','Item Level Mínimo: 600','Item Level Máximo: 610','Nivel: 90')),
    ('Pandaemonium Anabaseios',CONCAT_WS('\n\n','Expansión: EndWalker','Parche de salida: 6.4','Sync Item Level: 615','Nivel: 90')),
    ('Pandaemonium Anabaseios (Savage)',CONCAT_WS('\n\n','Expansión: EndWalker','Parche de salida: 6.4','Item Level Mínimo: 630','Item Level Máximo: 660','Nivel: 90'));

INSERT INTO `usuarios` (`nombre_usuario`, `passwd_usuario`) VALUES
('alex', '4135aa9dc1b842a653dea846903ddb95bfb8c5a10c504a7fa16e10bc31d1fdf0'),
('pepe', '7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834'),
('test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08');

INSERT INTO `actividades` (`id_actividad`, `nombre_actividad`, `descripcion_actividad`, `tipo_actividad`, `passwd_actividad`, `fecha`, `autor`) VALUES
(1, 'Early Omega Prog', 'hello world prog', 5, '7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834', '2024-05-31', 'alex'),
(2, 'Tea Kill Party', 'Fate B into kill', 1, NULL, '2024-06-04', 'pepe'),
(3, 'E8S Prog party', 'I like mirrors', 26, NULL, '2024-06-04', 'pepe'),
(4, 'P8S Prog party', 'ALien Concept Prog', 32, NULL, '2024-07-04', 'alex');

INSERT INTO `horas_disponibles` (`id_actividad`,`id_usuario`,`hora_inicio`,`hora_final`) VALUES
(1,'alex','12:30:00','17:30:00'),
(1,'pepe','16:30:00','18:50:00'),
(2,'alex','15:15:00','18:00:00'),
(2,'pepe','14:15:00','21:15:00'),
(3,'alex','11:00:00','16:00:00'),
(4,'pepe','10:00:00','20:00:00');