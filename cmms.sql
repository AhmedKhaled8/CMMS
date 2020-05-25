-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: CMMS
-- ------------------------------------------------------
-- Server version	5.6.37

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
-- Table structure for table `device_description`
--

DROP TABLE IF EXISTS `device_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_description` (
  `d_code` smallint(5) unsigned NOT NULL,
  `description` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`d_code`),
  CONSTRAINT `device_description_ibfk_1` FOREIGN KEY (`d_code`) REFERENCES `device_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_description`
--

LOCK TABLES `device_description` WRITE;
/*!40000 ALTER TABLE `device_description` DISABLE KEYS */;
INSERT INTO `device_description` VALUES (1,''),(2,''),(3,''),(5,''),(6,''),(7,''),(8,''),(9,''),(10,''),(11,''),(12,''),(13,''),(14,''),(15,''),(16,''),(17,''),(18,''),(19,''),(20,''),(21,''),(22,''),(23,''),(24,''),(25,''),(26,''),(27,''),(28,''),(29,''),(30,''),(31,''),(32,''),(33,'');
/*!40000 ALTER TABLE `device_description` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_essentials`
--

DROP TABLE IF EXISTS `device_essentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_essentials` (
  `code` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `serial` bigint(20) unsigned NOT NULL DEFAULT '0',
  `type` varchar(50) NOT NULL DEFAULT '0',
  `status` enum('operational','obselete') DEFAULT 'operational',
  `maint_date` date DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_essentials`
--

LOCK TABLES `device_essentials` WRITE;
/*!40000 ALTER TABLE `device_essentials` DISABLE KEYS */;
INSERT INTO `device_essentials` VALUES (1,1000,'Ventilator','operational','2020-06-20'),(2,1001,'Ventilator','operational','2020-06-20'),(3,1002,'Ventilator','operational','2020-06-20'),(5,1100,'Defibrillator','operational','2020-06-20'),(6,1101,'Defibrillator','operational','2020-06-20'),(7,1200,'Monitor','operational','2020-06-20'),(8,1201,'Monitor','operational','2020-06-20'),(9,1202,'Monitor','operational','2020-06-20'),(10,1203,'Monitor','operational','2020-06-20'),(11,1300,'Ultrasonic','operational','2020-06-20'),(12,1301,'Ultrasonic','operational','2020-06-20'),(13,1302,'Ultrasonic','operational','2020-06-20'),(14,1400,'X-Ray','operational','2020-06-20'),(15,1401,'X-Ray','operational','2020-06-20'),(16,2000,'Ultrasonic','operational','2020-06-20'),(17,2001,'Ultrasonic','operational','2020-06-20'),(18,2002,'Ultrasonic','operational','2020-06-20'),(19,2100,'X-Ray','operational','2020-06-20'),(20,2101,'X-Ray','operational','2020-06-20'),(21,2102,'X-Ray','operational','2020-06-20'),(22,2200,'CT','operational','2020-06-20'),(23,2201,'Ultrasonic','operational','2020-06-20'),(24,2300,'MRI','operational','2020-06-20'),(25,2301,'MRI','operational','2020-06-20'),(26,3000,'Syringe Pump','operational','2020-06-20'),(27,3001,'Syringe Pump','operational','2020-06-20'),(28,3100,'Monitor','operational','2020-06-20'),(29,3101,'Monitor','operational','2020-06-20'),(30,3200,'Defibrillator','operational','2020-06-20'),(31,3201,'Defibrillator','operational','2020-06-20'),(32,3300,'ECG','operational','2020-06-20'),(33,3301,'ECG','operational','2020-06-20');
/*!40000 ALTER TABLE `device_essentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_extras`
--

DROP TABLE IF EXISTS `device_extras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_extras` (
  `d_code` smallint(5) unsigned NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT '0',
  `model` varchar(30) NOT NULL DEFAULT '0',
  `manufacturer` varchar(50) NOT NULL,
  `country` enum('AFG','ALA','ALB','DZA','ASM','AND','AGO','AIA','ATA','ATG','ARG','ARM','ABW','AUS','AUT','AZE','BHS','BHR','BGD','BRB','BLR','BEL','BLZ','BEN','BMU','BTN','BOL','BES','BIH','BWA','BVT','BRA','IOT','BRN','BGR','BFA','BDI','KHM','CMR','CAN','CPV','CYM','CAF','TCD','CHL','CHN','CXR','CCK','COL','COM','COG','COD','COK','CRI','CIV','HRV','CUB','CUW','CYP','CZE','DNK','DJI','DMA','DOM','ECU','EGY','SLV','GNQ','ERI','EST','ETH','FLK','FRO','FJI','FIN','FRA','GUF','PYF','ATF','GAB','GMB','GEO','DEU','GHA','GIB','GRC','GRL','GRD','GLP','GUM','GTM','GGY','GIN','GNB','GUY','HTI','HMD','VAT','HND','HKG','HUN','ISL','IND','IDN','IRN','IRQ','IRL','IMN','ISR','ITA','JAM','JPN','JEY','JOR','KAZ','KEN','KIR','PRK','KOR','KWT','KGZ','LAO','LVA','LBN','LSO','LBR','LBY','LIE','LTU','LUX','MAC','MKD','MDG','MWI','MYS','MDV','MLI','MLT','MHL','MTQ','MRT','MUS','MYT','MEX','FSM','MDA','MCO','MNG','MNE','MSR','MAR','MOZ','MMR','NAM','NRU','NPL','NLD','NCL','NZL','NIC','NER','NGA','NIU','NFK','MNP','NOR','OMN','PAK','PLW','PSE','PAN','PNG','PRY','PER','PHL','PCN','POL','PRT','PRI','QAT','REU','ROU','RUS','RWA','BLM','SHN','KNA','LCA','MAF','SPM','VCT','WSM','SMR','STP','SAU','SEN','SRB','SYC','SLE','SGP','SXM','SVK','SVN','SLB','SOM','ZAF','SGS','SSD','ESP','LKA','SDN','SUR','SJM','SWZ','SWE','CHE','SYR','TWN','TJK','TZA','THA','TLS','TGO','TKL','TON','TTO','TUN','TUR','TKM','TCA','TUV','UGA','UKR','ARE','GBR','USA','UMI','URY','UZB','VUT','VEN','VNM','VGB','VIR','WLF','ESH','YEM','ZMB','ZWE') DEFAULT NULL,
  `receive_date` date NOT NULL,
  `cost` int(10) unsigned DEFAULT NULL,
  `department` enum('Admissions','Open Cardiology','Radiology') DEFAULT NULL,
  `remove_date` date DEFAULT NULL,
  PRIMARY KEY (`d_code`),
  CONSTRAINT `device_extras_ibfk_1` FOREIGN KEY (`d_code`) REFERENCES `device_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_extras`
--

LOCK TABLES `device_extras` WRITE;
/*!40000 ALTER TABLE `device_extras` DISABLE KEYS */;
INSERT INTO `device_extras` VALUES (1,'Yuwell Ventilator I','YH-830','Oxford Ventilators','GBR','2020-05-20',320000,'Open Cardiology',NULL),(2,'Yuwell Ventilator II','YH-830','Oxford Ventilators','GBR','2020-05-20',320000,'Open Cardiology',NULL),(3,'Yuwell Ventilator III','YH-830','Oxford Ventilators','GBR','2020-05-20',320000,'Open Cardiology',NULL),(5,'HeartStart XL Defibrillator I','HeartStart XL','Philips ','GBR','2020-05-20',60000,'Open Cardiology',NULL),(6,'HeartStart XL Defibrillator II','HeartStart XL','Philips','GBR','2020-05-20',60000,'Open Cardiology',NULL),(7,'Infinity Delta Monitor I','Infinity Delta','Draeger','DEU','2020-05-20',30000,'Open Cardiology',NULL),(8,'Infinity Delta Monitor II','Infinity Delta','Draeger','DEU','2020-05-20',30000,'Open Cardiology',NULL),(9,'Infinity Delta Monitor III','Infinity Delta','Draeger','DEU','2020-05-20',30000,'Open Cardiology',NULL),(10,'Infinity Delta Monitor IV','Infinity Delta','Draeger','DEU','2020-05-20',30000,'Open Cardiology',NULL),(11,'Ultrasound Machine I','DW-370','Dawei Medical','CHN','2020-05-20',400000,'Open Cardiology',NULL),(12,'Ultrasound Machine II','DW-370	','Dawei Medical','CHN','2020-05-20',400000,'Open Cardiology',NULL),(13,'Ultrasound Machine III','ACUSON','SIEMENS','DEU','2020-05-20',1000000,'Open Cardiology',NULL),(14,'X-Ray Device I','ROTANODE','TOSHIBA','JPN','2020-05-20',100000,'Open Cardiology',NULL),(15,'X-Ray Device I','ROTANODE','TOSHIBA','JPN','2020-05-20',100000,'Open Cardiology',NULL),(16,'Ultrasound Machine IV','ACUSON','SIEMENS','DEU','2020-05-20',1000000,'Radiology',NULL),(17,'Ultrasound Machine V','ACUSON','SIEMENS','DEU','2020-05-20',1000000,'Radiology',NULL),(18,'Ultrasound Machine VI','ACUSON','SIEMENS','DEU','2020-05-20',1000000,'Radiology',NULL),(19,'X-Ray Device II','ROTANODE','TOSHIBA','JPN','2020-05-20',100000,'Radiology',NULL),(20,'X-Ray Device III','ROTANODE','TOSHIBA','JPN','2020-05-20',100000,'Radiology',NULL),(21,'X-Ray Device IV','ROTANODE','TOSHIBA','JPN','2020-05-20',100000,'Radiology',NULL),(22,'Brilliance CT Machine I','Brilliance 16-Akron','Philips ','GBR','2020-05-20',1500000,'Radiology',NULL),(23,'Brilliance CT Machine II','Brilliance 16-Akron','Philips','GBR','2020-05-20',1500000,'Radiology',NULL),(24,'Espree MRI Machine I','Espree TiM','Siemens','DEU','2020-05-20',3000000,'Radiology',NULL),(25,'Espree MRI Machine II','Espree TiM','Siemens','DEU','2020-05-20',3000000,'Radiology',NULL),(26,'IPS-12 Syringe Pump I','IPS-12','Inovenso ','TUR','2020-05-20',10000,'Admissions',NULL),(27,'IPS-12 Syringe Pump II','IPS-12','Inovenso ','TUR','2020-05-20',10000,'Admissions',NULL),(28,'Infinity Delta Monitor V','Infinity Delta','Draeger	','DEU','2020-05-20',30000,'Admissions',NULL),(29,'Infinity Delta Monitor VI','Infinity Delta','Draeger	','DEU','2020-05-20',30000,'Admissions',NULL),(30,'HeartStart XL Defibrillator III','HeartStart XL','Philips','GBR','2020-05-20',60000,'Admissions',NULL),(31,'HeartStart XL Defibrillator IV','HeartStart XL','Philips','GBR','2020-05-20',60000,'Admissions',NULL),(32,'ECG MACHINE I','ELI 250C','BURDICK','USA','2020-05-20',65000,'Admissions',NULL),(33,'ECG MACHINE II','ELI 250C','BURDICK ','USA','2020-05-20',65000,'Admissions',NULL);
/*!40000 ALTER TABLE `device_extras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintain_dates`
--

DROP TABLE IF EXISTS `maintain_dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintain_dates` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `device_code` mediumint(8) unsigned NOT NULL,
  `maint_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintain_dates`
--

LOCK TABLES `maintain_dates` WRITE;
/*!40000 ALTER TABLE `maintain_dates` DISABLE KEYS */;
INSERT INTO `maintain_dates` VALUES (1,1,'2020-06-20'),(2,2,'2020-06-20'),(3,3,'2020-06-20'),(5,5,'2020-06-20'),(6,6,'2020-06-20'),(7,7,'2020-06-20'),(8,8,'2020-06-20'),(9,9,'2020-06-20'),(10,10,'2020-06-20'),(11,11,'2020-06-20'),(12,12,'2020-06-20'),(13,13,'2020-06-20'),(14,14,'2020-06-20'),(15,15,'2020-06-20'),(16,16,'2020-06-20'),(17,17,'2020-06-20'),(18,18,'2020-06-20'),(19,19,'2020-06-20'),(20,20,'2020-06-20'),(21,21,'2020-06-20'),(22,22,'2020-06-20'),(23,23,'2020-06-20'),(24,24,'2020-06-20'),(25,25,'2020-06-20'),(26,26,'2020-06-20'),(27,27,'2020-06-20'),(28,28,'2020-06-20'),(29,29,'2020-06-20'),(30,30,'2020-06-20'),(31,31,'2020-06-20'),(32,32,'2020-06-20'),(33,33,'2020-06-20');
/*!40000 ALTER TABLE `maintain_dates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_essentials`
--

DROP TABLE IF EXISTS `manager_essentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_essentials` (
  `code` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(80) NOT NULL,
  `department` enum('Admissions','Open Cardiology','Radiology') DEFAULT NULL,
  `status` enum('hired','fired','resigned') NOT NULL DEFAULT 'hired',
  `insurance` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_essentials`
--

LOCK TABLES `manager_essentials` WRITE;
/*!40000 ALTER TABLE `manager_essentials` DISABLE KEYS */;
INSERT INTO `manager_essentials` VALUES (1,'Ahmed Khaled','Radiology','hired',0),(2,'Bassam Mostafa','Open Cardiology','hired',0),(3,'Mossad Ibrahim','Admissions','hired',0);
/*!40000 ALTER TABLE `manager_essentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_extras`
--

DROP TABLE IF EXISTS `manager_extras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_extras` (
  `r_code` smallint(5) unsigned NOT NULL,
  `SSN` bigint(20) unsigned NOT NULL DEFAULT '0',
  `sex` enum('male','female') NOT NULL DEFAULT 'male',
  `phone` bigint(20) unsigned NOT NULL,
  `bdate` date DEFAULT NULL,
  `street` varchar(100) NOT NULL DEFAULT '0',
  `province` enum('ALX','ASN','AST','BA','BH','BNS','C','DK','DT','FYM','GH','GZ','IS','JS','KB','KFS','KN','MN','MNF','MT','PTS','SHG','SHR','SIN','SUZ','WAD') DEFAULT NULL,
  PRIMARY KEY (`r_code`),
  CONSTRAINT `manager_extras_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `manager_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_extras`
--

LOCK TABLES `manager_extras` WRITE;
/*!40000 ALTER TABLE `manager_extras` DISABLE KEYS */;
INSERT INTO `manager_extras` VALUES (1,29811080106278,'male',1000957893,'1998-11-08','19','C'),(2,29711030108923,'male',1013609634,'1997-11-03','20','GZ'),(3,29511090205983,'male',1001983456,'1995-11-09','12 Maadi','C');
/*!40000 ALTER TABLE `manager_extras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_essentials`
--

DROP TABLE IF EXISTS `order_essentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_essentials` (
  `code` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `serial` bigint(20) unsigned NOT NULL DEFAULT '0',
  `place` varchar(80) NOT NULL,
  `type` varchar(80) NOT NULL,
  `department` enum('Admissions','Open Cardiology','Radiology') DEFAULT NULL,
  `tech_code` smallint(5) unsigned DEFAULT NULL,
  `date_issued` date NOT NULL,
  `date_responded` date DEFAULT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `serial` (`serial`,`date_issued`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_essentials`
--

LOCK TABLES `order_essentials` WRITE;
/*!40000 ALTER TABLE `order_essentials` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_essentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_CT`
--

DROP TABLE IF EXISTS `order_extras_CT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_CT` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `Above_limit_radiation` enum('found','none') NOT NULL DEFAULT 'none',
  `Compromised_image_quality` enum('found','none') NOT NULL DEFAULT 'none',
  `Lubricate_bearings` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Lubricate_gears` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_ct_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_CT`
--

LOCK TABLES `order_extras_CT` WRITE;
/*!40000 ALTER TABLE `order_extras_CT` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_CT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_ECG`
--

DROP TABLE IF EXISTS `order_extras_ECG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_ECG` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `foreign_substance` enum('found','none') NOT NULL DEFAULT 'none',
  `cracks` enum('found','none') NOT NULL DEFAULT 'none',
  `broken_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `leaky_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `drained_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_cable` enum('found','none') NOT NULL DEFAULT 'none',
  `expired_electrode` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_elec_package` enum('found','none') NOT NULL DEFAULT 'none',
  `Incorrect_paper_loading` enum('found','none') NOT NULL DEFAULT 'none',
  `Printing_head_problem` enum('found','none') NOT NULL DEFAULT 'none',
  `service_indicator` enum('available','not found') NOT NULL DEFAULT 'not found',
  `spare_batteries_avaiable` enum('available','not found') NOT NULL DEFAULT 'not found',
  `spare_electrodes_avaiable` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_ecg_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_ECG`
--

LOCK TABLES `order_extras_ECG` WRITE;
/*!40000 ALTER TABLE `order_extras_ECG` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_ECG` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_Gamma_Camera`
--

DROP TABLE IF EXISTS `order_extras_Gamma_Camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_Gamma_Camera` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `Above_limit_radiation` enum('found','none') NOT NULL DEFAULT 'none',
  `Compromised_image_quality` enum('found','none') NOT NULL DEFAULT 'none',
  `Lubricate_bearings` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Lubricate_gears` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_gamma_camera_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_Gamma_Camera`
--

LOCK TABLES `order_extras_Gamma_Camera` WRITE;
/*!40000 ALTER TABLE `order_extras_Gamma_Camera` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_Gamma_Camera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_MRI`
--

DROP TABLE IF EXISTS `order_extras_MRI`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_MRI` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `Above_limit_magnetization` enum('found','none') NOT NULL DEFAULT 'none',
  `Compromised_image_quality` enum('found','none') NOT NULL DEFAULT 'none',
  `Lubricate_bearings` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Lubricate_gears` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_mri_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_MRI`
--

LOCK TABLES `order_extras_MRI` WRITE;
/*!40000 ALTER TABLE `order_extras_MRI` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_MRI` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_Ultrasonic`
--

DROP TABLE IF EXISTS `order_extras_Ultrasonic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_Ultrasonic` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_transducer` enum('found','none') NOT NULL DEFAULT 'none',
  `Compromised_image_quality` enum('found','none') NOT NULL DEFAULT 'none',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_ultrasonic_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_Ultrasonic`
--

LOCK TABLES `order_extras_Ultrasonic` WRITE;
/*!40000 ALTER TABLE `order_extras_Ultrasonic` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_Ultrasonic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_X_Ray`
--

DROP TABLE IF EXISTS `order_extras_X_Ray`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_X_Ray` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `Above_limit_radiation` enum('found','none') NOT NULL DEFAULT 'none',
  `Compromised_image_quality` enum('found','none') NOT NULL DEFAULT 'none',
  `Lubricate_bearings` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Lubricate_gears` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_x_ray_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_X_Ray`
--

LOCK TABLES `order_extras_X_Ray` WRITE;
/*!40000 ALTER TABLE `order_extras_X_Ray` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_X_Ray` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_blood_gas`
--

DROP TABLE IF EXISTS `order_extras_blood_gas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_blood_gas` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_bulbs` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_heaters` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_blood_gas_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_blood_gas`
--

LOCK TABLES `order_extras_blood_gas` WRITE;
/*!40000 ALTER TABLE `order_extras_blood_gas` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_blood_gas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_defib`
--

DROP TABLE IF EXISTS `order_extras_defib`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_defib` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `foreign_substance` enum('found','none') NOT NULL DEFAULT 'none',
  `cracks` enum('found','none') NOT NULL DEFAULT 'none',
  `broken_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `leaky_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `drained_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_cable` enum('found','none') NOT NULL DEFAULT 'none',
  `expired_electrode` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_elecrode_package` enum('found','none') NOT NULL DEFAULT 'none',
  `service_indicator` enum('available','not found') NOT NULL DEFAULT 'not found',
  `illumination_self_test` enum('available','not found') NOT NULL DEFAULT 'not found',
  `LEDs_on` enum('available','not found') NOT NULL DEFAULT 'not found',
  `speaker_beep` enum('available','not found') NOT NULL DEFAULT 'not found',
  `spare_batteries_avaiable` enum('available','not found') NOT NULL DEFAULT 'not found',
  `spare_electrodes_avaiable` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_defib_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_defib`
--

LOCK TABLES `order_extras_defib` WRITE;
/*!40000 ALTER TABLE `order_extras_defib` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_defib` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_infusion_pump`
--

DROP TABLE IF EXISTS `order_extras_infusion_pump`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_infusion_pump` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `cracks_in_strain_reliefs` enum('found','none') NOT NULL DEFAULT 'none',
  `Casters_or_brakes_not_mounted` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_detectors` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_Flow_and_Stop_Mechanisms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_infusion_pump_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_infusion_pump`
--

LOCK TABLES `order_extras_infusion_pump` WRITE;
/*!40000 ALTER TABLE `order_extras_infusion_pump` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_infusion_pump` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_mob_ventilator`
--

DROP TABLE IF EXISTS `order_extras_mob_ventilator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_mob_ventilator` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `broken_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `leaky_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `drained_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_charger` enum('found','none') NOT NULL DEFAULT 'none',
  `All_modes_working` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_air_filter` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_bacteria_filter` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_fan_filter` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_oxygen_sensor` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Spare_air_filters` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Spare_bacteria_filters` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Spare_oxygen_sensors` enum('available','not found') NOT NULL DEFAULT 'not found',
  `spare_batteries_avaiable` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_mob_ventilator_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_mob_ventilator`
--

LOCK TABLES `order_extras_mob_ventilator` WRITE;
/*!40000 ALTER TABLE `order_extras_mob_ventilator` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_mob_ventilator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_monitor`
--

DROP TABLE IF EXISTS `order_extras_monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_monitor` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `cracks_in_strain_reliefs` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_cable` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_probes` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `broken_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `leaky_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `drained_battery` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_charger` enum('found','none') NOT NULL DEFAULT 'none',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `spare_batteries_avaiable` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_monitor_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_monitor`
--

LOCK TABLES `order_extras_monitor` WRITE;
/*!40000 ALTER TABLE `order_extras_monitor` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_monitor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_syringe_pump`
--

DROP TABLE IF EXISTS `order_extras_syringe_pump`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_syringe_pump` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `cracks_in_strain_reliefs` enum('found','none') NOT NULL DEFAULT 'none',
  `Casters_or_brakes_not_mounted` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_detectors` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_Flow_and_Stop_Mechanisms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_syringe_pump_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_syringe_pump`
--

LOCK TABLES `order_extras_syringe_pump` WRITE;
/*!40000 ALTER TABLE `order_extras_syringe_pump` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_syringe_pump` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_extras_ventilator`
--

DROP TABLE IF EXISTS `order_extras_ventilator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_extras_ventilator` (
  `r_code` mediumint(8) unsigned NOT NULL,
  `cracks_in_chassis` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_AC_plug` enum('found','none') NOT NULL DEFAULT 'none',
  `damaged_line_cord` enum('found','none') NOT NULL DEFAULT 'none',
  `tripped_Breaker` enum('found','none') NOT NULL DEFAULT 'none',
  `unconnected_cable_connectors` enum('found','none') NOT NULL DEFAULT 'none',
  `malfunctional_Switches` enum('found','none') NOT NULL DEFAULT 'none',
  `All_modes_working` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_air_filter` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_bacteria_filter` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_fan_filter` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Change_oxygen_sensor` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Indicators_or_displays` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_alarms` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Audible_signals` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Operational_labeling` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Spare_air_filters` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Spare_bacteria_filters` enum('available','not found') NOT NULL DEFAULT 'not found',
  `Spare_oxygen_sensors` enum('available','not found') NOT NULL DEFAULT 'not found',
  `notes` varchar(255) NOT NULL DEFAULT '0',
  KEY `r_code` (`r_code`),
  CONSTRAINT `order_extras_ventilator_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `order_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_extras_ventilator`
--

LOCK TABLES `order_extras_ventilator` WRITE;
/*!40000 ALTER TABLE `order_extras_ventilator` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_extras_ventilator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_install`
--

DROP TABLE IF EXISTS `report_install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_install` (
  `code` mediumint(8) unsigned NOT NULL,
  `receive_date` date DEFAULT NULL,
  `device_name` varchar(50) NOT NULL DEFAULT '0',
  `device_type` varchar(50) NOT NULL DEFAULT '0',
  `device_serial` bigint(20) unsigned NOT NULL DEFAULT '0',
  `device_manufacturer` varchar(50) NOT NULL,
  `cost` int(10) unsigned NOT NULL DEFAULT '0',
  `department` enum('Admissions','Open Cardiology','Radiology') DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_install`
--

LOCK TABLES `report_install` WRITE;
/*!40000 ALTER TABLE `report_install` DISABLE KEYS */;
INSERT INTO `report_install` VALUES (1,'2020-05-20','Yuwell Bi-level PAP Ventilator','Ventilator',1000,'Oxford Ventilators',320000,'Open Cardiology'),(2,'2020-05-20','Yuwell Ventilator II','Ventilator',1001,'Oxford Ventilators',320000,'Open Cardiology'),(3,'2020-05-20','Yuwell Ventilator III','Ventilator',1002,'Oxford Ventilators',320000,'Open Cardiology'),(5,'2020-05-20','HeartStart XL Defibrillator I','Defibrillator',2000,'Philips ',6000,'Open Cardiology'),(6,'2020-05-20','HeartStart XL Defibrillator II','Defibrillator',2001,'Philips',60000,'Open Cardiology'),(7,'2020-05-20','Infinity Delta Monitor I','Monitor',3000,'Draeger',30000,'Open Cardiology'),(8,'2020-05-20','Infinity Delta Monitor II','Monitor',3001,'Draeger',30000,'Open Cardiology'),(9,'2020-05-20','Infinity Delta Monitor III','Monitor',3002,'Draeger',30000,'Open Cardiology'),(10,'2020-05-20','Infinity Delta Monitor IV','Monitor',3003,'Draeger',30000,'Open Cardiology'),(11,'2020-05-20','Ultrasound Machine I','Ultrasonic',4000,'Dawei Medical',200000,'Open Cardiology'),(12,'2020-05-20','Ultrasound Machine II','Ultrasonic',4001,'Dawei Medical',200000,'Open Cardiology'),(13,'2020-05-20','Ultrasound Machine III','Ultrasonic',4002,'SIEMENS',500000,'Open Cardiology'),(14,'2020-05-20','X-Ray Device I','X-Ray',1400,'TOSHIBA',500000,'Open Cardiology'),(15,'2020-05-20','X-Ray Device I','X-Ray',1401,'TOSHIBA',500000,'Open Cardiology'),(16,'2020-05-20','Ultrasound Machine IV','Ultrasonic',2000,'SIEMENS',500000,'Radiology'),(17,'2020-05-20','Ultrasound Machine V','Ultrasonic',2001,'SIEMENS',500000,'Radiology'),(18,'2020-05-20','Ultrasound Machine VI','Ultrasonic',2002,'SIEMENS',500000,'Radiology'),(19,'2020-05-20','X-Ray Device II','X-Ray',2100,'TOSHIBA',100000,'Radiology'),(20,'2020-05-20','X-Ray Device III','X-Ray',2101,'TOSHIBA',100000,'Radiology'),(21,'2020-05-20','X-Ray Device IV','X-Ray',2102,'TOSHIBA',100000,'Radiology'),(22,'2020-05-20','Brilliance CT Machine I','CT',2200,'Philips ',1500000,'Radiology'),(23,'2020-05-20','Brilliance CT Machine II','Ultrasonic',2201,'Philips',1500000,'Radiology'),(24,'2020-05-20','Espree MRI Machine I','MRI',2300,'Siemens',3000000,'Radiology'),(25,'2020-05-20','Espree MRI Machine II','MRI',2301,'Siemens',3000000,'Radiology'),(26,'2020-05-20','IPS-12 Syringe Pump I','Syringe Pump',3000,'Inovenso ',10000,'Admissions'),(27,'2020-05-20','IPS-12 Syringe Pump II','Syringe Pump',3001,'Inovenso ',10000,'Admissions'),(28,'2020-05-20','Infinity Delta Monitor I','Monitor',3100,'Draeger	',30000,'Open Cardiology'),(29,'2020-05-20','Infinity Delta Monitor VI','Monitor',3101,'Draeger	',30000,'Admissions'),(30,'2020-05-20','HeartStart XL Defibrillator III','Defibrillator',3200,'Philips',60000,'Admissions'),(31,'2020-05-20','HeartStart XL Defibrillator IV','Defibrillator',3201,'Philips',60000,'Admissions'),(32,'2020-05-20','ECG MACHINE I','ECG',3300,'BURDICK',65000,'Admissions'),(33,'2020-05-20','ECG MACHINE II','ECG',3301,'BURDICK ',65000,'Admissions');
/*!40000 ALTER TABLE `report_install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_move`
--

DROP TABLE IF EXISTS `report_move`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_move` (
  `code` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `to_dep` enum('Admissions','Open Cardiology','Radiology') DEFAULT NULL,
  `from_dep` enum('Admissions','Open Cardiology','Radiology') DEFAULT NULL,
  `move_date` date DEFAULT NULL,
  `device_code` mediumint(8) unsigned NOT NULL,
  `device_name` varchar(50) NOT NULL DEFAULT '0',
  `device_type` varchar(50) NOT NULL DEFAULT '0',
  `device_serial` bigint(20) unsigned NOT NULL DEFAULT '0',
  `device_manufacturer` varchar(50) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_move`
--

LOCK TABLES `report_move` WRITE;
/*!40000 ALTER TABLE `report_move` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_move` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_scrap`
--

DROP TABLE IF EXISTS `report_scrap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_scrap` (
  `code` mediumint(8) unsigned NOT NULL,
  `date` date NOT NULL,
  `device_name` varchar(50) NOT NULL DEFAULT '0',
  `device_type` varchar(50) NOT NULL DEFAULT '0',
  `device_serial` bigint(20) unsigned NOT NULL DEFAULT '0',
  `device_manufacturer` varchar(50) NOT NULL,
  `cause` enum('upgrading','non-functional') NOT NULL DEFAULT 'non-functional',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_scrap`
--

LOCK TABLES `report_scrap` WRITE;
/*!40000 ALTER TABLE `report_scrap` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_scrap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tech_essentials`
--

DROP TABLE IF EXISTS `tech_essentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tech_essentials` (
  `code` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(80) NOT NULL,
  `department` enum('Admissions','Open Cardiology','Radiology') DEFAULT NULL,
  `status` enum('hired','fired','resigned') NOT NULL DEFAULT 'hired',
  `insurance` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tech_essentials`
--

LOCK TABLES `tech_essentials` WRITE;
/*!40000 ALTER TABLE `tech_essentials` DISABLE KEYS */;
INSERT INTO `tech_essentials` VALUES (1,'Mahmoud Mohamed','Admissions','hired',20000),(2,'Mona Abdelaziz','Radiology','hired',20000),(3,'Ismail Yasser','Open Cardiology','hired',40000),(4,'Mohamed Khaled','Admissions','hired',20000),(5,'Moataz Shaaban','Open Cardiology','hired',25000),(6,'Osama Emam','Radiology','hired',20000);
/*!40000 ALTER TABLE `tech_essentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tech_extras`
--

DROP TABLE IF EXISTS `tech_extras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tech_extras` (
  `r_code` smallint(5) unsigned NOT NULL,
  `SSN` bigint(20) unsigned NOT NULL DEFAULT '0',
  `sex` enum('male','female') NOT NULL DEFAULT 'male',
  `phone` bigint(20) unsigned NOT NULL,
  `bdate` date DEFAULT NULL,
  `street` varchar(100) NOT NULL DEFAULT '0',
  `province` enum('ALX','ASN','AST','BA','BH','BNS','C','DK','DT','FYM','GH','GZ','IS','JS','KB','KFS','KN','MN','MNF','MT','PTS','SHG','SHR','SIN','SUZ','WAD') DEFAULT NULL,
  PRIMARY KEY (`r_code`),
  CONSTRAINT `tech_extras_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `tech_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tech_extras`
--

LOCK TABLES `tech_extras` WRITE;
/*!40000 ALTER TABLE `tech_extras` DISABLE KEYS */;
INSERT INTO `tech_extras` VALUES (1,29011080102038,'male',1009356444,'1990-11-08','18 Mohamed Bakr, Autostrad','C'),(2,29410060509789,'female',1009456543,'1994-10-06','20 Saqr Koraysh','C'),(3,29311080106273,'male',1111967836,'1993-11-08','12B Main Road, Degla, Maadi','C'),(4,29511090203874,'male',1259027839,'1993-11-09','18 Badr El Mokaddam, Nasr City','C'),(5,29511030209387,'male',1273020301,'1995-11-03','28 Bolak St, Omaranya','GZ'),(6,29405050903283,'male',1000968203,'1994-05-05','98 Mahmoud Sakr, Helwan','C');
/*!40000 ALTER TABLE `tech_extras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_man`
--

DROP TABLE IF EXISTS `users_man`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_man` (
  `code` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(51) NOT NULL,
  `hash` char(74) NOT NULL,
  `token` char(32) NOT NULL,
  `email` varchar(70) NOT NULL,
  `r_code` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `username` (`username`),
  KEY `r_code` (`r_code`),
  CONSTRAINT `users_man_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `manager_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_man`
--

LOCK TABLES `users_man` WRITE;
/*!40000 ALTER TABLE `users_man` DISABLE KEYS */;
INSERT INTO `users_man` VALUES (1,'Ahmed08','xvfWou92$a2b98b2601baa19c7d364f56f3f3b4c67c687634d76a9bf60120aec755ebb04d','7b2e2047bfabab51d95ee073c0930a94','ahmed.khaled0811@gmail.com',1),(2,'Bassam10','VtUxGDyM$3dfc21c16fc6563bce273abed9bfe7925804890cdea0ceb8e79196ea4e89da4a','1586ea44a676618a2a39b7d34c97388e','bassam.mostafa@gmail.com',2),(3,'Mossad95','tvuR7Y80$e75846cdda04c9f85b3985942e820d5bc6ab62ed01e49406d0dfd495c9f04e6b','ba101f6dabd687d4e9d1f1cf0c9442fa','mossad.ibrahim@hotmail.com',3);
/*!40000 ALTER TABLE `users_man` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_tech`
--

DROP TABLE IF EXISTS `users_tech`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_tech` (
  `code` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(51) NOT NULL,
  `hash` char(74) NOT NULL,
  `token` char(32) NOT NULL,
  `email` varchar(70) NOT NULL,
  `r_code` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `username` (`username`),
  KEY `r_code` (`r_code`),
  CONSTRAINT `users_tech_ibfk_1` FOREIGN KEY (`r_code`) REFERENCES `tech_essentials` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_tech`
--

LOCK TABLES `users_tech` WRITE;
/*!40000 ALTER TABLE `users_tech` DISABLE KEYS */;
INSERT INTO `users_tech` VALUES (1,'Mahmoud90','tHUqOwmn$bdd54de70e1de214ad0348a5066f8b2988619495cd905c049cb6fb55f7f7c395','e7d5a51d90d37fb8e4dab8083cebe13f','mahmoud.mohamed@yahoo.com',1),(2,'Mona94','zTweYt3N$97f58dedbab6f7506ea130ea33179d3c3bf6de86ca0faca133ae0bb822cf61e7','1a47c116b3776f21733b5697866edd27','mona.abdelaziz@yahoo.com',2),(3,'Ismail1993','lKafFlKI$c846ef430410a6d0f3772a746496b2722b8ef9e5880b77289817c3e48c5a252c','9944668fd27c09e64fdb46985021c661','ismail.yasser@gmail.com',3),(4,'MoKhaled9','ZSqGuvMA$f6272b3321f37d9dae1a772cf0d9bacde5d9a25988ce57a738a8a404a370e7e1','9d191c69e29e9707fd7cdeab050cb7c4','mohamed.khaled@gmail.com',4),(5,'Moataz95','sgbIDods$d93473f209b6100224925051cdb9065f8e38f7f93a920f603a7c8d2df0336564','7dcd5676c05fb9d45ad3bd6dd9c54be7','moataz.shaaban@gmail.com',5),(6,'Osama94','Ht8OwhFs$6b02d4020f74b27b3892979d11ad66cea01ec11405a278abb619ef3b6edc9be3','280f82be962f15b4a12d72fc88ec50ae','osama.emam@gmail.com',6);
/*!40000 ALTER TABLE `users_tech` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-24 17:40:22
