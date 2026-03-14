from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_runtime_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def test_embedded_chat_app_stage_does_not_force_document_background():
    source = read_runtime_file('static/js/runtime/chatAppStage.js')

    assert 'background: transparent !important;' not in source
    assert "'  background: transparent;'," in source


def test_embedded_iframe_template_does_not_force_document_background():
    source = read_runtime_file('static/js/runtime/renderIframeTemplate.js')

    assert 'background: transparent !important;' not in source
    assert "'  background: transparent;'," in source
