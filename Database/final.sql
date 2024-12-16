CREATE DATABASE IF NOT EXISTS `machine_customer` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `machine_customer`;

/* Table structure for table `customer` */
DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/* Table structure for table `item` */
DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `description` text,
  `link` text,
  `rate` decimal(4,2) DEFAULT NULL,
  `tags` text,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/* Table structure for table `search_result` */
DROP TABLE IF EXISTS `search_result`;
CREATE TABLE `search_result` (
  `search_id` int NOT NULL AUTO_INCREMENT,
  `time_stamp` timestamp NULL DEFAULT NULL,
  `customer_id` int NOT NULL,
  PRIMARY KEY (`search_id`),
  KEY `customer_id_idx` (`customer_id`),
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/* Table structure for table `history` */
DROP TABLE IF EXISTS `history`;
CREATE TABLE `history` (
  `customer_id` int NOT NULL,
  `item_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`customer_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/* Table structure for table `search_item` */
DROP TABLE IF EXISTS `search_item`;
CREATE TABLE `search_item` (
  `search_id` int NOT NULL,
  `item_id` int NOT NULL,
  `score` decimal(4,2) DEFAULT NULL,
  PRIMARY KEY (`search_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `search_item_ibfk_1` FOREIGN KEY (`search_id`) REFERENCES `search_result` (`search_id`),
  CONSTRAINT `search_item_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Dump completed on 2024-12-17  0:09:10

-- ********************************************************************************************************

-- Insertions
-- Customer insertions
INSERT INTO `customer` (`customer_name`, `email`, `password`) VALUES
('John Doe', 'john@email.com', 'pass123'),
('Jane Smith', 'jane@email.com', 'pass456'),
('Bob Wilson', 'bob@email.com', 'pass789');

-- Item insertions
INSERT INTO `item` (`name`, `price`, `description`, `link`, `rate`, `tags`) VALUES
('Laptop', 999.99, 'High performance laptop', 'laptop.html', 4.50, 'electronics,computer,dell,silver,intel i7,16gb ram,ssd storage,gaming capable,windows 11,lightweight,backlit keyboard,full hd'),
('Smartphone', 699.99, '5G enabled phone', 'phone.html', 4.30, 'electronics,mobile,samsung,black,5g,dual sim,256gb storage,water resistant,amoled display,fast charging,wireless charging,android'),
('Headphones', 149.99, 'Wireless noise cancelling', 'headphones.html', 4.70, 'electronics,audio,sony,black,wireless,noise cancelling,bluetooth 5.0,40mm drivers,voice assistant,foldable,multipoint pairing,high resolution'),
('Coffee Maker', 79.99, 'Programmable coffee machine', 'coffee.html', 4.20, 'appliances,kitchen,cuisinart,stainless steel,12 cup capacity,programmable timer,auto shutoff,brew strength control,permanent filter,self cleaning,hot plate,anti drip'),
('Running Shoes', 89.99, 'Lightweight running shoes', 'shoes.html', 4.40, 'sports,footwear,nike,blue white,breathable mesh,cushioned sole,arch support,reflective details,moisture wicking,shock absorbing,flexible,anti slip'),
('Backpack', 49.99, 'Durable travel backpack', 'backpack.html', 4.60, 'accessories,travel,north face,navy blue,water resistant,laptop compartment,usb charging port,anti theft,padded straps,multiple compartments,breathable back,hidden pockets'),
('Watch', 199.99, 'Smart fitness watch', 'watch.html', 4.30, 'electronics,accessories,fitbit,black,heart rate monitor,sleep tracking,water resistant,gps,touchscreen,week long battery,smartphone notifications,stress monitoring'),
('Camera', 549.99, 'Digital SLR camera', 'camera.html', 4.80, 'electronics,photography,canon,black,24mp sensor,4k video,wifi enabled,touchscreen lcd,image stabilization,dual pixel autofocus,raw shooting,weather sealed'),
('Tablet', 399.99, '10-inch display tablet', 'tablet.html', 4.40, 'electronics,computer,apple,space gray,retina display,64gb storage,touch id,pencil compatible,10 hour battery,face recognition,stereo speakers,cellular capable'),
('Speaker', 129.99, 'Bluetooth portable speaker', 'speaker.html', 4.20, 'electronics,audio,jbl,black,waterproof,bluetooth 5.0,20 hour battery,voice assistant,party boost,usb c charging,built in powerbank,stereo pairing'),
('Monitor', 299.99, '27-inch 4K monitor', 'monitor.html', 4.60, 'electronics,computer,lg,black,4k uhd,ips panel,hdr10,freesync,height adjustable,eye care,multiple inputs,thin bezel'),
('Keyboard', 89.99, 'Mechanical gaming keyboard', 'keyboard.html', 4.50, 'electronics,gaming,razer,black,mechanical switches,rgb backlight,macro keys,anti ghosting,wrist rest,multimedia controls,usb passthrough,programmable'),
('Mouse', 59.99, 'Wireless gaming mouse', 'mouse.html', 4.30, 'electronics,gaming,logitech,black red,wireless,16000 dpi,programmable buttons,rgb lighting,rechargeable battery,lightweight design,ergonomic grip,quick dpi switching'),
('Printer', 199.99, 'All-in-one printer', 'printer.html', 4.10, 'electronics,office,hp,white,wireless printing,scanner,copier,duplex printing,mobile printing,touchscreen,document feeder,borderless printing'),
('External HD', 129.99, '2TB portable drive', 'hdd.html', 4.40, 'electronics,storage,western digital,black,2tb capacity,usb 3.0,password protection,automatic backup,shock resistant,compact size,plug and play,compatible all os'),
('Router', 149.99, 'Mesh WiFi router', 'router.html', 4.50, 'electronics,networking,netgear,white,wifi 6,dual band,parental controls,cyber security,easy setup,beamforming,mu mimo,guest network'),
('Webcam', 79.99, 'HD webcam', 'webcam.html', 4.20, 'electronics,computer,logitech,black,1080p resolution,auto focus,stereo audio,privacy shutter,low light correction,wide angle,plug and play,noise reduction'),
('Microphone', 119.99, 'USB condenser microphone', 'mic.html', 4.60, 'electronics,audio,blue yeti,silver,condenser,multiple patterns,zero latency,gain control,mute button,desk stand,plug and play,studio quality'),
('Power Bank', 49.99, '20000mAh portable charger', 'powerbank.html', 4.30, 'electronics,accessories,anker,black,20000mah capacity,fast charging,multiple ports,led indicator,compact design,safe charging,airline approved,power delivery'),
('USB Hub', 39.99, '7-port USB hub', 'usbhub.html', 4.20, 'electronics,accessories,anker,black silver,7 ports,usb 3.0,individual switches,led indicators,compact design,data transfer,power adapter,plug and play');

-- Search Result insertions
INSERT INTO `search_result` (`time_stamp`, `customer_id`) VALUES
('2024-01-15 10:30:00', 1),
('2024-01-15 14:45:00', 2),
('2024-01-16 09:15:00', 3),
('2024-01-16 16:20:00', 1);

-- History insertions
INSERT INTO `history` (`customer_id`, `item_id`, `quantity`) VALUES
(1, 1, 1),
(1, 3, 2),
(1, 5, 1),
(1, 7, 1),
(1, 9, 1),
(2, 2, 1),
(2, 4, 2),
(2, 6, 1),
(2, 8, 1),
(2, 10, 1),
(3, 11, 1),
(3, 13, 2),
(3, 15, 1),
(3, 17, 1),
(3, 19, 2);

-- Search Item insertions
INSERT INTO `search_item` (`search_id`, `item_id`, `score`) VALUES
-- Search 1 results
(1, 1, 9.5),
(1, 2, 8.5),
(1, 3, 7.8),
(1, 7, 7.2),
(1, 9, 6.5),
(1, 12, 6.0),
-- Search 2 results
(2, 4, 9.2),
(2, 5, 8.8),
(2, 6, 8.2),
(2, 8, 7.5),
(2, 10, 7.0),
(2, 14, 6.5),
-- Search 3 results
(3, 11, 9.4),
(3, 13, 8.9),
(3, 15, 8.4),
(3, 16, 7.9),
(3, 17, 7.3),
(3, 18, 6.8),
-- Search 4 results
(4, 19, 9.6),
(4, 20, 9.1),
(4, 1, 8.7),
(4, 3, 8.2),
(4, 5, 7.8),
(4, 7, 7.3),
(4, 9, 7.0);
