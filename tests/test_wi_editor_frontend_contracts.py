from pathlib import Path
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding='utf-8')


def extract_js_function_block(source: str, signature: str) -> str:
    start = source.index(signature)
    brace_start = source.index('{', start)
    depth = 1
    index = brace_start + 1
    while depth > 0:
        char = source[index]
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
        index += 1
    return source[start:index]


def run_js(script: str) -> None:
    subprocess.run(
        ['node', '-e', script],
        cwd=ROOT,
        check=True,
        text=True,
    )


def test_wi_editor_runtime_maps_position_and_role_to_unique_select_values():
    source = read_project_file('static/js/components/wiEditor.js')
    get_block = extract_js_function_block(source, 'getEditorPositionSelectValue(entry) {')
    update_block = extract_js_function_block(source, 'updateEditorPositionFromSelect(entry, rawValue) {')

    script = textwrap.dedent(
        f'''
        const component = {{
          {get_block}
          ,
          {update_block}
        }};

        if (component.getEditorPositionSelectValue({{ position: 4, role: 0 }}) !== '4:0') {{
          throw new Error('expected system at-depth select value');
        }}
        if (component.getEditorPositionSelectValue({{ position: 4, role: 1 }}) !== '4:1') {{
          throw new Error('expected user at-depth select value');
        }}
        if (component.getEditorPositionSelectValue({{ position: 4, role: 2 }}) !== '4:2') {{
          throw new Error('expected assistant at-depth select value');
        }}
        if (component.getEditorPositionSelectValue({{ position: 4, role: 99 }}) !== '4:0') {{
          throw new Error('expected invalid role to fall back to system');
        }}

        const depthEntry = {{ position: 1, role: null }};
        component.updateEditorPositionFromSelect(depthEntry, '4:2');
        if (depthEntry.position !== 4 || depthEntry.role !== 2) {{
          throw new Error('expected at-depth assistant writeback');
        }}

        component.updateEditorPositionFromSelect(depthEntry, '3');
        if (depthEntry.position !== 3 || depthEntry.role !== null) {{
          throw new Error('expected non-depth selection to clear role');
        }}
        '''
    )

    run_js(script)


def test_wi_editor_runtime_preserves_non_depth_positions_and_defaults_invalid_position():
    source = read_project_file('static/js/components/wiEditor.js')
    get_block = extract_js_function_block(source, 'getEditorPositionSelectValue(entry) {')
    update_block = extract_js_function_block(source, 'updateEditorPositionFromSelect(entry, rawValue) {')

    script = textwrap.dedent(
        f'''
        const component = {{
          {get_block},
          {update_block}
        }};

        if (component.getEditorPositionSelectValue({{ position: 6, role: 2 }}) !== '6') {{
          throw new Error('expected non-depth position passthrough');
        }}

        const entry = {{ position: 4, role: 2 }};
        component.updateEditorPositionFromSelect(entry, 'bad-value');
        if (entry.position !== 1 || entry.role !== null) {{
          throw new Error('expected invalid select value to fall back to position 1 and clear role');
        }}
        '''
    )

    run_js(script)
