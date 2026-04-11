"""Preset detail model helpers."""

import copy
import os

from core.utils.source_revision import build_file_source_revision


PRESET_KIND_LABELS = {
    'textgen': '文本生成预设',
    'instruct': '指令模板',
    'context': '上下文模板',
    'sysprompt': '系统提示词',
    'reasoning': '思维链模板',
}


COMMON_FIELD_KEYS = {
    'name',
    'title',
    'description',
    'note',
    'extensions',
    'prompts',
    'prompt_order',
}


FIELD_ALIAS_MAP = {}


SECTION_DEFINITIONS = {
    'textgen': {
        'sampling': [
            {'key': 'temp', 'aliases': ['temperature'], 'label': '温度'},
            {'key': 'top_p', 'aliases': [], 'label': 'Top P'},
            {'key': 'top_k', 'aliases': [], 'label': 'Top K'},
            {'key': 'top_a', 'aliases': [], 'label': 'Top A'},
            {'key': 'min_p', 'aliases': [], 'label': 'Min P'},
            {'key': 'typical_p', 'aliases': ['typical'], 'label': 'Typical P'},
            {'key': 'tfs', 'aliases': [], 'label': 'TFS'},
            {'key': 'temperature_last', 'aliases': [], 'label': 'Temperature Last'},
        ],
        'penalties': [
            {'key': 'repetition_penalty', 'aliases': ['rep_pen'], 'label': '重复惩罚'},
            {'key': 'repetition_penalty_range', 'aliases': [], 'label': '重复范围'},
            {'key': 'repetition_penalty_decay', 'aliases': [], 'label': '重复衰减'},
            {'key': 'frequency_penalty', 'aliases': ['freq_pen'], 'label': '频率惩罚'},
            {'key': 'presence_penalty', 'aliases': ['pres_pen'], 'label': '存在惩罚'},
            {'key': 'no_repeat_ngram_size', 'aliases': [], 'label': 'No Repeat Ngram'},
        ],
        'length_and_output': [
            {'key': 'max_tokens', 'aliases': ['openai_max_tokens', 'max_length'], 'label': '最大生成长度'},
            {'key': 'min_length', 'aliases': [], 'label': '最小长度'},
            {'key': 'num_beams', 'aliases': [], 'label': 'Beam 数'},
            {'key': 'length_penalty', 'aliases': [], 'label': 'Length Penalty'},
            {'key': 'do_sample', 'aliases': [], 'label': 'Do Sample'},
            {'key': 'early_stopping', 'aliases': [], 'label': 'Early Stopping'},
        ],
        'dynamic_temperature': [
            {'key': 'dynamic_temperature', 'aliases': [], 'label': '动态温度'},
            {'key': 'dynatemp_low', 'aliases': [], 'label': '动态温度下限'},
            {'key': 'dynatemp_high', 'aliases': [], 'label': '动态温度上限'},
        ],
        'mirostat': [
            {'key': 'mirostat_mode', 'aliases': [], 'label': 'Mirostat 模式'},
            {'key': 'mirostat_tau', 'aliases': [], 'label': 'Mirostat Tau'},
            {'key': 'mirostat_eta', 'aliases': [], 'label': 'Mirostat Eta'},
        ],
        'guidance': [
            {'key': 'guidance_scale', 'aliases': [], 'label': 'Guidance Scale'},
            {'key': 'negative_prompt', 'aliases': [], 'label': 'Negative Prompt'},
        ],
        'formatting': [
            {'key': 'stream_openai', 'aliases': [], 'label': '流式输出'},
            {'key': 'wrap_in_quotes', 'aliases': [], 'label': '包裹引号'},
            {'key': 'show_thoughts', 'aliases': [], 'label': '显示思维链'},
        ],
        'schema_and_grammar': [
            {'key': 'json_schema', 'aliases': [], 'label': 'JSON Schema'},
            {'key': 'grammar', 'aliases': [], 'label': 'Grammar'},
        ],
        'bans_and_bias': [
            {'key': 'banned_tokens', 'aliases': [], 'label': '禁词'},
            {'key': 'logit_bias', 'aliases': [], 'label': 'Logit Bias'},
        ],
        'sampler_ordering': [
            {'key': 'sampler_order', 'aliases': [], 'label': 'Sampler Order'},
            {'key': 'samplers', 'aliases': [], 'label': 'Sampler Priority'},
        ],
    },
    'instruct': {
        'sequences': [
            {'key': 'input_sequence', 'aliases': [], 'label': '输入序列'},
            {'key': 'output_sequence', 'aliases': [], 'label': '输出序列'},
            {'key': 'system_sequence', 'aliases': [], 'label': '系统序列'},
            {'key': 'first_output_sequence', 'aliases': [], 'label': '首输出序列'},
            {'key': 'last_output_sequence', 'aliases': [], 'label': '尾输出序列'},
            {'key': 'stop_sequence', 'aliases': ['stop_sequences'], 'label': '停止序列'},
        ],
        'wrapping_and_behavior': [
            {'key': 'wrap', 'aliases': [], 'label': '包装与宏'},
            {'key': 'macro', 'aliases': [], 'label': '宏'},
            {'key': 'names_behavior', 'aliases': [], 'label': '名称行为'},
            {'key': 'skip_examples', 'aliases': [], 'label': '跳过示例'},
        ],
        'activation': [
            {'key': 'activation_regex', 'aliases': [], 'label': '激活正则'},
        ],
        'compatibility': [
            {'key': 'system_same_as_user', 'aliases': [], 'label': 'system same as user'},
            {'key': 'last_system_sequence', 'aliases': [], 'label': '尾系统序列'},
            {'key': 'system_sequence_prefix', 'aliases': [], 'label': '系统前缀'},
            {'key': 'sequences_as_stop_strings', 'aliases': [], 'label': '序列作为停止词'},
        ],
    },
    'context': {
        'story': [
            {'key': 'story_string', 'aliases': [], 'label': 'Story String'},
            {'key': 'example_separator', 'aliases': [], 'label': 'Example Separator'},
            {'key': 'chat_start', 'aliases': [], 'label': 'Chat Start'},
        ],
        'separator_and_chat': [
            {'key': 'use_stop_strings', 'aliases': [], 'label': '使用 Stop Strings'},
            {'key': 'names_as_stop_strings', 'aliases': [], 'label': '名称作为 Stop Strings'},
        ],
        'insertion_behavior': [
            {'key': 'injection_depth', 'aliases': ['depth'], 'label': '插入深度'},
            {'key': 'insertion_position', 'aliases': ['position'], 'label': '插入位置'},
            {'key': 'injection_role', 'aliases': ['role'], 'label': '插入角色'},
        ],
        'formatting_behavior': [
            {'key': 'always_force_name2', 'aliases': [], 'label': 'always_force_name2'},
            {'key': 'trim_sentences', 'aliases': [], 'label': 'trim_sentences'},
            {'key': 'single_line', 'aliases': [], 'label': 'single_line'},
        ],
        'compatibility': [
            {'key': 'conversation_separator', 'aliases': [], 'label': '兼容分隔符'},
        ],
    },
    'sysprompt': {
        'prompt': [
            {'key': 'content', 'aliases': [], 'label': '主提示词内容'},
        ],
        'placement': [
            {'key': 'post_history', 'aliases': [], 'label': '后置到历史后'},
        ],
    },
    'reasoning': {
        'template': [
            {'key': 'prefix', 'aliases': [], 'label': '前缀'},
            {'key': 'suffix', 'aliases': [], 'label': '后缀'},
            {'key': 'separator', 'aliases': [], 'label': '分隔符'},
        ],
        'runtime_notes': [
            {'key': 'note', 'aliases': [], 'label': '运行态说明'},
        ],
    },
}

