from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_node_tag_filter_modal_blacklist_regression_script_passes():
    result = subprocess.run(
        ['node', 'tests/tag_filter_modal_blacklist_regression_test.mjs'],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert 'tag_filter_modal_blacklist_regression_test: ok' in result.stdout
