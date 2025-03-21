# Domain Search

一个智能域名生成和检查工具，可以帮助你快速生成域名创意并检查其可用性。

## 功能特点

- 基于关键词生成域名
- 支持多种顶级域名（TLD）
- 敏感词检查
- WHOIS 信息查询
- 域名可用性检查
- 缓存机制优化查询性能
- 美观的 Web 界面

## 技术栈

- Python 3.9
- Flask
- Docker
- WhoIs
- 多线程处理

## 快速开始

### 使用 Docker 部署

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/search-domain.git
cd search-domain
```

2. 创建缓存文件：
```bash
touch whois_cache.json
```

3. 构建并启动容器：
```bash
docker-compose up -d
```

4. 访问应用：
打开浏览器访问 `http://你的服务器IP:8888`

### 本地运行

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

3. 创建缓存文件：
```bash
touch whois_cache.json
```

4. 运行应用：
```bash
python main.py --web
```

5. 访问应用：
打开浏览器访问 `http://localhost:5000`

### Docker 配置说明

- 镜像名称：search-domain:latest
- 容器名称：domain-service
- 端口映射：8888:5000
- 数据卷：whois_cache.json
- 环境变量：
  - FLASK_APP=main.py
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
  - TZ=Asia/Shanghai
  - FLASK_RUN_HOST=0.0.0.0

## API 接口

### 生成域名
- 端点：`/generate`
- 方法：POST
- 参数：
  - keywords: 关键词列表
  - min_length: 最小长度
  - max_length: 最大长度
  - tlds: 顶级域名列表
  - count: 生成数量

### 刷新 WHOIS 信息
- 端点：`/refresh_whois`
- 方法：POST
- 参数：
  - domain: 域名

## 许可证

MIT License

## 作者

[Tom]

## 致谢

感谢所有贡献者的付出！ 