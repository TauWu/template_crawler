CREATE DATABASE `crawler_data`;

USE `crawler_data`;

CREATE TABLE `house_base_infolj` (
  `house_info_id` varchar(60) NOT NULL COMMENT '房源编号',
  `house_id` varchar(60) DEFAULT NULL COMMENT '源系统房屋id',
  `house_title` varchar(100) DEFAULT NULL COMMENT '房源标题',
  `insert_date` varchar(20) DEFAULT NULL COMMENT '入库日期',
  `district` varchar(100) DEFAULT NULL COMMENT '行政区',
  `community_id` varchar(60) DEFAULT NULL COMMENT '地标id',
  `community_name` varchar(100) DEFAULT NULL COMMENT '地标名称',
  `house_type` varchar(20) DEFAULT NULL COMMENT '房型',
  `house_type_new` varchar(20) DEFAULT NULL COMMENT '房型（详情页面）',
  `house_area` varchar(20) DEFAULT NULL COMMENT '面积大小',
  `orientation` varchar(20) DEFAULT NULL COMMENT '朝向',
  `distinct_name` varchar(100) DEFAULT NULL COMMENT '行政区名称',
  `house_floor` varchar(20) DEFAULT NULL COMMENT '房间楼层',
  `house_total_floor` varchar(20) DEFAULT NULL COMMENT '总楼层',
  `house_create_year` varchar(20) DEFAULT NULL COMMENT '建房时间',
  `see_count` int(11) DEFAULT NULL COMMENT '带看人数',
  `house_price` int(11) DEFAULT NULL COMMENT '房间价格',
  `sale_date` varchar(20) DEFAULT NULL COMMENT '上架时间',
  `sale_date_new` varchar(20) DEFAULT NULL COMMENT '上架时间（详情页面）',
  `extra_info_select` longtext COMMENT '房间标签',
  `basic_info` varchar(100) DEFAULT NULL COMMENT '基本属性',
  `house_tags` varchar(100) DEFAULT NULL COMMENT '房源标签',
  `house_feature` longtext COMMENT '房源特色',
  `position` varchar(100) DEFAULT NULL COMMENT '房源坐标',
  `see_stat_total` int(11) DEFAULT NULL COMMENT '带看总数',
  `see_stat_weekly` int(11) DEFAULT NULL COMMENT '周带看总数',
  `community_sold_count` int(11) DEFAULT NULL COMMENT '同小区成交数',
  `busi_sold_count` int(11) DEFAULT NULL COMMENT '同商圈成交数',
  `enabled` varchar(1) DEFAULT NULL COMMENT '是否删除',
  `create_by` varchar(100) DEFAULT NULL COMMENT '创建人',
  `create_time` varchar(20) DEFAULT NULL COMMENT '创建时间',
  `modify_by` varchar(100) DEFAULT NULL COMMENT '修改人',
  `modify_time` varchar(20) DEFAULT NULL COMMENT '修改时间',
  `ll_get_province` varchar(100) DEFAULT NULL COMMENT '经纬解析省',
  `ll_get_city` varchar(100) DEFAULT NULL COMMENT '经纬解析市',
  `ll_get_strict` varchar(100) DEFAULT NULL COMMENT '经纬解析区',
  `ll_get_busarea` varchar(100) DEFAULT NULL COMMENT '经纬解析商圈',
  `ll_get_quarter` varchar(100) DEFAULT NULL COMMENT '经纬解析小区',
  `ll_get_detail` varchar(100) DEFAULT NULL COMMENT '经纬解析详细地址',
  PRIMARY KEY (`house_info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='HOUSE_BASE_INFOLJ';

CREATE TABLE `house_base_infoqk` (
  `house_info_id` varchar(60) NOT NULL COMMENT '房屋ID',
  `orientation` varchar(100) DEFAULT NULL COMMENT '房间朝向',
  `comm_name` varchar(100) DEFAULT NULL COMMENT '小区名称',
  `price` decimal(18,2) DEFAULT NULL COMMENT '价格',
  `lat` varchar(20) DEFAULT NULL COMMENT '纬度',
  `floor` varchar(20) DEFAULT NULL COMMENT '楼层',
  `busi` varchar(100) DEFAULT NULL COMMENT '商圈名称',
  `origin_price` decimal(18,2) DEFAULT NULL COMMENT '原始价格',
  `house_id` varchar(60) DEFAULT NULL COMMENT '源房屋ID',
  `area` decimal(18,2) DEFAULT NULL COMMENT '面积',
  `lng` varchar(20) DEFAULT NULL COMMENT '经度',
  `ll_get_province` varchar(100) DEFAULT NULL COMMENT '经纬解析省',
  `ll_get_city` varchar(100) DEFAULT NULL COMMENT '经纬解析市',
  `ll_get_strict` varchar(100) DEFAULT NULL COMMENT '经纬解析区',
  `ll_get_busarea` varchar(100) DEFAULT NULL COMMENT '经纬解析商圈',
  `ll_get_quarter` varchar(100) DEFAULT NULL COMMENT '经纬解析小区',
  `ll_get_detail` varchar(100) DEFAULT NULL COMMENT '经纬解析详细地址',
  `enabled` varchar(1) DEFAULT NULL COMMENT '是否删除',
  `create_by` varchar(100) DEFAULT NULL COMMENT '创建人',
  `create_time` varchar(20) DEFAULT NULL COMMENT '创建时间',
  `modify_by` varchar(100) DEFAULT NULL COMMENT '修改人',
  `modify_time` varchar(20) DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`house_info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='HOUSE_BASE_INFOQK';

CREATE TABLE `house_base_infozr` (
  `house_info_id` varchar(60) NOT NULL COMMENT '房屋ID',
  `house_id` varchar(60) DEFAULT NULL COMMENT '源房屋ID',
  `price` decimal(18,2) DEFAULT NULL COMMENT '价格',
  `floor` varchar(20) DEFAULT NULL COMMENT '楼层',
  `house_type` varchar(20) DEFAULT NULL COMMENT '户型',
  `house_quarter_id` varchar(60) DEFAULT NULL COMMENT '小区ID',
  `enabled` varchar(1) DEFAULT NULL COMMENT '是否删除',
  `create_by` varchar(100) DEFAULT NULL COMMENT '创建人',
  `create_time` varchar(20) DEFAULT NULL COMMENT '创建时间',
  `modify_by` varchar(100) DEFAULT NULL COMMENT '修改人',
  `modify_time` varchar(20) DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`house_info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='HOUSE_BASE_INFOZR';

CREATE TABLE `house_paytype_infozr` (
  `paytype_info_id` varchar(60) NOT NULL COMMENT '房屋付款方式ID',
  `house_id` varchar(60) DEFAULT NULL COMMENT '源房屋ID',
  `service_charge` decimal(18,2) DEFAULT NULL COMMENT '服务收费',
  `rent` decimal(18,2) DEFAULT NULL COMMENT '房屋租金',
  `period` varchar(20) DEFAULT NULL COMMENT '付款方式',
  `deposit` decimal(18,2) DEFAULT NULL COMMENT '保证金',
  `enabled` varchar(1) DEFAULT NULL COMMENT '是否删除',
  `create_by` varchar(100) DEFAULT NULL COMMENT '创建人',
  `create_time` varchar(20) DEFAULT NULL COMMENT '创建时间',
  `modify_by` varchar(100) DEFAULT NULL COMMENT '修改人',
  `modify_time` varchar(20) DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`paytype_info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='HOUSE_PAYTYPE_INFOZR';

CREATE TABLE `house_quarter_infozr` (
  `house_quarter_id` varchar(60) NOT NULL COMMENT '小区ID',
  `house_quarter_name` varchar(100) DEFAULT NULL COMMENT '小区名称',
  `lat` varchar(20) DEFAULT NULL COMMENT '纬度',
  `lng` varchar(20) DEFAULT NULL COMMENT '经度',
  `area` varchar(100) DEFAULT NULL COMMENT '区域',
  `busiarea` varchar(100) DEFAULT NULL COMMENT '业务描述',
  `ll_get_province` varchar(100) DEFAULT NULL COMMENT '经纬解析省',
  `ll_get_city` varchar(100) DEFAULT NULL COMMENT '经纬解析市',
  `ll_get_strict` varchar(100) DEFAULT NULL COMMENT '经纬解析区',
  `ll_get_busarea` varchar(100) DEFAULT NULL COMMENT '经纬解析商圈',
  `ll_get_quarter` varchar(100) DEFAULT NULL COMMENT '经纬解析小区',
  `ll_get_detail` varchar(100) DEFAULT NULL COMMENT '经纬解析详细地址',
  `enabled` varchar(1) DEFAULT NULL COMMENT '是否删除',
  `create_by` varchar(100) DEFAULT NULL COMMENT '创建人',
  `create_time` varchar(20) DEFAULT NULL COMMENT '创建时间',
  `modify_by` varchar(100) DEFAULT NULL COMMENT '修改人',
  `modify_time` varchar(20) DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`house_quarter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='HOUSE_QUARTER_INFOZR';

CREATE TABLE `house_recomm_infozr` (
  `house_recomm_id` varchar(60) NOT NULL COMMENT '房屋推荐ID',
  `house_id` varchar(60) DEFAULT NULL COMMENT '源房屋ID',
  `price_unit` varchar(20) DEFAULT NULL COMMENT '单位',
  `url` varchar(255) DEFAULT NULL COMMENT 'URL相对路径',
  `index_no` varchar(20) DEFAULT NULL COMMENT '索引编号',
  `district` varchar(100) DEFAULT NULL COMMENT '区域',
  `price` decimal(18,2) DEFAULT NULL COMMENT '价格',
  `info` varchar(100) DEFAULT NULL COMMENT '房屋描述',
  `photo` varchar(255) DEFAULT NULL COMMENT '房屋图片',
  `sell_price` decimal(18,2) DEFAULT NULL COMMENT '销售价格',
  `enabled` varchar(1) DEFAULT NULL COMMENT '是否删除',
  `create_by` varchar(100) DEFAULT NULL COMMENT '创建人',
  `create_time` varchar(20) DEFAULT NULL COMMENT '创建时间',
  `modify_by` varchar(100) DEFAULT NULL COMMENT '修改人',
  `modify_time` varchar(20) DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`house_recomm_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='HOUSE_RECOMM_INFOZR';

CREATE TABLE `house_spider_log` (
  `spider_log_id` varchar(60) NOT NULL COMMENT '抓取日志ID',
  `pid` varchar(20) DEFAULT NULL COMMENT '进程ID',
  `spider_time` varchar(20) DEFAULT NULL COMMENT '抓取时间',
  `spider_type` varchar(20) DEFAULT NULL COMMENT '抓取类型',
  `log_type` varchar(20) DEFAULT NULL COMMENT '日志类型',
  `spider_project` varchar(60) DEFAULT NULL COMMENT '抓取项目',
  `spider_content` varchar(100) DEFAULT NULL COMMENT '抓取内容',
  PRIMARY KEY (`spider_log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='HOUSE_SPIDER_LOG';





