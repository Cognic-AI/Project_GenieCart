CREATE DATABASE  IF NOT EXISTS `machine_customer` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `machine_customer`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: machine_customer
-- ------------------------------------------------------
-- Server version	9.0.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
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
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(45) DEFAULT NULL,
  `email` varchar(45) NOT NULL,
  `password` text NOT NULL,
  `generated_key` text NOT NULL,
  `image` text,
  `country` VARCHAR(3) DEFAULT NULL, 
  `price_level` enum('Low','Middle',"High"),
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Jane Smith','jane@email.com','pass456','456',NULL,'AFA','Low'),(2,'Bob Wilson','bob@email.com','pass789','789',NULL,'USA','Middle'),(3,'ben 10','ben@email.com','$2b$10$Vjb62q4PjXRfdI/4ZT6jO.8b1nn0s/.KKj7Lm6SyM4yFZGEm.zlaO','p4z8ga02','https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flipkart.com%2Fwallpaper-ben-10-ultimate-alien-gwen-quality-paper-13x19-print%2Fp%2Fitm7319b909d7388&psig=AOvVaw3iS1sdR0HzNr7fKP2gsOMc&ust=1735120184631000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCIDQmcSQwIoDFQAAAAAdAAAAABAY','AUS','High');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `name` text,
  `price` decimal(10,2) DEFAULT NULL,
  `description` text,
  `link` text,
  `rate` decimal(4,2) DEFAULT NULL,
  `tags` text,
  `image_link` text,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=711 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,'Laptop',999.99,'High performance laptop','laptop.html',4.50,'electronics,computer,dell,silver,intel i7,16gb ram,ssd storage,gaming capable,windows 11,lightweight,backlit keyboard,full hd',NULL),(2,'Smartphone',699.99,'5G enabled phone','phone.html',4.30,'electronics,mobile,samsung,black,5g,dual sim,256gb storage,water resistant,amoled display,fast charging,wireless charging,android',NULL),(3,'Headphones',149.99,'Wireless noise cancelling','headphones.html',4.70,'electronics,audio,sony,black,wireless,noise cancelling,bluetooth 5.0,40mm drivers,voice assistant,foldable,multipoint pairing,high resolution',NULL),(4,'Coffee Maker',79.99,'Programmable coffee machine','coffee.html',4.20,'appliances,kitchen,cuisinart,stainless steel,12 cup capacity,programmable timer,auto shutoff,brew strength control,permanent filter,self cleaning,hot plate,anti drip',NULL),(5,'Running Shoes',89.99,'Lightweight running shoes','shoes.html',4.40,'sports,footwear,nike,blue white,breathable mesh,cushioned sole,arch support,reflective details,moisture wicking,shock absorbing,flexible,anti slip',NULL),(6,'Backpack',49.99,'Durable travel backpack','backpack.html',4.60,'accessories,travel,north face,navy blue,water resistant,laptop compartment,usb charging port,anti theft,padded straps,multiple compartments,breathable back,hidden pockets',NULL),(7,'Watch',199.99,'Smart fitness watch','watch.html',4.30,'electronics,accessories,fitbit,black,heart rate monitor,sleep tracking,water resistant,gps,touchscreen,week long battery,smartphone notifications,stress monitoring',NULL),(8,'Camera',549.99,'Digital SLR camera','camera.html',4.80,'electronics,photography,canon,black,24mp sensor,4k video,wifi enabled,touchscreen lcd,image stabilization,dual pixel autofocus,raw shooting,weather sealed',NULL),(9,'Tablet',399.99,'10-inch display tablet','tablet.html',4.40,'electronics,computer,apple,space gray,retina display,64gb storage,touch id,pencil compatible,10 hour battery,face recognition,stereo speakers,cellular capable',NULL),(10,'Speaker',129.99,'Bluetooth portable speaker','speaker.html',4.20,'electronics,audio,jbl,black,waterproof,bluetooth 5.0,20 hour battery,voice assistant,party boost,usb c charging,built in powerbank,stereo pairing',NULL),(11,'Monitor',299.99,'27-inch 4K monitor','monitor.html',4.60,'electronics,computer,lg,black,4k uhd,ips panel,hdr10,freesync,height adjustable,eye care,multiple inputs,thin bezel',NULL),(12,'Keyboard',89.99,'Mechanical gaming keyboard','keyboard.html',4.50,'electronics,gaming,razer,black,mechanical switches,rgb backlight,macro keys,anti ghosting,wrist rest,multimedia controls,usb passthrough,programmable',NULL),(13,'Mouse',59.99,'Wireless gaming mouse','mouse.html',4.30,'electronics,gaming,logitech,black red,wireless,16000 dpi,programmable buttons,rgb lighting,rechargeable battery,lightweight design,ergonomic grip,quick dpi switching',NULL),(14,'Printer',199.99,'All-in-one printer','printer.html',4.10,'electronics,office,hp,white,wireless printing,scanner,copier,duplex printing,mobile printing,touchscreen,document feeder,borderless printing',NULL),(15,'External HD',129.99,'2TB portable drive','hdd.html',4.40,'electronics,storage,western digital,black,2tb capacity,usb 3.0,password protection,automatic backup,shock resistant,compact size,plug and play,compatible all os',NULL),(16,'Router',149.99,'Mesh WiFi router','router.html',4.50,'electronics,networking,netgear,white,wifi 6,dual band,parental controls,cyber security,easy setup,beamforming,mu mimo,guest network',NULL),(17,'Webcam',79.99,'HD webcam','webcam.html',4.20,'electronics,computer,logitech,black,1080p resolution,auto focus,stereo audio,privacy shutter,low light correction,wide angle,plug and play,noise reduction','https://occ-0-8407-1361.1.nflxso.net/dnm/api/v6/6AYY37jfdO6hpXcMjf9Yu5cnmO0/AAAABR6vn8BtaC8r6FhDOfMCliOri5vm4p5bCnxzV61blyd_QJP0qr8VdYGGyoFxkLfwDc1nDVqf4ilKrmD1XquOAlXD29EyAM4UbC4i.jpg?r=54a'),(18,'Microphone',119.99,'USB condenser microphone','mic.html',4.60,'electronics,audio,blue yeti,silver,condenser,multiple patterns,zero latency,gain control,mute button,desk stand,plug and play,studio quality',NULL),(19,'Power Bank',49.99,'20000mAh portable charger','powerbank.html',3.30,'electronics,accessories,anker,black,20000mah capacity,fast charging,multiple ports,led indicator,compact design,safe charging,airline approved,power delivery',NULL),(20,'USB Hub',39.99,'7-port USB hub','usbhub.html',4.20,'electronics,accessories,anker,black silver,7 ports,usb 3.0,individual switches,led indicators,compact design,data transfer,power adapter,plug and play',NULL);
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_item`
--

DROP TABLE IF EXISTS `search_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_item` (
  `search_id` int NOT NULL,
  `item_id` int NOT NULL,
  `score` decimal(4,2) DEFAULT NULL,
  PRIMARY KEY (`search_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `search_item_ibfk_1` FOREIGN KEY (`search_id`) REFERENCES `search_result` (`search_id`),
  CONSTRAINT `search_item_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_item`
