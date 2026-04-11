from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')


def test_sidebar_template_places_beautify_last_in_second_resource_row():
    template = read_project_file('templates/components/sidebar.html')

    presets_index = template.index("switchMode('presets')")
    regex_index = template.index("switchMode('regex')")
    scripts_index = template.index("switchMode('scripts')")
    quick_replies_index = template.index("switchMode('quick_replies')")
    beautify_index = template.index("switchMode('beautify')")

    assert presets_index < regex_index < scripts_index < quick_replies_index < beautify_index
    assert '美化' in template[beautify_index: beautify_index + 120]


def test_index_template_includes_dedicated_beautify_grid_view():
    template = read_project_file('templates/index.html')
    assert '{% include "components/grid_beautify.html" %}' in template


def test_beautify_grid_template_exposes_two_pane_stage_and_controls():
    template = read_project_file('templates/components/grid_beautify.html')

    assert '$store.global.currentMode === \"beautify\"' in template or "$store.global.currentMode === 'beautify'" in template
    assert 'beautify-layout' in template
    assert 'beautify-sidebar-pane' in template
    assert 'beautify-stage-pane' in template
    assert '导入主题' in template
    assert '导入壁纸' in template
    assert '立即应用' in template
    assert '安装到 ST' in template
    assert '当前预览为近似效果' in template
    assert 'selectedVariantPlatform === \'pc\'' in template or 'selectedVariantPlatform === "pc"' in template
    assert 'selectedVariantPlatform === \'mobile\'' in template or 'selectedVariantPlatform === "mobile"' in template


def test_beautify_grid_template_keeps_unavailable_device_button_disabled_instead_of_hidden():
    template = read_project_file('templates/components/grid_beautify.html')
    assert ':disabled="!hasPcVariant"' in template or ":disabled='!hasPcVariant'" in template
    assert ':disabled="!hasMobileVariant"' in template or ":disabled='!hasMobileVariant'" in template
