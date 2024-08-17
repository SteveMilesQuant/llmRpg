-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: mysql-level-up-writing.cfsjncjzpepg.us-east-1.rds.amazonaws.com    Database: level-up-writing
-- ------------------------------------------------------
-- Server version	8.0.35

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `camp`
--

DROP TABLE IF EXISTS `camp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `primary_instructor_id` int NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `daily_start_time` time DEFAULT NULL,
  `daily_end_time` time DEFAULT NULL,
  `cost` float DEFAULT NULL,
  `location` text,
  PRIMARY KEY (`id`),
  KEY `program_id` (`program_id`),
  KEY `primary_instructor_id` (`primary_instructor_id`),
  CONSTRAINT `camp_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`),
  CONSTRAINT `camp_ibfk_2` FOREIGN KEY (`primary_instructor_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp`
--

LOCK TABLES `camp` WRITE;
/*!40000 ALTER TABLE `camp` DISABLE KEYS */;
INSERT INTO `camp` VALUES (2,6,2,0,'09:00:00','16:00:00',90,'Apex Baptist Church (110 S Salem St, Apex, NC 27502)'),(3,7,2,0,'09:00:00','16:00:00',90,'Apex Baptist Church (110 S Salem St, Apex, NC 27502)'),(4,2,2,1,'09:00:00','16:00:00',315,'Apex Baptist Church (110 S Salem St, Apex, NC 27502)'),(5,4,2,1,'09:00:00','12:00:00',90,'Apex Baptist Church (110 S Salem St, Apex, NC 27502)'),(6,3,2,1,'09:00:00','16:00:00',315,'Hope Community Church (Apex Campus) - 2080 East Williams St, Apex, NC 27539'),(8,3,2,1,'09:00:00','16:00:00',315,'TBD: As a new small business we are renting spaces from local venues until we are able to attain a permanent establishment. We are currently in the process of confirming our location for this camp; this event will be in the Apex area. '),(12,5,6,1,'09:00:00','16:00:00',315,'Hope Community Church (Apex Campus) - 2080 East Williams St, Apex, NC 27539'),(13,8,2,1,'09:00:00','16:00:00',315,'TBD: As a new small business we are renting spaces from local venues until we are able to attain a permanent establishment. We are currently in the process of confirming our location for this camp; this event will be in the Apex area.');
/*!40000 ALTER TABLE `camp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camp_x_dates`
--

DROP TABLE IF EXISTS `camp_x_dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camp_x_dates` (
  `date` date NOT NULL,
  `camp_id` int NOT NULL,
  PRIMARY KEY (`date`),
  KEY `camp_id` (`camp_id`),
  CONSTRAINT `camp_x_dates_ibfk_1` FOREIGN KEY (`camp_id`) REFERENCES `camp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_x_dates`
--

LOCK TABLES `camp_x_dates` WRITE;
/*!40000 ALTER TABLE `camp_x_dates` DISABLE KEYS */;
INSERT INTO `camp_x_dates` VALUES ('2024-03-26',2),('2024-03-28',3),('2024-06-17',4),('2024-06-18',4),('2024-06-19',4),('2024-06-20',4),('2024-06-21',4),('2024-04-29',5),('2024-07-08',6),('2024-07-09',6),('2024-07-10',6),('2024-07-11',6),('2024-07-12',6),('2024-07-22',8),('2024-07-23',8),('2024-07-24',8),('2024-07-25',8),('2024-07-26',8),('2024-07-15',12),('2024-07-16',12),('2024-07-17',12),('2024-07-18',12),('2024-07-19',12),('2024-08-12',13),('2024-08-13',13),('2024-08-14',13),('2024-08-15',13),('2024-08-16',13);
/*!40000 ALTER TABLE `camp_x_dates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camp_x_instructors`
--

DROP TABLE IF EXISTS `camp_x_instructors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camp_x_instructors` (
  `camp_id` int NOT NULL,
  `instructor_id` int NOT NULL,
  PRIMARY KEY (`camp_id`,`instructor_id`),
  KEY `instructor_id` (`instructor_id`),
  CONSTRAINT `camp_x_instructors_ibfk_1` FOREIGN KEY (`camp_id`) REFERENCES `camp` (`id`),
  CONSTRAINT `camp_x_instructors_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_x_instructors`
--

LOCK TABLES `camp_x_instructors` WRITE;
/*!40000 ALTER TABLE `camp_x_instructors` DISABLE KEYS */;
INSERT INTO `camp_x_instructors` VALUES (2,2),(3,2),(4,2),(5,2),(6,2),(8,2),(12,2),(13,2),(2,6),(3,6),(4,6),(5,6),(6,6),(8,6),(12,6),(13,6);
/*!40000 ALTER TABLE `camp_x_instructors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camp_x_students`
--

DROP TABLE IF EXISTS `camp_x_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camp_x_students` (
  `camp_id` int NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`camp_id`,`student_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `camp_x_students_ibfk_1` FOREIGN KEY (`camp_id`) REFERENCES `camp` (`id`),
  CONSTRAINT `camp_x_students_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_x_students`
