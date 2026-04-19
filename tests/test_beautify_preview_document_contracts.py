import json
import subprocess
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'static/js/components/beautifyPreviewDocument.js'


def run_preview_document_check(script_body: str) -> None:
    node_script = textwrap.dedent(
        f'''
        import {{ pathToFileURL }} from 'node:url';
        const module = await import(pathToFileURL({json.dumps(str(MODULE_PATH.resolve()))}).href);
        {textwrap.dedent(script_body)}
        '''
    )
    result = subprocess.run(
        ['node', '--input-type=module', '-e', node_script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_build_beautify_preview_document_includes_st_theme_variables_and_key_surfaces():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewDocument({
          theme: {
            main_text_color: '#f8fafc',
            italics_text_color: '#c084fc',
            underline_text_color: '#22d3ee',
            quote_text_color: '#f59e0b',
            blur_tint_color: 'rgba(15, 23, 42, 0.48)',
            chat_tint_color: 'rgba(15, 23, 42, 0.52)',
            user_mes_blur_tint_color: 'rgba(59, 130, 246, 0.22)',
            bot_mes_blur_tint_color: 'rgba(15, 23, 42, 0.58)',
            shadow_color: 'rgba(15, 23, 42, 0.35)',
            border_color: 'rgba(148, 163, 184, 0.24)',
            font_scale: 1.1,
            blur_strength: 12,
            shadow_width: 3,
            chat_width: 55,
            custom_css: 'body { color: red; } #top-bar { border-color: blue; }',
          },
          wallpaperUrl: '/api/beautify/preview-asset/demo.png',
          platform: 'pc',
        });

        if (!html.includes('--SmartThemeBodyColor:#f8fafc')) throw new Error('missing ST body variable');
        if (!html.includes('--SmartThemeEmColor:#c084fc')) throw new Error('missing ST em variable');
        if (!html.includes('--SmartThemeUnderlineColor:#22d3ee')) throw new Error('missing ST underline variable');
        if (!html.includes('--SmartThemeQuoteColor:#f59e0b')) throw new Error('missing ST quote variable');
        if (!html.includes('--SmartThemeBlurTintColor:rgba(15, 23, 42, 0.48)')) throw new Error('missing ST blur tint variable');
        if (!html.includes('--SmartThemeChatTintColor:rgba(15, 23, 42, 0.52)')) throw new Error('missing ST chat tint variable');
        if (!html.includes('--SmartThemeUserMesBlurTintColor:rgba(59, 130, 246, 0.22)')) throw new Error('missing ST user tint variable');
        if (!html.includes('--SmartThemeBotMesBlurTintColor:rgba(15, 23, 42, 0.58)')) throw new Error('missing ST bot tint variable');
        if (!html.includes('--SmartThemeShadowColor:rgba(15, 23, 42, 0.35)')) throw new Error('missing ST shadow variable');
        if (!html.includes('--SmartThemeBorderColor:rgba(148, 163, 184, 0.24)')) throw new Error('missing ST border variable');
        if (!html.includes('--fontScale:1.1')) throw new Error('missing font scale');
        if (!html.includes('--blurStrength:12px')) throw new Error('missing blur strength');
        if (!html.includes('--shadowWidth:3px')) throw new Error('missing shadow width');
        if (!html.includes('--SmartThemeBlurStrength:var(--blurStrength)')) throw new Error('missing ST blur strength alias');
        if (!html.includes('--mainFontSize:calc(var(--fontScale) * 16px)')) throw new Error('missing main font size formula');
        if (!html.includes('--sheldWidth:55vw')) throw new Error('missing chat width');
        if (!html.includes('--wallpaperUrl:url("/api/beautify/preview-asset/demo.png")')) throw new Error('missing wallpaper css variable');
        if (!html.includes('id="top-bar"')) throw new Error('missing top bar');
        if (!html.includes('id="chat"')) throw new Error('missing chat surface');
        if (!html.includes('class="mes ')) throw new Error('missing ST message wrapper');
        if (!html.includes('class="mes_block"')) throw new Error('missing ST message block');
        if (!html.includes('class="mesAvatarWrapper"')) throw new Error('missing avatar wrapper');
        if (!html.includes('class="mes_buttons"')) throw new Error('missing message actions');
        if (!html.includes('class="st-preview-settings-drawer"')) throw new Error('missing settings drawer');
        if (!html.includes('class="st-preview-character-panel"')) throw new Error('missing character panel');
        if (!html.includes('id="send_form"')) throw new Error('missing send form');
        if (!html.includes('id="send_but"')) throw new Error('missing send button');
        if (!html.includes('id="top-settings-holder"')) throw new Error('missing top settings holder');
        if (!html.includes('fa-solid')) throw new Error('missing top bar icon classes');
        if (!html.includes('mes_edit')) throw new Error('missing ST message action class');
        if (!html.includes('data-panel-target="character"')) throw new Error('missing character toggle');
        if (!html.includes('data-panel-target="settings"')) throw new Error('missing settings toggle');
        if (!html.includes('body { color: red; }')) throw new Error('missing custom css');
        '''
    )


def test_build_beautify_preview_sample_markup_contains_rich_message_surfaces():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewSampleMarkup('pc');
        for (const token of [
          '<strong>',
          '<em>',
          '<u>',
          '<blockquote>',
          '<pre><code>',
          '<code>inline code</code>',
          '<ul>',
          '<hr',
          '<a href="#">',
          'id="chat"',
          'class="mesAvatarWrapper"',
          'class="name_text',
          'class="mes_buttons"',
          'class="mes_reasoning_summary"',
          'id="send_form"',
          'id="send_textarea"',
          'id="send_but"',
          'fa-solid',
          'mes_edit',
          'data-panel-target="character"',
          'data-panel-target="settings"',
          'id="table_drawer_content"'
        ]) {
          if (!html.includes(token)) throw new Error(`missing token: ${token}`);
        }
        '''
    )


def test_build_beautify_preview_markup_keeps_icon_only_controls_without_text_labels_in_buttons():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewSampleMarkup('pc');

        if (html.includes('>Character<')) throw new Error('top bar text label should not render inside button');
        if (html.includes('>Settings<')) throw new Error('top bar text label should not render inside button');
        if (html.includes('>Fg<')) throw new Error('message action fallback text should not render in markup');
        if (html.includes('>Ed<')) throw new Error('message action fallback text should not render in markup');
        if (html.includes('>Ct<')) throw new Error('input action fallback text should not render in markup');
        if (html.includes('>Sd<')) throw new Error('input action fallback text should not render in markup');
        '''
    )


def test_build_beautify_preview_theme_vars_normalizes_and_clamps_theme_inputs():
    run_preview_document_check(
        '''
        const vars = module.buildBeautifyPreviewThemeVars({
          font_scale: 'bad-value',
          blur_strength: -4,
          shadow_width: -2,
          chat_width: 300,
        }, '');

        if (vars['--fontScale'] !== '1') throw new Error(`expected normalized fontScale, got ${vars['--fontScale']}`);
        if (vars['--blurStrength'] !== '0px') throw new Error(`expected clamped blurStrength, got ${vars['--blurStrength']}`);
        if (vars['--shadowWidth'] !== '0px') throw new Error(`expected clamped shadowWidth, got ${vars['--shadowWidth']}`);
        if (vars['--SmartThemeBlurStrength'] !== 'var(--blurStrength)') throw new Error(`expected derived SmartThemeBlurStrength, got ${vars['--SmartThemeBlurStrength']}`);
        if (vars['--sheldWidth'] !== '100vw') throw new Error(`expected clamped sheldWidth, got ${vars['--sheldWidth']}`);
        '''
    )


def test_build_beautify_preview_document_preserves_platform_marker_and_escapes_css_sensitive_content():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewDocument({
          theme: {
            custom_css: 'body::before{content:"</style><script>window.BAD=1</script>";}',
          },
          wallpaperUrl: 'https://example.com/a") ;background:red;/*\\unsafe',
          platform: 'mobile',
          baseCss: 'body::after{content:"</style><script>window.BASE_BAD=1</script>";}',
        });

        if (!html.includes('data-platform="mobile"')) throw new Error('missing mobile platform marker');
        if (!html.includes('>Mobile<')) throw new Error('missing mobile label');
        if (html.includes('</style><script>window.BAD=1</script>')) throw new Error('custom css escaped unsafely');
        if (html.includes('</style><script>window.BASE_BAD=1</script>')) throw new Error('base css escaped unsafely');
        if (!html.includes('<\\/style><script>window.BAD=1</script>')) throw new Error('custom css escape marker missing');
        if (!html.includes('<\\/style><script>window.BASE_BAD=1</script>')) throw new Error('base css escape marker missing');
        if (!html.includes('--wallpaperUrl:url("https://example.com/a\\\") ;background:red;/*\\\\unsafe")')) {
          throw new Error('wallpaper url not escaped for css url syntax');
        }
        '''
    )


