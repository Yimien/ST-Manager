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


def test_sync_folder_prefix_after_fs_move_updates_db_ui_cache_and_index(monkeypatch, tmp_path):
    from core.services import card_service

    cards_root = tmp_path / 'cards'
    moved_file = cards_root / 'dst' / 'pack' / 'sub' / 'hero.json'
    moved_file.parent.mkdir(parents=True, exist_ok=True)
    moved_file.write_text('{"spec":"chara_card_v2"}', encoding='utf-8')

    saved_ui_payloads = []
    update_calls = []
    sync_calls = []
    events = []

    class _FakeConn:
        def __init__(self):
            self.executed = []
            self._rows = []
            self.commit_calls = 0

        def execute(self, sql, params=()):
            self.executed.append((sql, params))
            normalized_sql = ' '.join(str(sql).split())
            if normalized_sql.startswith("SELECT id FROM card_metadata WHERE id LIKE ? || '/%' ESCAPE '\\'"):
                self._rows = [('src/pack/sub/hero.json',)]
            return self

        def fetchall(self):
            return list(self._rows)

        def commit(self):
            self.commit_calls += 1
            events.append('commit')
            return None

    class _FakeCache:
        def __init__(self):
            self.id_map = {
                'src/pack/sub/hero.json': {
                    'id': 'src/pack/sub/hero.json',
                    'category': 'src/pack/sub',
                    'is_bundle': False,
                    'last_modified': 1,
                }
            }
            self.bundle_map = {}
            self.visible_folders = []

        def move_folder_update(self, old_path_prefix, new_path_prefix):
            moved_items = []
            for card_id in list(self.id_map.keys()):
                if not card_id.startswith(old_path_prefix + '/'):
                    continue
                moved_items.append((card_id, self.id_map.pop(card_id)))

            for old_id, card in moved_items:
                suffix = old_id[len(old_path_prefix):]
                new_id = new_path_prefix + suffix
                old_category = card.get('category', '')
                if old_category == old_path_prefix:
                    new_category = new_path_prefix
                elif old_category.startswith(old_path_prefix + '/'):
                    new_category = new_path_prefix + old_category[len(old_path_prefix):]
                else:
                    new_category = new_id.rsplit('/', 1)[0] if '/' in new_id else ''

                card = dict(card)
                card['id'] = new_id
                card['category'] = new_category
                self.id_map[new_id] = card

    fake_conn = _FakeConn()
    fake_cache = _FakeCache()
    ui_data = {
        'src/pack': {'summary': 'folder note'},
        'src/pack/sub/hero.json': {
            'summary': 'nested note',
            card_service.VERSION_REMARKS_KEY: {
                'src/pack/sub/hero.json': {'label': 'old remark'},
            },
        },
        '_worldinfo_notes_v1': {
            'embedded::src/pack/sub/hero.json': {'summary': 'embedded note'},
            'resource::book.json': {'summary': 'keep resource note'},
            'global::lorebook.json': {'summary': 'keep global note', 'updated_at': 99},
        },
    }

    monkeypatch.setattr(card_service, 'CARDS_FOLDER', str(cards_root), raising=False)
    monkeypatch.setattr(
        card_service,
        'save_ui_data',
        lambda payload: ((
            events.append('save_ui_data'),
            saved_ui_payloads.append(json.loads(json.dumps(payload, ensure_ascii=False))),
        ), None)[1],
    )
    monkeypatch.setattr(
        card_service,
        'update_card_cache',
        lambda card_id, full_path, **kwargs: ((
            events.append('update_card_cache'),
            update_calls.append({'card_id': card_id, 'full_path': full_path, 'kwargs': kwargs}),
            {
                'cache_updated': True,
                'has_embedded_wi': False,
                'previous_has_embedded_wi': False,
            },
        ))[2],
    )
    monkeypatch.setattr(
        card_service,
        'sync_card_index_jobs',
        lambda **kwargs: ((events.append('sync_card_index_jobs'), sync_calls.append(kwargs)), {})[1],
    )
    monkeypatch.setattr(card_service.ctx, 'cache', fake_cache, raising=False)

    card_service.sync_folder_prefix_after_fs_move(
        conn=fake_conn,
        ui_data=ui_data,
        old_path='src/pack',
        new_path='dst/pack',
    )

    assert saved_ui_payloads[-1] == {
        'dst/pack': {'summary': 'folder note'},
        'dst/pack/sub/hero.json': {
            'summary': 'nested note',
            card_service.VERSION_REMARKS_KEY: {
                'dst/pack/sub/hero.json': {'label': 'old remark'},
            },
        },
        '_worldinfo_notes_v1': {
            'embedded::dst/pack/sub/hero.json': {'summary': 'embedded note'},
            'resource::book.json': {'summary': 'keep resource note'},
            'global::lorebook.json': {'summary': 'keep global note', 'updated_at': 99},
        },
    }
    assert fake_conn.executed == [
        ("SELECT id FROM card_metadata WHERE id LIKE ? || '/%' ESCAPE '\\'", ('src/pack',)),
        (
            """
            UPDATE card_metadata 
            SET id = ?, category = REPLACE(category, ?, ?) 
            WHERE id = ?
        """,
            ('dst/pack/sub/hero.json', 'src/pack', 'dst/pack', 'src/pack/sub/hero.json'),
        ),
    ]
    assert fake_conn.commit_calls == 1
    assert events == ['commit', 'save_ui_data', 'update_card_cache', 'sync_card_index_jobs']
    assert update_calls == [
        {
            'card_id': 'dst/pack/sub/hero.json',
            'full_path': str(cards_root / 'dst' / 'pack' / 'sub' / 'hero.json'),
            'kwargs': {'remove_entity_ids': ['src/pack/sub/hero.json']},
        }
    ]
    assert sync_calls == [
        {
            'card_id': 'dst/pack/sub/hero.json',
            'source_path': str(cards_root / 'dst' / 'pack' / 'sub' / 'hero.json'),
            'file_content_changed': False,
            'rename_changed': True,
            'cache_updated': True,
            'has_embedded_wi': False,
            'previous_has_embedded_wi': False,
            'remove_entity_ids': ['src/pack/sub/hero.json'],
            'remove_owner_ids': ['src/pack/sub/hero.json'],
        }
    ]
    assert fake_cache.id_map == {
        'dst/pack/sub/hero.json': {
            'id': 'dst/pack/sub/hero.json',
            'category': 'dst/pack/sub',
            'is_bundle': False,
            'last_modified': 1,
        }
    }