--

LOCK TABLES `camp_x_students` WRITE;
/*!40000 ALTER TABLE `camp_x_students` DISABLE KEYS */;
INSERT INTO `camp_x_students` VALUES (2,8),(3,8),(5,8),(5,9),(2,14),(3,14),(5,15),(5,16),(5,18),(4,19),(6,19),(12,19),(5,20),(3,21),(13,21),(3,22),(13,22),(4,23),(6,23),(12,23),(4,24),(12,24),(13,26),(3,27),(5,27),(13,27),(3,28),(5,28),(13,28),(6,29),(13,30),(3,31),(5,31),(4,32),(8,32),(12,32),(13,32),(8,33),(4,34),(6,34),(13,34),(6,35),(13,36);
/*!40000 ALTER TABLE `camp_x_students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupon`
--

DROP TABLE IF EXISTS `coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupon` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` text NOT NULL,
  `discount_type` text NOT NULL,
  `discount_amount` int NOT NULL,
  `expiration` date DEFAULT NULL,
  `used_count` int NOT NULL,
  `max_count` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupon`
--

LOCK TABLES `coupon` WRITE;
/*!40000 ALTER TABLE `coupon` DISABLE KEYS */;
INSERT INTO `coupon` VALUES (1,'LEVELUPGIRLS','percent',15,'2024-08-01',0,NULL),(2,'SHANNONM','percent',100,'2024-04-30',1,1),(3,'DDESTEAM','percent',10,'2024-08-01',0,300);
/*!40000 ALTER TABLE `coupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `endpoint`
--

DROP TABLE IF EXISTS `endpoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `endpoint` (
  `role` varchar(32) NOT NULL,
  `url` varchar(32) NOT NULL,
  `title` text NOT NULL,
  PRIMARY KEY (`role`,`url`),
  CONSTRAINT `endpoint_ibfk_1` FOREIGN KEY (`role`) REFERENCES `role` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endpoint`
--

LOCK TABLES `endpoint` WRITE;
/*!40000 ALTER TABLE `endpoint` DISABLE KEYS */;
INSERT INTO `endpoint` VALUES ('ADMIN','/members','Manage Members'),('ADMIN','/schedule','Schedule Camps'),('GUARDIAN','/camps','Find Camps'),('GUARDIAN','/students','My Students'),('INSTRUCTOR','/programs','Design Programs'),('INSTRUCTOR','/teach','My Camps');
/*!40000 ALTER TABLE `endpoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `level`
--

DROP TABLE IF EXISTS `level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `level` (
  `id` int NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `title` text NOT NULL,
  `description` text NOT NULL,
  `list_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `program_id` (`program_id`),
  CONSTRAINT `level_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `level`
--

LOCK TABLES `level` WRITE;
/*!40000 ALTER TABLE `level` DISABLE KEYS */;
INSERT INTO `level` VALUES (10,2,'Schedule','Schedule TBD',1),(11,3,'Schedule','Schedule TBD',1),(12,4,'Schedule','Schedule TBD',1),(13,5,'Schedule','Schedule TBD',1);
/*!40000 ALTER TABLE `level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_record`
--

DROP TABLE IF EXISTS `payment_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `square_payment_id` text,
  `square_order_id` text,
  `square_receipt_number` text,
  `camp_id` int NOT NULL,
  `student_id` int NOT NULL,
  `user_id` int NOT NULL DEFAULT '1',
  `coupon_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `camp_id` (`camp_id`),
  KEY `student_id` (`student_id`),
  KEY `fk_user_id` (`user_id`),
  KEY `fk_coupon_id` (`coupon_id`),
  CONSTRAINT `fk_coupon_id` FOREIGN KEY (`coupon_id`) REFERENCES `coupon` (`id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `payment_record_ibfk_1` FOREIGN KEY (`camp_id`) REFERENCES `camp` (`id`),
  CONSTRAINT `payment_record_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_record`
--

LOCK TABLES `payment_record` WRITE;
/*!40000 ALTER TABLE `payment_record` DISABLE KEYS */;
INSERT INTO `payment_record` VALUES (1,'DBelvIKu0NQR0jf7icLkZ9D5fdNZY','pi7X57dsPR5bmaY4LgCP1znSt59YY','DBel',4,19,17,NULL),(2,'DBelvIKu0NQR0jf7icLkZ9D5fdNZY','pi7X57dsPR5bmaY4LgCP1znSt59YY','DBel',6,19,17,NULL),(3,'DBelvIKu0NQR0jf7icLkZ9D5fdNZY','pi7X57dsPR5bmaY4LgCP1znSt59YY','DBel',12,19,17,NULL),(4,'VCAa4uQVXKCsYnuZT8zrO0yL2SQZY','jtMKDsMtHDG7AuutqBnvFtRxKoWZY','VCAa',6,23,20,NULL),(5,'VCAa4uQVXKCsYnuZT8zrO0yL2SQZY','jtMKDsMtHDG7AuutqBnvFtRxKoWZY','VCAa',4,23,20,NULL),(6,'VCAa4uQVXKCsYnuZT8zrO0yL2SQZY','jtMKDsMtHDG7AuutqBnvFtRxKoWZY','VCAa',12,23,20,NULL),(7,'','','',2,8,9,NULL),(8,'','','',3,8,9,NULL),(9,'','','',5,8,9,NULL),(10,'','','',5,9,11,NULL),(11,'','','',2,14,13,NULL),(12,'','','',3,14,13,NULL),(13,'','','',4,14,13,NULL),(14,'','','',5,14,13,NULL),(15,'','','',6,14,13,NULL),(16,'','','',12,14,13,NULL),(17,'','','',13,14,13,NULL),(18,'','','',5,15,14,NULL),(19,'','','',5,16,15,NULL),(20,'','','',5,17,14,NULL),(21,'','','',5,18,16,NULL),(22,'','','',5,20,18,NULL),(23,'','','',3,21,19,NULL),(24,'','','',8,21,19,NULL),(25,'','','',13,21,19,NULL),(26,'','','',3,22,19,NULL),(27,'','','',8,22,19,NULL),(28,'','','',13,22,19,NULL),(38,'hIWxyEsrcDFrSrBgGm3slkuTNcEZY','7vNXtnISvEQfZLcEODSf37TOsvOZY','hIWx',4,24,21,NULL),(39,'hIWxyEsrcDFrSrBgGm3slkuTNcEZY','7vNXtnISvEQfZLcEODSf37TOsvOZY','hIWx',12,24,21,NULL),(40,'j58QcREYZaS2X6HRtssBSKezqo6YY','dwPibYoNDpOPF8BjTGc2DBuoBfGZY','j58Q',13,26,23,NULL),(41,'777yE5GFdJS26TW4Xn7BJxwiqSYZY','1EHsCqFWRtCRB6gygaFzaz4oBLRZY','777y',3,27,24,NULL),(42,'777yE5GFdJS26TW4Xn7BJxwiqSYZY','1EHsCqFWRtCRB6gygaFzaz4oBLRZY','777y',3,28,24,NULL),(43,'777yE5GFdJS26TW4Xn7BJxwiqSYZY','1EHsCqFWRtCRB6gygaFzaz4oBLRZY','777y',5,27,24,NULL),(44,'777yE5GFdJS26TW4Xn7BJxwiqSYZY','1EHsCqFWRtCRB6gygaFzaz4oBLRZY','777y',5,28,24,NULL),(45,'777yE5GFdJS26TW4Xn7BJxwiqSYZY','1EHsCqFWRtCRB6gygaFzaz4oBLRZY','777y',13,27,24,NULL),(46,'777yE5GFdJS26TW4Xn7BJxwiqSYZY','1EHsCqFWRtCRB6gygaFzaz4oBLRZY','777y',13,28,24,NULL),(47,'pgMTCvBUv0Qy7eOp93iGD7vMyw7YY','1AdaJNzB1exfWMcgGtoVqblcf77YY','pgMT',6,29,25,NULL),(48,'zjFiBgxWMH1bO9WZSp7DcFFq2ADZY','pAY6GUeGG6xAybzDAw3fPmE8tFfZY','zjFi',13,30,26,NULL),(49,'JksWWBQmhNj6GpOWiJcKWPS5RqBZY','FQdcLpsa12VMXnVRXegNNT7z7OHZY','JksW',3,31,28,NULL),(50,'JksWWBQmhNj6GpOWiJcKWPS5RqBZY','FQdcLpsa12VMXnVRXegNNT7z7OHZY','JksW',5,31,28,NULL),(51,'Z8I8CEmkqLjpx3Sw87k3pS339WbZY','35HXayhyz8Nq6MSlqYNanLjxuFXZY','Z8I8',4,32,29,NULL),(52,'Z8I8CEmkqLjpx3Sw87k3pS339WbZY','35HXayhyz8Nq6MSlqYNanLjxuFXZY','Z8I8',12,32,29,NULL),(53,'Z8I8CEmkqLjpx3Sw87k3pS339WbZY','35HXayhyz8Nq6MSlqYNanLjxuFXZY','Z8I8',8,32,29,NULL),(54,'Z8I8CEmkqLjpx3Sw87k3pS339WbZY','35HXayhyz8Nq6MSlqYNanLjxuFXZY','Z8I8',13,32,29,NULL),(55,NULL,NULL,NULL,8,33,30,2),(56,'71KNvUdF1M3vRG9w4b8C3Fj7hIYZY','zFCj6Nf6zRN6GJUNldsiOpW12nBZY','71KN',4,34,31,NULL),(57,'71KNvUdF1M3vRG9w4b8C3Fj7hIYZY','zFCj6Nf6zRN6GJUNldsiOpW12nBZY','71KN',6,34,31,NULL),(58,'71KNvUdF1M3vRG9w4b8C3Fj7hIYZY','zFCj6Nf6zRN6GJUNldsiOpW12nBZY','71KN',13,34,31,NULL),(59,'bpq4B6fL8RDY9OmiwqDNCUAVtuGZY','Fo1Uf4jp9UipMTnGxB3tzi6PT0SZY','bpq4',6,35,32,NULL),(60,'RSfLzExj2zPaLI2O08gGbEKnGEFZY','dYdfXmuPVHwQchBH00aiTqNtYBbZY','RSfL',13,36,34,NULL);
/*!40000 ALTER TABLE `payment_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `from_grade` int DEFAULT NULL,
  `to_grade` int DEFAULT NULL,
  `tags` text NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
INSERT INTO `program` VALUES (2,'Creative Writing (Full Week)',3,7,'Writing','Students will grow as creative writers through mini lessons focusing on writing skills such as characterization and descriptive language. In addition to the language arts focus, campers can also look forward to crafts, games, team challenges, projects, and experiments.\n\nLanguage Arts Focus: \nCharacter Development\nCharacterization\nDescriptive Language \nDialogue Development\nElements of Plot \nFigurative Language\n\n(partial week enrollment options available upon request)'),(3,'Language Arts Breakout (Full Week)',3,7,'Language Arts, Breakout','Students will level up their ELA analysis skills by working their way through a series of challenging tasks in order to solve a mystery. Each step of the ELA breakout, which is similar to an escape room, will have students reading and analyzing texts, thinking critically, and collaborating in order to collect the clues they need to complete the challenge. In this event, students will be engaged in building their language arts skills through high interest activities that are sure to keep them intrigued and having fun. In addition to the language arts focus, campers can also look forward to crafts, games, team challenges, projects, and experiments.\n\nLanguage Arts Focus: \nNonfiction Text w/context clues and EOG style questions\nNonfiction Text w/tone\nShort Story w/characterization and figurative language \nAdditional ELA skills - complex brain teasers and Greek/Latin prefixes, roots, and suffixes\n\n(partial week enrollment options available upon request)'),(4,'Language Arts EOG Prep (Half Day Camp)',4,8,'Language Arts, EOG','Students will prepare for the language arts EOG through engaging activities that practice the skills needed to be successful.  \n\nLanguage Arts Focus: \nComprehension Strategies \nAnalysis Skills\nTest Taking Strategies \nTone\nContext Clues \nFigurative Language\n'),(5,'Think Like A Lawyer Debate (Full Week)',3,7,'Debate','Students will develop their critical thinking skills by conducting research, creating an argument, and selecting evidence to support their thinking. Students will participate in a mock court hearing where they will put their debate skills to the test. \n\nLanguage Arts Focus: \nResearch\nDeveloping an argument\nIdentifying evidence to support a claim\nSpeaking skills\n\n(partial week enrollment options available upon request)'),(6,'Creative Writing (Single Day)',3,7,'Creative writing, single day','Students will grow as creative writers through mini lessons focusing on writing skills such as characterization and descriptive language. In addition to the language arts focus, campers can also look forward to crafts, games, team challenges, projects, and experiments.\n\nLanguage Arts Focus: \nCharacter Development\nCharacterization\nDescriptive Language \nDialogue Development\nElements of Plot \nFigurative Language\n'),(7,'Language Arts Breakout (Single Day)',3,7,'breakout, single day','Students will level up their ELA analysis skills by working their way through a series of challenging tasks in order to solve a mystery. Each step of the ELA breakout, which is similar to an escape room, will have students reading and analyzing texts, thinking critically, and collaborating in order to collect the clues they need to complete the challenge. In this event, students will be engaged in building their language arts skills through high interest activities that are sure to keep them intrigued and having fun. In addition to the language arts focus, campers can also look forward to crafts, games, team challenges, projects, and experiments.\n\nLanguage Arts Focus: \nNonfiction Text w/context clues and EOG style questions\nNonfiction Text w/tone\nShort Story w/characterization and figurative language \nAdditional ELA skills - complex brain teasers and Greek/Latin prefixes, roots, and suffixes\n'),(8,'Back to School ELA Refresh (Full Week)',3,7,'back to school','Students will be engaged in a variety of fun activities to refresh key ELA skills like reading and analyzing texts, working with vocabulary and context clues, and writing short responses. These high interest activities will help students get back into the school mindset to start the year off right! In addition to the language arts focus, campers can also look forward to crafts, games, team challenges, projects, and experiments that will have them thinking critically and collaborating with peers.\n\nLanguage Arts Focus: \nReading and analyzing texts \nVocabulary and Context Clues\nWriting short responses\n\n(partial week enrollment options available upon request)'),(9,'Test program',6,8,'',''),(10,'Test program',6,8,'','');
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `list_index` int NOT NULL,
  `title` text NOT NULL,
  `url` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `resource_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `resource_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource`
--

LOCK TABLES `resource` WRITE;
/*!40000 ALTER TABLE `resource` DISABLE KEYS */;
INSERT INTO `resource` VALUES (1,1,1,'Click here to access the 3rd & 4th Grade Nonfiction EOG Practice','https://docs.google.com/document/d/1EWPlNTlDo8NcFPrYXmEy0uB5mBU9YjYh3UHVPVoWxm4/edit'),(2,2,1,'Click here to access the 5th & 6th Grade Nonfiction EOG Practice','https://docs.google.com/document/d/1w253jYZp3kF4NSGT9pWyWRTFYP8XGu9xHSPC-vox9Ao/edit?usp=drive_link');
/*!40000 ALTER TABLE `resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource_group`
--

DROP TABLE IF EXISTS `resource_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_group`
--

LOCK TABLES `resource_group` WRITE;
/*!40000 ALTER TABLE `resource_group` DISABLE KEYS */;
INSERT INTO `resource_group` VALUES (1,'3rd & 4th Grade'),(2,'5th & 6th Grade');
/*!40000 ALTER TABLE `resource_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES ('ADMIN'),('GUARDIAN'),('INSTRUCTOR');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `birthdate` date DEFAULT NULL,
  `grade_level` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'Karen','2023-03-09',6),(3,'Renee',NULL,8),(4,'Megan Miller',NULL,6),(7,'Serena Adhikari',NULL,4),(8,'Janelle Abebe',NULL,4),(9,'Harper Ostroth',NULL,5),(10,'Ethan Ostroth',NULL,8),(11,'Janelle Abebe',NULL,4),(12,'Test',NULL,6),(13,'Jacob Templin',NULL,4),(14,'Eli Nguyen',NULL,2),(15,'Bhavya Dhiran',NULL,5),(16,'Jayden Adams',NULL,4),(17,'Bhavya Dhiran',NULL,5),(18,'Andrew Jiang',NULL,5),(19,'Ethan Peng',NULL,5),(20,'Evan Ramsbottom',NULL,4),(21,'Diya Karlekar',NULL,5),(22,'Tanvi Karlekar',NULL,3),(23,'Andy Guo',NULL,3),(24,'Rishi Nair',NULL,5),(25,'Ezra Rodriguez',NULL,6),(26,'Jackson Austin',NULL,3),(27,'Olivia Kyte',NULL,6),(28,'Vivian Kyte',NULL,4),(29,'Maggie Norcross',NULL,3),(30,'Carter Ivy',NULL,6),(31,'Liana Benn',NULL,5),(32,'Alex Peters',NULL,2),(33,'Abigail Maraschiello ',NULL,2),(34,'Haeun Choe',NULL,2),(35,'Abbey Chen',NULL,3),(36,'Alexandra Frohock',NULL,3),(37,'Bentley Kilcollins ',NULL,4);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `google_id` text NOT NULL,
  `full_name` text NOT NULL,
  `email_address` text NOT NULL,
  `phone_number` text,
  `instructor_subjects` text,
  `instructor_description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_x_programs`
--

DROP TABLE IF EXISTS `user_x_programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_x_programs` (
  `user_id` int NOT NULL,
  `program_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`program_id`),
  KEY `program_id` (`program_id`),
  CONSTRAINT `user_x_programs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_x_programs_ibfk_2` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_x_programs`
--

LOCK TABLES `user_x_programs` WRITE;
/*!40000 ALTER TABLE `user_x_programs` DISABLE KEYS */;
INSERT INTO `user_x_programs` VALUES (1,2),(2,3),(2,4),(5,5),(2,6),(2,7),(5,8),(1,9),(1,10);
/*!40000 ALTER TABLE `user_x_programs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_x_roles`
--

DROP TABLE IF EXISTS `user_x_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_x_roles` (
  `user_id` int NOT NULL,
  `role` varchar(32) NOT NULL,
  PRIMARY KEY (`user_id`,`role`),
  KEY `role` (`role`),
  CONSTRAINT `user_x_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_x_roles_ibfk_2` FOREIGN KEY (`role`) REFERENCES `role` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_x_roles`
--

LOCK TABLES `user_x_roles` WRITE;
/*!40000 ALTER TABLE `user_x_roles` DISABLE KEYS */;
INSERT INTO `user_x_roles` VALUES (1,'ADMIN'),(2,'ADMIN'),(5,'ADMIN'),(6,'ADMIN'),(1,'GUARDIAN'),(2,'GUARDIAN'),(3,'GUARDIAN'),(4,'GUARDIAN'),(5,'GUARDIAN'),(6,'GUARDIAN'),(7,'GUARDIAN'),(8,'GUARDIAN'),(9,'GUARDIAN'),(10,'GUARDIAN'),(11,'GUARDIAN'),(12,'GUARDIAN'),(13,'GUARDIAN'),(14,'GUARDIAN'),(15,'GUARDIAN'),(16,'GUARDIAN'),(17,'GUARDIAN'),(18,'GUARDIAN'),(19,'GUARDIAN'),(20,'GUARDIAN'),(21,'GUARDIAN'),(22,'GUARDIAN'),(23,'GUARDIAN'),(24,'GUARDIAN'),(25,'GUARDIAN'),(26,'GUARDIAN'),(27,'GUARDIAN'),(28,'GUARDIAN'),(29,'GUARDIAN'),(30,'GUARDIAN'),(31,'GUARDIAN'),(32,'GUARDIAN'),(33,'GUARDIAN'),(34,'GUARDIAN'),(35,'GUARDIAN'),(1,'INSTRUCTOR'),(2,'INSTRUCTOR'),(5,'INSTRUCTOR'),(6,'INSTRUCTOR');
/*!40000 ALTER TABLE `user_x_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_x_students`
--

DROP TABLE IF EXISTS `user_x_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_x_students` (
  `user_id` int NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`student_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `user_x_students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_x_students_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_x_students`
--

LOCK TABLES `user_x_students` WRITE;
/*!40000 ALTER TABLE `user_x_students` DISABLE KEYS */;
INSERT INTO `user_x_students` VALUES (1,1),(1,3),(7,4),(10,7),(9,8),(11,9),(11,10),(9,11),(5,12),(12,13),(13,14),(14,15),(15,16),(14,17),(16,18),(17,19),(18,20),(19,21),(19,22),(20,23),(21,24),(22,25),(23,26),(24,27),(24,28),(25,29),(26,30),(28,31),(29,32),(30,33),(31,34),(32,35),(34,36),(35,37);
/*!40000 ALTER TABLE `user_x_students` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-17 12:32:50