def test_build_beautify_preview_document_injects_base_css_and_normalizes_unknown_platform_to_pc():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewDocument({
          platform: 'tablet',
          baseCss: '.st-preview-root { outline: 1px solid red; }',
        });

        if (!html.includes('.st-preview-root { outline: 1px solid red; }')) {
          throw new Error('missing injected base css');
        }
        if (!html.includes('data-platform="pc"')) {
          throw new Error('unexpected platform normalization result');
        }
        if (!html.includes('>PC<')) {
          throw new Error('unexpected platform label normalization result');
        }
        '''
    )


def test_build_beautify_preview_document_keeps_custom_css_inside_document_output_only():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewDocument({
          theme: {
            custom_css: 'body { background: hotpink; } .mes_text { color: lime; } #top-bar { outline: 1px solid red; }',
          },
          platform: 'mobile',
        });

        if (!html.includes('body { background: hotpink; }')) throw new Error('custom css missing from document');
        if (!html.includes('.mes_text { color: lime; }')) throw new Error('message selector missing');
        if (!html.includes('#top-bar { outline: 1px solid red; }')) throw new Error('top-bar selector missing');
        if (!html.includes('data-platform="mobile"')) throw new Error('mobile mode marker missing');
        '''
    )


def test_build_beautify_preview_document_escapes_unsafe_theme_variable_values_in_vars_style_block():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewDocument({
          theme: {
            main_text_color: '</style><script>window.BAD=1</script><style>',
          },
        });

        if (html.includes('</style><script>window.BAD=1</script><style>')) {
          throw new Error('theme variable value escaped unsafely');
        }
        if (!html.includes('--SmartThemeBodyColor:<\\/style><script>window.BAD=1</script><style>')) {
          throw new Error('theme variable escape marker missing');
        }
        '''
    )


def test_st_preview_base_css_defines_core_st_surfaces():
    css = (ROOT / 'static/css/modules/st-preview-base.css').read_text(encoding='utf-8')

    assert ':root {' in css
    assert '--SmartThemeBodyColor:' in css
    assert '--SmartThemeBlurTintColor:' in css
    assert '--SmartThemeBorderColor:' in css
    assert '--SmartThemeShadowColor:' in css
    assert '--SmartThemeQuoteColor:' in css
    assert '--SmartThemeBlurStrength:' in css
    assert 'body {' in css
    assert '#top-bar {' in css
    assert '#chat {' in css
    assert '#top-settings-holder {' in css
    assert '.mes {' in css
    assert '.mes_block {' in css
    assert '.mes_text {' in css
    assert '.mesAvatarWrapper {' in css
    assert '.name_text {' in css
    assert '.mes_buttons {' in css
    assert '.mes_reasoning_summary {' in css
    assert '.mes_text blockquote,' in css or '.mes_text blockquote {' in css
    assert '.mes_text pre code {' in css
    assert '#send_form {' in css
    assert '[class*="fa-"]::before {' in css or "[class*='fa-']::before {" in css
    assert '.st-preview-settings-drawer {' in css
    assert '.drawer-content {' in css
    assert '#table_drawer_content {' in css
    assert '.st-preview-character-panel {' in css
    assert '#send_textarea {' in css
    assert '#send_but {' in css


def test_build_beautify_preview_document_wires_panel_toggle_script_and_default_state():
    run_preview_document_check(
        '''
        const html = module.buildBeautifyPreviewDocument({ platform: 'pc' });

        if (!html.includes('data-active-panel="none"')) throw new Error('missing default panel state');
        if (!html.includes('root.dataset.activePanel')) throw new Error('missing panel toggle runtime');
        if (!html.includes('button.dataset.panelTarget')) throw new Error('missing panel button toggle loop');
        if (!html.includes('aria-pressed')) throw new Error('missing top bar pressed state');
        '''
    )
