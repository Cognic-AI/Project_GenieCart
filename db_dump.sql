CREATE DATABASE  IF NOT EXISTS `machine_customer` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `machine_customer`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: machine_customer
-- ------------------------------------------------------
-- Server version	8.0.38

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
  `country` varchar(3) DEFAULT NULL,
  `price_level` enum('Low','Middle','High') DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (3,'ben 10','ben@email.com','$2b$10$Vjb62q4PjXRfdI/4ZT6jO.8b1nn0s/.KKj7Lm6SyM4yFZGEm.zlaO','p4z8ga02','https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flipkart.com%2Fwallpaper-ben-10-ultimate-alien-gwen-quality-paper-13x19-print%2Fp%2Fitm7319b909d7388&psig=AOvVaw3iS1sdR0HzNr7fKP2gsOMc&ust=1735120184631000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCIDQmcSQwIoDFQAAAAAdAAAAABAY','AUS','High'),(10,'John Silva','akinduhiman2@gmail.com','$2b$10$fuEqkYrEXG3R9pjUUEgTfOwTmttX/DzjNtb0tauO5MGqxcrr5stby','G6QJ6DDNI0C9','https://i.pinimg.com/originals/97/31/02/9731022f0be7c965e880505461643850.jpg','US','Middle');
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
) ENGINE=InnoDB AUTO_INCREMENT=729 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (716,'Classico Italian Sausage Spaghetti Pasta Sauce with Tomato, Peppers & Onions (24 oz Jar)',2.79,'Classico Italian Sausage With Peppers & Onions Pasta Sauce adds authentic Italian flavor to recipes. Blend tomato puree and green bell peppers with Italian sausage, garlic, onion and spices. Serve over baked ziti or in pasta bake. Packaged in a resealable & reusable Mason jar. Refrigerate Classico pasta sauce after opening.','https://www.amazon.com/Classico-Italian-Sausage-Peppers-Onions/dp/B000RY88VC',4.60,'classico,pasta,sauce,italian,sausage,tomato,peppers,onions,24,oz,jar','https://m.media-amazon.com/images/I/41x6q3FKmiL._SX300_SY300_QL70_ML2_.jpg'),(717,'Prego Traditional No Sugar Added Pasta Sauce, 23.5 Oz Jar',2.48,'Be the hero at dinner with Prego Traditional No Sugar Added Pasta Sauce. Versatile and delicious, this classic red sauce features the rich, sweet taste of vine-ripened tomatoes balanced with flavorful herbs and seasonings, with no sugar added (1). This pasta sauce has a taste everyone loves and a thick texture that doesn’t water out, making it a perfect pairing with any pasta. Prego pasta sauce is gluten free, vegan and made without artificial colors or added MSG for a spaghetti sauce you can feel good about. Top off any pasta with this Prego Italian sauce for a quick, family-pleasing meal, or use it as a base for your favorite recipes. The tomato sauce jar top is easy to close and store in the refrigerator for leftovers. Give your family the taste everyone loves with Prego sauces. In addition to Traditional No Sugar Added Pasta Sauce, Prego offers a variety of favorites, including Chunky Tomato, Garlic and Onion Italian, Low FODMAP and more! (1) Not a calorie reduced food. See nutrition facts panel for sugar and calorie content','https://www.amazon.com/Prego-Pasta-Sauce-Sugar-Traditional/dp/B07DFRQLNQ/ref=zg_bs_g_6465030011_d_sccl_9/130-0780116-4726006?psc=1',4.60,'prego,pasta,sauce,traditional,no,sugar,added,23.5,oz,jar,gluten-free,vegan','https://m.media-amazon.com/images/I/41t8PN4cYmL._SX300_SY300_QL70_ML2_.jpg'),(718,'Prego Traditional Sensitive Recipe Low FODMAP Pasta Sauce, 23.75 Oz Jar',2.79,'One (1) 23.75 oz jar of Prego Traditional Sensitive Recipe Low FODMAP Pasta Sauce  Low FODMAP spaghetti sauce with thickness you can see and a taste that everyone loves, without garlic and onions that may cause stomach sensitivities  This Prego sauce features the rich, sweet taste of vine-ripened tomatoes balanced with flavorful herbs and seasonings  Each half cup serving of this gluten free, vegan sauce is a good source of fiber, and does not contain artificial colors or added MSG  Makes a great spaghetti sauce, bolognese sauce or base to other recipes','https://www.amazon.com/Prego-Traditional-Italian-Sensitive-Recipe/dp/B07DFQMRRR/ref=zg_bs_g_6465030011_d_sccl_10/130-0780116-4726006?psc=1',4.50,'prego,pasta,sauce,low,fodmap,sensitive,traditional,23.75,oz,jar,gluten-free,vegan','https://m.media-amazon.com/images/I/41XMbVUY0yL._SX300_SY300_QL70_ML2_.jpg'),(719,'Muir Glen Organic Tomato Sauce, 15 oz. (Pack of 12)',45.99,'Add big flavor to your homemade pasta sauce or favorite soup recipe with Muir Glen Organic Tomato Sauce. This tomato sauce is made with vine-sweetened tomatoes for the perfect taste. Muir Glen organic tomatoes are grown in the soil of California and are perfectly pureed and lightly salted to create rich and creamy tomato sauce. USDA Certified Organic, Non-GMO Project Verified and gluten free, Muir Glen Organic Tomato Sauce is the perfect addition to shakshuka, ratatouille, pizza sauce or your favorite sloppy joes. Muir Glen organic tomatoes fresh from the vine are an easy and delicious way to upgrade your favorite recipes. These organic tomatoes are grown in California and are canned quickly for peak freshness.','https://www.amazon.com/Muir-Glen-Organic-Tomato-Sauce/dp/B000LKXG64',4.50,'muir,glen,organic,tomato,sauce,15,oz,pack,12,california','https://m.media-amazon.com/images/I/5144XKEr9SL._SX300_SY300_QL70_ML2_.jpg'),(720,'KC Natural | Traditional Style Tomato Free Pasta Sauce | 280mg Sodium (2-pack, 1.00)',21.99,'Tomato Free, Vegan, 280mg of Sodium Per Serv., Paleo AIP, Refined Sugar Free, Nightshade Free','https://www.amazon.com/KC-Natural-Traditional-Tomato-Sodium/dp/B0BD5LCJ64',4.00,'kc,natural,pasta,sauce,tomato,free,vegan,280mg,sodium,2-pack,paleo,aip,refined,sugar,free,nightshade,free','https://m.media-amazon.com/images/I/41-nFAGxf8L._SX300_SY300_QL70_ML2_.jpg'),(721,'Amazon Fresh Brand, Gold Potatoes, 5 Lb',14.99,'5-pound bag of gold potatoes\n\nNo preservatives\n\nGrown in the United States\n\nGood for roasting, pan-frying, and smashing\n\nOur Fresh brand products are all about high-quality food that fits every budget, every day.\n\nAn Amazon Brand','https://www.amazon.com/Fresh-Brand-Gold-Potatoes/dp/B07XW1GNZL',4.70,'potatoes,gold,amazon,fresh,5lb,roasting,pan-frying,smashing','https://m.media-amazon.com/images/I/41ioG9K7DHL._SY300_SX300_QL70_ML2_.jpg'),(722,'POTATOES RUSSET FRESH PRODUCE 10 LBS',14.98,'Russet potatoes are high in starch. Russet are perfect to cook mashed potatoes and also are good for baking.','https://www.amazon.com/POTATOES-RUSSET-FRESH-PRODUCE-LBS/dp/B00B8SZWCO',4.00,'potatoes,russet,fresh,produce,10lbs,mashed,baking','https://m.media-amazon.com/images/I/31nbqyyeRpL._QL70_ML2_.jpg'),(723,'Premium Quality White Potatoes 10Lbs',17.99,'Farm Fresh USDA #1 / Premium Quality White Potatoes 10Lbs Medium Size (B Size Potatoes 1.5 - 2.25 Inches In Diameter)  These Are White Potatoes, A Popular Variety Known For Their Buttery Flavor And Versatility In Various Dishes. With Their Thin, Smooth Skin And Creamy White Flesh, These Potatoes Have A Velvety Texture When Cooked  Suitable For Baking, Roasting, Mashing, Smashing, Or Frying, Yukon Golds Hold Their Shape Well During Cooking  Grown In The United States','https://www.amazon.com/Premium-Quality-White-Potatoes-10Lbs/dp/B0DFF4GJ8F',0.00,'potatoes,white,premium,quality,10lbs,medium,farmfresh,versatile','https://m.media-amazon.com/images/I/31wvIrCUqPL._SX300_SY300_QL70_ML2_.jpg'),(724,'Russet Idaho Potatoes Fresh Premium Fruit and Produce Vegetables, 4 pound case',26.59,'Despite the popular misconception that potatoes are fattening, baked potatoes can be used as part of a healthy diet','https://www.amazon.com/Russet-Potatoes-Premium-Produce-Vegetables/dp/B00B0M2WZ8',3.70,'potatoes,russet,idaho,fresh,premium,produce,vegetables,4lb','https://m.media-amazon.com/images/I/21-iecFuJ8L._QL70_ML2_.jpg'),(725,'50 Pound Box of Famous Idaho Russet Potatoes/ 80 Potatoes by Wilcox Farms',24.70,'50 Pound Box of Famous Idaho Russet Potatoes/ 80 Potatoes by Wilcox Farms','https://www.amazon.com/Famous-Russet-Potatoes-Wilcox-Farms/dp/B00A0ZS5FC',3.30,'potatoes,russet,idaho,wilcoxfarms,50lb,bulk','https://m.media-amazon.com/images/I/51UxLA5L+bL._SY300_SX300_QL70_ML2_.jpg'),(726,'Generic Yukon Gold Fresh Yellow Potatoes, USA GROWN, NON-GMO, Bulk (5 Pounds)',25.95,'Yukon Gold potatoes are a versatile and delicious variety that have become a staple in many kitchens. These potatoes have a smooth, buttery texture and a rich, creamy flavor that sets them apart from other varieties. Their thin, golden skin and bright yellow flesh make them visually appealing, while their low to medium starch content ensures they hold their shape well during cooking. Yukon Golds are perfect for roasting, mashing, baking, or frying into crispy fries or potato wedges. Whether you\'re looking to add a burst of flavor to your classic potato dishes or experiment with new recipes, these potatoes are a reliable choice. With their excellent taste and texture, Yukon Golds are sure to become a go-to ingredient in your kitchen.','https://www.amazon.com/Generic-Yellow-Potatoes-NON-GMO-Pounds/dp/B0D6M2HW23',2.40,'potatoes,yukon gold,yellow,fresh,usa,non-gmo,bulk,5lbs','https://m.media-amazon.com/images/I/51m5H0SFcbL._SX300_SY300_QL70_ML2_.jpg'),(727,'Potatoes Fresh Idaho Russet and Red Produce Bundle',31.49,'Brand: Idaho 08/21/2017\nNumber of Items: 2\nUnit Count: 10 pound\nTemperature Condition: Fresh\nSpecialty: No Preservatives','https://www.amazon.com/Potatoes-Idaho-Russet-Produce-Bundle/dp/B00NS3RCNE',2.90,'potatoes,russet,red,idaho,fresh,produce,bundle,10lb','https://m.media-amazon.com/images/I/51hutf+vxrL._SY300_SX300_.jpg'),(728,'Organic Fresh Russet Potatoes by RawJoy Farms',45.00,'Russet potatoes are a versatile and beloved staple in kitchens across America. These oblong, brown-skinned tubers boast a fluffy, starchy flesh that lends itself beautifully to baking, mashing, and frying. Russets are prized for their ability to achieve a crispy exterior and light, airy interior when baked or fried, making them the perfect choice for classic dishes like french fries, baked potatoes, and hash browns. Their robust flavor and texture also shine in hearty stews, soups, and casseroles. Whether you\'re craving a comforting side dish or a satisfying main course, these all-purpose potatoes are an excellent choice for their reliability and crowd-pleasing taste.','https://www.amazon.com/Organic-Fresh-Russet-Potatoes-RawJoy/dp/B0DDHXC3VD',0.00,'potatoes,russet,organic,fresh,rawjoyfarms,baking,mashing,frying','https://m.media-amazon.com/images/I/41qyVbgpoPL._SY300_SX300_QL70_ML2_.jpg');
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
INSERT INTO `search_item` VALUES (37,716,10.05),(37,717,9.08),(37,718,8.97),(37,719,5.60),(37,720,5.58),(38,721,10.16),(38,722,9.60),(38,723,5.65),(38,724,5.63),(38,725,4.76),(38,726,4.72),(38,727,4.47),(38,728,2.00);
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
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_result`
--

LOCK TABLES `search_result` WRITE;
/*!40000 ALTER TABLE `search_result` DISABLE KEYS */;
INSERT INTO `search_result` VALUES (37,'2025-01-03 08:11:50',10),(38,'2025-01-03 10:03:17',10);
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

-- Dump completed on 2025-01-03 16:05:53
