import whois
import socket
import time

def test_whois(domain):
    print(f"\n测试域名: {domain}")
    try:
        # 设置socket超时
        socket.setdefaulttimeout(5)
        print("开始查询...")
        start_time = time.time()
        
        w = whois.whois(domain)
        
        end_time = time.time()
        print(f"查询耗时: {end_time - start_time:.2f}秒")
        
        print("\n查询结果:")
        print(f"注册商: {w.registrar}")
        print(f"创建日期: {w.creation_date}")
        print(f"过期日期: {w.expiration_date}")
        print(f"状态: {w.status}")
        print(f"原始文本: {w.text[:200]}...")  # 只显示前200个字符
        
    except socket.timeout:
        print("查询超时")
    except Exception as e:
        print(f"查询出错: {str(e)}")

if __name__ == "__main__":
    # 测试一些知名域名
    test_domains = [
        "google.com",
        "github.com",
        "example.com",
        "test123456789.com"  # 一个不存在的域名
    ]
    
    for domain in test_domains:
        test_whois(domain)
        time.sleep(2)  # 等待2秒再查询下一个 