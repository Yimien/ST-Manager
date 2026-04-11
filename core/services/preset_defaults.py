"""Default preset lookup helpers."""

import json
import os

from core.services.st_client import STClient


DEFAULT_KIND_DIRS = {
    'textgen': ['TextGen', 'textgen'],
    'instruct': ['Instruct', 'instruct'],
    'context': ['Context', 'context'],
    'sysprompt': ['Sysprompt', 'sysprompt'],
    'reasoning': ['Reasoning', 'reasoning'],
}

DEFAULT_CONTENT_TYPES = {
    'textgen': 'textgen_preset',
    'instruct': 'instruct',
    'context': 'context',
    'sysprompt': 'sysprompt',
    'reasoning': 'reasoning',
}


def _load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _load_from_content_index(st_root, preset_kind, filename):
    if not st_root:
        return None, ''

    index_path = os.path.join(st_root, 'default', 'content', 'index.json')
    if not os.path.exists(index_path):
        return None, ''

    content_type = DEFAULT_CONTENT_TYPES.get(preset_kind)
    target_name = os.path.basename(filename or '')
    try:
        items = _load_json(index_path)
    except Exception:
        return None, ''

    for item in items:
        if item.get('type') != content_type:
            continue
        item_filename = str(item.get('filename') or '').replace('\\', '/')
        if os.path.basename(item_filename) != target_name:
            continue
        full_path = os.path.join(st_root, 'default', 'content', item_filename)
        if os.path.exists(full_path):
            return _load_json(full_path), full_path
    return None, ''


def load_default_preset_content(preset_kind, filename):
    st_client = STClient()
    presets_root = st_client.get_presets_dir()
    if presets_root:
        for subdir in DEFAULT_KIND_DIRS.get(preset_kind, []):
            candidate = os.path.join(presets_root, subdir, filename)
            if os.path.exists(candidate):
                return _load_json(candidate), candidate

    st_root = getattr(st_client, 'st_data_dir', '') or st_client.detect_st_path()
    content_data, content_path = _load_from_content_index(st_root, preset_kind, filename)
    if content_path:
        return content_data, content_path

    raise FileNotFoundError('默认模板不存在')
