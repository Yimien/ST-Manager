#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.automation.forum_tag_fetcher import NaobaijinTagParser
import re

class DebugParser(NaobaijinTagParser):
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'div':
            class_attr = attrs_dict.get('class', '')
            if re.search(r'tags_[a-z0-9_]+', class_attr):
                print(f"[START] Found tags container: {class_attr[:50]}")
                print(f"  found_first_tags={self.found_first_tags}, in_tags_container={self.in_tags_container}")
        super().handle_starttag(tag, attrs)
    
    def handle_endtag(self, tag):
        if tag == 'div' and self.in_tags_container:
            print(f"[END] Closing tags container, depth={self.tags_container_depth}, tags={self.tags}")
        super().handle_endtag(tag)

with open('abc.html', 'r', encoding='utf-8') as f:
    html = f.read()

parser = DebugParser()
parser.feed(html)
parser.close()
print(f"\nFinal tags: {parser.tags}")
