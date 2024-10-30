-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 30-10-2024 a las 19:38:09
-- Versión del servidor: 5.7.44-log
-- Versión de PHP: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `techcafe`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos_del_pedido`
--

CREATE TABLE `articulos_del_pedido` (
  `identificacion` int(8) NOT NULL,
  `id_del_pedido` int(8) NOT NULL,
  `id_del_producto` int(8) NOT NULL,
  `cantidad` int(4) NOT NULL,
  `precio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenes`
--

CREATE TABLE `ordenes` (
  `identificacion` int(8) NOT NULL,
  `id_de_usuario` int(8) NOT NULL,
  `precio_total` int(11) NOT NULL,
  `estado` text COLLATE utf8_spanish_ci NOT NULL,
  `direccion_de_entrega` text COLLATE utf8_spanish_ci NOT NULL,
  `creado_en` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(8) NOT NULL,
  `nombre` text COLLATE utf8_spanish_ci NOT NULL,
  `descripcion` text COLLATE utf8_spanish_ci NOT NULL,
  `precio` int(11) NOT NULL,
  `categoria` text COLLATE utf8_spanish_ci NOT NULL,
  `existencias` int(4) NOT NULL,
  `creado_en` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `correo` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `clave` varchar(200) COLLATE utf8_spanish_ci NOT NULL,
  `fechareg` datetime NOT NULL,
  `perfil` char(1) COLLATE utf8_spanish_ci NOT NULL DEFAULT 'U'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `correo`, `clave`, `fechareg`, `perfil`) VALUES
(1, 'asda', 'asfafafa@gmail.com', 'scrypt:32768:8:1$xjhsx4Q9Ee7OJYBk$2c57589c006020b639bdcab448c3fb592662813098c11feaf9a75453a50386059a7a398a74f7e8249e8ffe72c466ea9c00a2b1df519203900f961ae7d18684e1', '2024-09-24 09:58:00', 'U'),
(2, 'asfcas', 'andres.rojas1816@alumnos.udg.mx', 'scrypt:32768:8:1$CocrhxxIohcdT1Yq$8f292aa7c388fc908b80d26c9119d3a31a9d326408adc64a16ae051acf2cd48c534abd17afbbed43c3c51bfcf26aee04f67381ee150d0ae6cd07da5c971d96ca', '2024-10-03 09:54:30', 'A'),
(3, 'Nigger', 'dihaos@gmail.com', 'scrypt:32768:8:1$B3Uay9WdO4OlSFyV$dd334beae258b4d41c09eb72080cd1e52ac17c6f1e855b054fb511a84e05e596d311b8ecc2df084b2268d957b86e53ef7dab9278fc05c75ea6d5d49f9ee41295', '2024-10-17 10:49:34', 'U'),
(4, 'Yael', 'nigger@gmail.com', 'scrypt:32768:8:1$f132Hn13NoC5caKY$3d63bb072419d0b4e998919771543e4fbb3fda77aa297177f4f801041bb80a62ea8c68d344d7079b4e335853f9adb804d5b44b6da913524f2275483bb7c16a00', '2024-10-17 10:49:55', 'U');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `articulos_del_pedido`
--
ALTER TABLE `articulos_del_pedido`
  ADD PRIMARY KEY (`identificacion`),
  ADD KEY `id_del_pedido` (`id_del_pedido`),
  ADD KEY `id_del_producto` (`id_del_producto`);

--
-- Indices de la tabla `ordenes`
--
ALTER TABLE `ordenes`
  ADD PRIMARY KEY (`identificacion`),
  ADD KEY `id_de_usuario` (`id_de_usuario`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `articulos_del_pedido`
--
ALTER TABLE `articulos_del_pedido`
  MODIFY `identificacion` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ordenes`
--
ALTER TABLE `ordenes`
  MODIFY `identificacion` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `articulos_del_pedido`
--
ALTER TABLE `articulos_del_pedido`
  ADD CONSTRAINT `articulos_del_pedido_ibfk_1` FOREIGN KEY (`id_del_producto`) REFERENCES `productos` (`id_producto`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `ordenes`
--
ALTER TABLE `ordenes`
  ADD CONSTRAINT `ordenes_ibfk_1` FOREIGN KEY (`id_de_usuario`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `ordenes_ibfk_2` FOREIGN KEY (`identificacion`) REFERENCES `articulos_del_pedido` (`id_del_pedido`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
