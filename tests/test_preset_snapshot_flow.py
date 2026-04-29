import json
import sys
from pathlib import Path

from flask import Flask


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from core.api.v1 import system as system_api


def _make_app():
    app = Flask(__name__)
    app.register_blueprint(system_api.bp)
    return app


def test_create_snapshot_accepts_preset_type(monkeypatch, tmp_path):
    preset_file = tmp_path / 'presets' / 'sample.json'
    preset_file.parent.mkdir(parents=True, exist_ok=True)
    preset_file.write_text(json.dumps({'name': 'Sample'}, ensure_ascii=False), encoding='utf-8')

    monkeypatch.setattr(system_api, 'BASE_DIR', str(tmp_path))
    monkeypatch.setattr(system_api, 'DATA_DIR', str(tmp_path / 'data'))
    monkeypatch.setattr(
        system_api,
        'load_config',
        lambda: {
            'resources_dir': str(tmp_path / 'resources'),
            'presets_dir': str(tmp_path / 'presets'),
            'world_info_dir': str(tmp_path / 'lorebooks'),
            'chats_dir': str(tmp_path / 'chats'),
        },
    )

    client = _make_app().test_client()
    res = client.post(
        '/api/create_snapshot',
        json={
            'id': 'global::sample.json',
            'type': 'preset',
            'file_path': str(preset_file),
            'content': {'name': 'Sample'},
            'label': 'manual',
        },
    )

    assert res.status_code == 200
    payload = res.get_json()
    assert payload['success'] is True
    assert Path(payload['path']).exists()


def test_list_backups_returns_preset_snapshots(monkeypatch, tmp_path):
    preset_file = tmp_path / 'presets' / 'sample.json'
    preset_file.parent.mkdir(parents=True, exist_ok=True)
    preset_file.write_text(json.dumps({'name': 'Sample'}, ensure_ascii=False), encoding='utf-8')

    monkeypatch.setattr(system_api, 'BASE_DIR', str(tmp_path))
    monkeypatch.setattr(system_api, 'DATA_DIR', str(tmp_path / 'data'))
    monkeypatch.setattr(
        system_api,
        'load_config',
        lambda: {
            'resources_dir': str(tmp_path / 'resources'),
            'presets_dir': str(tmp_path / 'presets'),
            'world_info_dir': str(tmp_path / 'lorebooks'),
            'chats_dir': str(tmp_path / 'chats'),
        },
    )

    client = _make_app().test_client()
    create_res = client.post(
        '/api/create_snapshot',
        json={
            'id': 'global::sample.json',
            'type': 'preset',
            'file_path': str(preset_file),
            'content': {'name': 'Sample'},
            'label': 'manual',
        },
    )
    assert create_res.status_code == 200

    list_res = client.post(
        '/api/list_backups',
        json={
            'id': 'global::sample.json',
            'type': 'preset',
            'file_path': str(preset_file),
        },
    )

    assert list_res.status_code == 200
    payload = list_res.get_json()
    assert payload['success'] is True
    assert len(payload['backups']) == 1


def test_restore_backup_restores_preset_file(monkeypatch, tmp_path):
    preset_file = tmp_path / 'presets' / 'sample.json'
    preset_file.parent.mkdir(parents=True, exist_ok=True)
    preset_file.write_text(json.dumps({'name': 'Before'}, ensure_ascii=False), encoding='utf-8')

    monkeypatch.setattr(system_api, 'BASE_DIR', str(tmp_path))
    monkeypatch.setattr(system_api, 'DATA_DIR', str(tmp_path / 'data'))
    monkeypatch.setattr(
        system_api,
        'load_config',
        lambda: {
            'resources_dir': str(tmp_path / 'resources'),
            'presets_dir': str(tmp_path / 'presets'),
            'world_info_dir': str(tmp_path / 'lorebooks'),
            'chats_dir': str(tmp_path / 'chats'),
        },
    )

    client = _make_app().test_client()
    create_res = client.post(
        '/api/create_snapshot',
        json={
            'id': 'global::sample.json',
            'type': 'preset',
            'file_path': str(preset_file),
            'content': {'name': 'Before'},
            'label': 'manual',
        },
    )
    backup_path = create_res.get_json()['path']

    preset_file.write_text(json.dumps({'name': 'After'}, ensure_ascii=False), encoding='utf-8')
    restore_res = client.post(
        '/api/restore_backup',
        json={
            'backup_path': backup_path,
            'target_id': 'global::sample.json',
            'type': 'preset',
            'target_file_path': str(preset_file),
        },
    )

    assert restore_res.status_code == 200
    assert restore_res.get_json()['success'] is True
    restored = json.loads(preset_file.read_text(encoding='utf-8'))
    assert restored['name'] == 'Before'
