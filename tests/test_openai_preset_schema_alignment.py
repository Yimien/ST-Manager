import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from core.services.preset_editor_schema import build_editor_profile_payload


def test_openai_schema_exposes_required_st_alignment_field_subset():
    profile = build_editor_profile_payload({}, 'openai')

    assert profile['id'] == 'st_chat_completion_preset'
    assert set(profile['fields']) >= {
        'chat_completion_source',
        'openai_model',
        'openrouter_model',
        'custom_url',
        'reverse_proxy',
        'proxy_password',
        'openai_max_context',
        'openai_max_tokens',
        'names_behavior',
        'use_sysprompt',
        'show_thoughts',
        'reasoning_effort',
        'verbosity',
        'function_calling',
        'media_inlining',
        'request_images',
        'request_image_aspect_ratio',
        'request_image_resolution',
        'prompts',
        'prompt_order',
        'extensions',
    }
    assert profile['fields']['use_sysprompt']['section'] == 'templates_and_features'
    assert profile['fields']['media_inlining']['section'] == 'images_and_advanced'
    assert set(profile['fields']['chat_completion_source']['options']) >= {
        'openai',
        'openrouter',
        'custom',
        'claude',
        'azure_openai',
        'zai',
    }
