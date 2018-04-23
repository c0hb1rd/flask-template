# c0hb1rd Flask Template
[![Python 3](https://img.shields.io/badge/python-3.x-green.svg)](https://www.python.org/)
[![Flask 0.11.1](https://img.shields.io/badge/flask-0.11.1-yellow.svg)](https://github.com/pallets/flask)

## 目录
+ [一、结构](#一结构)
+ [二、API文档](#二API文档)

## 一、结构
```bash
.
├── README.md
├── app.py                  # 程序入口
├── blueprint               # 蓝图目录
│   └── __init__.py
├── config.py               # 配置文件
├── core                    # 核心模块
│   ├── __init__.py
│   ├── base_model.py       # Mysql ORM 对象基类
│   ├── base_print.py       # 蓝图基类
│   ├── base_url.py         # URL与视图映射基类
│   ├── base_view.py        # 视图基类
│   ├── dbconnector         # Mysql ORM 对象模块目录
│   │   ├── __init__.py
│   │   ├── conditions.py   # ORM 条件对象
│   │   ├── joins.py        # ORM 条件关联对象，如 AND、OR
│   │   └── models.py       # ORM 对象
│   ├── functions.py        # 公用函数方法
│   └── init_project.py     # 蓝图初始化模块
├── init.py
├── model                   # ORM 对象目录
│   └── __init__.py
├── requirements.txt        # 依赖清单
├── static                  # 静态资源目录
├── templates               # HTML 页面目录
│   └── index.html
├── tornado.py              # Tornaado 入口
└── wsgi.py                 # WSGI 入口
```

## 一、结构
```bash
.
├── README.md
├── app.py                  # 程序入口
├── blueprint               # 蓝图目录
│   └── __init__.py
├── config.py               # 配置文件
├── core                    # 核心模块
│   ├── __init__.py
│   ├── base_model.py       # Mysql ORM 对象基类
│   ├── base_print.py       # 蓝图基类
│   ├── base_url.py         # URL与视图映射基类
│   ├── base_view.py        # 视图基类
│   ├── dbconnector         # Mysql ORM 对象模块目录
│   │   ├── __init__.py 
│   │   ├── conditions.py   # ORM 条件对象
│   │   ├── joins.py        # ORM 条件关联对象，如 AND、OR
│   │   └── models.py       # ORM 对象
│   ├── functions.py        # 公用函数方法
│   └── init_project.py     # 蓝图初始化模块
├── init.py
├── model                   # ORM 对象目录
│   └── __init__.py
├── requirements.txt        # 依赖清单
├── static                  # 静态资源目录
├── templates               # HTML 页面目录
│   └── index.html
├── tornado.py              # Tornaado 入口
└── wsgi.py                 # WSGI 入口
```

## 二、API文档
介绍整个项目结构下每个目录和模块的具体用法
### 2.1 核心模块 core
core 模块下的各个子模块
#### 2.1.1 functions 模块
core._**functions**_
- _**format_md5(s: str)**_
  返回：`hashlib.md5` 哈希过后的值

- _**random_password()**_:
  返回：已当前时间戳为参数的 _**format_md5**_ 
  
- _**now(length=13, stamp=True, format_type="%Y-%m-%d %H:%M:%S")**_
  返回：当前时间戳，默认长度为13，如过 `stamp` 为 `False`，则根据 `format_type` 返回当前时间的日期格式

- _**base64_decode_dict(s)**_


_**待续...**_


