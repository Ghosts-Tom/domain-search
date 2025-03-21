# Domain Generator

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

### 使用 Docker 运行

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/domain-search.git  
cd domain-search
```

2. 构建并运行 Docker 容器：
```bash
docker-compose up --build -d
```

3. 访问应用：
打开浏览器访问 `http://localhost:8080`

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

3. 运行应用：
```bash
python main.py --web
```

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

## 配置说明

### 环境变量
- `FLASK_APP`: 应用入口文件
- `FLASK_ENV`: 运行环境
- `PYTHONUNBUFFERED`: Python 输出缓冲设置
- `TZ`: 时区设置

### Docker 配置
- 端口映射：8080:5000
- 数据卷：whois_cache.json
- 健康检查：每30秒检查一次

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 作者

[Tom]

## 致谢
