import json
import re
import subprocess
import textwrap

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def run_preset_detail_reader_runtime_check(script_body):
    source_path = PROJECT_ROOT / 'static/js/components/presetDetailReader.js'
    node_script = textwrap.dedent(
        f"""
        import {{ readFileSync }} from 'node:fs';

        const sourcePath = {json.dumps(str(source_path))};
        let source = readFileSync(sourcePath, 'utf8');
        source = source.replace(/^import[\\s\\S]*?;\\r?\\n/gm, '');
        source = source.replace('export default function presetDetailReader()', 'function presetDetailReader()');

        const stubs = `
        const getPresetDetail = async () => ({{ success: true, preset: {{}} }});
        const apiSavePresetExtensions = async () => ({{ success: true }});
        const clearActiveRuntimeContext = () => {{}};
        const setActiveRuntimeContext = () => {{}};
        const downloadFileFromApi = async () => {{}};
        const formatDate = (value) => value;
        globalThis.window = {{
          addEventListener() {{}},
          removeEventListener() {{}},
          dispatchEvent() {{}},
        }};
        globalThis.CustomEvent = class CustomEvent {{
          constructor(name, options = {{}}) {{
            this.type = name;
            this.detail = options.detail;
          }}
        }};
        `;

        const module = await import(
          'data:text/javascript,' + encodeURIComponent(stubs + source + '\\nexport default presetDetailReader;'),
        );
        const reader = module.default();
        reader.$store = {{
          global: {{
            deviceType: 'desktop',
            showToast() {{}},
          }},
        }};

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


def test_preset_detail_reader_js_exposes_prompt_workspace_helpers():
    source = read_project_file('static/js/components/presetDetailReader.js')

    assert 'activeWorkspace:' in source
    assert 'activePromptId:' in source
    assert 'get isPromptWorkspaceReader() {' in source
    assert 'get promptItems() {' in source
    assert 'get orderedPromptItems() {' in source
    assert 'get activePromptItem() {' in source
    assert 'get activeContextItem() {' in source
    assert 'selectWorkspace(workspaceId) {' in source
    assert 'selectPrompt(itemId) {' in source
    assert 'getPromptPreview(item) {' in source
    assert 'getPromptFullDetail(item) {' in source
    assert 'getPromptPositionLabel(item) {' in source


def test_preset_detail_reader_runtime_initializes_prompt_workspace_and_switches_active_context():
    run_preset_detail_reader_runtime_check(
        """
        reader.activePresetDetail = {
          reader_view: {
            family: 'prompt_manager',
            groups: [
              { id: 'prompts', label: 'Prompts' },
              { id: 'extensions', label: 'Extensions' },
            ],
            items: [
              {
                id: 'prompt:main',
                type: 'prompt',
                group: 'prompts',
                title: 'Main Prompt',
                payload: { identifier: 'main', content: 'hello' },
                prompt_meta: { order_index: 1 },
              },
              {
                id: 'prompt:summary',
                type: 'prompt',
                group: 'prompts',
                title: 'Summary Prompt',
                payload: { identifier: 'summary', content: 'world' },
                prompt_meta: { order_index: 0 },
              },
              {
                id: 'ext:memory',
                type: 'extension',
                group: 'extensions',
                title: 'Memory',
                payload: { value: { enabled: true } },
              },
            ],
            stats: {},
          },
        };

        reader.initializeReaderState();
        if (reader.activeWorkspace !== 'prompts') {
          throw new Error(`expected prompt workspace by default, got ${reader.activeWorkspace}`);
        }
        if (reader.activePromptId !== 'prompt:summary') {
          throw new Error(`expected first ordered prompt active, got ${reader.activePromptId}`);
        }
        if (reader.activeContextItem?.id !== 'prompt:summary') {
          throw new Error(`expected active context to use prompt item, got ${reader.activeContextItem?.id}`);
        }

        reader.selectWorkspace('extensions');
        if (reader.activeGroup !== 'extensions') {
          throw new Error(`expected workspace switch to sync activeGroup, got ${reader.activeGroup}`);
        }
        if (reader.activeItemId !== 'ext:memory') {
          throw new Error(`expected extension item selection, got ${reader.activeItemId}`);
        }
        if (reader.activeContextItem?.id !== 'ext:memory') {
          throw new Error(`expected generic context item after workspace switch, got ${reader.activeContextItem?.id}`);
        }

        reader.selectPrompt('prompt:main');
        if (reader.activeWorkspace !== 'prompts') {
          throw new Error(`expected prompt selection to switch workspace, got ${reader.activeWorkspace}`);
        }
        if (reader.activePromptId !== 'prompt:main') {
          throw new Error(`expected prompt selection to persist id, got ${reader.activePromptId}`);
        }
        if (reader.activeContextItem?.id !== 'prompt:main') {
          throw new Error(`expected prompt context after selectPrompt, got ${reader.activeContextItem?.id}`);
        }
        """
    )


def test_preset_detail_reader_runtime_preserves_items_when_reader_groups_are_missing():
    run_preset_detail_reader_runtime_check(
        """
        reader.activePresetDetail = {
          reader_view: {
            family: 'generic',
            groups: null,
            items: [
              {
                id: 'field:temperature',
                type: 'field',
                group: 'scalar_fields',
                title: 'Temperature',
                payload: { value: 0.7 },
              },
            ],
            stats: { total_count: 1 },
          },
        };

        if (reader.readerItems.length !== 1) {
          throw new Error(`expected reader items to survive missing groups, got ${reader.readerItems.length}`);
        }
        if (reader.readerGroups.length !== 0) {
          throw new Error(`expected missing groups to degrade to empty group list, got ${reader.readerGroups.length}`);
        }

        reader.initializeReaderState();
        if (reader.activeItem?.id !== 'field:temperature') {
          throw new Error(`expected first item to remain selectable, got ${reader.activeItem?.id}`);
        }
        if (reader.readerStats.total_count !== 1) {
          throw new Error(`expected stats total count to stay intact, got ${reader.readerStats.total_count}`);
        }
        """
    )


def test_preset_detail_reader_runtime_does_not_borrow_item_from_other_workspace_when_filters_hide_target_items():
    run_preset_detail_reader_runtime_check(
        """
        reader.activePresetDetail = {
          reader_view: {
            family: 'generic',
            groups: [
              { id: 'scalar_fields', label: 'Fields' },
              { id: 'extensions', label: 'Extensions' },
            ],
            items: [
              {
                id: 'field:temperature',
                type: 'field',
                group: 'scalar_fields',
                title: 'Temperature',
                payload: { value: 0.7 },
              },
              {
                id: 'ext:memory',
                type: 'extension',
                group: 'extensions',
                title: 'Memory',
                payload: { value: { enabled: true } },
              },
            ],
            stats: { total_count: 2 },
          },
        };

        reader.initializeReaderState();
        reader.uiFilter = 'structured';
        reader.searchTerm = 'missing';
        reader.selectWorkspace('extensions');

        if (reader.activeGroup !== 'extensions') {
          throw new Error(`expected workspace switch to target extensions, got ${reader.activeGroup}`);
        }
        if (reader.filteredItems.length !== 0) {
          throw new Error(`expected zero visible items in filtered workspace, got ${reader.filteredItems.length}`);
        }
        if (reader.activeItemId !== '') {
          throw new Error(`expected no active item id when workspace has no visible items, got ${reader.activeItemId}`);
        }
        if (reader.activeItem !== null) {
          throw new Error(`expected active item to stay empty instead of borrowing another workspace item, got ${reader.activeItem?.id}`);
        }
        if (reader.activeContextItem !== null) {
          throw new Error(`expected active context item to stay empty, got ${reader.activeContextItem?.id}`);
        }
        """
    )


def test_preset_detail_reader_runtime_falls_back_to_default_prompt_depth_for_invalid_values():
    run_preset_detail_reader_runtime_check(
        """
        reader.activePresetDetail = {
          reader_view: {
            family: 'prompt_manager',
            groups: [
              { id: 'prompts', label: 'Prompts' },
            ],
            items: [
              {
                id: 'prompt:main',
                type: 'prompt',
                group: 'prompts',
                title: 'Main Prompt',
                payload: {
                  identifier: 'main',
                  content: 'hello',
                  injection_position: 1,
                  injection_depth: 'oops',
                },
                prompt_meta: { order_index: 0 },
              },
            ],
            stats: {},
          },
        };

        reader.initializeReaderState();
        const label = reader.getPromptPositionLabel(reader.activePromptItem);
        if (label !== '聊天中 @ 4') {
          throw new Error(`expected invalid prompt depth to fall back to 4, got ${label}`);
        }
        """
    )


def test_preset_detail_reader_runtime_localizes_prompt_labels_and_hides_marker_placeholder_preview():
    run_preset_detail_reader_runtime_check(
        """
        const relativePrompt = {
          id: 'prompt:relative',
          type: 'prompt',
          group: 'prompts',
          title: 'Relative Prompt',
          payload: {
            identifier: 'relative',
            content: 'relative content',
            injection_position: 0,
          },
          prompt_meta: { order_index: 0, is_enabled: true, is_marker: false },
        };
        const markerPrompt = {
          id: 'prompt:marker',
          type: 'prompt',
          group: 'prompts',
          title: 'Marker Prompt',
          payload: {
            identifier: 'marker',
            marker: true,
            injection_position: 1,
            injection_depth: 'bad-depth',
          },
          prompt_meta: { order_index: 1, is_enabled: false, is_marker: true },
        };

        const relativeLabel = reader.getPromptPositionLabel(relativePrompt);
        if (relativeLabel !== '相对') {
          throw new Error(`expected relative prompt label to be localized, got ${relativeLabel}`);
        }

        const markerPreview = reader.getPromptPreview(markerPrompt);
        if (markerPreview !== '') {
          throw new Error(`expected marker preview to be empty, got ${JSON.stringify(markerPreview)}`);
        }

        const inChatLabel = reader.getPromptPositionLabel(markerPrompt);
        if (inChatLabel !== '聊天中 @ 4') {
          throw new Error(`expected invalid in-chat depth to fall back to 4, got ${inChatLabel}`);
        }
        """
    )


def test_preset_detail_reader_runtime_exposes_full_prompt_detail_without_preview_truncation():
    run_preset_detail_reader_runtime_check(
        """
        const longContent = 'A'.repeat(300);
        const promptItem = {
          id: 'prompt:long',
          type: 'prompt',
          group: 'prompts',
          title: 'Long Prompt',
          payload: {
            identifier: 'long',
            content: longContent,
          },
          prompt_meta: { order_index: 0, is_marker: false },
        };
        const markerPrompt = {
          id: 'prompt:marker',
          type: 'prompt',
          group: 'prompts',
          title: 'Marker Prompt',
          payload: {
            identifier: 'marker',
            marker: true,
            content: longContent,
          },
          prompt_meta: { order_index: 1, is_marker: true },
        };

        const preview = reader.getPromptPreview(promptItem);
        const fullDetail = reader.getPromptFullDetail(promptItem);
        const markerFullDetail = reader.getPromptFullDetail(markerPrompt);

        if (preview.length >= longContent.length) {
          throw new Error(`expected preview to remain truncated, got length ${preview.length}`);
        }
        if (fullDetail !== longContent) {
          throw new Error(`expected full prompt detail to keep complete content, got length ${fullDetail.length}`);
        }
        if (markerFullDetail !== '') {
          throw new Error(`expected marker prompt full detail to stay empty, got ${JSON.stringify(markerFullDetail)}`);
        }
        """
    )


def test_preset_detail_reader_runtime_accepts_zero_depth_and_rejects_negative_or_fractional_depths():
    run_preset_detail_reader_runtime_check(
        """
        const zeroDepthPrompt = {
          id: 'prompt:zero',
          type: 'prompt',
          group: 'prompts',
          title: 'Zero Depth Prompt',
          payload: {
            identifier: 'zero',
            injection_position: 1,
            injection_depth: 0,
          },
          prompt_meta: { order_index: 0, is_marker: false },
        };
        const negativeDepthPrompt = {
          id: 'prompt:negative',
          type: 'prompt',
          group: 'prompts',
          title: 'Negative Depth Prompt',
          payload: {
            identifier: 'negative',
            injection_position: 1,
            injection_depth: -1,
          },
          prompt_meta: { order_index: 1, is_marker: false },
        };
        const fractionalDepthPrompt = {
          id: 'prompt:fractional',
          type: 'prompt',
          group: 'prompts',
          title: 'Fractional Depth Prompt',
          payload: {
            identifier: 'fractional',
            injection_position: 1,
            injection_depth: 2.5,
          },
          prompt_meta: { order_index: 2, is_marker: false },
        };

        if (reader.getPromptPositionLabel(zeroDepthPrompt) !== '聊天中 @ 0') {
          throw new Error(`expected zero depth to stay valid, got ${reader.getPromptPositionLabel(zeroDepthPrompt)}`);
        }
        if (reader.getPromptPositionLabel(negativeDepthPrompt) !== '聊天中 @ 4') {
          throw new Error(`expected negative depth to fall back to 4, got ${reader.getPromptPositionLabel(negativeDepthPrompt)}`);
        }
        if (reader.getPromptPositionLabel(fractionalDepthPrompt) !== '聊天中 @ 4') {
          throw new Error(`expected fractional depth to fall back to 4, got ${reader.getPromptPositionLabel(fractionalDepthPrompt)}`);
        }
        """
    )


def test_preset_detail_reader_runtime_filters_prompt_workspace_items_and_visible_count():
    run_preset_detail_reader_runtime_check(
        """
        reader.activePresetDetail = {
          reader_view: {
            family: 'prompt_manager',
            groups: [
              { id: 'prompts', label: 'Prompts' },
              { id: 'extensions', label: 'Extensions' },
            ],
            items: [
              {
                id: 'prompt:main',
                type: 'prompt',
                group: 'prompts',
                title: 'Main Prompt',
                summary: 'system · 启用 · 相对位置',
                payload: { identifier: 'main', content: 'hello' },
                prompt_meta: { order_index: 0, is_enabled: true, is_marker: false },
              },
              {
                id: 'prompt:worldInfoAfter',
                type: 'prompt',
                group: 'prompts',
                title: 'World Info (after)',
                summary: 'prompt · 禁用 · 相对位置 · 预留字段',
                payload: { identifier: 'worldInfoAfter', marker: true },
                prompt_meta: { order_index: 1, is_enabled: false, is_marker: true },
              },
              {
                id: 'ext:memory',
                type: 'extension',
                group: 'extensions',
                title: 'Memory',
                payload: { value: { enabled: true } },
              },
            ],
            stats: {},
          },
        };

        reader.initializeReaderState();
        reader.uiFilter = 'marker';

        if (reader.promptFilteredItems.length !== 1) {
          throw new Error(`expected marker filter to keep one prompt, got ${reader.promptFilteredItems.length}`);
        }
        if (reader.promptFilteredItems[0].id !== 'prompt:worldInfoAfter') {
          throw new Error(`expected marker filter to keep worldInfoAfter, got ${reader.promptFilteredItems[0]?.id}`);
        }
        if (reader.readerStats.visible_count !== 1) {
          throw new Error(`expected prompt workspace visible count to follow filtered prompts, got ${reader.readerStats.visible_count}`);
        }

        reader.uiFilter = 'all';
        reader.searchTerm = 'worldinfoafter';
        if (reader.promptFilteredItems.length !== 1) {
          throw new Error(`expected search to narrow prompt workspace to one item, got ${reader.promptFilteredItems.length}`);
        }
        if (reader.promptFilteredItems[0].id !== 'prompt:worldInfoAfter') {
          throw new Error(`expected prompt search to match identifier, got ${reader.promptFilteredItems[0]?.id}`);
        }
        if (reader.readerStats.visible_count !== 1) {
          throw new Error(`expected prompt search visible count to stay in sync, got ${reader.readerStats.visible_count}`);
        }
        """
    )


def test_preset_detail_reader_runtime_normalizes_filters_when_switching_workspaces():
    run_preset_detail_reader_runtime_check(
        """
        reader.activePresetDetail = {
          reader_view: {
            family: 'prompt_manager',
            groups: [
              { id: 'prompts', label: 'Prompts' },
              { id: 'extensions', label: 'Extensions' },
            ],
            items: [
              {
                id: 'prompt:main',
                type: 'prompt',
                group: 'prompts',
                title: 'Main Prompt',
                payload: { identifier: 'main', content: 'hello' },
                prompt_meta: { order_index: 0, is_enabled: true, is_marker: false },
              },
              {
                id: 'ext:memory',
                type: 'extension',
                group: 'extensions',
                title: 'Memory',
                payload: { value: { enabled: true } },
              },
            ],
            stats: {},
          },
        };

        reader.initializeReaderState();
        reader.uiFilter = 'marker';
        reader.selectWorkspace('extensions');

        if (reader.uiFilter !== 'all') {
          throw new Error(`expected prompt-only filter to reset for generic workspace, got ${reader.uiFilter}`);
        }

        reader.uiFilter = 'structured';
        reader.selectWorkspace('prompts');

        if (reader.uiFilter !== 'all') {
          throw new Error(`expected generic-only filter to reset for prompts workspace, got ${reader.uiFilter}`);
        }
        """
    )


def test_preset_detail_reader_template_uses_reader_view_three_column_layout_contracts():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert 'x-if="!isPromptWorkspaceReader"' in source
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


def test_preset_detail_reader_template_adds_prompt_workspace_branch_contracts():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert 'x-if="isPromptWorkspaceReader"' in source
    assert "@click=\"selectWorkspace('prompts')\"" in source
    assert 'x-for="item in promptFilteredItems"' in source
    assert '@click="selectPrompt(item.id)"' in source
    assert 'x-text="getPromptPreview(item)"' in source
    assert 'x-text="getPromptPositionLabel(item)"' in source
    assert 'x-text="activeContextItem?.title ||' in source
    assert 'x-text="getPromptFullDetail(activeContextItem)"' in source
    assert "activeWorkspace === 'prompts' && orderedPromptItems.length > 0 && promptFilteredItems.length === 0" in source
    assert '`${promptFilteredItems.length} / ${orderedPromptItems.length}`' in source or '`${promptFilteredItems.length}/${orderedPromptItems.length}`' in source
    assert '`${orderedPromptItems.length} / ${readerStats.total_count}`' not in source
    assert '启用' in source
    assert '禁用' in source
    assert '预留字段' in source


def test_preset_detail_reader_template_removes_marker_placeholder_copy():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert '占位用预留字段，不承载提示词内容' not in source


def test_preset_detail_reader_template_keeps_generic_items_available_for_non_prompt_workspaces():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert 'x-show="activeWorkspace !== \"prompts\""' in source or "x-show=\"activeWorkspace !== 'prompts'\"" in source
    assert 'x-text="getItemValuePreview(activeContextItem)"' in source
    assert 'x-text="getItemFullDetail(activeContextItem)"' in source
    assert "x-if=\"activeContextItem?.group !== 'prompts'\"" in source


def test_preset_detail_reader_template_prevents_blank_prompt_content_cards_and_shows_prompt_empty_state():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert "activeWorkspace === 'prompts' && orderedPromptItems.length > 0 && promptFilteredItems.length === 0" in source
    assert '没有匹配的 Prompt' in source
    assert "x-if=\"activeContextItem?.group !== 'prompts'\"" in source
    assert "activeContextItem?.group === 'prompts' ? getPromptPreview(activeContextItem) : getItemFullDetail(activeContextItem)" not in source


def test_preset_detail_reader_template_restores_prompt_copy_action_without_reopening_generic_content_card():
    source = read_project_file('templates/modals/detail_preset_popup.html')

    assert "x-if=\"activeContextItem?.group === 'prompts' && getPromptFullDetail(activeContextItem)\"" in source
    assert '@click="copyText(getPromptFullDetail(activeContextItem), \"条目内容\")"' in source or "@click=\"copyText(getPromptFullDetail(activeContextItem), '条目内容')\"" in source
    assert "x-if=\"activeContextItem?.group !== 'prompts'\"" in source
    assert '@click="copyText(getItemFullDetail(activeContextItem), \"条目内容\")"' in source or "@click=\"copyText(getItemFullDetail(activeContextItem), '条目内容')\"" in source


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
