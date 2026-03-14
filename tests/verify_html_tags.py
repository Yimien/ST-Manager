#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.automation.forum_tag_fetcher import NaobaijinTagParser

# Test with UTF-8 output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_file(filename, expected_count):
    print(f"\n{'='*60}")
    print(f"测试: {filename}")
    print(f"期望标签数: {expected_count}")
    print('='*60)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
        
        parser = NaobaijinTagParser()
        parser.feed(html)
        parser.close()
        
        actual_count = len(parser.tags)
        status = "✓ PASS" if actual_count == expected_count else "✗ FAIL"
        
        print(f"实际标签数: {actual_count} {status}")
        print(f"标签列表:")
        for i, tag in enumerate(parser.tags, 1):
            print(f"  {i}. {tag}")
        
        return actual_count == expected_count
        
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == '__main__':
    results = []
    
    # 测试文件：(文件名, 期望标签数)
    test_cases = [
        ('abc.html', 4),    # 调教、系统/工具、纯爱、其他
        ('abc1.html', 4),   # 调教、系统/工具、纯爱、其他
        ('123.html', 3),    # 纯文字、多路线、其他
        ('456.html', 3),    # 纯文字、多路线、其他
    ]
    
    for filename, expected in test_cases:
        results.append(test_file(filename, expected))
    
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    for i, (filename, expected) in enumerate(test_cases):
        status = "✓ 通过" if results[i] else "✗ 失败"
        print(f"{filename}: {status} (期望{expected}个标签)")
    
    all_passed = all(results)
    print(f"\n总体: {'✓ 全部通过' if all_passed else '✗ 有失败'}")
    print("="*60)
