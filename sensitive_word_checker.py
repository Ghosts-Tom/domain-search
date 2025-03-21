from typing import List, Dict, Set

class SensitiveWordChecker:
    def __init__(self):
        # 预定义的敏感词分类
        self.sensitive_words: Dict[str, Set[str]] = {
            'illegal': {
                'gambling', 'betting', 'casino', 'lottery', 'porn', 'xxx',
                'drugs', 'weapon', 'hack', 'crack', 'warez'
            },
            'political': {
                'government', 'political', 'party', 'leader', 'president',
                'minister', 'official', 'authority'
            },
            'religious': {
                'religion', 'church', 'temple', 'mosque', 'buddha',
                'christian', 'muslim', 'jewish'
            },
            'commercial': {
                'trademark', 'copyright', 'patent', 'brand', 'logo',
                'registered', 'official'
            }
        }

    def load_sensitive_words(self, category: str, words: List[str]) -> None:
        """加载自定义敏感词"""
        if category not in self.sensitive_words:
            self.sensitive_words[category] = set()
        self.sensitive_words[category].update(words)

    def exact_match(self, domain: str) -> List[str]:
        """精确匹配检测"""
        found_words = []
        domain = domain.lower()
        
        # 检查所有分类中的敏感词
        for category, words in self.sensitive_words.items():
            for word in words:
                if word.lower() in domain:
                    found_words.append(word)
        
        return found_words

    def check_domain(self, domain: str) -> Dict:
        """检查单个域名"""
        # 移除TLD
        domain_name = domain.split('.')[0]
        
        # 进行检测
        sensitive_words = self.exact_match(domain_name)
        
        return {
            'domain': domain,
            'sensitive_words': sensitive_words,
            'is_safe': len(sensitive_words) == 0
        }

    def check_domains(self, domains: List[str]) -> List[Dict]:
        """批量检查域名"""
        results = []
        for domain in domains:
            result = self.check_domain(domain)
            results.append(result)
        return results

    def get_statistics(self, results: List[Dict]) -> Dict:
        """获取检测结果统计信息"""
        total_domains = len(results)
        safe_domains = sum(1 for r in results if r['is_safe'])
        unsafe_domains = total_domains - safe_domains
        
        # 统计各类敏感词出现次数
        word_frequency = {}
        for result in results:
            for word in result['sensitive_words']:
                word_frequency[word] = word_frequency.get(word, 0) + 1
        
        return {
            'total_domains': total_domains,
            'safe_domains': safe_domains,
            'unsafe_domains': unsafe_domains,
            'word_frequency': word_frequency
        } 