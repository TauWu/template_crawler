CREATE DATABASE IF NOT EXISTS `crawler_data`;

USE `crawler_data`;

-- Create table for saving Lianjia house base info.
DROP TABLE IF EXISTS `house_base_infolj`;
CREATE TABLE `house_base_infolj` (
  `house_info_id`     int(11) NOT NULL AUTO_INCREMENT COMMENT '自增 ID',
  `house_id`          varchar(60) NOT NULL DEFAULT '' COMMENT '源系统房屋 ID',
  `house_title`       varchar(100) NOT NULL DEFAULT '' COMMENT '房源标题',
  `community_id`      varchar(60) NOT NULL DEFAULT '' COMMENT '地标id',
  `house_type`        varchar(20) NOT NULL DEFAULT '' COMMENT '房型',
  `house_type_new`    varchar(20) NOT NULL DEFAULT '' COMMENT '房型（详情页面）',
  `house_area`        varchar(20) NOT NULL DEFAULT '' COMMENT '面积大小',
  `orientation`       varchar(20) NOT NULL DEFAULT '' COMMENT '朝向',
  `house_floor`       varchar(20) NOT NULL DEFAULT '' COMMENT '房间楼层',
  `house_total_floor` varchar(20) NOT NULL DEFAULT '' COMMENT '总楼层',
  `house_create_year` varchar(20) NOT NULL DEFAULT '' COMMENT '建房时间',
  `see_count`         int(11) NOT NULL DEFAULT 0 COMMENT '带看人数',
  `house_price`       int(11) NOT NULL DEFAULT 0 COMMENT '房间价格',
  `sale_date`         varchar(20) NOT NULL DEFAULT '' COMMENT '上架时间',
  `sale_date_new`     varchar(20) NOT NULL DEFAULT '' COMMENT '上架时间（详情页面）',
  `extra_info_select` longtext COMMENT '房间标签',
  `basic_info`        varchar(100) NOT NULL DEFAULT '' COMMENT '基本属性',
  `house_tags`        varchar(100) NOT NULL DEFAULT '' COMMENT '房源标签',
  `house_feature`     longtext COMMENT '房源特色',
  `see_stat_total`    int(11) NOT NULL DEFAULT 0 COMMENT '带看总数',
  `see_stat_weekly`   int(11) NOT NULL DEFAULT 0 COMMENT '周带看总数',
  `community_sold_count` int(11) NOT NULL DEFAULT 0 COMMENT '同小区成交数',
  `busi_sold_count`   int(11) NOT NULL DEFAULT 0 COMMENT '同商圈成交数',

  `enabled`     int(1) NOT NULL DEFAULT 1 COMMENT '是否删除',
  `create_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '创建人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '修改人',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',

  PRIMARY KEY (`house_info_id`),
  INDEX (`community_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='HOUSE_BASE_INFOLJ';

-- Create table for saving Qingke house base info.
DROP TABLE IF EXISTS `house_base_infoqk`;
CREATE TABLE `house_base_infoqk` (
  `house_info_id`   int(11) NOT NULL AUTO_INCREMENT COMMENT '自增 ID',
  `house_id`        varchar(60) NOT NULL DEFAULT '' COMMENT '源房屋 ID',
  `community_id`    varchar(60) NOT NULL DEFAULT '' COMMENT '源地标 ID',
  `orientation`     varchar(100) NOT NULL DEFAULT '' COMMENT '房间朝向',
  `floor`           varchar(20) NOT NULL DEFAULT '' COMMENT '楼层',
  `area`            varchar(20) NOT NULL DEFAULT '' COMMENT '面积',
  `origin_price`    decimal(18,2) NOT NULL DEFAULT 0.0 COMMENT '原始价格',
  `price`           decimal(18,2) NOT NULL DEFAULT 0.0 COMMENT '价格',

  `enabled`     int(1) NOT NULL DEFAULT 1 COMMENT '是否删除',
  `create_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '创建人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '修改人',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
  
  PRIMARY KEY (`house_info_id`),
  INDEX (`community_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='HOUSE_BASE_INFOQK';

-- Create table for saving Ziroom house base info.
DROP TABLE IF EXISTS `house_base_infozr`;
CREATE TABLE `house_base_infozr` (
  `house_info_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增 ID',
  `house_id`      varchar(60) NOT NULL DEFAULT '' COMMENT '源房屋ID',
  `house_code`    varchar(30) NOT NULL DEFAULT '' COMMENT '房间编号',
  `price`         decimal(18,2) NOT NULL DEFAULT 0.0 COMMENT '价格',
  `floor`         varchar(20) NOT NULL DEFAULT '' COMMENT '楼层',
  `house_type`    varchar(20) NOT NULL DEFAULT '' COMMENT '户型',
  `community_id`  varchar(60) NOT NULL DEFAULT '' COMMENT '小区ID',
  `status`        varchar(20) NOT NULL DEFAULT '' COMMENT '房间状态',


  `enabled`     int(1) NOT NULL DEFAULT 1 COMMENT '是否删除',
  `create_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '创建人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '修改人',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
  
  PRIMARY KEY (`house_info_id`),
  INDEX (`community_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='HOUSE_BASE_INFOZR';

-- Create table for saving community base info.
DROP TABLE IF EXISTS `community_info`;
CREATE TABLE `community_info` (
  `community_info_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增 ID',
  `source_from`       int(11) NOT NULL DEFAULT 0 COMMENT '信息来源 0-unknown 1-Lianjia 2-Ziroom 3-QK',
  `source_name`       varchar(20) NOT NULL DEFAULT '' COMMENT '信息来源名称',
  `community_id`      varchar(60) NOT NULL DEFAULT '' COMMENT '源系统地标 ID',
  `community_name`    varchar(100) NOT NULL DEFAULT '' COMMENT '小区名称',
  `lat`               varchar(20) NOT NULL DEFAULT '' COMMENT '纬度',
  `lng`               varchar(20) NOT NULL DEFAULT '' COMMENT '经度',

  -- Crawler Info.
  `cw_district` varchar(100) NOT NULL DEFAULT '' COMMENT 'Crawler 区县',
  `cw_busi`     varchar(100) NOT NULL DEFAULT '' COMMENT 'Crawler 商圈',
  `cw_detail`   varchar(100) NOT NULL DEFAULT '' COMMENT 'Crawler 详细地址',

  -- Formatted Info from BaiduMap.
  `bd_province` varchar(100) NOT NULL DEFAULT '' COMMENT '百度地图 省份',
  `bd_city`     varchar(100) NOT NULL DEFAULT '' COMMENT '百度地图 地级市',
  `bd_district` varchar(100) NOT NULL DEFAULT '' COMMENT '百度地图 区县',
  `bd_busi`     varchar(100) NOT NULL DEFAULT '' COMMENT '百度地图 商圈',
  `bd_street`   varchar(100) NOT NULL DEFAULT '' COMMENT '百度地图 街道',
  `bd_detail`   varchar(100) NOT NULL DEFAULT '' COMMENT '百度地图 详细地址',
  `bd_adcode`   varchar(15) NOT NULL DEFAULT '' COMMENT '百度地图 行政区域编码',

  `enabled`     int(1) NOT NULL DEFAULT 1 COMMENT '是否删除',
  `create_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '创建人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '修改人',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',

  PRIMARY KEY (`community_info_id`, `source_from`),
  INDEX (`community_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='COMMUNITY_INFO';

-- Create table for saving Ziroom price info with different payments.
DROP TABLE IF EXISTS `house_price_infozr`;
CREATE TABLE `house_price_infozr` (
  `price_info_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '房屋付款方式ID',
  `house_id`      varchar(60) NOT NULL DEFAULT '' COMMENT '源房屋ID',
  `period`        varchar(20) NOT NULL DEFAULT '' COMMENT '付款方式',
  `rent`      decimal(18,2) NOT NULL DEFAULT 0.0 COMMENT '房屋租金',
  `deposit`   decimal(18,2) NOT NULL DEFAULT 0.0 COMMENT '押金',
  `service_charge`   decimal(18,2) NOT NULL DEFAULT 0.0 COMMENT '服务收费',

  `enabled`     int(1) NOT NULL DEFAULT 1 COMMENT '是否删除',
  `create_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '创建人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '修改人',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',

  PRIMARY KEY (`price_info_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='HOUSE_PRICE_INFOZR';

-- Create table for saving Ziroom house recomm info.
DROP TABLE IF EXISTS `house_recomm_infozr`;
CREATE TABLE `house_recomm_infozr` (
  `house_recomm_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增 ID',
  `house_id`        varchar(60) NOT NULL DEFAULT '' COMMENT '源房屋ID',
  `url`             varchar(255) NOT NULL DEFAULT '' COMMENT 'URL相对路径',
  `index_no`        varchar(20) NOT NULL DEFAULT '' COMMENT '索引编号',
  `price`           decimal(18,2) NOT NULL DEFAULT 0.0 COMMENT '价格',
  `price_unit`      varchar(20) NOT NULL DEFAULT '' COMMENT '价格单位',
  `info`            varchar(100) NOT NULL DEFAULT '' COMMENT '房屋描述',
  `photo`           varchar(255) NOT NULL DEFAULT '' COMMENT '房屋图片',

  `enabled`     int(1) NOT NULL DEFAULT 1 COMMENT '是否删除',
  `create_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '创建人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_by`   varchar(100) NOT NULL DEFAULT '' COMMENT '修改人',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',

  PRIMARY KEY (`house_recomm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='HOUSE_RECOMM_INFOZR';

-- Create table for saving log info.
DROP TABLE IF EXISTS `crawler_log`;
CREATE TABLE `crawler_log` (
  `log_id`      int(11) NOT NULL AUTO_INCREMENT COMMENT '自增 ID',
  `time`        varchar(20) NOT NULL DEFAULT '' COMMENT '时间',
  `pid`         varchar(20) NOT NULL DEFAULT '' COMMENT '进程 ID',
  `level`       varchar(4) NOT NULL DEFAULT '' COMMENT '日志等级',
  `log_type`    varchar(20) NOT NULL DEFAULT '' COMMENT '日志类型',
  `project`     varchar(60) NOT NULL DEFAULT '' COMMENT '项目名称',
  `content`     varchar(100) NOT NULL DEFAULT '' COMMENT '日志内容',
  
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='CRAWLER_LOG';

-- Table info view.
DROP VIEW IF EXISTS `v_table_info`;
CREATE VIEW `v_table_info` AS 
SELECT 
  `TABLE_SCHEMA`, `TABLE_NAME`, `COLUMN_NAME`, `COLUMN_COMMENT`,
  `ORDINAL_POSITION`, `IS_NULLABLE`, `DATA_TYPE`, `COLUMN_TYPE`,
  `COLUMN_KEY`
FROM 
  `information_schema`.`columns` 
WHERE 
  (`TABLE_SCHEMA` = 'crawler_data');

-- Lianjia House Info view.
DROP VIEW IF EXISTS `v_lianjia_house_info`;
CREATE VIEW `v_lianjia_house_info` AS
SELECT 
  `lj`.`house_id`, `lj`.`house_title`, `lj`.`community_id`, 
  `lj`.`house_type`, `lj`.`house_type_new`, `lj`.`house_area`,
  `lj`.`orientation`, `lj`.`house_floor`, `lj`.`house_total_floor`,
  `lj`.`house_create_year`, `lj`.`see_count`, `lj`.`house_price`,
  `lj`.`sale_date`, `lj`.`sale_date_new`, `lj`.`extra_info_select`,
  `lj`.`basic_info`,`lj`.`house_tags`, `lj`.`house_feature`,
  `lj`.`see_stat_total`,`lj`.`see_stat_weekly`, 
  `lj`.`community_sold_count`, `lj`.`busi_sold_count`, 
  `lj`.`enabled`, `lj`.`create_time`, `lj`.`modify_time`,
  `c`.`community_name`, `c`.`lat`,`c`.`lng`,
  `c`.`cw_district`,`c`.`cw_busi`,`c`.`cw_detail`, `c`.`bd_province`,
  `c`.`bd_city`,`c`.`bd_district`,`c`.`bd_busi`,`c`.`bd_street`,
  `c`.`bd_detail`,`c`.`bd_adcode`
FROM `house_base_infolj` AS `lj`
INNER JOIN `community_info` AS `c` 
  ON `c`.`source_from` = 1 AND `c`.`community_id` = `lj`.`community_id`
  AND `c`.`enabled` = 1;

-- Ziroom House Info view.
DROP VIEW IF EXISTS `v_ziroom_house_info`;
CREATE VIEW `v_ziroom_house_info` AS
SELECT 
  `zr`.`house_id`, `zr`.`price`,`zr`.`floor`, `zr`.`house_type`, 
  `zr`.`community_id`,`zr`.`enabled`, `zr`.`create_time`, 
  `zr`.`modify_time`, `c`.`community_name`,
  `c`.`lat`,`c`.`lng`, `c`.`cw_district`,`c`.`cw_busi`,
  `c`.`cw_detail`, `c`.`bd_province`,`c`.`bd_city`,`c`.`bd_district`,
  `c`.`bd_busi`,`c`.`bd_street`,`c`.`bd_detail`,`c`.`bd_adcode`
FROM `house_base_infozr` AS `zr`
INNER JOIN `community_info` AS `c`
  ON `c`.`source_from` = 2 AND `c`.`community_id` = `zr`.`community_id`
  AND `c`.`enabled` = 1;

-- Ziroom House Payment Info view.
DROP VIEW IF EXISTS `v_ziroom_payment_info`;
CREATE VIEW `v_ziroom_payment_info` AS
SELECT 
  `p_zr`.`period`, `p_zr`.`rent`, `p_zr`.`deposit`, 
  `p_zr`.`service_charge`,
  `v_zr`.*
FROM `house_price_infozr` AS `p_zr`
INNER JOIN `v_ziroom_house_info` AS `v_zr`
  ON `v_zr`.`house_id` = `p_zr`.`house_id`;


-- Ziroom House Recomm Info view.
DROP VIEW IF EXISTS `v_ziroom_recomm_info`;
CREATE VIEW `v_ziroom_recomm_info` AS
SELECT 
  `r_zr`.`url`,`r_zr`.`index_no`,`r_zr`.`price` as `recomm_price`,
  `r_zr`.`price_unit`,`r_zr`.`info`,`r_zr`.`photo`,
  `v_zr`.*
FROM `house_recomm_infozr` AS `r_zr`
INNER JOIN `v_ziroom_house_info` AS `v_zr`
  ON `v_zr`.`house_id` = `r_zr`.`house_id`;

-- QK House Info view.
DROP VIEW IF EXISTS `v_qk_house_info`;
CREATE VIEW `v_qk_house_info` AS
SELECT 
  `qk`.`house_info_id`,`qk`.`house_id`,`qk`.`community_id`,`qk`.`orientation`,
  `qk`.`floor`,`qk`.`area`,`qk`.`origin_price`,`qk`.`price`,`qk`.`enabled`,
  `qk`.`create_time`, `qk`.`modify_time`,
  `c`.`community_name`, `c`.`lat`,`c`.`lng`,
  `c`.`cw_district`,`c`.`cw_busi`,`c`.`cw_detail`, `c`.`bd_province`,
  `c`.`bd_city`,`c`.`bd_district`,`c`.`bd_busi`,`c`.`bd_street`,
  `c`.`bd_detail`,`c`.`bd_adcode`
FROM `house_base_infoqk` AS `qk`
INNER JOIN `community_info` AS `c` 
  ON `c`.`source_from` = 3 AND `c`.`community_id` = `qk`.`community_id`
  AND `c`.`enabled` = 1;