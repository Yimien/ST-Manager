#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证HTML文件中的标签
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from core.automation.forum_tag_fetcher import NaobaijinTagParser

def check_html_file(filename):
    print(f"\n{'='*60}")
    print(f"检查文件: {filename}")
    print('='*60)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 方法1: 使用解析器
        parser = NaobaijinTagParser()
        parser.feed(html)
        parser.close()
        
        print(f"\n解析器结果 ({len(parser.tags)} 个标签):")
        for i, tag in enumerate(parser.tags, 1):
            print(f"  {i}. {tag}")
        
        # 方法2: 正则提取所有pill内容
        print(f"\n正则提取前20个pill内容:")
        pattern = r'<div[^>]*class="[^"]*pill_a2c9e8[^"]*"[^>]*>[\s\S]*?<div[^>]*class="[^"]*lineClamp1[^"]*"[^>]*>([^<]+)</div>'
        matches = re.findall(pattern, html)
        for i, tag in enumerate(matches[:20], 1):
            tag_clean = tag.strip()
            if tag_clean:
                print(f"  {i}. {tag_clean}")
        
        # 查找标题
        title_match = re.search(r'<title>.*?Discord \| "([^"]+)"', html)
        if title_match:
            print(f"\n页面标题: {title_match.group(1)}")
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == '__main__':
    files = ['abc.html', 'abc1.html', '123.html', '456.html']
    for f in files:
        check_html_file(f)
    
    print("\n" + "="*60)
    print("检查完成")
    print("="*60)
