# Template Crawler

## Description

Using config files to crawl web data.

## Basic Info

Project Name | Author | CreateDate | OS | Language
:-: | :-: | :-: | :-: | :-:
Template Crawler | [@TauWu](https://github.com/TauWu/) | 2018-07-19 | Linux (Based on Debain) | Python 3

## TODOs

- [x] Code
	- [x] Transplant Module `Downloader` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [x] Transplant Module `Proxies` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [x] Transplant Module `Parser` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [x] Transplant Module `Common` from [spider\_anjuke](https://github.com/TauWu/spider_anjuke)
	- [x] Create Module `Config Parser`
	- [x] Create Module `Common Crawler`

- [x] Test
	- [x] Test House Info from [ZiRoom](http://sh.ziroom.com)
	- [x] Test House Info from [qk365](http://www.qk365.com)
	- [x] Test House Info from [lianjia](https://sh.lianjia.com)

- [x] Full Test
	- [x] Test Full House Info from [ZiRoom](http://sh.ziroom.com)
	- [x] Test Full House Info from [qk365](http://www.qk365.com)
	- [x] Test Full House Info from [lianjia](https://sh.lianjia.com)

- [x] ETL Project
	- [x] Extract Data from Redis
	- [x] Transform and clean data
	- [x] Load Data and save

- [ ] Log Module
	- [ ] Log into files.
	- [ ] log into database.
	
## Future TODOs

- [ ] Data Warehouse
- [ ] Data Mining
- [ ] Data API
- [ ] Price Trend Prediction

## Requirements

### Softwares Needs

```sh
# Python interpreter.
apt-get install python3

# Pip tools to install 3rd-party modules.
apt-get install python3-pip

# Save Hash Map data.
apt-get install redis-server

# Save structured data.
apt-get install mysql-server

# Use tesseract-ocr to convert img to string.
apt-get install tesseract-ocr
```

### Module Needs

```sh
# Better method to start requests.
pip3 install requests

# Connect to MySQL and control it.
pip3 install PyMySQL

# Read and write config files.
pip3 install configparser

# Read HTML files as a balance tree.
pip3 install lxml

# Provide random UA when request a host.
pip3 install fake-useragent

# Connect to Redis server and control it.
pip3 install redis

# Edit images.
pip3 install pillow

# Use tesseract-ocr in python.
pip3 install pytesseract
```

## Crawler Types

For different websites, there are some methods to get its data. For instance, you can get house info list from externally exposed HTTP APIs, howerver, some sites don't provide them, because some sites are rendered by templates. Thus, we are supposed to provide different types to slove these problems. And here is the `enumeration of carwler types`.

Type No. | Crawler methods
:-: | :-:
1 | Request HTTP APIs to get list info.
2 | Request HTTP APIs to get detail info.
3 | Request Web HTML to get list info.
4 | Request Web HTML to get detail info.

## Tips

1. Here is the crawl difficulty's order of different websites: ziroom > lianjia > qk.
2. When you get the rent price of ziroom, you're supposed to download a temp img, and then, get the string from img by using OCR tools. Ziroom website will give the index of each number and you should joint it.