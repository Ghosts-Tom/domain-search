import argparse
from typing import List, Tuple
from domain_generator import DomainGenerator
from sensitive_word_checker import SensitiveWordChecker
from flask import Flask, render_template, request, jsonify
import whois
import socket
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
import time
from functools import wraps
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
domain_generator = DomainGenerator()
sensitive_checker = SensitiveWordChecker()

# WHOIS缓存配置
CACHE_FILE = 'whois_cache.json'
CACHE_EXPIRY = 3600 * 24  # 24小时的缓存时间

# 初始化缓存
WHOIS_CACHE = {}

def load_cache():
    """从文件加载WHOIS缓存"""
    global WHOIS_CACHE
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                # 过滤掉过期的缓存
                current_time = time.time()
                WHOIS_CACHE = {
                    domain: (timestamp, data)
                    for domain, (timestamp, data) in cache_data.items()
                    if current_time - timestamp < CACHE_EXPIRY
                }
    except Exception as e:
        print(f"加载缓存失败: {e}")
        WHOIS_CACHE = {}

def save_cache():
    """保存WHOIS缓存到文件"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(WHOIS_CACHE, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存缓存失败: {e}")

# 启动时加载缓存
load_cache()

def retry_on_failure(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:  # 最后一次尝试
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=2)
def get_whois_info(domain: str) -> dict:
    """获取域名的whois信息"""
    try:
        # 设置socket超时
        socket.setdefaulttimeout(0.005)  # 设置超时时间为5ms
        w = whois.whois(domain)
        
        # 处理日期格式
        def format_date(date):
            if isinstance(date, list):
                date = date[0]
            if hasattr(date, 'strftime'):
                return date.strftime('%Y-%m-%d %H:%M:%S')
            return str(date) if date else 'Unknown'
        
        # 处理状态格式
        def format_status(status):
            if isinstance(status, list):
                status = status[0]
            if isinstance(status, str):
                # 移除URL部分
                status = status.split('https://')[0].strip()
            return str(status) if status else 'Unknown'
        
        return {
            'registrar': str(w.registrar) if w.registrar else 'Unknown',
            'creation_date': format_date(w.creation_date),
            'expiration_date': format_date(w.expiration_date),
            'status': format_status(w.status),
            'success': True
        }
    except socket.timeout:
        return {
            'success': False,
            'error': '查询超时'
        }
    except Exception as e:
        # 精简错误信息
        error_msg = str(e)
        if 'No match' in error_msg:
            return {
                'success': False,
                'error': '未注册'
            }
        elif 'timed out' in error_msg.lower():
            return {
                'success': False,
                'error': '查询超时'
            }
        else:
            return {
                'success': False,
                'error': '查询失败'
            }

def get_whois_info_cached(domain: str) -> dict:
    """带缓存的WHOIS查询"""
    current_time = time.time()
    
    # 检查缓存
    if domain in WHOIS_CACHE:
        cache_time, result = WHOIS_CACHE[domain]
        if current_time - cache_time < CACHE_EXPIRY:
            print(f"命中缓存: {domain}")
            return result
    
    # 缓存未命中，执行查询
    try:
        result = get_whois_info(domain)
        # 更新缓存
        WHOIS_CACHE[domain] = (current_time, result)
        # 异步保存缓存
        save_cache()
        return result
    except Exception as e:
        print(f"WHOIS查询失败: {domain} - {e}")
        return {
            'success': False,
            'error': '查询失败'
        }

def get_whois_info_parallel(domains: List[str], max_workers: int = 5, timeout: int = 5) -> List[dict]:
    """并行执行WHOIS查询"""
    results = []
    completed_domains = set()
    
    # 首先检查缓存
    for domain in domains:
        if domain in WHOIS_CACHE:
            cache_time, result = WHOIS_CACHE[domain]
            if time.time() - cache_time < CACHE_EXPIRY:
                results.append({
                    'domain': domain,
                    'whois': result
                })
                completed_domains.add(domain)
                print(f"缓存命中: {domain}")
    
    # 获取未缓存的域名
    remaining_domains = [d for d in domains if d not in completed_domains]
    if not remaining_domains:
        return results
    
    print(f"需要查询的域名数量: {len(remaining_domains)}")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_domain = {
            executor.submit(get_whois_info, domain): domain 
            for domain in remaining_domains
        }
        
        try:
            for future in as_completed(future_to_domain, timeout=timeout):
                domain = future_to_domain[future]
                try:
                    whois_info = future.result(timeout=0.005)  # 将单个查询超时改为5ms
                    # 更新缓存
                    WHOIS_CACHE[domain] = (time.time(), whois_info)
                    results.append({
                        'domain': domain,
                        'whois': whois_info
                    })
                    print(f"查询成功: {domain}")
                except TimeoutError:
                    print(f"查询超时: {domain}")
                    results.append({
                        'domain': domain,
                        'whois': {
                            'success': False,
                            'error': '查询超时'
                        }
                    })
                except Exception as e:
                    print(f"查询失败: {domain} - {str(e)}")
                    results.append({
                        'domain': domain,
                        'whois': {
                            'success': False,
                            'error': '查询失败'
                        }
                    })
        except TimeoutError:
            print("整体查询超时")
            # 处理未完成的查询
            for domain in remaining_domains:
                if domain not in [r['domain'] for r in results]:
                    results.append({
                        'domain': domain,
                        'whois': {
                            'success': False,
                            'error': '查询超时'
                        }
                    })
    
    # 保存缓存
    try:
        save_cache()
    except Exception as e:
        print(f"保存缓存失败: {str(e)}")
    
    # 确保返回结果的顺序与输入域名顺序一致
    ordered_results = []
    for domain in domains:
        for result in results:
            if result['domain'] == domain:
                ordered_results.append(result)
                break
    
    return ordered_results

def generate_and_check_domains(
    keywords: List[str] = None,
    length_range: Tuple[int, int] = None,
    tlds: List[str] = None,
    count: int = 10  # 默认生成10个域名
) -> List[dict]:
    """生成域名并进行敏感词检测"""
    try:
        # 验证后缀格式
        valid_tlds = []
        for tld in tlds:
            tld = tld.strip()
            if tld.startswith('.'):
                valid_tlds.append(tld)
        
        if not valid_tlds:
            raise ValueError("没有有效的域名后缀")
            
        # 测量域名生成时间
        generation_start = time.time()
        domains = domain_generator.generate_domains(keywords, length_range, valid_tlds)
        generation_time = time.time() - generation_start
        print(f"域名生成时间: {generation_time:.2f}秒")
        
        # 限制生成的域名数量
        if count > 20:
            count = 20
        domains = domains[:count]
        print(f"生成域名数量: {len(domains)}")
        
        # 测量敏感词检测时间
        sensitive_check_start = time.time()
        results = sensitive_checker.check_domains(domains)
        sensitive_check_time = time.time() - sensitive_check_start
        print(f"敏感词检测时间: {sensitive_check_time:.2f}秒")
        
        # 测量WHOIS并行查询时间
        whois_start = time.time()
        whois_results = get_whois_info_parallel(domains, max_workers=5, timeout=5)
        whois_time = time.time() - whois_start
        print(f"WHOIS查询总时间: {whois_time:.2f}秒")
        
        # 合并结果
        for result, whois_result in zip(results, whois_results):
            result['whois'] = whois_result['whois']
        
        # 添加时间统计信息
        timing_info = {
            'generation_time': round(generation_time * 1000, 2),  # 毫秒
            'sensitive_check_time': round(sensitive_check_time * 1000, 2),  # 毫秒
            'whois_time': round(whois_time * 1000, 2),  # 毫秒
            'total_time': round((generation_time + sensitive_check_time + whois_time) * 1000, 2)  # 毫秒
        }
        
        return results, timing_info
    except Exception as e:
        print(f"生成域名时发生错误: {str(e)}")
        return [], {}

@app.route('/')
def index():
    """Web界面主页"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """处理域名生成请求"""
    try:
        data = request.get_json()
        
        # 处理 keywords，支持字符串和列表类型
        keywords_data = data.get('keywords', '')
        if isinstance(keywords_data, str):
            keywords = keywords_data.split()
        elif isinstance(keywords_data, list):
            keywords = keywords_data
        else:
            keywords = []
            
        # 如果没有提供关键词，使用默认关键词
        if not keywords:
            keywords = ['web', 'app', 'site']
            
        min_length = int(data.get('min_length', 3))  # 修改默认最小长度为3
        max_length = int(data.get('max_length', 63))  # 修改默认最大长度为63
        
        # 处理 TLDs，支持字符串和列表类型
        tlds_data = data.get('tlds', '.com,.net')
        if isinstance(tlds_data, str):
            tlds = tlds_data.split(',')
        else:
            tlds = tlds_data
            
        count = int(data.get('count', 10))  # 获取生成数量，默认为10
        
        if count > 20:
            return jsonify({
                'success': False,
                'error': '生成数量不能超过20个'
            }), 400
            
        if not tlds:
            return jsonify({
                'success': False,
                'error': '请至少选择一个域名后缀'
            }), 400
        
        # 测量总开始时间
        start_time = time.time()
        
        results, timing_info = generate_and_check_domains(
            keywords=keywords,
            length_range=(min_length, max_length),
            tlds=tlds,
            count=count
        )
        
        # 测量总结束时间
        end_time = time.time()
        total_time = round((end_time - start_time) * 1000, 2)  # 转换为毫秒
        
        statistics = sensitive_checker.get_statistics(results)
        
        return jsonify({
            'success': True,
            'results': results,
            'statistics': statistics,
            'timing_info': timing_info,
            'total_time': total_time
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/refresh_whois', methods=['POST'])
def refresh_whois():
    """处理单个域名的WHOIS刷新请求"""
    try:
        data = request.get_json()
        domain = data.get('domain')
        
        if not domain:
            return jsonify({
                'success': False,
                'error': '请提供域名'
            }), 400
            
        # 从缓存中移除该域名
        if domain in WHOIS_CACHE:
            del WHOIS_CACHE[domain]
            
        # 重新查询
        whois_info = get_whois_info(domain)
        
        # 更新缓存
        if whois_info['success']:
            WHOIS_CACHE[domain] = (time.time(), whois_info)
            save_cache()
            
        return jsonify({
            'success': True,
            'whois': whois_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Domain Generator Service')
    parser.add_argument('--web', action='store_true', help='Run web server')
    args = parser.parse_args()

    if args.web:
        app.run(host='0.0.0.0', port=5000)
    else:
        print("Please use --web flag to run web server") 