def test_sync_exact_card_after_fs_move_updates_db_ui_cache_and_index(monkeypatch, tmp_path):
    from core.services import card_service

    cards_root = tmp_path / 'cards'
    moved_file = cards_root / 'dst' / 'hero.json'
    moved_file.parent.mkdir(parents=True, exist_ok=True)
    moved_file.write_text('{"spec":"chara_card_v2"}', encoding='utf-8')

    saved_ui_payloads = []
    update_calls = []
    sync_calls = []
    move_card_calls = []
    events = []

    class _FakeConn:
        def __init__(self):
            self.executed = []
            self.commit_calls = 0

        def execute(self, sql, params=()):
            self.executed.append((sql, params))
            return self

        def commit(self):
            self.commit_calls += 1
            events.append('commit')
            return None

    fake_conn = _FakeConn()
    ui_data = {
        'src/hero.json': {
            'summary': 'card note',
            card_service.VERSION_REMARKS_KEY: {
                'src/hero.json': {'summary': 'version note'},
            },
        },
        '_worldinfo_notes_v1': {
            'embedded::src/hero.json': {'summary': 'embedded note'},
            'embedded::src/other.json': {'summary': 'keep other note'},
            'resource::book.json': {'summary': 'keep resource note'},
        },
    }

    monkeypatch.setattr(card_service, 'CARDS_FOLDER', str(cards_root), raising=False)
    monkeypatch.setattr(
        card_service,
        'save_ui_data',
        lambda payload: ((
            events.append('save_ui_data'),
            saved_ui_payloads.append(json.loads(json.dumps(payload, ensure_ascii=False))),
        ), None)[1],
    )
    monkeypatch.setattr(
        card_service,
        'update_card_cache',
        lambda card_id, full_path, **kwargs: ((
            events.append('update_card_cache'),
            update_calls.append({'card_id': card_id, 'full_path': full_path, 'kwargs': kwargs}),
            {
                'cache_updated': True,
                'has_embedded_wi': False,
                'previous_has_embedded_wi': False,
            },
        ))[2],
    )
    monkeypatch.setattr(
        card_service,
        'sync_card_index_jobs',
        lambda **kwargs: ((events.append('sync_card_index_jobs'), sync_calls.append(kwargs)), {})[1],
    )
    monkeypatch.setattr(
        card_service.ctx,
        'cache',
        SimpleNamespace(
            move_card_update=lambda *args: move_card_calls.append(args),
        ),
        raising=False,
    )

    card_service.sync_exact_card_after_fs_move(
        conn=fake_conn,
        ui_data=ui_data,
        old_card_id='src/hero.json',
        new_card_id='dst/hero.json',
        dst_full_path=str(moved_file),
        final_name='hero.json',
        old_category='src',
    )

    assert fake_conn.executed == [
        ('UPDATE card_metadata SET id = ?, category = ? WHERE id = ?', ('dst/hero.json', 'dst', 'src/hero.json')),
    ]
    assert fake_conn.commit_calls == 1
    assert saved_ui_payloads[-1] == {
        'dst/hero.json': {
            'summary': 'card note',
            card_service.VERSION_REMARKS_KEY: {
                'dst/hero.json': {'summary': 'version note'},
            },
        },
        '_worldinfo_notes_v1': {
            'embedded::dst/hero.json': {'summary': 'embedded note'},
            'embedded::src/other.json': {'summary': 'keep other note'},
            'resource::book.json': {'summary': 'keep resource note'},
        },
    }
    assert events == ['commit', 'save_ui_data', 'update_card_cache', 'sync_card_index_jobs']
    assert move_card_calls == [
        ('src/hero.json', 'dst/hero.json', 'src', 'dst', 'hero.json', str(moved_file)),
    ]
    assert update_calls == [
        {
            'card_id': 'dst/hero.json',
            'full_path': str(moved_file),
            'kwargs': {'remove_entity_ids': ['src/hero.json']},
        }
    ]
    assert sync_calls == [
        {
            'card_id': 'dst/hero.json',
            'source_path': str(moved_file),
            'file_content_changed': False,
            'rename_changed': True,
            'cache_updated': True,
            'has_embedded_wi': False,
            'previous_has_embedded_wi': False,
            'remove_entity_ids': ['src/hero.json'],
            'remove_owner_ids': ['src/hero.json'],
        }
    ]


