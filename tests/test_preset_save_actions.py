import json
import sys
from pathlib import Path

from flask import Flask


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from core.api.v1 import presets as presets_api


def _make_test_app():
    app = Flask(__name__)
    app.register_blueprint(presets_api.bp)
    return app


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def _configure(monkeypatch, tmp_path, presets_dir):
    monkeypatch.setattr(presets_api, 'BASE_DIR', str(tmp_path))
    monkeypatch.setattr(
        presets_api,
        'load_config',
        lambda: {'presets_dir': str(presets_dir), 'resources_dir': str(tmp_path / 'resources')},
    )


def test_preset_save_overwrite_preserves_unknown_fields(monkeypatch, tmp_path):
    presets_dir = tmp_path / 'presets'
    preset_file = presets_dir / 'textgen.json'
    _write_json(
        preset_file,
        {
            'name': 'Textgen',
            'temp': 0.7,
            'top_p': 0.9,
            'custom_flag': {'keep': True},
            'extensions': {'regex_scripts': []},
        },
    )

    _configure(monkeypatch, tmp_path, presets_dir)

    client = _make_test_app().test_client()
    detail_res = client.get('/api/presets/detail/global::textgen.json')
    revision = detail_res.get_json()['preset']['source_revision']

    save_res = client.post(
        '/api/presets/save',
        json={
            'preset_id': 'global::textgen.json',
            'preset_kind': 'textgen',
            'save_mode': 'overwrite',
            'source_revision': revision,
            'content': {'name': 'Textgen', 'temp': 1.1, 'top_p': 0.92},
        },
    )

    assert save_res.status_code == 200
    payload = json.loads(preset_file.read_text(encoding='utf-8'))
    assert payload['temp'] == 1.1
    assert payload['top_p'] == 0.92
    assert payload['custom_flag'] == {'keep': True}
    assert payload['extensions'] == {'regex_scripts': []}


def test_preset_save_rejects_stale_source_revision(monkeypatch, tmp_path):
    presets_dir = tmp_path / 'presets'
    preset_file = presets_dir / 'textgen.json'
    _write_json(preset_file, {'name': 'Textgen', 'temp': 0.7})

    _configure(monkeypatch, tmp_path, presets_dir)

    client = _make_test_app().test_client()
    save_res = client.post(
        '/api/presets/save',
        json={
            'preset_id': 'global::textgen.json',
            'preset_kind': 'textgen',
            'save_mode': 'overwrite',
            'source_revision': '1:1',
            'content': {'name': 'Textgen', 'temp': 0.8},
        },
    )

    assert save_res.status_code == 409
    assert 'source_revision' in save_res.get_json()['msg']


def test_preset_save_requires_source_revision_for_overwrite(monkeypatch, tmp_path):
    presets_dir = tmp_path / 'presets'
    preset_file = presets_dir / 'textgen.json'
    _write_json(preset_file, {'name': 'Textgen', 'temp': 0.7})

    _configure(monkeypatch, tmp_path, presets_dir)

    client = _make_test_app().test_client()
    save_res = client.post(
        '/api/presets/save',
        json={
            'preset_id': 'global::textgen.json',
            'preset_kind': 'textgen',
            'save_mode': 'overwrite',
            'content': {'name': 'Textgen', 'temp': 0.8},
        },
    )

    assert save_res.status_code == 409
    assert 'source_revision' in save_res.get_json()['msg']


def test_preset_save_as_creates_new_global_file(monkeypatch, tmp_path):
    presets_dir = tmp_path / 'presets'
    presets_dir.mkdir(parents=True, exist_ok=True)

    _configure(monkeypatch, tmp_path, presets_dir)

    client = _make_test_app().test_client()
    res = client.post(
        '/api/presets/save',
        json={
            'preset_kind': 'textgen',
            'save_mode': 'save_as',
            'name': '新的文本生成预设',
            'content': {'name': '新的文本生成预设', 'temp': 0.8},
        },
    )

    assert res.status_code == 200
    payload = res.get_json()
    assert payload['success'] is True
    assert (presets_dir / '新的文本生成预设.json').exists()


def test_preset_rename_updates_filename_and_object_name(monkeypatch, tmp_path):
    presets_dir = tmp_path / 'presets'
    preset_file = presets_dir / 'old-name.json'
    _write_json(preset_file, {'name': 'Old Name', 'temp': 0.7})

    _configure(monkeypatch, tmp_path, presets_dir)

    client = _make_test_app().test_client()
    detail_res = client.get('/api/presets/detail/global::old-name.json')
    revision = detail_res.get_json()['preset']['source_revision']
    res = client.post(
        '/api/presets/save',
        json={
            'preset_id': 'global::old-name.json',
            'save_mode': 'rename',
            'new_name': 'New Name',
            'source_revision': revision,
        },
    )

    assert res.status_code == 200
    assert (presets_dir / 'New Name.json').exists()
    renamed = json.loads((presets_dir / 'New Name.json').read_text(encoding='utf-8'))
    assert renamed['name'] == 'New Name'


def test_preset_delete_requires_revision_and_removes_file(monkeypatch, tmp_path):
    presets_dir = tmp_path / 'presets'
    preset_file = presets_dir / 'delete-me.json'
    _write_json(preset_file, {'name': 'Delete Me', 'temp': 0.7})

    _configure(monkeypatch, tmp_path, presets_dir)

    client = _make_test_app().test_client()
    detail_res = client.get('/api/presets/detail/global::delete-me.json')
    revision = detail_res.get_json()['preset']['source_revision']
    res = client.post(
        '/api/presets/save',
        json={
            'preset_id': 'global::delete-me.json',
            'save_mode': 'delete',
            'source_revision': revision,
        },
    )

    assert res.status_code == 200
    assert res.get_json()['success'] is True
    assert preset_file.exists() is False


def test_preset_restore_default_returns_preview_payload(monkeypatch, tmp_path):
    presets_dir = tmp_path / 'presets'
    preset_file = presets_dir / 'textgen.json'
    _write_json(preset_file, {'name': 'Local Textgen', 'temp': 0.7})

    class _FakeSTClient:
        def get_presets_dir(self, custom_path=None):
            default_dir = tmp_path / 'SillyTavern' / 'data' / 'default-user' / 'OpenAI Settings' / 'TextGen'
            default_dir.mkdir(parents=True, exist_ok=True)
            _write_json(default_dir / 'textgen.json', {'name': 'Default Textgen', 'temp': 1.0})
            return str(default_dir.parent)

    _configure(monkeypatch, tmp_path, presets_dir)
    monkeypatch.setattr('core.services.preset_defaults.STClient', _FakeSTClient)

    client = _make_test_app().test_client()
    res = client.post(
        '/api/presets/default-preview',
        json={
            'preset_id': 'global::textgen.json',
            'preset_kind': 'textgen',
        },
    )

    assert res.status_code == 200
    payload = res.get_json()
    assert payload['success'] is True
    assert payload['default_content']['name'] == 'Default Textgen'
