# Domain Search

一个智能域名生成和检查工具，可以帮助你快速生成域名创意并检查其可用性。

## 功能特点

- 基于关键词智能生成域名
- 支持多种顶级域名（TLD）检查
- 内置敏感词过滤
- 实时 WHOIS 信息查询
- 域名可用性检查
- 智能缓存机制
- 现代化 Web 界面
- 完全本地化部署，无需外部依赖

## 技术栈

- Python 3.9
- Flask Web 框架
- Docker 容器化
- WHOIS 查询服务
- 多线程并发处理
- Bootstrap 5.1.3
- Font Awesome 6.0.0

## 快速开始

### Docker 部署（推荐）

1. 克隆项目：
```bash
git clone https://github.com/yourusername/search-domain.git
cd search-domain
```

2. 下载静态资源（可选，如果需要更新静态资源）：
```bash
python download_assets.py
```

3. 构建并启动服务：
```bash
docker-compose up -d
```

4. 访问服务：
打开浏览器访问 `http://localhost:8888` 或 `http://你的服务器IP:8888`

### 本地开发

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 下载静态资源：
```bash
python download_assets.py
```

4. 启动服务：
```bash
python main.py --web
```

5. 访问服务：
打开浏览器访问 `http://localhost:8888`

## API 接口

### 生成域名
- 端点：`/generate`
- 方法：POST
- 参数：
  ```json
  {
    "keywords": ["关键词1", "关键词2"],
    "min_length": 4,
    "max_length": 15,
    "tlds": [".com", ".net"],
    "count": 10
  }
  ```

### 检查域名
- 端点：`/refresh_whois`
- 方法：POST
- 参数：
  ```json
  {
    "domain": "example.com"
  }
  ```

## Docker 配置

- 镜像名称：`search-domain:latest`
- 容器名称：`domain-service`
- 端口映射：`8888:8888`
- 数据卷：`whois_cache.json`
- 环境变量：
  - `FLASK_APP=main.py`
  - `FLASK_ENV=production`
  - `FLASK_RUN_HOST=0.0.0.0`

## 开发说明

### 目录结构
```
search-domain/
├── main.py                 # 主程序入口
├── domain_generator.py     # 域名生成器
├── sensitive_word_checker.py  # 敏感词检查
├── download_assets.py      # 静态资源下载脚本
├── requirements.txt        # 项目依赖
├── Dockerfile             # Docker 构建文件
├── docker-compose.yml     # Docker 编排配置
├── whois_cache.json       # WHOIS 缓存文件
├── static/                # 静态资源目录
│   ├── css/              # CSS 文件
│   │   ├── bootstrap.min.css
│   │   ├── all.min.css
│   │   └── styles.css
│   └── fonts/            # 字体文件
│       ├── fa-solid-900.woff2
│       ├── fa-brands-400.woff2
│       └── fa-regular-400.woff2
└── templates/            # 模板文件
    └── index.html        # 主页模板
```

### 依赖版本
```
Flask==2.0.1
Werkzeug==2.0.1
python-whois==0.8.0
requests==2.31.0
tqdm==4.66.1
whois21==1.4.6
pypinyin==0.49.0
```

### 本地化说明

项目已完全本地化，所有静态资源（CSS、字体等）都存储在本地，无需依赖外部 CDN。这样做的好处是：

1. 提高加载速度
2. 支持离线运行
3. 更好的稳定性
4. 减少外部依赖
5. 更容易维护和定制

如果需要更新静态资源，只需运行：
```bash
python download_assets.py
```

## 许可证

MIT License

## 作者

[Tom]

## 致谢

感谢所有贡献者的付出！
