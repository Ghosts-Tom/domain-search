import os
import requests
import shutil
from pathlib import Path

def download_file(url, filename):
    """下载文件到指定路径"""
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def main():
    # 创建必要的目录
    static_dir = Path('static')
    css_dir = static_dir / 'css'
    fonts_dir = static_dir / 'fonts'
    
    css_dir.mkdir(parents=True, exist_ok=True)
    fonts_dir.mkdir(parents=True, exist_ok=True)
    
    # 使用国内 CDN
    bootstrap_url = 'https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.1.3/css/bootstrap.min.css'
    fa_url = 'https://cdn.bootcdn.net/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    
    try:
        # 下载 Bootstrap CSS
        print('下载 Bootstrap CSS...')
        download_file(bootstrap_url, css_dir / 'bootstrap.min.css')
        
        # 下载 Font Awesome CSS
        print('下载 Font Awesome CSS...')
        download_file(fa_url, css_dir / 'all.min.css')
        
        # 下载 Font Awesome 字体文件
        font_files = {
            'fa-solid-900.woff2': 'https://cdn.bootcdn.net/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2',
            'fa-brands-400.woff2': 'https://cdn.bootcdn.net/ajax/libs/font-awesome/6.0.0/webfonts/fa-brands-400.woff2',
            'fa-regular-400.woff2': 'https://cdn.bootcdn.net/ajax/libs/font-awesome/6.0.0/webfonts/fa-regular-400.woff2'
        }
        
        for font_file, font_url in font_files.items():
            print(f'下载字体文件: {font_file}...')
            try:
                download_file(font_url, fonts_dir / font_file)
            except Exception as e:
                print(f'下载字体文件 {font_file} 失败: {str(e)}')
        
        # 更新 Font Awesome CSS 中的字体路径
        print('更新字体文件路径...')
        fa_css_path = css_dir / 'all.min.css'
        with open(fa_css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # 替换字体文件路径
        css_content = css_content.replace(
            '../webfonts/',
            '../fonts/'
        )
        
        with open(fa_css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print('所有资源文件下载完成！')
        
    except Exception as e:
        print(f'下载过程中出现错误: {str(e)}')
        print('请检查网络连接或手动下载所需文件。')

if __name__ == '__main__':
    main() 