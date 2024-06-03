-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-06-2024 a las 10:04:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `when2raid`
--
CREATE DATABASE IF NOT EXISTS `when2raid` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `when2raid`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividades`
--

CREATE TABLE `actividades` (
  `id_actividad` int(11) NOT NULL,
  `nombre_actividad` varchar(64) NOT NULL,
  `descripcion_actividad` varchar(128) DEFAULT NULL,
  `tipo_actividad` int(11) DEFAULT NULL,
  `passwd_actividad` varchar(64) DEFAULT NULL,
  `fecha` date NOT NULL,
  `autor` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividades`
--

INSERT INTO `actividades` (`id_actividad`, `nombre_actividad`, `descripcion_actividad`, `tipo_actividad`, `passwd_actividad`, `fecha`, `autor`) VALUES
(1, 'Early Omega Prog', 'hello world prog', 5, '7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834', '2024-05-31', 'alex'),
(2, 'Tea Kill Party', 'Fate B into kill', 1, NULL, '2024-06-04', 'pepe'),
(3, 'test', 'no se lol', 32, NULL, '2024-06-03', 'alex'),
(5, 'test apuntar 2', 'ayuda', 32, NULL, '2024-06-04', 'pepe'),
(6, 'test apuntar 3', 'autocritica y seguimos pa alante', 34, NULL, '2024-07-16', 'pepe');

--
-- Disparadores `actividades`
--
DELIMITER $$
CREATE TRIGGER `log_insert_actividad` AFTER INSERT ON `actividades` FOR EACH ROW BEGIN
    INSERT INTO log_actividades (id_actividad,usuario,fecha) VALUES (NEW.id_actividad,NEW.autor,CURRENT_TIMESTAMP());
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horas_disponibles`
--

CREATE TABLE `horas_disponibles` (
  `id_actividad` int(11) NOT NULL,
  `id_usuario` varchar(16) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_final` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horas_disponibles`
--

INSERT INTO `horas_disponibles` (`id_actividad`, `id_usuario`, `hora_inicio`, `hora_final`) VALUES
(1, 'alex', '22:30:00', '23:55:00'),
(2, 'pepe', '10:45:00', '21:35:00'),
(2, 'alex', '17:45:00', '21:35:00'),
(3, 'alex', '18:00:00', '23:00:00'),
(5, 'pepe', '04:00:00', '08:00:00'),
(6, 'pepe', '12:00:00', '20:00:00'),
(1, 'pepe', '01:00:00', '22:00:00'),
(3, 'pepe', '17:40:00', '22:10:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `log_actividades`
--

CREATE TABLE `log_actividades` (
  `id_log` int(11) NOT NULL,
  `id_actividad` int(11) NOT NULL,
  `usuario` varchar(16) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `log_actividades`
--

INSERT INTO `log_actividades` (`id_log`, `id_actividad`, `usuario`, `fecha`) VALUES
(1, 1, 'alex', '2024-05-30 14:04:11'),
(2, 2, 'pepe', '2024-05-30 14:04:11'),
(3, 3, 'alex', '2024-05-30 14:04:58'),
(4, 4, 'alex', '2024-05-31 07:45:49'),
(5, 5, 'pepe', '2024-05-31 10:05:43'),
(6, 6, 'pepe', '2024-05-31 10:08:55'),
(7, 7, 'pepe', '2024-05-31 10:12:03'),
(8, 8, 'pepe', '2024-05-31 10:13:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `log_usuarios`
--

CREATE TABLE `log_usuarios` (
  `id_log` int(11) NOT NULL,
  `nombre_usuario` varchar(16) DEFAULT user(),
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `log_usuarios`
--

INSERT INTO `log_usuarios` (`id_log`, `nombre_usuario`, `fecha`) VALUES
(1, 'alex', '2024-05-30 14:04:11'),
(2, 'pepe', '2024-05-30 14:04:11'),
(3, 'test', '2024-05-30 14:04:11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos`
--

