from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def test_header_template_does_not_expose_runtime_inspector_controls():
    header_template = read_project_file('templates/components/header.html')

    assert 'openRuntimeInspector' not in header_template
    assert 'open-runtime-inspector' not in header_template
    assert '运行时检查器' not in header_template
    assert 'title="运行时检查器"' not in header_template
    assert '<div class="menu-label">运行时</div>' not in header_template


def test_index_template_does_not_include_runtime_inspector_modal():
    index_template = read_project_file('templates/index.html')

    assert 'runtime_inspector.html' not in index_template
    assert 'runtime_inspector' not in index_template


def test_app_js_does_not_import_or_register_runtime_inspector():
    app_source = read_project_file('static/js/app.js')

    assert 'runtimeInspector' not in app_source
    assert 'runtimeInspector.js' not in app_source


def test_header_component_does_not_wire_runtime_inspector_events():
    header_source = read_project_file('static/js/components/header.js')

    assert 'openRuntimeInspector' not in header_source
    assert 'open-runtime-inspector' not in header_source


def test_advanced_editor_no_longer_listens_for_runtime_inspector_bridge_events():
    advanced_editor_source = read_project_file('static/js/components/advancedEditor.js')

    assert 'runtime-inspector-control' not in advanced_editor_source
    assert 'focus-script-runtime-owner' not in advanced_editor_source


def test_chat_reader_css_defines_workbench_theme_tokens():
    chat_reader_css = read_project_file('static/css/modules/view-chats.css')

    required_tokens = [
        '--chat-reader-accent-soft',
        '--chat-reader-accent-strong',
        '--chat-reader-accent-border',
        '--chat-reader-accent-text',
        '--chat-reader-surface-raised',
        '--chat-reader-danger-soft',
    ]

    for token in required_tokens:
        assert token in chat_reader_css
