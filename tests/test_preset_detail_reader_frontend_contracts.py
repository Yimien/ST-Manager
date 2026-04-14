import re

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def test_preset_detail_reader_js_exposes_reader_view_state_and_helpers_contracts():
    source = read_project_file('static/js/components/presetDetailReader.js')

    assert 'activeGroup:' in source
    assert 'activeItemId:' in source
    assert 'searchTerm:' in source
    assert 'uiFilter:' in source
    assert 'showRightPanel:' in source
    assert 'showMobileSidebar:' in source

    assert 'get readerView() {' in source
    assert 'get readerGroups() {' in source
    assert 'get readerItems() {' in source
    assert 'get filteredItems() {' in source
    assert 'get activeItem() {' in source
    assert 'get readerStats() {' in source

    assert 'selectGroup(groupId) {' in source
    assert 'selectItem(itemId) {' in source
    assert 'getItemValuePreview(item) {' in source
    assert 'getItemFullDetail(item) {' in source
    assert 'getItemBadge(item) {' in source
    assert 'formatItemPayload(item) {' not in source


def test_preset_detail_reader_js_search_haystack_includes_prompt_identifier():
    source = read_project_file('static/js/components/presetDetailReader.js')

    assert 'item.payload?.identifier' in source


def test_preset_detail_reader_template_uses_reader_view_three_column_layout_contracts():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert 'x-model="searchTerm"' in source
    assert '@click="selectGroup(group.id)"' in source
    assert 'x-for="item in filteredItems"' in source
    assert '@click="selectItem(item.id)"' in source
    assert 'x-show="showRightPanel || $store.global.deviceType !== ' in source
    assert 'x-text="activeItem?.title ||' in source
    assert 'readerStats.prompt_count' not in source
    assert 'readerStats.unknown_count' not in source


def test_preset_detail_reader_template_removes_prompt_order_unknown_and_metadata_sections():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert 'Payload' not in source
    assert 'Revision' not in source
    assert '保存能力' not in source
    assert 'x-if="activeItem?.type === \'prompt_order\'"' not in source
    assert "x-if=\"activeItem?.group === 'unknown_fields' || activeItem?.type === 'unknown_field'\"" not in source


def test_preset_detail_reader_flow_keeps_full_content_in_right_panel_only():
    js_source = read_project_file('static/js/components/presetDetailReader.js')
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert 'line-clamp-3' in source or 'line-clamp-4' in source
    assert 'getItemDetailContent(' not in js_source
    assert 'getItemFullDetail(item) {' in js_source
    assert 'x-text="getItemFullDetail(activeItem)"' in source
    assert 'Summary' not in source
    assert 'Prompt Detail' not in source


def test_preset_detail_reader_template_guards_active_item_accesses():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert 'x-if="activeItem?.type === \'prompt_order\'"' not in source
    assert 'x-if="activeItem?.type === \'extension\'"' in source
    assert 'x-if="activeItem?.type === \'field\'"' in source
    assert 'x-if="activeItem?.type === \'structured\'"' in source
    assert "x-if=\"activeItem?.group === 'unknown_fields' || activeItem?.type === 'unknown_field'\"" not in source


def test_preset_detail_reader_template_removes_invalid_raw_json_and_restore_default_actions():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert not re.search(r'<button\s+@click="openRawViewer\(\)"[\s\S]*?>[\s\S]*?查看原始 JSON[\s\S]*?</button>', source)
    assert not re.search(r'<button\s+@click="previewRestoreDefault\(\)"[\s\S]*?>[\s\S]*?恢复默认[\s\S]*?</button>', source)
