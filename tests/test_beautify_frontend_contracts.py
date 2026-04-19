from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def assert_contains_any(text, variants):
    assert any(variant in text for variant in variants), f'Missing expected variants: {variants}'


def test_index_template_lifts_beautify_scope_to_main_container_above_shared_includes():
    template = read_project_file('templates/index.html')

    main_container_index = template.index('<div class="main-container" x-data="beautifyGrid">')
    sidebar_index = template.index('{% include "components/sidebar.html" %}')
    beautify_grid_index = template.index('{% include "components/grid_beautify.html" %}')

    assert main_container_index < sidebar_index < beautify_grid_index


def test_sidebar_template_hosts_beautify_toolbar_filters_and_package_list_contract():
    sidebar_template = read_project_file('templates/components/sidebar.html')
    theme_change_handlers = (
        '@change="handleThemeFiles($event.target.files); $event.target.value = \'\'"',
        '@change="handleThemeFiles($event.target.files); $event.target.value = \"\""',
    )
    wallpaper_change_handlers = (
        '@change="handleWallpaperFiles($event.target.files); $event.target.value = \'\'"',
        '@change="handleWallpaperFiles($event.target.files); $event.target.value = \"\""',
    )

    assert "currentMode === 'beautify' && visibleSidebar" in sidebar_template
    assert 'beautify-sidebar-panel' in sidebar_template
    assert 'class="flex-1 flex flex-col overflow-hidden bg-[var(--bg-panel)] beautify-sidebar-panel beautify-sidebar-pane"' in sidebar_template
    assert 'beautify-toolbar' in sidebar_template
    assert 'beautify-package-list custom-scrollbar' in sidebar_template
    assert 'x-model.debounce.200ms="beautifySearch"' in sidebar_template
    assert 'x-model="platformFilter"' in sidebar_template
    assert 'x-model="installFilter"' in sidebar_template
    assert '@click="fetchPackages()"' in sidebar_template
    assert any(handler in sidebar_template for handler in theme_change_handlers)
    assert any(handler in sidebar_template for handler in wallpaper_change_handlers)
    assert 'filteredPackages' in sidebar_template
    assert '@click="selectPackage(item.id)"' in sidebar_template
    assert 'selectedPackageId === item.id' in sidebar_template


def test_app_js_registers_beautify_runtime_components():
    app_js = read_project_file('static/js/app.js')

    assert_contains_any(app_js, ('import beautifyGrid from "./components/beautifyGrid.js";', "import beautifyGrid from './components/beautifyGrid.js';"))
    assert_contains_any(app_js, ('import beautifyPreviewFrame from "./components/beautifyPreviewFrame.js";', "import beautifyPreviewFrame from './components/beautifyPreviewFrame.js';"))
    assert_contains_any(app_js, ('Alpine.data("beautifyGrid", beautifyGrid);', "Alpine.data('beautifyGrid', beautifyGrid);"))
    assert_contains_any(app_js, ('Alpine.data("beautifyPreviewFrame", beautifyPreviewFrame);', "Alpine.data('beautifyPreviewFrame', beautifyPreviewFrame);"))


def test_beautify_api_exports_core_runtime_helpers():
    beautify_api = read_project_file('static/js/api/beautify.js')

    expected_exports = (
        'listBeautifyPackages',
        'getBeautifyPackage',
        'importBeautifyTheme',
        'importBeautifyWallpaper',
        'updateBeautifyVariant',
        'installBeautifyVariant',
        'applyBeautifyVariant',
        'deleteBeautifyPackage',
        'buildBeautifyPreviewAssetUrl',
    )

    for export_name in expected_exports:
        assert_contains_any(
            beautify_api,
            (
                f'export async function {export_name}(',
                f'export function {export_name}(',
            ),
        )


def test_state_js_keeps_beautify_store_keys():
    state_js = read_project_file('static/js/state.js')

    expected_keys = (
        'beautifyList',
        'beautifySearch',
        'beautifyPlatformFilter',
        'beautifyInstallFilter',
        'beautifySelectedPackageId',
        'beautifySelectedVariantId',
        'beautifySelectedWallpaperId',
        'beautifyPreviewDevice',
        'beautifyActiveDetail',
        'beautifyActiveVariant',
        'beautifyActiveWallpaper',
    )

    for key in expected_keys:
        assert_contains_any(state_js, (f'{key}:', f'"{key}":', f"'{key}':"))