--

LOCK TABLES `search_item` WRITE;
/*!40000 ALTER TABLE `search_item` DISABLE KEYS */;
INSERT INTO `search_item` VALUES (1,1,9.50),(1,2,8.50),(1,3,7.80),(1,7,7.20),(1,9,6.50),(1,12,6.00),(2,4,9.20),(2,5,8.80),(2,6,8.20),(2,8,7.50),(2,10,7.00),(2,14,6.50),(3,11,9.40),(3,13,8.90),(3,15,8.40),(3,16,7.90),(3,17,7.30),(3,18,6.80),(4,1,8.70),(4,3,8.20),(4,5,7.80),(4,7,7.30),(4,9,7.00),(4,19,9.60),(4,20,9.10);
/*!40000 ALTER TABLE `search_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_result`
--

DROP TABLE IF EXISTS `search_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_result` (
  `search_id` int NOT NULL AUTO_INCREMENT,
  `time_stamp` timestamp NULL DEFAULT NULL,
  `customer_id` int NOT NULL,
  PRIMARY KEY (`search_id`),
  KEY `customer_id_idx` (`customer_id`),
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_result`
--

LOCK TABLES `search_result` WRITE;
/*!40000 ALTER TABLE `search_result` DISABLE KEYS */;
INSERT INTO `search_result` VALUES (1,'2024-01-15 10:30:00',1),(2,'2024-01-15 14:45:00',2),(3,'2024-01-16 09:15:00',3),(4,'2024-01-16 16:20:00',1),(7,'2024-12-17 03:58:06',2),(8,'2024-12-17 03:58:51',2);
/*!40000 ALTER TABLE `search_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'machine_customer'
--

--
-- Dumping routines for database 'machine_customer'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-24 15:44:41
