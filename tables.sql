-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: leverage_philly
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `candidacy`
--

DROP TABLE IF EXISTS `candidacy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidacy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `candidate_id` int(11) NOT NULL,
  `race_id` int(11) NOT NULL,
  `party_id` tinyint(4) NOT NULL,
  `candidacy_order` int(11) NOT NULL,
  `slug` varchar(64) NOT NULL,
  `candidacy_type` enum('incumbent','challenger') NOT NULL DEFAULT 'challenger',
  `outcome` enum('won','lost','upcoming') NOT NULL DEFAULT 'upcoming',
  PRIMARY KEY (`id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `race_id` (`race_id`),
  KEY `candidacy_type` (`candidacy_type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `candidate`
--

DROP TABLE IF EXISTS `candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `party_id` int(1) unsigned NOT NULL,
  `fec_id` char(9) DEFAULT NULL,
  `district` tinyint(3) unsigned NOT NULL,
  `name_first` varchar(128) NOT NULL,
  `name_middle` varchar(32) NOT NULL DEFAULT '',
  `name_last` varchar(32) NOT NULL,
  `name_suffix` varchar(8) NOT NULL DEFAULT '',
  `slug` varchar(64) NOT NULL,
  `website` varchar(128) NOT NULL DEFAULT '',
  `social_blob` text NOT NULL,
  `is_active` int(1) NOT NULL DEFAULT '1',
  `candidate_order` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fec_id` (`fec_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `candidate_committees`
--

DROP TABLE IF EXISTS `candidate_committees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate_committees` (
  `candidate_id` int(11) NOT NULL,
  `committee_id` int(11) NOT NULL,
  PRIMARY KEY (`candidate_id`,`committee_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `committee`
--

DROP TABLE IF EXISTS `committee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `committee` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `candidate_id` int(4) unsigned NOT NULL DEFAULT '0',
  `is_candidates` int(10) unsigned NOT NULL DEFAULT '0',
  `committee_name` varchar(128) NOT NULL,
  `committee_slug` varchar(128) DEFAULT NULL,
  `committee_description` text,
  `donations_2015` decimal(10,2) DEFAULT '0.00',
  `donations_2016` decimal(10,2) DEFAULT '0.00',
  `donations_2017` decimal(10,2) DEFAULT '0.00',
  `donations_in_philly` decimal(10,2) DEFAULT '0.00',
  `donations_in_pa` decimal(10,2) DEFAULT '0.00',
  `donations_out_pa` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `committee_name` (`committee_name`),
  KEY `committee_slug` (`committee_slug`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contributor`
--

DROP TABLE IF EXISTS `contributor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contributor` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `address_id` int(4) NOT NULL DEFAULT '0',
  `name_prefix` varchar(64) NOT NULL DEFAULT '',
  `name_first` varchar(64) NOT NULL DEFAULT '',
  `name_middle` varchar(64) NOT NULL DEFAULT '',
  `name_last` varchar(64) NOT NULL DEFAULT '',
  `name_suffix` varchar(64) NOT NULL DEFAULT '',
  `name_business` varchar(255) NOT NULL DEFAULT '',
  `slug` varchar(128) DEFAULT NULL,
  `is_person` smallint(1) NOT NULL DEFAULT '0',
  `is_business` smallint(1) NOT NULL DEFAULT '0',
  `num_contributions` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `num_committees_contrib_to` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `total_contributed_2015` decimal(12,2) DEFAULT NULL,
  `total_contributed_2016` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name_first` (`name_first`),
  KEY `name_last` (`name_last`),
  KEY `name_prefix` (`name_prefix`),
  KEY `name_suffix` (`name_suffix`),
  KEY `address_id` (`address_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contributor_address`
--

DROP TABLE IF EXISTS `contributor_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contributor_address` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `address_type` varchar(64) NOT NULL DEFAULT '',
  `number` varchar(16) NOT NULL DEFAULT '',
  `street` varchar(64) NOT NULL DEFAULT '',
  `addr1` varchar(128) NOT NULL DEFAULT '',
  `addr2` varchar(128) NOT NULL DEFAULT '',
  `po_box` varchar(16) NOT NULL DEFAULT '',
  `city` varchar(64) NOT NULL DEFAULT '',
  `state` varchar(32) NOT NULL DEFAULT '',
  `zipcode` varchar(16) NOT NULL DEFAULT '',
  `slug` varchar(64) DEFAULT NULL,
  `num_individual_contribs` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `num_non_individual_contribs` mediumint(8) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `city` (`city`,`state`),
  KEY `zipcode` (`zipcode`),
  KEY `addr1` (`addr1`),
  KEY `address_type` (`address_type`),
  KEY `number` (`number`),
  KEY `street` (`street`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contributor_type`
--

DROP TABLE IF EXISTS `contributor_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contributor_type` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `type_name` varchar(64) NOT NULL,
  `type_slug` varchar(32) NOT NULL DEFAULT '',
  `type_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`),
  KEY `type_slug` (`type_slug`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `party`
--

DROP TABLE IF EXISTS `party`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `party` (
  `id` tinyint(1) unsigned NOT NULL AUTO_INCREMENT,
  `party_name` varchar(32) NOT NULL,
  `slug` varchar(32) NOT NULL,
  `party_order` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation`
--

DROP TABLE IF EXISTS `political_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `is_annonymous` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `contributor_id` int(4) unsigned NOT NULL,
  `contributor_type_id` int(4) unsigned NOT NULL,
  `contribution_type_id` int(4) unsigned NOT NULL,
  `committee_id` int(4) unsigned NOT NULL,
  `filing_period_id` int(4) unsigned NOT NULL,
  `employer_name_id` int(4) unsigned NOT NULL,
  `employer_occupation_id` int(4) unsigned NOT NULL,
  `donation_date` date NOT NULL,
  `donation_amount` decimal(10,2) NOT NULL,
  `provided_name` varchar(128) NOT NULL,
  `provided_address` varchar(128) NOT NULL,
  `is_fixed_asset` smallint(1) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contributor_id` (`contributor_id`),
  KEY `contributor_type_id` (`contributor_type_id`),
  KEY `contribution_type_id` (`contribution_type_id`),
  KEY `committee_id` (`committee_id`),
  KEY `filing_period_id` (`filing_period_id`),
  KEY `donation_date` (`donation_date`),
  KEY `donation_amount` (`donation_amount`),
  KEY `employer_name_id` (`employer_name_id`,`employer_occupation_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_contribution_type`
--

DROP TABLE IF EXISTS `political_donation_contribution_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_contribution_type` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `is_donation` tinyint(4) NOT NULL DEFAULT '0',
  `type_name` varchar(128) NOT NULL,
  `type_name_short` varchar(32) NOT NULL DEFAULT '',
  `type_slug` varchar(32) NOT NULL DEFAULT '',
  `type_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`),
  KEY `type_slug` (`type_slug`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_employer_name`
--

DROP TABLE IF EXISTS `political_donation_employer_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_employer_name` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `employer_name` varchar(128) NOT NULL,
  `employer_slug` varchar(32) NOT NULL DEFAULT '',
  `employer_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employer_name` (`employer_name`),
  KEY `employer_slug` (`employer_slug`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_employer_occupation`
--

DROP TABLE IF EXISTS `political_donation_employer_occupation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_employer_occupation` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `occupation_name` varchar(64) NOT NULL,
  `occupation_slug` varchar(32) NOT NULL DEFAULT '',
  `occupation_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `occupation_name` (`occupation_name`),
  KEY `occupation_slug` (`occupation_slug`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_filing_period`
--

DROP TABLE IF EXISTS `political_donation_filing_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_filing_period` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `period_name` varchar(64) NOT NULL,
  `period_slug` varchar(32) NOT NULL DEFAULT '',
  `period_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `period_name` (`period_name`),
  KEY `period_slug` (`period_slug`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `race`
--

DROP TABLE IF EXISTS `race`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `race` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `election_type` enum('primary','general') NOT NULL,
  `election_year` year(4) NOT NULL,
  `election_date` int(11) NOT NULL,
  `seat_status` enum('filled','open seat','retired') NOT NULL,
  `race_order` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `race_name` varchar(64) NOT NULL,
  `race_district` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `race_description` text,
  `num_candidates` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `parties_short_text` varchar(16) NOT NULL DEFAULT '',
  `slug` varchar(48) NOT NULL,
  `is_statewide` int(11) NOT NULL DEFAULT '0',
  `area` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `race_order` (`race_order`),
  KEY `race_name` (`race_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-08 10:24:04