for _kind_sections in SECTION_DEFINITIONS.values():
    for _field_defs in _kind_sections.values():
        for _field_def in _field_defs:
            FIELD_ALIAS_MAP[_field_def['key']] = [_field_def['key'], *_field_def.get('aliases', [])]


def detect_preset_kind(raw_data, source_folder='', file_path=''):
    folder = str(source_folder or '').replace('\\', '/').lower()
    file_hint = str(file_path or '').replace('\\', '/').lower()
    combined = f'{folder} {file_hint}'

    if 'sysprompt' in combined:
        return 'sysprompt'
    if 'reasoning' in combined:
        return 'reasoning'
    if 'context' in combined:
        return 'context'
    if 'instruct' in combined:
        return 'instruct'
    if 'textgen' in combined:
        return 'textgen'

    data = raw_data or {}
    if 'content' in data and 'post_history' in data:
        return 'sysprompt'
    if all(key in data for key in ('prefix', 'suffix', 'separator')):
        return 'reasoning'
    if 'story_string' in data and 'chat_start' in data:
        return 'context'
    if any(key in data for key in ('input_sequence', 'output_sequence', 'system_sequence')):
        return 'instruct'
    return 'textgen'


def _resolve_field(data, field_def):
    candidates = [field_def['key'], *field_def.get('aliases', [])]
    for source_key in candidates:
        if source_key in data:
            return source_key, data.get(source_key)
    return None, None


