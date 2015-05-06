# url-shortener
Python application to shorten and unshorten web URLs.

### Development Environment
OS: Windows 8.1 64-bit

Tools:
* Python 2.7.9
* PostgreSQL 9.4.1
( Download 64-bit installer from http://www.enterprisedb.com/products-services-training/pgdownload#windows )
* psycopg2 ( pip install psycopg2 )
* argparse
* Git

### Usage

You can use this application both as a module and as a command line utility.

##### As a module
```python
import url_shortener
urlshortener = UrlShortener()
short_url = urlshortener.shorten("http://google.com/rajenrauppal", 'http://bit.ly/')
print short_url
long_url = urlshortener.unshorten(short_url)
print long_url
```

##### As command line utility

Run following command for help
```
$ python url_shortener.py -h or --help
```

Shorten:
```
$ python url_shortener.py -l "http://google.co.in/uppal" -p "http://yor.co"
```

Un-shorten:
```
$ python url_shortener.py -s "http://yor.co/6cs8t"
```
