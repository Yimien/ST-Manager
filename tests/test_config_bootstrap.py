import json
import logging
import sys
from io import StringIO
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module
from core import config as config_module


def test_ensure_config_file_creates_default_config_when_missing(tmp_path, monkeypatch):
    target = tmp_path / 'config.json'
    monkeypatch.setattr(config_module, 'CONFIG_FILE', str(target))

    created = config_module.ensure_config_file()

    assert created is True
    assert target.exists()
    assert json.loads(target.read_text(encoding='utf-8')) == config_module.normalize_config()


def test_ensure_config_file_applies_default_overrides(tmp_path, monkeypatch):
    target = tmp_path / 'config.json'
    monkeypatch.setattr(config_module, 'CONFIG_FILE', str(target))

    created = config_module.ensure_config_file({'host': '0.0.0.0', 'port': 8001})

    assert created is True
    raw = json.loads(target.read_text(encoding='utf-8'))
    assert raw['host'] == '0.0.0.0'
    assert raw['port'] == 8001


def test_ensure_config_file_does_not_overwrite_existing_file(tmp_path, monkeypatch):
    target = tmp_path / 'config.json'
    target.write_text(json.dumps({'host': '1.2.3.4', 'port': 9000}), encoding='utf-8')
    original = target.read_text(encoding='utf-8')
    monkeypatch.setattr(config_module, 'CONFIG_FILE', str(target))

    created = config_module.ensure_config_file({'host': '0.0.0.0'})

    assert created is False
    assert target.read_text(encoding='utf-8') == original


def test_load_config_warns_when_existing_file_is_invalid(tmp_path, monkeypatch, caplog):
    target = tmp_path / 'config.json'
    target.write_text('{invalid json', encoding='utf-8')
    monkeypatch.setattr(config_module, 'CONFIG_FILE', str(target))

    with caplog.at_level(logging.WARNING):
        cfg = config_module.load_config()

    assert cfg == config_module.normalize_config()
    assert target.read_text(encoding='utf-8') == '{invalid json'
    assert 'config.json could not be parsed' in caplog.text
    assert 'falling back to defaults for the current process' in caplog.text


def test_get_default_config_overrides_uses_docker_host():
    assert app_module.get_default_config_overrides(True) == {'host': '0.0.0.0'}


def test_get_default_config_overrides_uses_localhost_outside_docker():
    assert app_module.get_default_config_overrides(False) is None


def test_is_running_in_docker_detects_docker_cgroup_marker(monkeypatch):
    real_exists = app_module.os.path.exists

    def fake_exists(path):
        if path == '/.dockerenv':
            return False
        if path == '/proc/1/cgroup':
            return True
        return real_exists(path)

    def fake_open(path, *args, **kwargs):
        if path == '/proc/1/cgroup':
            return StringIO('12:memory:/docker/abcdef\n')
        return open(path, *args, **kwargs)

    monkeypatch.setattr(app_module.os.path, 'exists', fake_exists)
    monkeypatch.setattr(app_module, 'open', fake_open, raising=False)

    assert app_module.is_running_in_docker() is True


def test_is_running_in_docker_detects_containerd_cgroup_marker(monkeypatch):
    real_exists = app_module.os.path.exists

    def fake_exists(path):
        if path == '/.dockerenv':
            return False
        if path == '/proc/1/cgroup':
            return True
        return real_exists(path)

    def fake_open(path, *args, **kwargs):
        if path == '/proc/1/cgroup':
            return StringIO('12:memory:/containerd/io.containerd.runtime.v2.task/k8s.io/abcdef\n')
        return open(path, *args, **kwargs)

    monkeypatch.setattr(app_module.os.path, 'exists', fake_exists)
    monkeypatch.setattr(app_module, 'open', fake_open, raising=False)

    assert app_module.is_running_in_docker() is True


def test_resolve_server_settings_prefers_cli_over_config(monkeypatch):
    monkeypatch.delenv('FLASK_DEBUG', raising=False)
    cfg = {'host': '127.0.0.1', 'port': 5000}
    cli_args = Namespace(debug=True, host='0.0.0.0', port=7000)

    host, port, debug = app_module.resolve_server_settings(cfg, cli_args)

    assert host == '0.0.0.0'
    assert port == 7000
    assert debug is True


def test_resolve_server_settings_uses_cli_port_zero(monkeypatch):
    monkeypatch.delenv('FLASK_DEBUG', raising=False)
    cfg = {'host': '127.0.0.1', 'port': 5000}
    cli_args = Namespace(debug=False, host=None, port=0)

    host, port, debug = app_module.resolve_server_settings(cfg, cli_args)

    assert host == '127.0.0.1'
    assert port == 0
    assert debug is False


def test_resolve_server_settings_uses_flask_debug_env(monkeypatch):
    monkeypatch.setenv('FLASK_DEBUG', '1')
    cfg = {'host': '127.0.0.1', 'port': 5000}
    cli_args = Namespace(debug=False, host=None, port=None)

    host, port, debug = app_module.resolve_server_settings(cfg, cli_args)

    assert host == '127.0.0.1'
    assert port == 5000
    assert debug is True


def test_parse_cli_args_accepts_debug_host_and_port():
    args = app_module.parse_cli_args(['--debug', '--host', '0.0.0.0', '--port', '9001'])

    assert args.debug is True
    assert args.host == '0.0.0.0'
    assert args.port == 9001


def test_cli_resolution_does_not_persist_config_changes(tmp_path, monkeypatch):
    target = tmp_path / 'config.json'
    target.write_text(json.dumps({'host': '127.0.0.1', 'port': 5000}), encoding='utf-8')
    monkeypatch.setattr(config_module, 'CONFIG_FILE', str(target))
    cfg = config_module.load_config()
    cli_args = Namespace(debug=False, host='0.0.0.0', port=8123)
    before = target.read_text(encoding='utf-8')

    host, port, debug = app_module.resolve_server_settings(cfg, cli_args)

    assert (host, port, debug) == ('0.0.0.0', 8123, False)
    assert cfg['host'] == '127.0.0.1'
    assert cfg['port'] == 5000
    assert target.read_text(encoding='utf-8') == before


def test_ensure_startup_config_passes_docker_default_overrides(monkeypatch):
    captured = {}

    def fake_ensure_config_file(default_overrides=None):
        captured['default_overrides'] = default_overrides

    monkeypatch.setattr(app_module, 'ensure_config_file', fake_ensure_config_file)

    app_module.ensure_startup_config(True)

    assert captured['default_overrides'] == {'host': '0.0.0.0'}
