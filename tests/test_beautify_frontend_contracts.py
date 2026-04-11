from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def test_app_registers_beautify_components_and_api_module_contracts():
    app_source = read_project_file('static/js/app.js')
    api_source = read_project_file('static/js/api/beautify.js')

    assert 'import beautifyGrid from "./components/beautifyGrid.js";' in app_source
    assert 'import beautifyPreviewFrame from "./components/beautifyPreviewFrame.js";' in app_source
    assert 'Alpine.data("beautifyGrid", beautifyGrid);' in app_source
    assert 'Alpine.data("beautifyPreviewFrame", beautifyPreviewFrame);' in app_source

    assert 'export async function listBeautifyPackages(' in api_source
    assert 'export async function getBeautifyPackage(' in api_source
    assert 'export async function importBeautifyTheme(' in api_source
    assert 'export async function importBeautifyWallpaper(' in api_source
    assert 'export async function installBeautifyVariant(' in api_source
    assert 'export async function applyBeautifyVariant(' in api_source


def test_state_and_header_sources_add_beautify_mode_search_and_selection_state():
    state_source = read_project_file('static/js/state.js')
    header_source = read_project_file('static/js/components/header.js')

    assert 'beautifyList: [],' in state_source
    assert 'beautifySearch: "",' in state_source
    assert 'beautifyPlatformFilter: "all",' in state_source
    assert 'beautifyInstallFilter: "all",' in state_source
    assert 'beautifySelectedPackageId: "",' in state_source
    assert 'beautifySelectedVariantId: "",' in state_source
    assert 'beautifySelectedWallpaperId: "",' in state_source
    assert 'beautifyPreviewDevice: "pc",' in state_source

    assert '"beautify",' in header_source
    assert 'get beautifySearch() {' in header_source
    assert 'set beautifySearch(val) {' in header_source


def test_sidebar_and_layout_sources_route_beautify_mode_and_mobile_upload_contracts():
    sidebar_source = read_project_file('static/js/components/sidebar.js')
    layout_source = read_project_file('static/js/components/layout.js')

    assert "mode === 'beautify'" in sidebar_source
    assert 'window.stUploadBeautifyThemeFiles' in sidebar_source
    assert 'window.dispatchEvent(new CustomEvent(\'refresh-beautify-list\'' in sidebar_source or 'window.dispatchEvent(new CustomEvent("refresh-beautify-list"' in sidebar_source
    assert "mode !== 'cards' && mode !== 'worldinfo' && mode !== 'chats' && mode !== 'beautify'" in layout_source or "mode !== 'beautify'" in layout_source