def test_header_js_binds_beautify_search_and_mobile_upload_mode():
    header_js = read_project_file('static/js/components/header.js')

    assert_contains_any(header_js, ('"beautify"', "'beautify'"))
    assert_contains_any(header_js, ('get beautifySearch()', 'get beautifySearch ()'))
    assert_contains_any(header_js, ('return this.$store.global.beautifySearch;', 'return this.$store.global.beautifySearch || "";', "return this.$store.global.beautifySearch || '';"))
    assert_contains_any(header_js, ('set beautifySearch(val)', 'set beautifySearch (val)'))
    assert 'this.$store.global.beautifySearch = val;' in header_js
    assert_contains_any(header_js, ('new CustomEvent("request-mobile-upload")', "new CustomEvent('request-mobile-upload')"))


def test_layout_or_sidebar_keeps_beautify_mode_refresh_and_upload_routing():
    layout_js = read_project_file('static/js/components/layout.js')
    sidebar_js = read_project_file('static/js/components/sidebar.js')

    assert_contains_any(layout_js, ('mode !== "beautify"', "mode !== 'beautify'"))
    assert_contains_any(layout_js, ('mode === "beautify"', "mode === 'beautify'"))
    assert_contains_any(layout_js, ('new CustomEvent("refresh-beautify-list")', "new CustomEvent('refresh-beautify-list')"))

    assert_contains_any(sidebar_js, ('const mode = this.currentMode;',))
    assert_contains_any(sidebar_js, ('mode === "beautify"', "mode === 'beautify'"))
    assert_contains_any(sidebar_js, ('window.stUploadBeautifyThemeFiles(files);',))
    assert_contains_any(sidebar_js, ('window.dispatchEvent(new CustomEvent("refresh-beautify-list"));', "window.dispatchEvent(new CustomEvent('refresh-beautify-list'));"))


def test_beautify_preview_document_module_exports_document_builder_contract():
    module_source = read_project_file('static/js/components/beautifyPreviewDocument.js')

    assert 'export function buildBeautifyPreviewDocument(' in module_source
    assert 'export function buildBeautifyPreviewThemeVars(' in module_source
    assert 'export function buildBeautifyPreviewSampleMarkup(' in module_source
    assert 'function buildPreviewBehaviorScript(' in module_source


def test_beautify_preview_frame_uses_render_isolated_html_and_preview_document_builder():
    source = read_project_file('static/js/components/beautifyPreviewFrame.js')

    assert 'renderIsolatedHtml' in source
    assert 'clearIsolatedHtml' in source
    assert 'buildBeautifyPreviewDocument' in source
    assert 'buildBeautifyPreviewAssetUrl' in source
    assert 'customCssMarkup()' not in source
    assert 'minHeight: state.platform === \'mobile\' ? 760 : 900' in source or 'minHeight: state.platform === "mobile" ? 760 : 900' in source
    assert 'maxHeight: state.platform === \'mobile\' ? 3200 : 4800' in source or 'maxHeight: state.platform === "mobile" ? 3200 : 4800' in source


def test_beautify_preview_frame_resets_css_cache_after_load_failures():
    source = read_project_file('static/js/components/beautifyPreviewFrame.js')

    assert 'if (!res.ok)' in source
    assert 'previewBaseCssPromise = null;' in source
    assert '.catch((error) => {' in source


def test_beautify_preview_frame_gracefully_degrades_when_base_css_loading_fails():
    source = read_project_file('static/js/components/beautifyPreviewFrame.js')

    assert 'async function resolvePreviewBaseCss() {' in source
    assert "console.warn('Beautify preview base CSS unavailable, using inline preview styles only.'" in source
    assert 'resolvePreviewBaseCss().then((css) => {' in source
    assert 'this.previewBaseCss = css;' in source
    assert 'if (!host) {' in source


def test_beautify_preview_frame_retries_render_after_preview_host_ref_appears():
    source = read_project_file('static/js/components/beautifyPreviewFrame.js')

    assert 'this.$nextTick(() =>' in source
    assert 'this.renderPreview();' in source
    assert "this.$watch('$store.global.beautifyActiveDetail'" in source
    assert "this.$watch('$store.global.beautifyActiveVariant'" in source
    assert "this.$watch('$store.global.beautifyActiveWallpaper'" in source
    assert "this.$watch('$store.global.beautifyPreviewDevice'" in source


def test_beautify_preview_frame_clears_runtime_when_active_detail_disappears():
    source = read_project_file('static/js/components/beautifyPreviewFrame.js')

    assert "this.$watch('$store.global.beautifyActiveDetail', (detail) => {" in source
    assert 'if (!detail) {' in source
    assert 'this.destroy();' in source


def test_beautify_preview_frame_falls_back_to_dom_query_when_alpine_ref_is_unavailable():
    source = read_project_file('static/js/components/beautifyPreviewFrame.js')

    assert 'this.$refs.previewHost' in source
    assert "querySelector('.beautify-preview-host')" in source or 'querySelector(".beautify-preview-host")' in source
