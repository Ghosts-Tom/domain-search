import random
import string
import itertools
from typing import List, Tuple, Optional
import pypinyin

class DomainGenerator:
    def __init__(self):
        # 预定义的字典（可以根据需要扩展）
        self.dictionary = [
            'web', 'app', 'site', 'online', 'digital', 'tech', 'cloud', 'data',
            'smart', 'global', 'world', 'info', 'pro', 'plus', 'hub', 'zone'
        ]
        
        # 常用字符集
        self.charsets = {
            'ascii': string.ascii_lowercase,
            'digits': string.digits,
            'alphanumeric': string.ascii_lowercase + string.digits
        }

        self.consonants = 'bcdfghjklmnpqrstvwxz'
        self.vowels = 'aeiou'
        self.numbers = '0123456789'
        
        # 拼音声母映射
        self.pinyin_initials = {
            'zh': 'zh', 'ch': 'ch', 'sh': 'sh',
            'ng': 'n', 'r': 'r', 'y': 'y', 'w': 'w'
        }

    def _is_pinyin(self, word: str) -> bool:
        """检查是否为拼音输入"""
        # 检查是否包含声调
        tones = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'
        if any(char in tones for char in word):
            return True
            
        # 检查是否包含拼音声母
        pinyin_initial = word[:2]
        if pinyin_initial in self.pinyin_initials:
            return True
            
        # 检查是否包含韵母
        vowels = 'aeiouü'
        if any(char in vowels for char in word):
            return True
            
        return False

    def _get_pinyin_variations(self, word: str) -> List[str]:
        """获取拼音变体"""
        variations = set()
        
        # 如果是拼音输入，直接处理
        if self._is_pinyin(word):
            # 移除声调
            word = ''.join(char for char in word if char not in 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ')
            
            # 处理特殊声母
            for initial, replacement in self.pinyin_initials.items():
                if word.startswith(initial):
                    word = replacement + word[2:]
                    break
            
            # 添加完整拼音
            variations.add(word)
            
            # 添加首字母
            initials = ''.join(p[0] for p in pypinyin.lazy_pinyin(word))
            variations.add(initials)
            
            # 添加声母
            shengmu = ''.join(p[0] for p in pypinyin.lazy_pinyin(word) if p[0] in self.consonants)
            if shengmu:
                variations.add(shengmu)
                
            # 添加韵母
            yunmu = ''.join(p[1:] for p in pypinyin.lazy_pinyin(word) if len(p) > 1)
            if yunmu:
                variations.add(yunmu)
        
        return list(variations)
    
    def _generate_variations(self, word: str) -> List[str]:
        """生成关键词变体"""
        variations = set()
        
        # 添加原始词
        variations.add(word)
        
        # 如果是拼音输入，添加拼音变体
        if self._is_pinyin(word):
            # 移除声调
            word = ''.join(char for char in word if char not in 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ')
            
            # 处理特殊声母
            for initial, replacement in self.pinyin_initials.items():
                if word.startswith(initial):
                    word = replacement + word[2:]
                    break
            
            # 添加完整拼音
            variations.add(word)
            
            # 添加首字母缩写
            initials = ''.join(p[0] for p in pypinyin.lazy_pinyin(word))
            variations.add(initials)
        
        # 添加数字变体
        for i in range(10):
            variations.add(f"{word}{i}")
            variations.add(f"{i}{word}")
        
        # 添加常见后缀
        suffixes = ['app', 'web', 'site', 'net', 'tech', 'pro', 'plus', 'hub']
        for suffix in suffixes:
            variations.add(f"{word}{suffix}")
            variations.add(f"{suffix}{word}")
        
        # 添加常见前缀
        prefixes = ['my', 'get', 'go', 'try', 'use', 'buy', 'shop', 'find']
        for prefix in prefixes:
            variations.add(f"{prefix}{word}")
        
        return list(variations)

    def generate_domains(
        self,
        keywords: List[str] = None,
        length_range: Tuple[int, int] = None,
        tlds: List[str] = None
    ) -> List[str]:
        """生成域名"""
        if not keywords:
            keywords = ['web', 'app', 'site']
        if not length_range:
            length_range = (5, 10)
        if not tlds:
            tlds = ['.com', '.net', '.org']
            
        domains = set()
        min_length, max_length = length_range
        
        # 处理每个关键词
        for keyword in keywords:
            # 生成关键词变体
            variations = self._generate_variations(keyword)
            
            # 为每个变体生成域名
            for variation in variations:
                # 如果变体长度已经满足要求，直接添加后缀
                if min_length <= len(variation) <= max_length:
                    for tld in tlds:
                        domains.add(variation + tld)
                # 如果变体长度不足，添加随机字符
                elif len(variation) < min_length:
                    remaining_length = min_length - len(variation)
                    # 添加随机字符
                    random_chars = ''.join(random.choice(self.consonants + self.vowels + self.numbers) 
                                         for _ in range(remaining_length))
                    domain = variation + random_chars
                    if len(domain) <= max_length:
                        for tld in tlds:
                            domains.add(domain + tld)
        
        # 如果生成的域名太少，添加一些基于关键词的随机域名
        while len(domains) < 10:
            keyword = random.choice(keywords)
            length = random.randint(min_length, max_length)
            # 确保域名包含完整的关键词
            if len(keyword) < length:
                remaining_length = length - len(keyword)
                random_chars = ''.join(random.choice(self.consonants + self.vowels + self.numbers) 
                                     for _ in range(remaining_length))
                domain = keyword + random_chars
                for tld in tlds:
                    if min_length <= len(domain) <= max_length:
                        domains.add(domain + tld)
        
        return list(domains) 