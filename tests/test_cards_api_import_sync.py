import json
import sys
from pathlib import Path
from types import SimpleNamespace

from flask import Flask


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from core.api.v1 import cards as cards_api


def _make_app():
    app = Flask(__name__)
    app.register_blueprint(cards_api.bp)
    return app


def test_import_from_url_enqueues_card_and_world_sync_jobs(monkeypatch, tmp_path):
    cards_dir = tmp_path / 'cards'
    temp_dir = tmp_path / 'temp'
    cards_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    downloaded_path = temp_dir / 'temp_dl_1_Hero.png'

    class _FakeResponse:
        def raise_for_status(self):
            return None

        def iter_content(self, chunk_size=8192):
            del chunk_size
            yield b'fake-card'

    sync_calls = []

    monkeypatch.setattr(cards_api, 'CARDS_FOLDER', str(cards_dir))
    monkeypatch.setattr(cards_api, 'TEMP_DIR', str(temp_dir))
    monkeypatch.setattr(cards_api, 'suppress_fs_events', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, 'requests', type('Requests', (), {'get': staticmethod(lambda *_args, **_kwargs: _FakeResponse())})())
    monkeypatch.setattr(cards_api, 'extract_card_info', lambda _path: {
        'data': {
            'name': 'Hero',
            'tags': ['blue'],
            'description': '',
            'first_mes': '',
            'mes_example': '',
            'alternate_greetings': [],
            'creator_notes': '',
            'personality': '',
            'scenario': '',
            'system_prompt': '',
            'post_history_instructions': '',
            'character_version': '',
            'character_book': {'name': 'Book', 'entries': {}},
            'extensions': {},
            'creator': '',
        }
    })
    monkeypatch.setattr(cards_api, 'sanitize_filename', lambda value: value)
    monkeypatch.setattr(cards_api, 'load_ui_data', lambda: {})
    monkeypatch.setattr(cards_api, 'save_ui_data', lambda _payload: None)
    monkeypatch.setattr(cards_api, 'ensure_import_time', lambda *_args, **_kwargs: (False, 123.0))
    monkeypatch.setattr(cards_api, 'get_file_hash_and_size', lambda _path: ('hash', 8))
    monkeypatch.setattr(cards_api, 'calculate_token_count', lambda _data: 0)
    monkeypatch.setattr(cards_api, 'schedule_reload', lambda **_kwargs: None)
    monkeypatch.setattr(cards_api, 'auto_run_rules_on_card', lambda _card_id: None)
    monkeypatch.setattr(cards_api, 'update_card_cache', lambda *_args, **_kwargs: {
        'cache_updated': True,
        'has_embedded_wi': True,
        'previous_has_embedded_wi': False,
    })
    monkeypatch.setattr(cards_api, 'sync_card_index_jobs', lambda **kwargs: sync_calls.append(kwargs) or {'jobs_enqueued': ['upsert_card', 'upsert_world_embedded', 'upsert_world_owner']})
    monkeypatch.setattr(cards_api, '_is_safe_rel_path', lambda _path, allow_empty=False: True)
    monkeypatch.setattr(cards_api, 'current_config', {'auto_rename_on_import': True})

    class _FakeCache:
        category_counts = {}

        def add_card_update(self, payload):
            return payload

    monkeypatch.setattr(cards_api.ctx, 'cache', _FakeCache())

    client = _make_app().test_client()
    res = client.post('/api/import_from_url', json={'url': 'https://example.com/hero.png', 'category': ''})

    assert res.status_code == 200
    assert res.get_json()['success'] is True
    assert sync_calls == [
        {
            'card_id': 'Hero.png',
            'source_path': str(cards_dir / 'Hero.png'),
            'file_content_changed': True,
            'cache_updated': True,
            'has_embedded_wi': True,
            'previous_has_embedded_wi': False,
        }
    ]
    assert downloaded_path.exists() is False


def test_upload_commit_enqueues_card_and_world_sync_jobs(monkeypatch, tmp_path):
    cards_dir = tmp_path / 'cards'
    temp_dir = tmp_path / 'temp'
    stage_dir = temp_dir / 'batch_upload' / 'batch-1'
    cards_dir.mkdir(parents=True, exist_ok=True)
    stage_dir.mkdir(parents=True, exist_ok=True)
    staged_card = stage_dir / 'hero.png'
    staged_card.write_bytes(b'fake-card')

    sync_calls = []

    monkeypatch.setattr(cards_api, 'CARDS_FOLDER', str(cards_dir))
    monkeypatch.setattr(cards_api, 'TEMP_DIR', str(temp_dir))
    monkeypatch.setattr(cards_api, 'suppress_fs_events', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, '_is_safe_filename', lambda _value: True)
    monkeypatch.setattr(cards_api, '_is_safe_rel_path', lambda _value, allow_empty=False: True)
    monkeypatch.setattr(cards_api, 'current_config', {'auto_rename_on_import': True})
    monkeypatch.setattr(cards_api, 'extract_card_info', lambda _path: {
        'data': {
            'name': 'Hero',
            'tags': ['blue'],
            'description': '',
            'first_mes': '',
            'mes_example': '',
            'alternate_greetings': [],
            'creator_notes': '',
            'personality': '',
            'scenario': '',
            'system_prompt': '',
            'post_history_instructions': '',
            'character_version': '',
            'character_book': {'name': 'Book', 'entries': {}},
            'extensions': {},
            'creator': '',
        }
    })
    monkeypatch.setattr(cards_api, 'sanitize_filename', lambda value: value)
    monkeypatch.setattr(cards_api, 'load_ui_data', lambda: {})
    monkeypatch.setattr(cards_api, 'save_ui_data', lambda _payload: None)
    monkeypatch.setattr(cards_api, 'ensure_import_time', lambda *_args, **_kwargs: (False, 123.0))
    monkeypatch.setattr(cards_api, 'get_import_time', lambda _ui_data, _ui_key, fallback: fallback)
    monkeypatch.setattr(cards_api, 'get_file_hash_and_size', lambda _path: ('hash', 8))
    monkeypatch.setattr(cards_api, 'calculate_token_count', lambda _data: 0)
    monkeypatch.setattr(cards_api, 'auto_run_rules_on_card', lambda _card_id: None)
    monkeypatch.setattr(cards_api, 'update_card_cache', lambda *_args, **_kwargs: {
        'cache_updated': True,
        'has_embedded_wi': True,
        'previous_has_embedded_wi': False,
    })
    monkeypatch.setattr(cards_api, 'sync_card_index_jobs', lambda **kwargs: sync_calls.append(kwargs) or {'jobs_enqueued': ['upsert_card', 'upsert_world_embedded', 'upsert_world_owner']})

    class _FakeCache:
        category_counts = {}

        def add_card_update(self, payload):
            return payload

    monkeypatch.setattr(cards_api.ctx, 'cache', _FakeCache())

    client = _make_app().test_client()
    res = client.post(
        '/api/upload/commit',
        json={
            'batch_id': 'batch-1',
            'category': '',
            'decisions': [{'filename': 'hero.png', 'action': 'overwrite'}],
        },
    )

    assert res.status_code == 200
    assert res.get_json()['success'] is True
    assert sync_calls == [
        {
            'card_id': 'Hero.png',
            'source_path': str(cards_dir / 'Hero.png'),
            'file_content_changed': True,
            'cache_updated': True,
            'has_embedded_wi': True,
            'previous_has_embedded_wi': False,
        }
    ]


