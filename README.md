# Template Crawler

## Description

Using config files to crawl web data.

## Basic Info

Project Name | Author | CreateDate | OS | Language
:-: | :-: | :-: | :-: | :-:
Template Crawler | [@TauWu](https://github.com/TauWu/) | 2018-07-19 | Linux (Based on Debain) | Python 3

## TODOs

- [ ] Code
	- [ ] Transplant Module `Downloader` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [ ] Transplant Module `Proxies` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [ ] Transplant Module `Parser` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [ ] Transplant Module `Common` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [ ] Create Module `Config Parser`
	- [ ] Create Module `Common Crawler`

- [ ] Test
	- [ ] Test House Info from [ZiRoom](http://sh.ziroom.com)
	- [ ] Test House Info from [qk365](http://www.qk365.com)
	- [ ] Test House Info from [lianjia](https://sh.lianjia.com)

## Future TODOs

- [ ] Data Warehouse
- [ ] ETL Project
- [ ] Data Mining
- [ ] Data API
- [ ] Price Trend Prediction

## Requirements

### Softwares Needs

```sh
apt-get install python3			# Python interpreter.
apt-get install python3-pip		# Pip tools to install 3rd-party modules.
apt-get install redis-server	# Save Hash Map data.
apt-get install mysql-server	# Save structured data.
apt-get install python-bs4		# Parse HTML files.
```

### Module Needs

```sh
pip3 install requests		# Better method to start requests.
pip3 install PyMySQL		# Connect to MySQL and control it.
pip3 install configparser	# Read and write config files.
pip3 install beautifulsoup4	# Parser HTML files.
pip3 install lxml			# Read HTML files as a balance tree.
pip3 install fake-useragent	# Provide random UA when request a host.
pip3 install redis			# Connect to Redis server and control it. 
```

## Crawler Types

For different websites, there are some methods to get its data. For instance, you can get house info list from externally exposed HTTP APIs, howerver, some sites don't provide them, because some sites are rendered by templates. Thus, we are supposed to provide different types to slove these problems. And here is the `enumeration of carwler types`.

Type No. | Crawler methods
:-: | :-:
1 | Request HTTP APIs to get list info.
2 | Request HTTP APIs to get detail info.
3 | Request Web HTML to get list info.
4 | Request Web HTML to get detail info.
