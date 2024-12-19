CREATE DATABASE  IF NOT EXISTS machine_customer /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `machine_customer`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: my-aiven-server-akinduhiman2-be40.g.aivencloud.com    Database: machine_customer
-- ------------------------------------------------------
-- Server version	8.0.30

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'b6dca3c5-be1d-11ef-bd64-06f7029b230f:1-16,
da5c93fd-bc50-11ef-aa95-02635e301d15:1-316';

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (2,'John Doe','john@email.com','pass123','jhone123'),(3,'Jane Smith','jane@email.com','pass456','jane456'),(4,'Bob Wilson','bob@email.com','pass789','bon789');
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
) ENGINE=InnoDB AUTO_INCREMENT=214 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,'Laptop',999.99,'High performance laptop','laptop.html',4.50,'electronics,computer,dell,silver,intel i7,16gb ram,ssd storage,gaming capable,windows 11,lightweight,backlit keyboard,full hd'),(2,'Smartphone',699.99,'5G enabled phone','phone.html',4.30,'electronics,mobile,samsung,black,5g,dual sim,256gb storage,water resistant,amoled display,fast charging,wireless charging,android'),(3,'Headphones',149.99,'Wireless noise cancelling','headphones.html',4.70,'electronics,audio,sony,black,wireless,noise cancelling,bluetooth 5.0,40mm drivers,voice assistant,foldable,multipoint pairing,high resolution'),(4,'Coffee Maker',79.99,'Programmable coffee machine','coffee.html',4.20,'appliances,kitchen,cuisinart,stainless steel,12 cup capacity,programmable timer,auto shutoff,brew strength control,permanent filter,self cleaning,hot plate,anti drip'),(5,'Running Shoes',89.99,'Lightweight running shoes','shoes.html',4.40,'sports,footwear,nike,blue white,breathable mesh,cushioned sole,arch support,reflective details,moisture wicking,shock absorbing,flexible,anti slip'),(6,'Backpack',49.99,'Durable travel backpack','backpack.html',4.60,'accessories,travel,north face,navy blue,water resistant,laptop compartment,usb charging port,anti theft,padded straps,multiple compartments,breathable back,hidden pockets'),(7,'Watch',199.99,'Smart fitness watch','watch.html',4.30,'electronics,accessories,fitbit,black,heart rate monitor,sleep tracking,water resistant,gps,touchscreen,week long battery,smartphone notifications,stress monitoring'),(8,'Camera',549.99,'Digital SLR camera','camera.html',4.80,'electronics,photography,canon,black,24mp sensor,4k video,wifi enabled,touchscreen lcd,image stabilization,dual pixel autofocus,raw shooting,weather sealed'),(9,'Tablet',399.99,'10-inch display tablet','tablet.html',4.40,'electronics,computer,apple,space gray,retina display,64gb storage,touch id,pencil compatible,10 hour battery,face recognition,stereo speakers,cellular capable'),(10,'Speaker',129.99,'Bluetooth portable speaker','speaker.html',4.20,'electronics,audio,jbl,black,waterproof,bluetooth 5.0,20 hour battery,voice assistant,party boost,usb c charging,built in powerbank,stereo pairing'),(11,'Monitor',299.99,'27-inch 4K monitor','monitor.html',4.60,'electronics,computer,lg,black,4k uhd,ips panel,hdr10,freesync,height adjustable,eye care,multiple inputs,thin bezel'),(12,'Keyboard',89.99,'Mechanical gaming keyboard','keyboard.html',4.50,'electronics,gaming,razer,black,mechanical switches,rgb backlight,macro keys,anti ghosting,wrist rest,multimedia controls,usb passthrough,programmable'),(13,'Mouse',59.99,'Wireless gaming mouse','mouse.html',4.30,'electronics,gaming,logitech,black red,wireless,16000 dpi,programmable buttons,rgb lighting,rechargeable battery,lightweight design,ergonomic grip,quick dpi switching'),(14,'Printer',199.99,'All-in-one printer','printer.html',4.10,'electronics,office,hp,white,wireless printing,scanner,copier,duplex printing,mobile printing,touchscreen,document feeder,borderless printing'),(15,'External HD',129.99,'2TB portable drive','hdd.html',4.40,'electronics,storage,western digital,black,2tb capacity,usb 3.0,password protection,automatic backup,shock resistant,compact size,plug and play,compatible all os'),(16,'Router',149.99,'Mesh WiFi router','router.html',4.50,'electronics,networking,netgear,white,wifi 6,dual band,parental controls,cyber security,easy setup,beamforming,mu mimo,guest network'),(17,'Webcam',79.99,'HD webcam','webcam.html',4.20,'electronics,computer,logitech,black,1080p resolution,auto focus,stereo audio,privacy shutter,low light correction,wide angle,plug and play,noise reduction'),(18,'Microphone',119.99,'USB condenser microphone','mic.html',4.60,'electronics,audio,blue yeti,silver,condenser,multiple patterns,zero latency,gain control,mute button,desk stand,plug and play,studio quality'),(19,'Power Bank',49.99,'20000mAh portable charger','powerbank.html',4.30,'electronics,accessories,anker,black,20000mah capacity,fast charging,multiple ports,led indicator,compact design,safe charging,airline approved,power delivery'),(20,'USB Hub',39.99,'7-port USB hub','usbhub.html',4.20,'electronics,accessories,anker,black silver,7 ports,usb 3.0,individual switches,led indicators,compact design,data transfer,power adapter,plug and play'),(21,'80 GSM A4 Paper 500 Sheets Bundle in White Color',1890.00,'Color : White Item Weight  : 80 Grams  Paper Finish : Smooth Paper Size : 21 x 29.7 Cm Sheets : 500 80 GSM A4 Paper 500 Sheets Bundle in White Color','https://www.daraz.lk/products/80-gsm-a4-paper-500-sheets-bundle-in-white-color-i196671991.html',0.00,'80gsm,a4,white,paper,smooth,multipurpose'),(22,'80 GSM A4 Paper 500 Sheets Bundle in White Color',1890.00,'Color : White Item Weight  : 80 Grams  Paper Finish : Smooth Paper Size : 21 x 29.7 Cm Sheets : 500 80 GSM A4 Paper 500 Sheets Bundle in White Color','https://www.daraz.lk/products/80-gsm-a4-paper-500-sheets-bundle-in-white-color-i196671991.html',0.00,'80gsm,a4,white,paper,smooth,multipurpose'),(23,'A4 White Photocopy Paper 50 Sheets Pack - 75 GSM',320.00,'pre {        white-space: pre-wrap;    }Step 1:- Product title: A4 White Photocopy Paper 50 Sheets Pack - 75 GSM- Number of sheets per ream: 50- Paper features: 100% Recycled Paper- Thickness (gsm): 75- Category path: Stationery & Craft>Paper Products>Copier PaperStep 2:- Additional keywords: Stationery, Recycled, Copier PaperStep 3:• A4 size with 75 GSM thickness for quality printing.• 100% recycled paper, eco-friendly and sustainable choice.• Each pack contains 50 sheets for your printing needs.• Ideal for stationery and copier paper use.• Fits into the Stationery & Craft>Paper Products category.Step 4:- N/AStep 5:- N/A','https://www.daraz.lk/products/a4-white-photocopy-paper-50-sheets-pack-75-gsm-i170816274.html',0.00,'a4,75gsm,photocopy,multipurpose'),(24,'A4 80Gsm Photocopy paper 100 sheet retail pack',650.00,'Brand : Promate or ik Photocopy Paper Dust free Peo white Thickness (gsm) : 80 Carton : Ream Paper Features : 100% Recycled Paper Number of Sheets per Ream : 100 Brand : Promate or ik Photocopy Paper Dust free Peo white Thickness (gsm) : 80 Carton : Ream Paper Features : 100% Recycled Paper Number of Sheets per Ream : 100','https://www.daraz.lk/products/a4-80gsm-photocopy-paper-100-sheet-retail-pack-i153437367.html',0.00,'80gsm,a4,photocopy,multipurpose,recycled'),(189,'Paper A4 White Printer Copier Fax Paper 100 Sheets',15984.00,'Printers and copy paper are perfect for daily use and various uses in the office and home. High quality paper ensures smooth printer throughput and reliable good print results.','https://www.amazon.com/Paper-A4-Printer-Copier-Sheets/dp/B0CGWYPSGG/ref=sr_1_29?dib=eyJ2IjoiMSJ9.Fupb2pj1I9ipTOWon3nh-zWysUdGcCAlY1OI5wvgipKD0FSJkSy6kZ44zritnd6VkExrXI2kpICVBfQPmylQW-McqtS2jn8-sU32l4Wj9sncuOl91ZmGOnuTTsTwdh9h6GvE0bJllBJ4yr0GWb3GYrRaTQzaFI6sFcQDEvaOTSBu0EhdGoHf_jH65C6YqsBn3DcHvXrxM_SlltKIkbCt7tweWYNO8406keD8ITuSczzItf1NpLiscJODNtXoSqhRXavg1ob36eEl16_5bVM8c2DXYZAtt0pmoxkuHIdmDssxsoXK_LetymhEXTSE4C1UF0IFkHPkqZfOxyA2B79-qkfRsjzj39zPdz7sDK7i7cYB1Bm-d5Ikv1Xz5EQUllufy6WCGxBNWDkyGzHAseT_RxQIIswJKbE7swEOxjYaGO7VG6VQTdipbnF4_lJZyTU8.mnzsD3pIEUFoIOkGZqOroh29JLChuvBtAODuxeWX-xk&dib_tag=se&keywords=a4+size+paper&qid=1734290983&sr=8-29',5.00,'printer paper,copier paper,fax paper,a4,white,100 sheets'),(190,'Nuburi - A4 Size Printer Paper - Great for Professional Documents - 80 gsm / 21lb (40 Sheets)',15501.00,'Nuburi Office Supply brand business paper. Nuburi\'s premium 80 GSM paper is ideal for work or play, home or office. It\'s a premium business paper you\'d select for all your most important legal documents. It\'s ideal for items such as forms and direct mail. Its consistently smooth printing surface makes for impressive flyers and handouts that pop. Add a splash of color to your important printouts to make a lasting impression. Your satisfaction if guaranteed. Return if not 100% satisfied.','https://www.amazon.com/Nuburi-Size-Printer-Paper-Sheets/dp/B0BRCN198C/ref=sr_1_6?dib=eyJ2IjoiMSJ9.Fupb2pj1I9ipTOWon3nh-zWysUdGcCAlY1OI5wvgipKD0FSJkSy6kZ44zritnd6VkExrXI2kpICVBfQPmylQW-McqtS2jn8-sU32l4Wj9sncuOl91ZmGOnuTTsTwdh9h6GvE0bJllBJ4yr0GWb3GYrRaTQzaFI6sFcQDEvaOTSBu0EhdGoHf_jH65C6YqsBn3DcHvXrxM_SlltKIkbCt7tweWYNO8406keD8ITuSczzItf1NpLiscJODNtXoSqhRXavg1ob36eEl16_5bVM8c2DXYZAtt0pmoxkuHIdmDssxsoXK_LetymhEXTSE4C1UF0IFkHPkqZfOxyA2B79-qkfRsjzj39zPdz7sDK7i7cYB1Bm-d5Ikv1Xz5EQUllufy6WCGxBNWDkyGzHAseT_RxQIIswJKbE7swEOxjYaGO7VG6VQTdipbnF4_lJZyTU8.mnzsD3pIEUFoIOkGZqOroh29JLChuvBtAODuxeWX-xk&dib_tag=se&keywords=a4+size+paper&qid=1734290983&sr=8-6',4.70,'printer paper,a4,80gsm,21lb,40 sheets,professional documents,smooth printing surface,impressive flyers,handouts,color,satisfaction guaranteed'),(191,'Phomemo A4 Thermal Paper-White Quick-Dry Printer Paper, Multipurpose A4 Thermal Paper Compatible for Phomemo M08F, M832, M833 Portable Thermal Printer, 8.27\"x11.69\"(210mm*297mm), 200 Sheets',23790.00,'Phomemo A4 white quick-dry Thermal Paper, 8.27\"x11.69\" (210mm*297mm) width, black text, 200 sheets in box. Compatible with Phomemo M08F/M832/M833/M834 portable A4 printer. Storage for 10 years  Multi-compatibility- This A4 thermal paper compatible with Phomemo M832.M833,M834 portable A4 printer  Phomemo A4 thermal paper prints clearly and does not leave print marks, the writing will not become blurred or blackened, and there is a coating on the surface that allows the writing to dry quickly. It is also waterproof, oil-proof and abrasion-resistance  Widely Use- This A4 thermal paper you can use anywhere, schools, offices, outdoor work, business meetings and more. With thermal printing technology, no ink is needed, portable and convenient  Safe Printing- Phomemo printing paper is BPA free, which can be used safely by the elderly and children, environmentally friendly and pollution-free, strong adhesion and waterproof','https://www.amazon.com/Phomemo-Paper-White-Quick-Dry-Multipurpose-Compatible/dp/B0CR1MLKDV',4.80,'thermal paper,a4,8.27\"x11.69\",200 sheets,compatible for phomemo m08f,m832,m833,m834,portable thermal printer,quick-dry,black text,waterproof,oil-proof,abrasion-resistance'),(192,'MIMA PREMIUM A4 COPY PAPER 80 GSM - 2500 SHEETS IN A BOX (500 X 5 Packets) ** FREE DELIVERY **',10000.00,'MIMA premium copy paper A4 80 GSM | 2,500 Sheets per Box | (500 X 5 Packets)** FREE DELIVERY ** MIMA premium copy is made with high-quality paper sourced from Indonesia. Its smooth finish makes it ideal for multiple applications from photocopy to double-sided printing.*Quick Drying*Sharp Contrast*Brilliant Color*Excellent runnability*Value for Money','https://www.daraz.lk/products/mima-premium-a4-copy-paper-80-gsm-2500-sheets-in-a-box-500-x-5-packets-free-delivery-i195517244.html',0.00,'copy paper,a4,80 gsm,2500 sheets,500 x 5 packets,free delivery,high-quality paper,smooth finish,quick drying,sharp contrast,brilliant color,excellent runnability,value for money'),(193,'Avalon 80GSM A4 Paper 500 Sheet',3450.00,'Built with new twin wire technology. Compatible for all photocopy systems and hassle-free both side copying. Most offices and corporate prefer commercial use. Ideal for quality printing, photocopying, employment. Suitable for home, store, office printers with any speed and configuration.','https://www.daraz.lk/products/avalon-80gsm-a4-paper-500-sheet-i154542697.html',0.00,'a4,80gsm,500 sheets,twin wire technology,photocopy,printing,office,home'),(194,'I Copier Premium A4 Paper 70gsm - White (500 Sheets)',2500.00,'Brand : I Copier Size: A4 70 gsm 100% Brand New density paper is great for quality printing and copying because it allows for printing and copying on both sides. Brighter white makes whatever you print or copy standout from the crowd smooth surface with low dust content reduces jams, sticking and curling of your paper while providing a quality finished result Sharper clarity for brilliant color and image reproduction Perfect for use at home, work and in the classroom. Excellent or all office machines, copiers, lasers and inkjet printers Quick dispatch and fast delivery island wide. Brand :- Icopier Item :- A4 PaperQuality :-  70GSMPages :- 500pgsUses:- B &amp; W Printouts, Colour printouts, Assignment, crafts','https://www.daraz.lk/products/i-copier-premium-a4-paper-70gsm-white-500-sheets-i225878123.html',0.00,'a4,70gsm,500 sheets,white,quality printing,copying,double-sided,brighter white,smooth surface,low dust content,sharp clarity,color reproduction,home,work,classroom'),(195,'Avalon Photocopy Paper 80gsm (A4 Bundle) 500 sheets',3200.00,'Paper for photocopy and everyday printing use.    High Speed Printing; guarantees exceptional results in Copier, Laser, Inkjet, and Fax   Brilliant Colours; bring colour images to life   Sharper Images; get super sharp colour images of photos, diagrams and charts    Description   Paper for photocopy and everyday printing use.   High Speed Printing; guarantees exceptional results in Copier, Laser, Inkjet, and Fax    Brilliant Colours; bring colour images to life    Sharper Images; get super sharp colour images of photos, diagrams and charts    Quick Ink Drying; low bleeding and superb colour density   Solid Black; sharper text and graphics with bolder blacks A4 80GSM AVALON PHOTOCOPY PAPER (500 SHEETS/SIZE:210 x 297mm) Paper for photocopy and everyday printing use.  Has been specially designed for trouble free use in all your office machines ISO APPROVAL This paper is produced in a plant awarded the ISO 9001 for Quality Management System, ISO 14001 for Environmental Management System, and ISO 9706 for permanency of paper. AVALON photocopy paper uses TRUTONE TECHNOLOGY to give superior printing results on pigment-based inkjet printers:Solid Black, Brilliant Colours,Quick Ink Drying and Sharp images. 80gsmA4 size','https://www.daraz.lk/products/avalon-photocopy-paper-80gsm-a4-bundle-500-sheets-i182255823.html',0.00,'photocopy paper,a4,80gsm,500 sheets,high speed printing,brilliant colors,sharper images,quick ink drying,solid black'),(196,'Icopier Premium Multipurpose Paper  A4 70g Photocopy Paper 70GSM 500 Sheet / 1Ream',3199.00,'Copier Paper by JKWhen it comes to stationery needs JK is the name which pops up in the head for photocopying sheets. In terms of the best study needs for educational purpose and office purpose, the A4 sheets have no match. These sheets are also compatible with all kinds of photocopying system.These sheets come with latest ColorLok technology. Faster drying, bolder blacks, vivid colours are the major feature of this sheets. Faster drying facilitates less smearing and faster handling time. Bolder blacks provide crisp sharp texts with improved contrast. Lastly, the vivid colours provide richer, brighter images and graphics.','https://www.daraz.lk/products/icopier-premium-multipurpose-paper-a4-70g-photocopy-paper-70gsm-500-sheet-1ream-i152117958.html',0.00,'multipurpose paper,a4,70gsm,photocopy paper,500 sheets,1 ream,colorlok technology,fast drying,bolder blacks,vivid colors'),(197,'King copy Photocopy Paper 80gsm (A4 Bundle) 500 sheets',2900.00,'100% Quality is ensured. 100% Recyclable  Reliable brand  Durable products Produce your creative and academic work  Premium multi-purpose photocopy paper.','https://www.daraz.lk/products/king-copy-photocopy-paper-80gsm-a4-bundle-500-sheets-i182256671.html',0.00,'photocopy paper,a4,80gsm,500 sheets,quality,recyclable,reliable,durable,creative,academic'),(198,'NK A4 Photocopy Paper 500 Sheet Bundle 80gsm',2500.00,'Introducing the NK A4 Photocopy Paper 500 Sheet Bundle 80gsm, perfect for all your printing needs. This bundle includes 500 sheets of 100% recycled paper, making it an eco-friendly choice. With a thickness of 80gsm, this paper is sturdy and durable, ensuring that your prints come out looking crisp and clear. The NK brand is known for its high-quality products, and this photocopy paper is no exception. Ideal for use in offices, schools, and homes, this paper is versatile and can be used for a variety of printing needs. Get your hands on this reliable and sustainable photocopy paper today!','https://www.daraz.lk/products/nk-a4-photocopy-paper-500-sheet-bundle-80gsm-i199567714.html',0.00,'photocopy paper,a4,80gsm,500 sheets,recycled paper,crisp,clear,office,school,home'),(199,'Photocopy Paper 70Gsm A4 Bundle 100 Sheets Pack',1000.00,'100% brand new and high quality. 100% Recyclable High Durability Easy to use Perfect Gift for any ones High-quality photocopy paperA4 size with 70GSM thickness100 sheets eachPerfect for everyday office use','https://www.daraz.lk/products/photocopy-paper-70gsm-a4-bundle-100-sheets-pack-i173864125.html',0.00,'photocopy paper,a4,70gsm,100 sheets,recyclable,durable,gift'),(212,'Copy A A4 White Sheet Bundle 70 GSM - 500 Sheets',2850.00,'Brand : A Copy Size - A4 70 gsm 100% Brand New density paper is great for quality printing and copying allows for printing and copying on both sides. Brighter white makes whatever you print or copy standout from the crowd Smooth surface with low dust content reduces jams, sticking and curling of your paper while provide a quality finished result Sharper clarity for brilliant color and image reproduction Perfect for use at home, work and in the classroom. Excellent or all office machines, copiers, laser, Fax Machine and inkjet printers Quick dispatch and fast delivery island wide.','https://www.daraz.lk/products/copy-a-a4-white-sheet-bundle-70-gsm-500-sheets-i158643678.html',0.00,'paper,photocopy,printing,quality,sharp,durable'),(213,'A4 70gsm 500 Sheets Bundle',2650.00,'No Brand 70GSM  Best Quality  500papers per bundle White Island wide delivery  No Brand70GSM Best Quality 500papers per bundleWhiteIsland wide delivery','https://www.daraz.lk/products/a4-70gsm-500-sheets-bundle-i140962569.html',0.00,'paper,printing,quality,durable,white');
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
INSERT INTO `search_item` VALUES (26,189,7.45),(26,190,6.74),(26,191,4.84),(26,192,3.88),(26,193,2.00),(26,194,2.00),(26,195,1.00),(26,196,1.00),(26,197,1.00),(26,198,1.00),(26,199,1.00),(30,21,2.00),(30,189,6.45),(30,190,6.74),(30,191,5.84),(30,192,3.88),(30,193,1.00),(30,194,1.00),(30,195,1.00),(30,196,1.00),(30,197,1.00),(30,198,1.00),(30,199,1.00),(31,21,1.00),(31,23,1.00),(31,189,5.05),(31,190,4.65),(31,191,8.24),(31,192,1.10),(31,193,1.01),(31,194,2.00),(31,195,1.01),(31,196,1.01),(31,197,1.01),(31,198,1.00),(31,199,1.00),(32,21,1.00),(32,189,5.05),(32,190,4.65),(32,191,8.24),(32,192,1.10),(32,193,1.01),(32,194,2.00),(32,195,1.01),(32,196,1.01),(32,197,1.01),(32,198,1.00),(32,212,1.00),(32,213,1.00);
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_result`
--

LOCK TABLES `search_result` WRITE;
/*!40000 ALTER TABLE `search_result` DISABLE KEYS */;
INSERT INTO `search_result` VALUES (25,'2024-12-18 05:46:28',2),(26,'2024-12-18 05:54:09',2),(27,'2024-12-18 05:58:56',2),(28,'2024-12-18 06:04:34',2),(29,'2024-12-18 06:10:46',2),(30,'2024-12-18 06:12:16',2),(31,'2024-12-18 06:14:15',2),(32,'2024-12-18 06:16:26',2);
/*!40000 ALTER TABLE `search_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'machine_customer'
--

--
-- Dumping routines for database 'machine_customer'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-19 21:03:57
