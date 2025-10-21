-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: pizza_ordering
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `birthdate` date NOT NULL,
  `address` varchar(255) NOT NULL,
  `postcode` varchar(20) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `pizzas_ordered_count` int NOT NULL DEFAULT '0',
  CONSTRAINT uq_customer_name UNIQUE (name, address),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DELIMITER $$

CREATE TRIGGER before_customer_insert
BEFORE INSERT ON customer
FOR EACH ROW
BEGIN
  IF NEW.birthdate > CURDATE() THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Birthdate cannot be in the future';
  END IF;
END$$

CREATE TRIGGER before_customer_update
BEFORE UPDATE ON customer
FOR EACH ROW
BEGIN
  IF NEW.birthdate > CURDATE() THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Birthdate cannot be in the future';
  END IF;
END$$

DELIMITER ;



--
-- Table structure for table `deliveryperson`
--

DROP TABLE IF EXISTS `deliveryperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveryperson` (
  `id` int NOT NULL,
  `postcode` varchar(20) NOT NULL,
  `available` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  CONSTRAINT `deliveryperson_ibfk_1` FOREIGN KEY (`id`) REFERENCES `staff` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliveryperson`
--

LOCK TABLES `deliveryperson` WRITE;
/*!40000 ALTER TABLE `deliveryperson` DISABLE KEYS */;
INSERT INTO `deliveryperson` VALUES (7,'00100',1),(8,'20100',1);
/*!40000 ALTER TABLE `deliveryperson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dessert`
--

DROP TABLE IF EXISTS `dessert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dessert` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `cost` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `dessert_chk_1` CHECK ((`cost` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dessert`
--

LOCK TABLES `dessert` WRITE;
/*!40000 ALTER TABLE `dessert` DISABLE KEYS */;
INSERT INTO `dessert` VALUES (1,'Tiramisu',3.50),(2,'Panna Cotta',3.00),(3,'Gelato',2.80);
/*!40000 ALTER TABLE `dessert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discountcode`
--

DROP TABLE IF EXISTS `discountcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discountcode` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `is_valid` tinyint(1) NOT NULL DEFAULT '1',
  `expiry_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discountcode`
--

LOCK TABLES `discountcode` WRITE;
/*!40000 ALTER TABLE `discountcode` DISABLE KEYS */;
INSERT INTO `discountcode` VALUES (1,'WELCOME10',1,'2025-12-31'),(2,'BIRTHDAYFREE',1,'2026-01-01'),(3,'LOYALTY2025',1,'2025-12-31');
/*!40000 ALTER TABLE `discountcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drink`
--

DROP TABLE IF EXISTS `drink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drink` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `cost` decimal(5,2) NOT NULL,
  `is_alcoholic` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `drink_chk_1` CHECK ((`cost` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drink`
--

LOCK TABLES `drink` WRITE;
/*!40000 ALTER TABLE `drink` DISABLE KEYS */;
INSERT INTO `drink` VALUES (1,'Coca Cola',2.00,0),(2,'Sparkling Water',1.50,0),(3,'Beer',3.50,1),(4,'Red Wine',4.50,1);
/*!40000 ALTER TABLE `drink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredient`
--

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `cost` decimal(5,2) NOT NULL,
  `is_vegan` tinyint(1) NOT NULL,
  `is_vegetarian` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `ingredient_chk_1` CHECK ((`cost` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'Tomato Sauce',0.50,1,1),(2,'Mozzarella',1.00,0,1),(3,'Pepperoni',1.50,0,0),(4,'Basil',0.20,1,1),(5,'Mushrooms',0.70,1,1),(6,'Onions',0.40,1,1),(7,'Ham',1.40,0,0),(8,'Pineapple',0.80,1,1),(9,'Olives',0.60,1,1),(10,'Vegan Cheese',1.20,1,1);
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `delivery_id` int DEFAULT NULL,
  `order_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','in preparation','prepared','in delivery','delivered','cancelled') NOT NULL DEFAULT 'pending',
  `total` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `delivery_id` (`delivery_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`delivery_id`) REFERENCES `deliveryperson` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,1,NULL,'2025-09-29 17:00:20','delivered',12.50),(2,1,NULL,'2025-09-29 17:00:20','delivered',18.20),(3,1,NULL,'2025-09-29 17:00:20','in delivery',9.80),(4,1,NULL,'2025-09-29 17:00:20','pending',15.00),(5,1,NULL,'2025-09-29 17:00:20','cancelled',7.50),(6,2,NULL,'2025-09-29 17:00:20','delivered',20.00),(7,2,NULL,'2025-09-29 17:00:20','in delivery',14.50),(8,2,NULL,'2025-09-29 17:00:20','prepared',16.30),(9,2,NULL,'2025-09-29 17:00:20','delivered',25.00),(10,2,NULL,'2025-09-29 17:00:20','pending',11.80),(11,3,NULL,'2025-09-29 17:00:20','delivered',22.50),(12,3,NULL,'2025-09-29 17:00:20','in delivery',17.00),(13,3,NULL,'2025-09-29 17:00:20','delivered',19.80),(14,3,NULL,'2025-09-29 17:00:20','pending',13.20),(15,3,NULL,'2025-09-29 17:00:20','prepared',21.50),(16,4,NULL,'2025-09-29 17:00:20','delivered',15.50),(17,4,NULL,'2025-09-29 17:00:20','in delivery',12.70),(18,4,NULL,'2025-09-29 17:00:20','delivered',23.00),(19,4,NULL,'2025-09-29 17:00:20','pending',18.40),(20,4,NULL,'2025-09-29 17:00:20','cancelled',9.50);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderdiscount`
--

DROP TABLE IF EXISTS `orderdiscount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderdiscount` (
  `order_id` int NOT NULL,
  `discount_id` int NOT NULL,
  PRIMARY KEY (`order_id`,`discount_id`),
  KEY `discount_id` (`discount_id`),
  CONSTRAINT `orderdiscount_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `orderdiscount_ibfk_2` FOREIGN KEY (`discount_id`) REFERENCES `discountcode` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderdiscount`
--

LOCK TABLES `orderdiscount` WRITE;
/*!40000 ALTER TABLE `orderdiscount` DISABLE KEYS */;
INSERT INTO `orderdiscount` VALUES (1,1),(11,1),(6,2),(18,2),(2,3);
/*!40000 ALTER TABLE `orderdiscount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitem` (
  `order_id` int NOT NULL,
  `product_type` enum('pizza','drink','dessert') NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`order_id`,`product_type`,`product_id`),
  CONSTRAINT `orderitem_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `orderitem_chk_1` CHECK ((`quantity` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitem`
--

LOCK TABLES `orderitem` WRITE;
/*!40000 ALTER TABLE `orderitem` DISABLE KEYS */;
INSERT INTO `orderitem` VALUES (1,'pizza',1,1),(1,'drink',1,1),(1,'dessert',1,1),(2,'pizza',2,2),(2,'drink',3,1),(3,'pizza',3,1),(4,'pizza',5,1),(4,'dessert',2,1),(5,'pizza',1,1),(6,'pizza',2,1),(6,'drink',2,2),(7,'pizza',3,2),(8,'pizza',4,1),(8,'drink',4,1),(8,'dessert',3,1),(9,'pizza',5,1),(9,'drink',1,1),(10,'pizza',1,1),(11,'pizza',5,1),(11,'dessert',3,1),(12,'pizza',1,2),(12,'drink',2,1),(13,'pizza',2,1),(13,'dessert',1,1),(14,'pizza',3,1),(14,'drink',1,1),(15,'pizza',4,1),(16,'pizza',1,1),(16,'dessert',2,1),(17,'pizza',2,1),(17,'drink',3,1),(18,'pizza',5,1),(18,'dessert',3,1),(19,'pizza',3,2),(20,'pizza',4,1),(20,'drink',1,1);
/*!40000 ALTER TABLE `orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza`
--

DROP TABLE IF EXISTS `pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza`
--

LOCK TABLES `pizza` WRITE;
/*!40000 ALTER TABLE `pizza` DISABLE KEYS */;
INSERT INTO `pizza` VALUES (3,'Funghi'),(4,'Hawaiian'),(1,'Margherita'),(2,'Pepperoni'),(5,'Vegan Special');
/*!40000 ALTER TABLE `pizza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizzaingredient`
--

DROP TABLE IF EXISTS `pizzaingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizzaingredient` (
  `pizza_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  PRIMARY KEY (`pizza_id`,`ingredient_id`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `pizzaingredient_ibfk_1` FOREIGN KEY (`pizza_id`) REFERENCES `pizza` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pizzaingredient_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizzaingredient`
--

LOCK TABLES `pizzaingredient` WRITE;
/*!40000 ALTER TABLE `pizzaingredient` DISABLE KEYS */;
INSERT INTO `pizzaingredient` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(1,2),(2,2),(3,2),(4,2),(2,3),(1,4),(5,4),(3,5),(3,6),(4,7),(4,8),(5,9),(5,10);
/*!40000 ALTER TABLE `pizzaingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `pizzamenu`
--

DROP TABLE IF EXISTS `pizzamenu`;
/*!50001 DROP VIEW IF EXISTS `pizzamenu`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `pizzamenu` AS SELECT 
 1 AS `pizza_id`,
 1 AS `pizza_name`,
 1 AS `price`,
 1 AS `is_vegan`,
 1 AS `is_vegetarian`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `role` enum('chef','driver','cashier','manager') NOT NULL,
  `salary` decimal(8,2) NOT NULL,
  `birthdate` date NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `staff_chk_1` CHECK ((`salary` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (6,'Giovanni Verdi','male','chef',2500.00,'1980-06-15'),(7,'Luca Neri','male','driver',1800.00,'1990-02-20'),(8,'Giulia Rosa','female','driver',1850.00,'1992-08-05'),(9,'Sofia Blu','female','manager',3000.00,'1975-03-25'),(10,'Marco Gialli','male','cashier',1700.00,'1988-11-10');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `pizzamenu`
--

/*!50001 DROP VIEW IF EXISTS `pizzamenu`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `pizzamenu` AS select `p`.`id` AS `pizza_id`,`p`.`name` AS `pizza_name`,round((((sum(`i`.`cost`) * 1.4) * 1.09) + 5),2) AS `price`,min((case when (`i`.`is_vegan` = false) then 0 else 1 end)) AS `is_vegan`,min((case when (`i`.`is_vegetarian` = false) then 0 else 1 end)) AS `is_vegetarian` from ((`pizza` `p` join `pizzaingredient` `pi` on((`p`.`id` = `pi`.`pizza_id`))) join `ingredient` `i` on((`pi`.`ingredient_id` = `i`.`id`))) group by `p`.`id`,`p`.`name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-29 19:28:33
