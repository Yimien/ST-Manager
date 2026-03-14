import sys
from pathlib import Path

from flask import Flask


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.api.v1 import chats as chats_api


def _make_test_app():
    app = Flask(__name__)
    app.register_blueprint(chats_api.bp)
    return app


def _mock_chat_list(monkeypatch):
    items = {
        'fav.jsonl': {
            'id': 'fav.jsonl',
            'title': 'Fav Chat',
            'favorite': True,
            'file_mtime': 200,
            'bound_card_count': 0,
        },
        'plain.jsonl': {
            'id': 'plain.jsonl',
            'title': 'Plain Chat',
            'favorite': False,
            'file_mtime': 100,
            'bound_card_count': 0,
        },
    }

    monkeypatch.setattr(chats_api, 'load_chat_data', lambda: {})
    monkeypatch.setattr(chats_api, 'load_ui_data', lambda: {})
    monkeypatch.setattr(chats_api, '_iter_chat_files', lambda: list(items.keys()))
    monkeypatch.setattr(chats_api, '_relative_chat_id', lambda full_path: full_path)
    monkeypatch.setattr(
        chats_api,
        '_refresh_chat_entry',
        lambda chat_id, full_path, chat_data, need_messages=False: ({}, False, None, [], []),
    )
    monkeypatch.setattr(
        chats_api,
        '_build_chat_item',
        lambda chat_id, entry, ui_data, full_path=None: dict(items[chat_id]),
    )
    monkeypatch.setattr(chats_api, '_cleanup_missing_chats', lambda chat_data, ui_data, found_chat_ids: (False, False))
    monkeypatch.setattr(chats_api, '_search_match', lambda query, item: True)


def test_chat_list_fav_filter_included(monkeypatch):
    _mock_chat_list(monkeypatch)
    client = _make_test_app().test_client()

    res = client.get('/api/chats/list?fav_filter=included')
    data = res.get_json()

    assert data['success'] is True
    assert [item['id'] for item in data['items']] == ['fav.jsonl']


def test_chat_list_fav_filter_excluded(monkeypatch):
    _mock_chat_list(monkeypatch)
    client = _make_test_app().test_client()

    res = client.get('/api/chats/list?fav_filter=excluded')
    data = res.get_json()

    assert data['success'] is True
    assert [item['id'] for item in data['items']] == ['plain.jsonl']
