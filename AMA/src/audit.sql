/*
MySQL Data

 Target Server Type    : MySQL
 Target Server Version : 50624
 File Encoding         : utf-8

*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `audit_log`
-- ----------------------------
DROP TABLE IF EXISTS `audit_log`;
CREATE TABLE `audit_log` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user` varchar(30) NOT NULL,
  `ip` varchar(30) NOT NULL,
  `host_user` varchar(30) NOT NULL,
  `cmd` varchar(30) NOT NULL,
  /*`date` datetime(6) NOT NULL ON UPDATE CURRENT_TIMESTAMP(6),*/
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `bind_hosts`
-- ----------------------------
DROP TABLE IF EXISTS `bind_hosts`;
CREATE TABLE `bind_hosts` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `host_id` int(10) NOT NULL,
  `host_user_id` int(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `host_id` (`host_id`),
  KEY `host_user_id` (`host_user_id`),
  CONSTRAINT `bind_hosts_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `bind_hosts_ibfk_2` FOREIGN KEY (`host_user_id`) REFERENCES `host_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `groups`
-- ----------------------------
DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `name` varchar(30) NOT NULL,
  `id` int(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `host_groups`
-- ----------------------------
DROP TABLE IF EXISTS `host_groups`;
CREATE TABLE `host_groups` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) NOT NULL,
  `bind_host_id` int(10) NOT NULL,
  `group_id` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `host_users`
-- ----------------------------
DROP TABLE IF EXISTS `host_users`;
CREATE TABLE `host_users` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `id` int(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `hosts`
-- ----------------------------
DROP TABLE IF EXISTS `hosts`;
CREATE TABLE `hosts` (
  `hostname` varchar(30) NOT NULL,
  `ip` varchar(30) NOT NULL,
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `port` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `username` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
