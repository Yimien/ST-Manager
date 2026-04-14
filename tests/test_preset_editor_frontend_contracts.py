import json
import re
import subprocess
import textwrap
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def run_preset_editor_runtime_check(script_body):
    source_path = PROJECT_ROOT / 'static/js/components/presetEditor.js'
    node_script = textwrap.dedent(
        f"""
        import {{ readFileSync }} from 'node:fs';

        const sourcePath = {json.dumps(str(source_path))};
        let source = readFileSync(sourcePath, 'utf8');
        source = source.replace(/^import[\\s\\S]*?;\\r?\\n/gm, '');
        source = source.replace('export default function presetEditor()', 'function presetEditor()');

        const stubs = `
        const createAutoSaver = () => ({{ stop() {{}}, initBaseline() {{}}, start() {{}} }});
        const apiCreateSnapshot = async () => ({{ success: true }});
        const getPresetDetail = async () => ({{ success: true, preset: {{}} }});
        const savePreset = async () => ({{ success: true }});
        const apiSavePresetExtensions = async () => ({{ success: true }});
        const estimateTokens = () => 0;
        const formatDate = (value) => value;
        const clearActiveRuntimeContext = () => {{}};
        const setActiveRuntimeContext = () => {{}};
        `;

        const module = await import(
          'data:text/javascript,' + encodeURIComponent(stubs + source + '\\nexport default presetEditor;'),
        );
        const editor = module.default();

        {textwrap.dedent(script_body)}
        """
    )
    result = subprocess.run(
        ['node', '--input-type=module', '-e', node_script],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_preset_editor_js_exposes_reader_item_workspace_state():
    source = read_project_file('static/js/components/presetEditor.js')

    assert 'activeGroup:' in source
    assert 'activeItemId:' in source
    assert 'searchTerm:' in source
    assert 'uiFilter:' in source
    assert 'showMobileSidebar:' in source
    assert 'showRightPanel:' in source
    assert 'get editorView() {' in source
    assert 'get filteredItems() {' in source
    assert 'get activeItem() {' in source
    assert 'getByPath(path) {' in source
    assert 'setByPath(path, value) {' in source


def test_preset_editor_js_exposes_complex_editor_handlers():
    source = read_project_file('static/js/components/presetEditor.js')

    assert 'updatePromptItem(index, key, value) {' not in source
    assert 'addPromptItem() {' not in source
    assert 'removePromptItem(index) {' not in source
    assert 'moveListItem(path, fromIndex, toIndex) {' in source
    assert 'addStringListItem(path) {' in source
    assert 'updateStringListItem(path, index, value) {' in source
    assert 'removeStringListItem(path, index) {' in source
    assert 'updateBiasEntry(index, key, value) {' in source
    assert 'openAdvancedExtensions() {' in source
    assert 'deletePreset() {' in source
    assert 'rawUnknownJsonText' not in source
    assert 'applyRawUnknownJson(text) {' not in source
    assert 'removedUnknownFields' not in source
    assert 'previewRestoreDefault() {' not in source


def test_preset_editor_template_removes_prompt_and_unknown_raw_editor_sections():
    source = read_project_file('templates/modals/detail_preset_fullscreen.html')
    js_source = read_project_file('static/js/components/presetEditor.js')

    assert not re.search(r'<button\s+@click="openRawEditor\(\)"[\s\S]*?>[\s\S]*?查看原始 JSON[\s\S]*?</button>', source)
    assert not re.search(r'<button\s+@click="previewRestoreDefault\(\)"[\s\S]*?>[\s\S]*?恢复默认[\s\S]*?</button>', source)
    assert 'openRawEditor() {' not in js_source
    assert "activeItem?.editor?.kind === 'prompt-item'" not in source
    assert '未知字段检查器' not in source
    assert '高级原始编辑区' not in source
    assert '@click="applyRawUnknownJson(rawUnknownDraft)"' not in source
    assert 'rawUnknownJsonText' not in js_source
    assert 'applyRawUnknownJson(text) {' not in js_source


def test_preset_editor_runtime_rejects_invalid_bias_numbers():
    run_preset_editor_runtime_check(
        """
        editor.editingData = {
          logit_bias: [{ text: 'blocked', value: -10 }],
        };

        editor.updateBiasEntry(0, 'value', '2.5');
        if (editor.editingData.logit_bias[0].value !== 2.5) {
          throw new Error(`expected numeric bias update, got ${JSON.stringify(editor.editingData.logit_bias[0])}`);
        }

        editor.updateBiasEntry(0, 'value', 'not-a-number');
        if (editor.editingData.logit_bias[0].value !== 0) {
          throw new Error(`expected invalid bias value to fall back to 0, got ${JSON.stringify(editor.editingData.logit_bias[0])}`);
        }
        """
    )


def test_preset_editor_runtime_updates_and_removes_string_list_entries_by_path():
    run_preset_editor_runtime_check(
        """
        editor.editingData = {
          stop_sequence: ['alpha', 'beta', 'gamma'],
        };

        editor.updateStringListItem('stop_sequence', 1, 'BETA');
        if (JSON.stringify(editor.editingData.stop_sequence) !== JSON.stringify(['alpha', 'BETA', 'gamma'])) {
          throw new Error(`expected string list update by path, got ${JSON.stringify(editor.editingData.stop_sequence)}`);
        }

        editor.removeStringListItem('stop_sequence', 0);
        if (JSON.stringify(editor.editingData.stop_sequence) !== JSON.stringify(['BETA', 'gamma'])) {
          throw new Error(`expected string list removal by path, got ${JSON.stringify(editor.editingData.stop_sequence)}`);
        }
        """
    )


def test_preset_editor_js_tracks_changed_state_and_safe_nested_path_writes():
    source = read_project_file('static/js/components/presetEditor.js')

    assert 'isItemDirty(item) {' in source
    assert 'return [item.value_path, item.source_key, item.key, item.id].some(' in source
    assert 'if (target[part] === null || typeof target[part] !== "object") {' in source
    assert 'markAllReaderItemsDirty() {' in source
    assert 'this.markAllReaderItemsDirty();' in source


def test_preset_editor_template_uses_three_column_workspace_contracts():
    source = read_project_file('templates/modals/detail_preset_fullscreen.html')

    assert 'x-model="searchTerm"' in source
    assert '@click="selectGroup(group.id)"' in source
    assert 'x-for="item in filteredItems"' in source
    assert '@click="selectItem(item.id)"' in source
    assert 'x-text="activeItem?.title ||' in source
    assert 'x-show="showRightPanel || $store.global.deviceType !== ' in source
    assert 'x-show="uiFilter ===' in source or 'uiFilter' in source


def test_preset_editor_template_routes_scalar_editors_through_field_helpers():
    source = read_project_file('templates/modals/detail_preset_fullscreen.html')

    assert ':value="getFieldValue(activeItem) || \'' in source
    assert '@input="setFieldValue(activeItem, $event.target.value)"' in source
    assert ':checked="Boolean(getFieldValue(activeItem))"' in source
    assert '@change="setFieldValue(activeItem, $event.target.checked)"' in source
    assert ':value="getFieldValue(activeItem) ?? 0"' in source
    assert '@input="setFieldValue(activeItem, Number($event.target.value))"' in source
    assert 'x-text="formatValue(getFieldValue(activeItem))"' in source
    assert ':value="getByPath(activeItem.value_path) || \'' not in source
    assert '@input="setByPath(activeItem.value_path, $event.target.value)"' not in source
    assert ':checked="Boolean(getByPath(activeItem.value_path))"' not in source
    assert '@change="setByPath(activeItem.value_path, $event.target.checked)"' not in source
    assert ':value="getByPath(activeItem.value_path) ?? 0"' not in source
    assert '@input="setByPath(activeItem.value_path, Number($event.target.value))"' not in source
    assert 'x-text="formatValue(getByPath(activeItem?.value_path))"' not in source


def test_preset_editor_template_keeps_right_info_toggle_mobile_only():
    source = read_project_file('templates/modals/detail_preset_fullscreen.html')

    assert re.search(
        r'<button\s+@click="showRightPanel = !showRightPanel"\s+class="btn-secondary px-3 py-1.5 text-xs rounded md:hidden"\s*>\s*右侧信息\s*</button>',
        source,
    )
    assert not re.search(
        r'<button\s+@click="showRightPanel = !showRightPanel"\s+class="btn-secondary px-3 py-1.5 text-xs rounded"\s*>\s*右侧信息\s*</button>',
        source,
    )


def test_preset_editor_template_exposes_specialized_editor_sections():
    source = read_project_file('templates/modals/detail_preset_fullscreen.html')

    assert (
        "item.editor?.kind === 'prompt-item'" not in source
        and "activeItem?.editor?.kind === 'prompt-item'" not in source
    )
    assert (
        "item.editor?.kind === 'sortable-string-list'" in source
        or "activeItem?.editor?.kind === 'sortable-string-list'" in source
    )
    assert (
        "item.editor?.kind === 'string-list'" in source
        or "activeItem?.editor?.kind === 'string-list'" in source
    )
    assert (
        "item.editor?.kind === 'key-value-list'" in source
        or "activeItem?.editor?.kind === 'key-value-list'" in source
    )
    assert '高级原始编辑区' not in source


def test_preset_editor_template_avoids_mixing_x_if_and_x_for_on_specialized_editor_templates():
    source = read_project_file('templates/modals/detail_preset_fullscreen.html')

    assert "<template x-if=\"item.editor?.kind === 'prompt-item'\" x-for=" not in source
    assert "<template x-if=\"item.editor?.kind === 'sortable-string-list'\" x-for=" not in source
    assert "<template x-if=\"item.editor?.kind === 'string-list'\" x-for=" not in source
    assert "<template x-if=\"item.editor?.kind === 'key-value-list'\" x-for=" not in source