def test_cleanup_deleted_cards_after_fs_delete_dispatches_cleanup_only_jobs(monkeypatch):
    from core.services import card_service

    sync_calls = []

    monkeypatch.setattr(card_service, 'sync_card_index_jobs', lambda **kwargs: sync_calls.append(kwargs) or {})

    card_service.cleanup_deleted_cards_after_fs_delete(
        deleted_card_ids=['src/a.json', 'src/b.json'],
        source_paths_by_card_id={
            'src/a.json': 'D:/cards/src/a.json',
            'src/b.json': 'D:/cards/src/b.json',
        },
    )

    assert sync_calls == [
        {
            'card_id': 'src/a.json',
            'source_path': 'D:/cards/src/a.json',
            'remove_entity_ids': ['src/a.json'],
            'remove_owner_ids': ['src/a.json'],
        },
        {
            'card_id': 'src/b.json',
            'source_path': 'D:/cards/src/b.json',
            'remove_entity_ids': ['src/b.json'],
            'remove_owner_ids': ['src/b.json'],
        },
    ]


def test_api_rename_folder_uses_shared_folder_sync_helper(monkeypatch, tmp_path):
    cards_dir = tmp_path / 'cards'
    source_dir = cards_dir / 'src' / 'pack'
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / 'hero.json').write_text('{"spec":"chara_card_v2"}', encoding='utf-8')

    sync_calls = []

    class _UnusedSqliteConnection:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def cursor(self):
            return self

        def execute(self, _sql, _params=()):
            return self

        def fetchall(self):
            return []

        def commit(self):
            return None

    monkeypatch.setattr(cards_api, 'CARDS_FOLDER', str(cards_dir))
    monkeypatch.setattr(cards_api, 'DEFAULT_DB_PATH', str(tmp_path / 'db.sqlite3'))
    monkeypatch.setattr(cards_api, 'suppress_fs_events', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, '_is_safe_rel_path', lambda _value, allow_empty=False: True)
    monkeypatch.setattr(cards_api, '_is_safe_filename', lambda _value: True)
    monkeypatch.setattr(cards_api, 'load_ui_data', lambda: {'src/pack': {'summary': 'folder note'}})
    monkeypatch.setattr(cards_api, 'save_ui_data', lambda _payload: None)
    monkeypatch.setattr(
        cards_api,
        'sqlite3',
        SimpleNamespace(connect=lambda *_args, **_kwargs: _UnusedSqliteConnection()),
    )
    monkeypatch.setattr(
        cards_api.ctx,
        'cache',
        SimpleNamespace(
            rename_folder_update=lambda *_args, **_kwargs: None,
            category_counts={'src': 1},
        ),
        raising=False,
    )
    def _record_sync(**kwargs):
        sync_calls.append(kwargs)

    monkeypatch.setattr(cards_api, 'sync_folder_prefix_after_fs_move', _record_sync, raising=False)

    client = _make_app().test_client()
    res = client.post('/api/rename_folder', json={'old_path': 'src/pack', 'new_name': 'renamed'})

    assert res.status_code == 200
    assert res.get_json() == {'success': True, 'new_path': 'src/renamed'}
    assert sync_calls == [
        {
            'conn': sync_calls[0]['conn'],
            'ui_data': {'src/pack': {'summary': 'folder note'}},
            'old_path': 'src/pack',
            'new_path': 'src/renamed',
        }
    ]
    assert (cards_dir / 'src' / 'pack').exists() is False
    assert (cards_dir / 'src' / 'renamed' / 'hero.json').exists() is True