def test_move_card_internal_enqueues_incremental_cleanup_for_single_card(monkeypatch, tmp_path):
    from core.services import card_service

    cards_root = tmp_path / 'cards'
    src_dir = cards_root / 'src'
    dst_dir = cards_root / 'dst'
    src_dir.mkdir(parents=True, exist_ok=True)
    dst_dir.mkdir(parents=True, exist_ok=True)
    src_path = src_dir / 'demo.json'
    src_path.write_text('{"spec":"chara_card_v2"}', encoding='utf-8')

    sync_calls = []
    cache_calls = {}
    saved_ui_payloads = []

    class _FakeConn:
        def execute(self, _sql, _params=()):
            return self

        def commit(self):
            return None

    monkeypatch.setattr(card_service, 'CARDS_FOLDER', str(cards_root), raising=False)
    monkeypatch.setattr(card_service, 'load_ui_data', lambda: {'src/demo.json': {'summary': 'note'}})
    monkeypatch.setattr(card_service, 'save_ui_data', lambda payload: saved_ui_payloads.append(dict(payload)))
    monkeypatch.setattr(card_service, 'get_db', lambda: _FakeConn())
    monkeypatch.setattr(card_service, 'update_card_cache', lambda *args, **kwargs: (
        cache_calls.setdefault('update_card_cache', {'args': args, 'kwargs': kwargs}),
        {
            'cache_updated': True,
            'has_embedded_wi': False,
            'previous_has_embedded_wi': False,
        }
    )[1])
    monkeypatch.setattr(card_service, 'sync_card_index_jobs', lambda **kwargs: sync_calls.append(kwargs) or {})
    monkeypatch.setattr(
        card_service.ctx,
        'cache',
        SimpleNamespace(
            id_map={'src/demo.json': {'id': 'src/demo.json', 'category': 'src'}},
            move_card_update=lambda *args, **kwargs: cache_calls.setdefault('move_card_update', (args, kwargs)),
        ),
        raising=False,
    )

    ok, new_id, msg = card_service.move_card_internal('src/demo.json', 'dst')

    assert ok is True
    assert msg == 'Success'
    assert new_id == 'dst/demo.json'
    assert sync_calls == [
        {
            'card_id': 'dst/demo.json',
            'source_path': str(dst_dir / 'demo.json'),
            'file_content_changed': False,
            'rename_changed': True,
            'cache_updated': True,
            'has_embedded_wi': False,
            'previous_has_embedded_wi': False,
            'remove_entity_ids': ['src/demo.json'],
            'remove_owner_ids': ['src/demo.json'],
        }
    ]


def test_api_move_card_uses_shared_move_card_internal(monkeypatch):
    move_calls = []

    monkeypatch.setattr(cards_api, 'suppress_fs_events', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, '_is_safe_rel_path', lambda _value, allow_empty=False: True)
    monkeypatch.setattr(cards_api, 'move_card_internal', lambda card_id, target_category: move_calls.append((card_id, target_category)) or (True, 'dst/demo.json', 'Success'))
    monkeypatch.setattr(
        cards_api.ctx,
        'cache',
        SimpleNamespace(
            id_map={'dst/demo.json': {'image_url': '/cards_file/dst%2Fdemo.json?t=1'}},
            category_counts={},
        ),
        raising=False,
    )

    client = _make_app().test_client()
    res = client.post('/api/move_card', json={'card_ids': ['src/demo.json'], 'target_category': 'dst'})

    assert res.status_code == 200
    assert res.get_json() == {
        'success': True,
        'count': 1,
        'moved_details': [
            {
                'old_id': 'src/demo.json',
                'new_id': 'dst/demo.json',
                'new_filename': 'demo.json',
                'new_category': 'dst',
                'new_image_url': '/cards_file/dst%2Fdemo.json?t=1',
            }
        ],
        'category_counts': {},
    }
    assert move_calls == [('src/demo.json', 'dst')]
