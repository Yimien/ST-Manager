"""Preset storage helpers."""

import json
import os

from core.utils.filesystem import sanitize_filename
from core.utils.source_revision import build_file_source_revision


class PresetConflictError(Exception):
    """Raised when source_revision does not match current file."""


def require_matching_revision(file_path, source_revision):
    current_revision = build_file_source_revision(file_path)
    if not source_revision:
        raise PresetConflictError(current_revision)
    if current_revision and source_revision != current_revision:
        raise PresetConflictError(current_revision)
    return current_revision


def write_preset_json(file_path, payload):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return build_file_source_revision(file_path)


def load_preset_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_save_as_path(base_dir, name):
    safe_name = sanitize_filename(name or '').strip() or 'preset'
    return os.path.join(base_dir, f'{safe_name}.json')


def ensure_unique_path(file_path):
    if not os.path.exists(file_path):
        return file_path

    base, ext = os.path.splitext(file_path)
    counter = 1
    candidate = file_path
    while os.path.exists(candidate):
        candidate = f'{base}_{counter}{ext}'
        counter += 1
    return candidate


def build_renamed_path(file_path, new_name):
    safe_name = sanitize_filename(new_name or '').strip() or 'preset'
    parent_dir = os.path.dirname(file_path)
    return os.path.join(parent_dir, f'{safe_name}.json')