def test_api_rename_folder_returns_warning_when_shared_sync_fails(monkeypatch, tmp_path):
    cards_dir = tmp_path / 'cards'
    source_dir = cards_dir / 'src' / 'pack'
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / 'hero.json').write_text('{"spec":"chara_card_v2"}', encoding='utf-8')

    schedule_calls = []

    monkeypatch.setattr(cards_api, 'CARDS_FOLDER', str(cards_dir))
    monkeypatch.setattr(cards_api, 'suppress_fs_events', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, '_is_safe_rel_path', lambda _value, allow_empty=False: True)
    monkeypatch.setattr(cards_api, '_is_safe_filename', lambda _value: True)
    monkeypatch.setattr(
        cards_api,
        'sync_folder_prefix_after_fs_move',
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError('sync failed')),
        raising=False,
    )
    monkeypatch.setattr(cards_api, 'schedule_reload', lambda **kwargs: schedule_calls.append(kwargs))

    client = _make_app().test_client()
    res = client.post('/api/rename_folder', json={'old_path': 'src/pack', 'new_name': 'renamed'})

    assert res.status_code == 200
    assert res.get_json() == {
        'success': True,
        'new_path': 'src/renamed',
        'warning': '文件夹已重命名，但数据库索引更新遇到问题，系统将自动修复。',
    }
    assert schedule_calls == [{'reason': 'rename_folder:fallback'}]
    assert (cards_dir / 'src' / 'pack').exists() is False
    assert (cards_dir / 'src' / 'renamed' / 'hero.json').exists() is True


