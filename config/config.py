import os


# spider
USE_PROXY = False
PROXY_HTTPS_URL = 'https://127.0.0.1:7890'
DOWNLOAD_DELAY = False
SCRAPY_LOG = True

# mysql
MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('DB_PORT', 3306))
MYSQL_USER = os.getenv('DB_USER', 'root')
MYSQL_PASSWORD = os.getenv('DB_PASSWORD', '123456')
MYSQL_DATABASE = os.getenv('DB_DATABASE', 'ahutoj')
MYSQL_CHARSET = 'utf8'
