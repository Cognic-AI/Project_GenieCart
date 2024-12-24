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
  `generated_key` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `generated_key_UNIQUE` (`generated_key`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (2,'John Doe','john@email.com','pass123','jhone123'),(3,'Jane Smith','jane@email.com','pass456','jane456'),(4,'Bob Wilson','bob@email.com','pass789','bon789'),(5,'Akindu Himan','akinduhiman2@gmail.com','$2b$10$OS6yXQDMiM7usWyYXLpkg.h5QaE89daAQRoDUx1eIc3/igI67V88e','nos9qkca');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `customer_id` int NOT NULL,
  `item_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`customer_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `description` text,
  `link` text,
  `rate` decimal(4,2) DEFAULT NULL,
  `tags` text,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=356 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (338,'High quality A4 size newly arrived multi-purpose copy paper 80gsm premium office computer paper white copy paper',1.50,'High Quality A4 Size Newly Arrived Multi-purpose Copy Paper 80gsm Premium Office Computer Paper White Copy Paper , Find Complete Details about High Quality A4 Size Newly Arrived Multi-purpose Copy Paper 80gsm Premium Office Computer Paper White Copy Paper from Tianjin Mobil Import And Export Co., Ltd. Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/High-quality-A4-size-newly-arrived_1601268756292.html',5.00,'a4,paper,80gsm,multipurpose,copy,office,computer,white,premium'),(339,'Paper A4 A4 Multipurpose Copy Printer Legal Size Paper 8.5 X 11 A4 White Double A a4 paper 80gsm',1.69,'Paper A4 A4 Multipurpose Copy Printer Legal Size Paper 8.5 X 11 A4 White Double A A4 Paper 80gsm , Find Complete Details about Paper A4 A4 Multipurpose Copy Printer Legal Size Paper 8.5 X 11 A4 White Double A A4 Paper 80gsm from Qingdao Flying Industrial Co., Ltd. Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/Paper-A4-A4-Multipurpose-Copy-Printer_1601255090055.html',5.00,'a4,paper,80gsm,multipurpose,copy,printer,white,office,legal'),(340,'White Office Copier Ram Paper Factory Direct Sale White A4 Size Copy Paper 80 gsm 70 gsm For Copiper Laser Printing manufacturer',2.00,'White Office Copier Ram Paper Factory Direct Sale White A4 Size Copy Paper 80 Gsm 70 Gsm For Copiper Laser Printing Manufacturer , Find Complete Details about White Office Copier Ram Paper Factory Direct Sale White A4 Size Copy Paper 80 Gsm 70 Gsm For Copiper Laser Printing Manufacturer from Hebei Dayun Industrial Co., Ltd. Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/White-Office-Copier-Ram-Paper-Factory_1601234868464.html',4.60,'a4,paper,80gsm,70gsm,copy,copier,white,office,laser,printing'),(341,'Hot Sale Cheap Copy Paper A4 Size 80gsm Office White Paper',0.70,'Hot Sale Cheap Copy Paper A4 Size 80gsm Office White Paper , Find Complete Details about Hot Sale Cheap Copy Paper A4 Size 80gsm Office White Paper from Shandong Mingchuangxin Material Technology Co., Ltd. Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/Hot-Sale-Cheap-Copy-Paper-A4_1601283963176.html',3.80,'a4,paper,80gsm,copy,office,white,cheap'),(342,'Printing Paper White A4 Size 70 75 80 GSM',0.08,'Printing Paper White A4 Size 70 75 80 Gsm , Find Complete Details about Printing Paper White A4 Size 70 75 80 Gsm from Hefei Yiren Import And Export Trading Co., Ltd. Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/Printing-Paper-White-A4-Size-70_1601198556822.html',3.50,'a4,paper,70gsm,75gsm,80gsm,white,printing'),(343,'Wholesale Cheap A4 Paper 70 gsm A4 Double A 210 x 297mm Letter Size Copy Paper White Office SuppliesA4 Paper Low Price',0.55,'Wholesale Cheap A4 Paper 70 Gsm A4 Double A 210 X 297mm Letter Size Copy Paper White Office Suppliesa4 Paper Low Price , Find Complete Details about Wholesale Cheap A4 Paper 70 Gsm A4 Double A 210 X 297mm Letter Size Copy Paper White Office Suppliesa4 Paper Low Price from SOLOWRLD LIMITED Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/Wholesale-Cheap-A4-Paper-70-gsm_10000018076004.html',3.50,'a4,paper,70gsm,copy,white,office,wholesale,cheap'),(344,'Paper A4 A4 Multipurpose Copy Printer Legal Size Paper 8.5 X 11 A4 White Double A a4 paper 80gsm',1.30,'Paper A4 A4 Multipurpose Copy Printer Legal Size Paper 8.5 X 11 A4 White Double A A4 Paper 80gsm , Find Complete Details about Paper A4 A4 Multipurpose Copy Printer Legal Size Paper 8.5 X 11 A4 White Double A A4 Paper 80gsm from Yiyan trading store inc Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/Paper-A4-A4-Multipurpose-Copy-Printer_1601163955259.html',3.50,'a4,paper,80gsm,multipurpose,copy,printer,white,office,legal'),(345,'china manufacturer A2 A3 A4 A5 letter size legal size double copy A 70g 80g paper',2.35,'China Manufacturer A2 A3 A4 A5 Letter Size Legal Size Double Copy A 70g 80g Paper , Find Complete Details about China Manufacturer A2 A3 A4 A5 Letter Size Legal Size Double Copy A 70g 80g Paper from Shandong Huabao Paper Co., Ltd. Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/china-manufacturer-A2-A3-A4-A5_1600951085621.html',5.00,'a2,a3,a4,a5,paper,70gsm,80gsm,copy,letter,legal,manufacturer'),(346,'Printing Paper White A4 Size 70 75 80 GSM',1.80,'Printing Paper White A4 Size 70 75 80 Gsm , Find Complete Details about Printing Paper White A4 Size 70 75 80 Gsm from Hefei Yiren Import And Export Trading Co., Ltd. Supplier or Manufacturer on Alibaba.com','https://www.alibaba.com/product-detail/Printing-Paper-White-A4-Size-70_1601198479786.html',3.50,'a4,paper,70gsm,75gsm,80gsm,white,printing'),(347,'A4 80gsm White Copy Paper / Multi use Paper / White Plain A4 Paper',6.59,'This A4 80gsm copier paper is a reliable and versatile choice for all your daily printing and copying needs. Designed for smooth performance in a variety of printers, copiers, and fax machines, this paper delivers consistent, high-quality results. Its lightweight 80gsm makes it ideal for everyday office tasks, including reports, memos, and general correspondence.\n\nFeatures:\nSize: A4 (210mm x 297mm) – standard paper size for office and home use.\nWeight: 80gsm – perfect balance between quality and affordability for everyday printing.\nCompatibility: Suitable for inkjet and laser printers, as well as copiers and fax machines.\nFinish: Smooth surface for crisp, clear text and images.\nEco-Friendly: Made from sustainably sourced materials.\nWhether for personal, academic, or professional use, this A4 copier paper is a dependable choice for achieving polished results with ease.','https://www.etsy.com/listing/796654811/a4-80gsm-white-copy-paper-multi-use',4.90,'a4,paper,80gsm,white,copy,multipurpose,plain'),(348,'Paper A4 White Printer Copier Fax Paper 100 Sheets',10.99,'A4 paper is in high-quality, made of sturdy, vivid paper.  100 sheets A4 paper 80gsm thick.  Suitable for creating leaflets, posters and flyers,craft projects.  Great for DIY art craft projects, funny origami, gift bags, or construction papers for interior design, house decorating, or office printer papers, copier papers.  Quality Warranty --- if you have any problems, please feel free to contact us, we will provide satisfied solution.','https://www.amazon.com/Paper-A4-Printer-Copier-Sheets/dp/B0CGWYPSGG',5.00,'a4,paper,white,printer,copier,fax,100sheets'),(349,'A4 Premium Printer Paper - Available in Packs of 40,100 or 500 Sheets - Imported from Thailand (40 Sheets)',8.88,'High quality moderately bright, white copier papers Consistently smooth papers won\'t jam in the printer. Double-sided thick paper for added worthiness. Delivers premium quality color and B&W printouts with details and crispness. Extend the duration of photocopy Ideal for copying or printing tasks Certified by TISI Standard. Certified by International Organization for Standardization (ISO 9001:2008) Certified by Environmental Management Certification (ISO 14001:2004) Certified by Occupational health and safety management systems (ISO 18001:2007) Keep away from flame and moisture. Paper Color : White Paper Thickness : 80 gsm, 21-lb weight. Paper Size (Width x Length) : 210 _ 297 mm. (A4) Contains : Return if not 100% Satisfied Package contains 40 sheets.','https://www.amazon.com/A4-Premium-Printer-Paper-Available/dp/B076QK6VLN',4.30,'a4,paper,premium,printer,40sheets,100sheets,500sheets,thailand'),(350,'A4 White Paper | For Copy, Printing, Writing | 210 x 297 mm.(8.27\" x 11.69\" inches) Pack of 250 sheets. | 24lb - 90 gsm',32.99,'A4 Paper is a standardized copy paper size established by the International Standards Organization. The paper dimensions are 210 x 297 mm. Throughout Europe and the world A4 is the close equivalent to U.S. letter size (8.5\" x 11\"), but measuring 8.27 x 11.69 inches.250 Sheets per pack','https://www.amazon.com/White-Printing-Writing-inches-sheets/dp/B07MWFG74G',5.00,'a4,paper,white,copy,printing,writing,250sheets,90gsm'),(351,'A4 Premium Bright White Paper – Great for Copy, Printing, Writing | 210 x 297 mm (8.27\" x 11.69\") | 24lb Bond / 60lb Text (90gsm) | 250 Sheets per Pack',25.99,'DIMENSIONS – 210 x 297 mm ( 8.27 x 11.69”) A4 is the close equivalent to U.S. letter size (8.5 x 11”)  PREMIUM QUALITY – Made from 24lb (90gsm) premium quality bond paper. Excellent use for art projects, business communications, posters, documents and many more!  DOUBLE-SIDED WHITE SMOOTH FINISH – 98 brightness rating that\'s perfect for designing eye-catching presentations and making your artsy designs pop. Holds colors well and delivers rich, vibrant colors and sharp images with flawless results.  FULL REAM OF 250 SHEETS – Acid and lignin-free cardstocks that won\'t make your documents, arts and print works turn yellow and brittle. This preserves the paper, texts, and images and keeps it last long. This paper is also made with SFI wood fibers.  Perfect paper choice for personal, office and school use!','https://www.amazon.com/A4-Premium-Bright-White-Paper/dp/B07VBP4Y74',4.30,'a4,paper,white,premium,copy,printing,writing,90gsm,250sheets'),(352,'Color Copy Copier Paper Premium Super Smooth Ream-Wrapped 100gsm A4 White Ref CCW0324 [500 Sheets]',22.00,'First FSC certified colour laser paper, ideal for brochures, reports and presentations  Designed specially for all dry toner colour laser copiers and printers  Excellent whiteness  Wood fibre from sustainable forests and elemental chlorine free  Ideal for archive use being accredited with ISO9706','https://www.amazon.com/Color-Copy-Premium-Ream-Wrapped-CCW0324/dp/B000J6A58M',4.50,'a4,paper,100gsm,color,copy,copier,premium,smooth,ream'),(353,'Hilitand A4 Paper White, 100 Sheets 11.8 x 8.3 inch Printer Plain White Paper Multipurpose Office Printer Paper Postcard',18.95,'100 SHEETS: 1Set 100 sheets high-grade paper, very convenient and practical to use.  PRINTING PRECAUTIONS: Please do not turn the printing paper before drying to avoid damage. The drying time shall not be less than 12 hours.  QUALITY PAPER: color, smooth surface, good touch feel.  OCCASION: It is mainly used for books, brochures, magazines, gift boxes, clothing tags, practice drawing, sketching, printing and more.  BLANK POSTCARD: It has excellent effect of printing and stability.','https://www.amazon.com/Sheets-Thermal-Printer-Multipurpose-Office/dp/B07H8VWN6B',2.00,'a4,paper,white,100sheets,printer,plain,multipurpose,office,postcard'),(354,'Copy Paper A4 White Copy Paper 500 Sheets a Pack Office A4 Printing Paper',9.90,'Copy Paper A4 White Copy Paper 500 Sheets a Pack Office A4 Printing Paper, Find Details and Price about Office Supply Paper from Copy Paper A4 White Copy Paper 500 Sheets a Pack Office A4 Printing Paper - Hebei Xianggao Import & Export Trading Co., Ltd.','https://hbxianggao.en.made-in-china.com/product/NQLpErdbXVWB/China-Copy-Paper-A4-White-Copy-Paper-500-Sheets-a-Pack-Office-A4-Printing-Paper.html',0.00,'a4,paper,white,copy,500sheets,office,printing'),(355,'WB A4 75gsm Office Copy Paper - High White (Large Pack of 2500)',9.97,'Do you have lot\'s of printing requirements? Or are you a forgetful person? Do you have loads of ideas swimming around just waiting to be written down and remembered? Maybe you\'re spending a lot of time on the computer and are in need of printing to keep your ideas and pages remembered and more organised.The pack of 2500 white A4 pages brought to you from WB will help you keep your thoughts and you paperwork organised. The paper is perfect for printing and comes in reams of 500 ready to be inserted in to most printers.WB is a great value brand of Office Supplies. The product range covers the full spectrum of office products used in offices everyday. These include copy paper, notepads, writing stationery, files and tapes.','https://www.amazon.com/WB-75gsm-Office-Copy-Paper/dp/B000UZA334',0.00,'a4,paper,75gsm,office,copy,white,bulk,2500');
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
INSERT INTO `search_item` VALUES (49,338,10.14),(49,339,10.10),(49,340,9.70),(49,341,9.34),(49,342,9.20),(49,343,9.12),(49,344,8.98),(49,345,8.94),(49,346,8.87),(49,347,8.45),(49,348,7.06),(49,349,6.13),(49,350,6.00),(49,351,5.45),(49,352,4.65),(49,353,3.72),(49,354,3.36),(49,355,3.34);
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
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_result`
--

LOCK TABLES `search_result` WRITE;
/*!40000 ALTER TABLE `search_result` DISABLE KEYS */;
INSERT INTO `search_result` VALUES (49,'2024-12-20 03:07:00',5);
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

-- Dump completed on 2024-12-20  9:52:09
