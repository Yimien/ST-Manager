from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_node_chat_reader_page_perf_policy_script_passes():
    result = subprocess.run(
        ['node', 'tests/chat_reader_page_perf_policy_test.mjs'],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert 'chat_reader_page_perf_policy_test: ok' in result.stdout