def test_api_move_folder_direct_uses_shared_folder_sync_helper(monkeypatch, tmp_path):
    cards_dir = tmp_path / 'cards'
    source_dir = cards_dir / 'src' / 'pack'
    target_parent_dir = cards_dir / 'dst'
    source_dir.mkdir(parents=True, exist_ok=True)
    target_parent_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / 'hero.json').write_text('{"spec":"chara_card_v2"}', encoding='utf-8')

    sync_calls = []

    monkeypatch.setattr(cards_api, 'CARDS_FOLDER', str(cards_dir))
    monkeypatch.setattr(cards_api, 'suppress_fs_events', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, '_is_safe_rel_path', lambda _value, allow_empty=False: True)
    monkeypatch.setattr(cards_api, 'load_ui_data', lambda: {'src/pack': {'summary': 'folder note'}})
    monkeypatch.setattr(cards_api, 'save_ui_data', lambda _payload: None)
    monkeypatch.setattr(cards_api, 'rename_folder_in_db', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, 'rename_folder_in_ui', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        cards_api.ctx,
        'cache',
        SimpleNamespace(
            move_folder_update=lambda *_args, **_kwargs: None,
            category_counts={'dst': 1},
        ),
        raising=False,
    )
    def _record_sync(**kwargs):
        sync_calls.append(kwargs)

    monkeypatch.setattr(cards_api, 'sync_folder_prefix_after_fs_move', _record_sync, raising=False)

    client = _make_app().test_client()
    res = client.post('/api/move_folder', json={'source_path': 'src/pack', 'target_parent_path': 'dst'})

    assert res.status_code == 200
    assert res.get_json() == {
        'success': True,
        'new_path': 'dst/pack',
        'mode': 'move',
        'category_counts': {'dst': 1},
    }
    assert sync_calls == [
        {
            'conn': sync_calls[0]['conn'],
            'ui_data': {'src/pack': {'summary': 'folder note'}},
            'old_path': 'src/pack',
            'new_path': 'dst/pack',
        }
    ]
    assert (cards_dir / 'src' / 'pack').exists() is False
    assert (cards_dir / 'dst' / 'pack' / 'hero.json').exists() is True


def test_api_move_folder_direct_returns_warning_when_shared_sync_fails(monkeypatch, tmp_path):
    cards_dir = tmp_path / 'cards'
    source_dir = cards_dir / 'src' / 'pack'
    target_parent_dir = cards_dir / 'dst'
    source_dir.mkdir(parents=True, exist_ok=True)
    target_parent_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / 'hero.json').write_text('{"spec":"chara_card_v2"}', encoding='utf-8')

    schedule_calls = []

    monkeypatch.setattr(cards_api, 'CARDS_FOLDER', str(cards_dir))
    monkeypatch.setattr(cards_api, 'suppress_fs_events', lambda *_args, **_kwargs: None)
    monkeypatch.setattr(cards_api, '_is_safe_rel_path', lambda _value, allow_empty=False: True)
    monkeypatch.setattr(cards_api, 'load_ui_data', lambda: {'src/pack': {'summary': 'folder note'}})
    monkeypatch.setattr(
        cards_api,
        'sync_folder_prefix_after_fs_move',
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError('sync failed')),
        raising=False,
    )
    monkeypatch.setattr(cards_api, 'schedule_reload', lambda **kwargs: schedule_calls.append(kwargs))
    monkeypatch.setattr(
        cards_api.ctx,
        'cache',
        SimpleNamespace(category_counts={'dst': 1}),
        raising=False,
    )

    client = _make_app().test_client()
    res = client.post('/api/move_folder', json={'source_path': 'src/pack', 'target_parent_path': 'dst'})

    assert res.status_code == 200
    assert res.get_json() == {
        'success': True,
        'new_path': 'dst/pack',
        'mode': 'move',
        'warning': '文件夹已移动，但数据库索引更新遇到问题，系统将自动修复。',
        'category_counts': {'dst': 1},
    }
    assert schedule_calls == [{'reason': 'move_folder:fallback'}]
    assert (cards_dir / 'src' / 'pack').exists() is False
    assert (cards_dir / 'dst' / 'pack' / 'hero.json').exists() is True