def build_sections(raw_data, preset_kind):
    data = raw_data or {}
    definitions = SECTION_DEFINITIONS.get(preset_kind, {})
    sections = {}
    consumed_keys = set(COMMON_FIELD_KEYS)

    for section_name, field_defs in definitions.items():
        items = []
        for field_def in field_defs:
            source_key, value = _resolve_field(data, field_def)
            if source_key is None:
                continue
            consumed_keys.add(source_key)
            items.append({
                'key': field_def['key'],
                'source_key': source_key,
                'label': field_def['label'],
                'value': value,
            })
        if items:
            sections[section_name] = items

    unknown_fields = sorted(key for key in data.keys() if key not in consumed_keys)
    return sections, unknown_fields


def build_capabilities(source_type, preset_kind):
    return {
        'can_save': True,
        'can_save_as': True,
        'can_rename': True,
        'can_delete': True,
        'can_restore_default': source_type == 'global' and preset_kind in PRESET_KIND_LABELS,
    }


def build_preset_detail(*, preset_id, file_path, filename, source_type, source_folder, raw_data, base_dir):
    preset_kind = detect_preset_kind(raw_data, source_folder=source_folder, file_path=file_path)
    sections, unknown_fields = build_sections(raw_data, preset_kind)

    try:
        mtime = os.path.getmtime(file_path)
    except OSError:
        mtime = 0
    try:
        file_size = os.path.getsize(file_path)
    except OSError:
        file_size = 0

    rel_path = file_path
    try:
        rel_path = os.path.relpath(file_path, base_dir)
    except Exception:
        pass

    return {
        'id': preset_id,
        'name': raw_data.get('name') or raw_data.get('title') or os.path.splitext(filename)[0],
        'filename': filename,
        'path': rel_path,
        'file_path': file_path,
        'source_folder': source_folder,
        'file_size': file_size,
        'mtime': mtime,
        'type': source_type,
        'preset_kind': preset_kind,
        'preset_kind_label': PRESET_KIND_LABELS[preset_kind],
        'capabilities': build_capabilities(source_type, preset_kind),
        'source_revision': build_file_source_revision(file_path),
        'is_default_candidate': source_type == 'global',
        'has_unknown_fields': bool(unknown_fields),
        'unknown_fields': unknown_fields,
        'raw_data': copy.deepcopy(raw_data or {}),
        'sections': sections,
        'extensions': copy.deepcopy((raw_data or {}).get('extensions') or {}),
    }


def merge_preset_content(raw_data, preset_kind, content):
    merged = copy.deepcopy(raw_data or {})
    content = copy.deepcopy(content or {})

    for canonical_key, aliases in FIELD_ALIAS_MAP.items():
        if canonical_key not in content:
            continue
        for alias in aliases[1:]:
            if alias in merged and alias != canonical_key:
                merged.pop(alias, None)
        merged[canonical_key] = content[canonical_key]

    for key, value in content.items():
        if key == 'extensions':
            continue
        merged[key] = value

    if 'extensions' in raw_data or 'extensions' in content:
        merged['extensions'] = copy.deepcopy(
            (raw_data or {}).get('extensions') if 'extensions' not in content else content.get('extensions')
        ) or {}

    return merged
