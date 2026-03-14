#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论坛标签抓取功能测试
用于验证从类脑论坛HTML中解析标签的功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.automation.forum_tag_fetcher import NaobaijinTagParser, TagProcessor
from core.api.v1.cards import _normalize_tag_list

def test_tag_parser():
    """测试HTML标签解析器"""
    print("=" * 60)
    print("测试标签解析器")
    print("=" * 60)

    # 读取测试HTML文件
    html_files = [
        ('abc.html', '有侧边栏版本'),
        ('abc1.html', '无侧边栏版本')
    ]

    for filename, desc in html_files:
        if not os.path.exists(filename):
            print(f"[警告] 跳过 {desc}: 文件 {filename} 不存在")
            continue

        print(f"\n[测试] {desc} ({filename})")

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # 解析标签
            parser = NaobaijinTagParser()
            parser.feed(html_content)
            parser.close()

            print(f"   解析到 {len(parser.tags)} 个标签:")
            for i, tag in enumerate(parser.tags, 1):
                print(f"   {i}. {tag}")

            # 验证期望的标签
            expected_tags = ['调教', '系统/工具', '纯爱', '其他']
            found_expected = [tag for tag in expected_tags if tag in parser.tags]
            missing = [tag for tag in expected_tags if tag not in parser.tags]

            print(f"\n   [成功] 找到期望标签: {found_expected}")
            if missing:
                print(f"   [警告] 未找到标签: {missing}")

        except Exception as e:
            print(f"   [错误] 解析失败: {e}")

    print("\n" + "=" * 60)


def test_tag_processor():
    """测试标签处理器"""
    print("\n测试标签处理器")
    print("=" * 60)

    # 测试数据
    test_tags = ['调教', '系统/工具', '纯爱', '其他', '重复标签', '重复标签']

    print(f"\n原始标签: {test_tags}")

    # 测试1: 排除标签
    print("\n--- 测试排除标签 ---")
    processor1 = TagProcessor(exclude_tags=['其他'])
    result1 = processor1.process(test_tags)
    print(f"排除 '其他': {result1}")
    assert '其他' not in result1, "排除标签失败"
    print("[通过] 排除标签测试通过")

    # 测试2: 替换标签
    print("\n--- 测试替换标签 ---")
    processor2 = TagProcessor(replace_rules={'其他': '杂项', '调教': 'BDSM'})
    result2 = processor2.process(test_tags)
    print(f"替换 '其他'->'杂项', '调教'->'BDSM': {result2}")
    assert '杂项' in result2, "替换标签失败"
    assert 'BDSM' in result2, "替换标签失败"
    assert '其他' not in result2, "替换标签失败(原标签仍存在)"
    print("[通过] 替换标签测试通过")

    # 测试3: 综合处理
    print("\n--- 测试综合处理 ---")
    processor3 = TagProcessor(
        exclude_tags=['其他'],
        replace_rules={'调教': 'BDSM'}
    )
    result3 = processor3.process(test_tags)
    print(f"排除'其他' + 替换'调教'->'BDSM': {result3}")
    assert '其他' not in result3, "综合处理排除失败"
    assert 'BDSM' in result3, "综合处理替换失败"
    print("[通过] 综合处理测试通过")

    # 测试4: 合并模式
    print("\n--- 测试合并模式 ---")
    existing = ['现有标签1', '调教']
    new = ['新标签', '调教', '纯爱']

    processor4 = TagProcessor()

    merged = processor4.merge_tags(existing, new, mode='merge')
    print(f"合并模式 - 现有: {existing}, 新: {new}")
    print(f"结果: {merged}")
    assert '现有标签1' in merged, "合并失败(丢失现有标签)"
    assert '新标签' in merged, "合并失败(丢失新标签)"
    assert merged.count('调教') == 1, "合并失败(未去重)"
    print("[通过] 合并模式测试通过")

    replaced = processor4.merge_tags(existing, new, mode='replace')
    print(f"\n替换模式 - 现有: {existing}, 新: {new}")
    print(f"结果: {replaced}")
    assert replaced == list(new), "替换失败"
    assert '现有标签1' not in replaced, "替换失败(未清空)"
    print("[通过] 替换模式测试通过")

    print("\n" + "=" * 60)


def test_url_validation():
    """测试URL验证"""
    print("\n测试URL验证")
    print("=" * 60)

    from core.automation.forum_tag_fetcher import ForumTagFetcher

    fetcher = ForumTagFetcher()

    test_urls = [
        ('https://naobaijin.app/channels/xxx/yyy', True, '有效URL'),
        ('https://www.naobaijin.app/post/123', True, '带www的有效URL'),
        ('https://example.com/post/123', False, '无效域名'),
        ('', False, '空URL'),
        (None, False, 'None URL'),
        ('not-a-url', False, '非URL字符串'),
    ]

    for url, expected, desc in test_urls:
        result = fetcher.is_valid_naobaijin_url(url)
        status = "[OK]" if result == expected else "[FAIL]"
        print(f"{status} {desc}: {url} -> {'有效' if result else '无效'}")

    print("\n" + "=" * 60)

def test_normalize_tag_list_supports_newline_separated_string_tags():
    raw_tags = '中文人名版\nv1.1'

    assert _normalize_tag_list(raw_tags) == ['中文人名版', 'v1.1']


def test_normalize_tag_list_supports_mixed_separators_and_dedupes():
    raw_tags = 'alpha,beta\nalpha，gamma'

    assert _normalize_tag_list(raw_tags) == ['alpha', 'beta', 'gamma']


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("论坛标签抓取功能测试套件")
    print("=" * 60 + "\n")
    
    # 运行测试
    test_tag_parser()
    test_tag_processor()
    test_url_validation()
    
    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60 + "\n")
