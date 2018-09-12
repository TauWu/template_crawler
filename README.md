# Template Crawler

## Description

Using config files to crawl web data, and load it to database.

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
	- [x] Test House Info from [danke](https://www.dankegongyu.com)

- [x] Full Test
	- [x] Test Full House Info from [ZiRoom](http://sh.ziroom.com)
	- [x] Test Full House Info from [qk365](http://www.qk365.com)
	- [x] Test Full House Info from [lianjia](https://sh.lianjia.com)
	- [x] Test Full House Info from [danke](https://www.dankegongyu.com)

- [x] ETL Project
	- [x] Extract Data from Redis
	- [x] Transform and clean data
	- [x] Load Data and save

- [x] Log Module
	- [x] Log into files.
	- [x] log into database.

- [x] Async Func
	- [x] Use async func to mutil-process ziroom price imgs.

- [x] Mail Monitor
	- [x] Package email module.
	- [x] Send mail when crawler finished.
	- [x] Send mail when etl finished.

- [ ] Mail Reporter
	- [ ] Send mail with xlsx file with cron.


## Future TODOs

- [ ] Data Warehouse
- [ ] Data Mining
- [ ] Data API
- [ ] Price Trend Prediction

## Flow Chart
![image](https://github.com/TauWu/template_crawler/blob/master/bin/template_crawler_flow.jpg)

## Requirements

### Software Needs

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

For different websites, there are some methods to get its data. For instance, you can get house info list from externally exposed HTTP APIs, howerver, some sites don't provide them, because some sites are rendered by templates. Thus, we are supposed to provide different types to slove these problems. And here is the **enumeration of carwler types**.

Type No. | Crawler methods
:-: | :-:
1 | `GET`  Request HTTP APIs, and parsering JSON object by json.
2 | `GET`  Request Webpage, and parsering HTML content by lxml.
3 | `POST` Request HTTP APIs, and parsering JSON object by json.

## Code Directory Structure

- [_output](https://github.com/TauWu/template_crawler#_output)
- [_test](https://github.com/TauWu/template_crawler#_test)
- [.vscode](https://github.com/TauWu/template_crawler#.vscode)
- [config](https://github.com/TauWu/template_crawler#config)
- [constant](https://github.com/TauWu/template_crawler#constant)
- [database](https://github.com/TauWu/template_crawler#database)
- [do](https://github.com/TauWu/template_crawler#do)
- [log](https://github.com/TauWu/template_crawler#log)
- [module](https://github.com/TauWu/template_crawler#module)
- [util](https://github.com/TauWu/template_crawler#util)
- .gitignore
- crawler_main.py
- etl_main.py
- [LICENSE](https://github.com/TauWu/template_crawler#license)
- README.md
- start_crawler.sh
- start_etl.sh
- stop_all.sh

### _output
The folder to save intermedidate temporary files. For instance, xlsx files, img files.

### _test
Test code when develop or debug, this folder won't be pushed to git.

### .vscode
Visual Studio Code config files, this folder won't be pushed to git.

### config
Contains crawler, elt and sys config files here. File **sys.cfg** won't be pushed to git.

### constant
Constant value, config, dict and so on.

### database
SQL files here.

### do
Try to do it!
- `crawler.py` => Do crawler.
- `etl.py` => Do etl project.

### log
Save log files here, contains subfolders named by different projects.

### module
Contains many modules used by **do**.
- `config` => Read config files in **./config** and return it.
- `database` => Create and execute SQL string
- `parser` => Parse the data from request file one by one by lxml or json module, and then **save them into redis server**.
	- `detail.py` => Parser detail webpage or HTTP API json and **update** the dict to redis.
	- `list.py` => Parser list webpage or HTTP API json and **update** the dict to redis.
	- `extra.py` => Extra function for this crawler, for instance, ziroom's house price is showed by a picture, we should do extra for it.
- `redis` => Redis scanner, scanning the redis-server to get request key list.
- `request` => Mutil-Proxy-Request ordered list or detail url list by ProxiesRequest Module and yield the content to parser module.

### util
Contains many base tools used by **do**, **module**.
- `common` => Common extensions here.
	- `date.py` => Class Time and DateTime.
	- `logger.py` => Class LogBase.
	- `timeout.py` => Function set_timeout.
	- `tools.py` => Tool functions.

- `config` => Config reader and writer module.
- `database` => Database connector and executor.
- `redis` => Redis connector and executor.
- `web` => Mutil-Proxy-Request module and test.
- `xlsx` => Read and write xlsx files.

## LICENSE

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/
```


## Tips

1. Here is the crawl difficulty's order of different websites: ziroom > lianjia > qk.
2. When you get the rent price of ziroom, you're supposed to download a temp img, and then, get the string from img by using OCR tools. Ziroom website will give the index of each number and you should joint it.
3. *__TODO__* This project use `gevent` to download webpage and use `asdef` and `await` request to download imgs. It can be quicker if turn `gevent` + `asdef` asynchronous mode to `gevent` mode or `asdef` asynchronous mode, because the waste of exchange for threads.