CREATE TABLE `tipos` (
  `id_tipo` int(11) NOT NULL,
  `nombre_tipo` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipos`
--

INSERT INTO `tipos` (`id_tipo`, `nombre_tipo`) VALUES
(1, "The Epic of Alexander (Ultimate)"),
(2, "The Unending Coil of Bahamut (Ultimate)"),
(3, "The Weapon's Refrain (Ultimate)"),
(4, "Dragonsong's Reprise (Ultimate)"),
(5, "The Omega Protocol (Ultimate)"),
(6, "Futures Rewritten (Ultimate)"),
(7, "The Binding Coil of Bahamut"),
(8, "The Second Coil of Bahamut"),
(9, "The Second Coil of Bahamut (Savage)"),
(10, "The Final Coil of Bahamut"),
(11, "Alexander: Gordias"),
(12, "Alexander: Gordias (Savage)"),
(13, "Alexander: Midas"),
(14, "Alexander: Midas (Savage)"),
(15, "Alexander: The Creator"),
(16, "Alexander: The Creator (Savage)"),
(17, "Omega: Deltascape"),
(18, "Omega: Deltascape (Savage)"),
(19, "Omega: Sigmascape"),
(20, "Omega: Sigmascape (Savage)"),
(21, "Omega: Alphascape"),
(22, "Omega: Alphascape (Savage)"),
(23, "Eden's Gate"),
(24, "Eden's Gate (Savage)"),
(25, "Eden's Verse"),
(26, "Eden's Verse (Savage)"),
(27, "Eden's Promise"),
(28, "Eden's Promise (Savage)"),
(29, "Pandaemonium: Asphodelos"),
(30, "Pandaemonium: Asphodelos (Savage)"),
(31, "Pandaemonium: Abyssos"),
(32, "Pandaemonium: Abyssos (Savage)"),
(33, "Pandaemonium: Anabaseios"),
(34, "Pandaemonium: Anabaseios (Savage)	");

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `nombre_usuario` varchar(16) NOT NULL,
  `passwd_usuario` varchar(64) NOT NULL,
  `nombre_completo` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`nombre_usuario`, `passwd_usuario`, `nombre_completo`) VALUES
('alex', '4135aa9dc1b842a653dea846903ddb95bfb8c5a10c504a7fa16e10bc31d1fdf0', 'alex'),
('pepe', '7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834', 'pepe'),
('test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'test');

--
-- Disparadores `usuarios`
--
DELIMITER $$
CREATE TRIGGER `log_insert_usuario` AFTER INSERT ON `usuarios` FOR EACH ROW BEGIN
    INSERT INTO log_usuarios (nombre_usuario,fecha) VALUES (NEW.nombre_usuario,CURRENT_TIMESTAMP());
END
$$
DELIMITER ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividades`
--
ALTER TABLE `actividades`
  ADD PRIMARY KEY (`id_actividad`),
  ADD KEY `tipo_actividad` (`tipo_actividad`),
  ADD KEY `autor` (`autor`);

--
-- Indices de la tabla `horas_disponibles`
--
ALTER TABLE `horas_disponibles`
  ADD KEY `id_actividad` (`id_actividad`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `log_actividades`
--
ALTER TABLE `log_actividades`
  ADD PRIMARY KEY (`id_log`);

--
-- Indices de la tabla `log_usuarios`
--
ALTER TABLE `log_usuarios`
  ADD PRIMARY KEY (`id_log`);

--
-- Indices de la tabla `tipos`
--
ALTER TABLE `tipos`
  ADD PRIMARY KEY (`id_tipo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`nombre_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividades`
--
ALTER TABLE `actividades`
  MODIFY `id_actividad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `log_actividades`
--
ALTER TABLE `log_actividades`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `log_usuarios`
--
ALTER TABLE `log_usuarios`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tipos`
--
ALTER TABLE `tipos`
  MODIFY `id_tipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividades`
--
ALTER TABLE `actividades`
  ADD CONSTRAINT `actividades_ibfk_1` FOREIGN KEY (`tipo_actividad`) REFERENCES `tipos` (`id_tipo`),
  ADD CONSTRAINT `actividades_ibfk_2` FOREIGN KEY (`autor`) REFERENCES `usuarios` (`nombre_usuario`);

--
-- Filtros para la tabla `horas_disponibles`
--
ALTER TABLE `horas_disponibles`
  ADD CONSTRAINT `horas_disponibles_ibfk_1` FOREIGN KEY (`id_actividad`) REFERENCES `actividades` (`id_actividad`),
  ADD CONSTRAINT `horas_disponibles_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`nombre_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
