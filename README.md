# AHUT OJ Crawl

AHUT OJ 附属爬虫项目

## 相关仓库

前端部分 [AHUT OJ front-end V2](https://github.com/JorbanSS/AHUT-OJ-front-end-V2)

后端部分 [ahutoj](https://github.com/ximoyuxiao/ahutoj/tree/docker)

## 技术架构

Py3.12 \ FastAPI \ scrapy

## 配置环境

```sh
pip freeze > requirements.txt  # 导出依赖项清单

pip install -r requirements.txt  # 安装所有依赖项
```

安装 scrapy

```sh
pip install scrapy

scrapy startproject crawl  # 创建项目

scrapy genspider itcast itcast.cn  # 创建新的蜘蛛
```

安装第三方库

```sh
pip install pymysql

pip install sqlalchemy
```

## 启动项目

```sh
uvicorn main:app --reload
```

运行在 http://127.0.0.1:8000

OpenAPI 标准的交互式 API 文档

- Swagger UI http://127.0.0.1:8000/docs

- Redoc http://127.0.0.1:8000/redoc

运行爬虫

```sh
scrapy crawl codeforces -a opt=contests --nolog
```