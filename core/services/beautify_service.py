import copy
import hashlib
import json
import logging
import os
import shutil
import time
from typing import Callable, Dict, Optional

from PIL import Image

from core.config import get_beautify_folder
from core.data.ui_store import get_beautify_library, load_ui_data, save_ui_data, set_beautify_library
from core.services.st_client import STClient


logger = logging.getLogger(__name__)


class BeautifyService:
    def __init__(
        self,
        library_root: Optional[str] = None,
        st_data_dir: Optional[str] = None,
        st_client: Optional[STClient] = None,
        ui_data_loader: Optional[Callable[[], Dict]] = None,
        ui_data_saver: Optional[Callable[[Dict], bool]] = None,
    ):
        self.library_root = os.path.abspath(library_root or get_beautify_folder())
        self.st_client = st_client or STClient(st_data_dir=st_data_dir)
        self._ui_data_loader = ui_data_loader or load_ui_data
        self._ui_data_saver = ui_data_saver or save_ui_data
        os.makedirs(self.library_root, exist_ok=True)

    def _project_root_for_library(self):
        normalized = self.library_root.replace('\\', '/').rstrip('/')
        suffix = '/data/library/beautify'
        if normalized.endswith(suffix):
            return normalized[: -len(suffix)]
        return os.path.dirname(os.path.dirname(os.path.dirname(self.library_root)))

    def _load_ui_data(self):
        data = self._ui_data_loader() or {}
        if not isinstance(data, dict):
            return {}
        return data

    def _save_library(self, ui_data: Dict, library_payload: Dict):
        changed = set_beautify_library(ui_data, library_payload)
        if changed:
            self._ui_data_saver(copy.deepcopy(ui_data))
        return changed

    def load_library(self):
        return get_beautify_library(self._load_ui_data())

    def list_packages(self):
        library = self.load_library()
        packages = []
        for package_info in library.get('packages', {}).values():
            variants = list(package_info.get('variants', {}).values())
            wallpapers = list(package_info.get('wallpapers', {}).values())
            packages.append(
                {
                    'id': package_info['id'],
                    'name': package_info.get('name') or package_info['id'],
                    'author': package_info.get('author', ''),
                    'variant_count': len(variants),
                    'wallpaper_count': len(wallpapers),
                    'platforms': sorted({variant.get('platform', 'dual') for variant in variants}),
                    'updated_at': package_info.get('updated_at', 0),
                    'install_state': copy.deepcopy(package_info.get('install_state', {})),
                    'wallpaper_previews': [wallpaper.get('file', '') for wallpaper in wallpapers[:3]],
                }
            )
        return sorted(packages, key=lambda item: (-(item.get('updated_at') or 0), item['name'].lower()))

    def get_package(self, package_id: str):
        library = self.load_library()
        package = library.get('packages', {}).get(str(package_id or '').strip())
        if not package:
            return None

        result = copy.deepcopy(package)
        for variant_id, variant in result.get('variants', {}).items():
            variant['theme_data'] = self._load_theme_data(variant.get('theme_file', ''))
            result['variants'][variant_id] = variant
        return result

    def import_theme(self, source_path: str, package_id: Optional[str] = None, platform: Optional[str] = None, source_name: Optional[str] = None):
        if not source_path or not os.path.isfile(source_path):
            raise ValueError('主题文件不存在')

        theme_payload = self._load_theme_payload(source_path)
        source_hint = source_name or source_path
        guessed_platform, needs_review = self.guess_platform(source_hint, theme_payload.get('name', ''), package_name='')
        resolved_platform = self._normalize_platform(platform) or guessed_platform
        if platform:
            needs_review = False

        ui_data = self._load_ui_data()
        library = get_beautify_library(ui_data)
        packages = dict(library.get('packages', {}))

        package_name = str(theme_payload.get('name') or '').strip() or PathLike.basename_without_ext(source_hint) or '未命名主题'
        resolved_package_id = str(package_id or '').strip() or self._build_package_id(package_name, packages)
        package_info = copy.deepcopy(packages.get(resolved_package_id) or self._build_empty_package(resolved_package_id, package_name))
        package_info['name'] = package_info.get('name') or package_name

        existing_variant = self._find_variant_by_platform(package_info, resolved_platform)
        variant_id = existing_variant['id'] if existing_variant else f'var_{resolved_platform}_{self._short_hash(source_path + str(time.time()))}'
        themes_dir = os.path.join(self.library_root, 'packages', resolved_package_id, 'themes')
        os.makedirs(themes_dir, exist_ok=True)

        target_file = os.path.join(themes_dir, f'{resolved_platform}.json')
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(theme_payload, f, ensure_ascii=False, indent=2)

        preview_accuracy = 'approx' if self._theme_has_custom_css(theme_payload) else ('approx' if resolved_platform in ('pc', 'mobile') else 'base')
        relative_theme_file = os.path.relpath(target_file, self._project_root_for_library()).replace('\\', '/')
        package_info['variants'][variant_id] = {
            'id': variant_id,
            'platform': resolved_platform,
            'theme_name': str(theme_payload.get('name') or package_info['name']).strip(),
            'theme_file': relative_theme_file,
            'wallpaper_ids': list((existing_variant or {}).get('wallpaper_ids', [])),
            'preview_hint': {
                'needs_platform_review': needs_review,
                'preview_accuracy': preview_accuracy,
            },
        }
        package_info['cover_variant_id'] = package_info.get('cover_variant_id') or variant_id
        now = int(time.time())
        package_info['updated_at'] = now
        if not package_info.get('created_at'):
            package_info['created_at'] = now
        packages[resolved_package_id] = package_info
        library['packages'] = packages
        self._save_library(ui_data, library)

        return {
            'package': copy.deepcopy(package_info),
            'variant': copy.deepcopy(package_info['variants'][variant_id]),
            'theme': theme_payload,
        }

    def update_variant(self, package_id: str, variant_id: str, platform: str):
        resolved_platform = self._normalize_platform(platform)
        if not resolved_platform:
            raise ValueError('无效的端类型')

        ui_data = self._load_ui_data()
        library, package_info, variant = self._load_package_variant(ui_data, package_id, variant_id)
        if variant.get('platform') != resolved_platform:
            conflict = self._find_variant_by_platform(package_info, resolved_platform)
            if conflict and conflict.get('id') != variant_id:
                raise ValueError('目标端类型已存在，请先调整或替换现有变体')

            old_theme_path = self._resolve_project_relative_path(variant.get('theme_file', ''))
            new_theme_path = os.path.join(self.library_root, 'packages', package_info['id'], 'themes', f'{resolved_platform}.json')
            os.makedirs(os.path.dirname(new_theme_path), exist_ok=True)
            if old_theme_path and os.path.exists(old_theme_path) and os.path.abspath(old_theme_path) != os.path.abspath(new_theme_path):
                if os.path.exists(new_theme_path):
                    os.remove(new_theme_path)
                shutil.move(old_theme_path, new_theme_path)
            variant['platform'] = resolved_platform
            variant['theme_file'] = os.path.relpath(new_theme_path, self._project_root_for_library()).replace('\\', '/')

        preview_hint = copy.deepcopy(variant.get('preview_hint') or {})
        preview_hint['needs_platform_review'] = False
        variant['preview_hint'] = preview_hint

        package_info['variants'][variant_id] = variant
        package_info['updated_at'] = int(time.time())
        library['packages'][package_info['id']] = package_info
        self._save_library(ui_data, library)
        return copy.deepcopy(variant)

    def import_wallpaper(self, package_id: str, variant_id: str, source_path: str, source_name: Optional[str] = None):
        if not source_path or not os.path.isfile(source_path):
            raise ValueError('壁纸文件不存在')

        ui_data = self._load_ui_data()
        library, package_info, variant = self._load_package_variant(ui_data, package_id, variant_id)

        wallpapers_dir = os.path.join(self.library_root, 'packages', package_info['id'], 'wallpapers')
        os.makedirs(wallpapers_dir, exist_ok=True)

        original_name = source_name or os.path.basename(source_path)
        target_name = self._build_unique_filename(wallpapers_dir, original_name)
        target_file = os.path.join(wallpapers_dir, target_name)
        shutil.copy2(source_path, target_file)

        with Image.open(target_file) as image:
            width, height = image.size

        wallpaper_id = f'wp_{self._short_hash(target_file + str(time.time()))}'
        relative_file = os.path.relpath(target_file, self._project_root_for_library()).replace('\\', '/')
        package_info['wallpapers'][wallpaper_id] = {
            'id': wallpaper_id,
            'variant_id': variant_id,
            'file': relative_file,
            'filename': target_name,
            'width': width,
            'height': height,
            'mtime': int(os.path.getmtime(target_file)),
        }

        wallpaper_ids = list(variant.get('wallpaper_ids', []))
        wallpaper_ids.append(wallpaper_id)
        variant['wallpaper_ids'] = wallpaper_ids
        package_info['variants'][variant_id] = variant
        package_info['updated_at'] = int(time.time())
        library['packages'][package_info['id']] = package_info
        self._save_library(ui_data, library)

        return {
            'package': copy.deepcopy(package_info),
            'variant': copy.deepcopy(variant),
            'wallpaper': copy.deepcopy(package_info['wallpapers'][wallpaper_id]),
        }

    def install_variant(self, package_id: str, variant_id: str, wallpaper_id: Optional[str] = None):
        ui_data = self._load_ui_data()
        library, package_info, variant = self._load_package_variant(ui_data, package_id, variant_id)

        themes_dir = self.st_client.get_themes_dir()
        backgrounds_dir = self.st_client.get_backgrounds_dir()
        if not themes_dir or not backgrounds_dir:
            raise ValueError('未找到 SillyTavern themes/backgrounds 目录')

        theme_source = self._resolve_project_relative_path(variant.get('theme_file', ''))
        if not theme_source or not os.path.exists(theme_source):
            raise ValueError('主题文件缺失，无法安装')

        theme_filename = f"stm-beautify-{package_info['id']}-{variant['platform']}.json"
        shutil.copy2(theme_source, os.path.join(themes_dir, theme_filename))

        wallpaper_filename = ''
        if wallpaper_id:
            wallpaper = package_info.get('wallpapers', {}).get(wallpaper_id)
            if not wallpaper or wallpaper.get('variant_id') != variant_id:
                raise ValueError('壁纸未绑定到当前变体')
            wallpaper_source = self._resolve_project_relative_path(wallpaper.get('file', ''))
            if not wallpaper_source or not os.path.exists(wallpaper_source):
                raise ValueError('壁纸文件缺失，无法安装')

            wallpaper_index = self._wallpaper_index_for_variant(variant, wallpaper_id)
            ext = os.path.splitext(wallpaper.get('filename') or wallpaper_source)[1] or '.png'
            wallpaper_filename = f"stm-beautify-{package_info['id']}-{variant['platform']}-bg-{wallpaper_index}{ext}"
            shutil.copy2(wallpaper_source, os.path.join(backgrounds_dir, wallpaper_filename))

        install_state = copy.deepcopy(package_info.get('install_state') or {})
        install_state.update(
            {
                'installed_variant_id': variant_id,
                'installed_theme_file': theme_filename,
                'installed_wallpaper_file': wallpaper_filename,
                'last_installed_at': int(time.time()),
            }
        )
        package_info['install_state'] = install_state
        package_info['updated_at'] = int(time.time())
        library['packages'][package_info['id']] = package_info
        self._save_library(ui_data, library)

        return {
            'package': copy.deepcopy(package_info),
            'variant': copy.deepcopy(variant),
            'theme_filename': theme_filename,
            'wallpaper_filename': wallpaper_filename,
        }

    def apply_variant(self, package_id: str, variant_id: str, wallpaper_id: Optional[str] = None):
        install_result = self.install_variant(package_id, variant_id, wallpaper_id)

        settings = self.st_client.read_settings()
        power_user = settings.get('power_user') if isinstance(settings.get('power_user'), dict) else {}
        background = settings.get('background') if isinstance(settings.get('background'), dict) else {}

        power_user['theme'] = install_result['variant'].get('theme_name') or install_result['package'].get('name', '')
        settings['power_user'] = power_user

        if install_result.get('wallpaper_filename'):
            background['name'] = install_result['wallpaper_filename']
            background['url'] = f"url('backgrounds/{install_result['wallpaper_filename']}')"
            settings['background'] = background

        if not self.st_client.write_settings(settings):
            raise ValueError('写入 SillyTavern settings.json 失败')

        ui_data = self._load_ui_data()
        library, package_info, _variant = self._load_package_variant(ui_data, package_id, variant_id)
        install_state = copy.deepcopy(package_info.get('install_state') or {})
        install_state['applied_variant_id'] = variant_id
        install_state['applied_wallpaper_id'] = wallpaper_id or ''
        package_info['install_state'] = install_state
        package_info['updated_at'] = int(time.time())
        library['packages'][package_info['id']] = package_info
        self._save_library(ui_data, library)

        install_result['package'] = copy.deepcopy(package_info)
        return install_result

    def delete_package(self, package_id: str):
        ui_data = self._load_ui_data()
        library = get_beautify_library(ui_data)
        resolved_package_id = str(package_id or '').strip()
        packages = dict(library.get('packages', {}))
        if resolved_package_id not in packages:
            return False

        del packages[resolved_package_id]
        library['packages'] = packages

        package_dir = os.path.join(self.library_root, 'packages', resolved_package_id)
        if os.path.isdir(package_dir):
            shutil.rmtree(package_dir)

        self._save_library(ui_data, library)
        return True

    def get_preview_asset_path(self, subpath: str):
        normalized = str(subpath or '').replace('\\', '/').strip().lstrip('/')
        if not normalized or '..' in normalized.split('/'):
            return None

        candidate = os.path.abspath(os.path.join(self.library_root, normalized.replace('/', os.sep)))
        if os.path.commonpath([candidate, self.library_root]) != self.library_root:
            return None
        if not os.path.exists(candidate) or not os.path.isfile(candidate):
            return None
        return candidate

    def guess_platform(self, source_path: str, theme_name: str = '', package_name: str = ''):
        tokens = ' '.join(
            [
                os.path.basename(source_path or ''),
                str(theme_name or ''),
                str(package_name or ''),
            ]
        ).lower()
        if any(keyword in tokens for keyword in ('mobile', '移动', '手机')):
            return 'mobile', False
        if any(keyword in tokens for keyword in ('pc', '电脑', '桌面')):
            return 'pc', False
        if any(keyword in tokens for keyword in ('dual', '双端', '通用')):
            return 'dual', False
        return 'dual', True

    def _load_theme_payload(self, source_path: str):
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                payload = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError('主题 JSON 无法解析') from exc

        if not isinstance(payload, dict):
            raise ValueError('主题 JSON 格式无效')

        if not payload.get('name'):
            raise ValueError('主题缺少 name 字段')

        if not any(key in payload for key in ('main_text_color', 'chat_tint_color', 'custom_css', 'font_scale')):
            raise ValueError('文件不是有效的 ST theme JSON')

        return payload

    def _normalize_platform(self, platform: Optional[str]):
        value = str(platform or '').strip().lower()
        if value in ('pc', 'mobile', 'dual'):
            return value
        return ''

    def _build_empty_package(self, package_id: str, package_name: str):
        return {
            'id': package_id,
            'name': package_name,
            'author': '',
            'tags': [],
            'notes': '',
            'cover_variant_id': '',
            'created_at': int(time.time()),
            'updated_at': int(time.time()),
            'variants': {},
            'wallpapers': {},
            'install_state': {},
        }

    def _build_package_id(self, package_name: str, existing_packages: Dict):
        base = self._slugify(package_name) or 'theme'
        candidate = f'pkg_{base}'
        if candidate not in existing_packages:
            return candidate
        suffix = self._short_hash(package_name + str(time.time()))
        return f'{candidate}_{suffix}'

    def _slugify(self, value: str):
        normalized = []
        for char in str(value or '').strip().lower():
            if char.isascii() and char.isalnum():
                normalized.append(char)
            elif char in (' ', '-', '_'):
                normalized.append('_')
        slug = ''.join(normalized).strip('_')
        while '__' in slug:
            slug = slug.replace('__', '_')
        return slug

    def _short_hash(self, value: str):
        return hashlib.md5(value.encode('utf-8')).hexdigest()[:8]

    def _theme_has_custom_css(self, payload: Dict):
        return bool(str(payload.get('custom_css') or '').strip())

    def _resolve_project_relative_path(self, relative_path: str):
        if not relative_path:
            return ''
        return os.path.join(self._project_root_for_library(), relative_path.replace('/', os.sep))

    def _load_package_variant(self, ui_data: Dict, package_id: str, variant_id: str):
        library = get_beautify_library(ui_data)
        resolved_package_id = str(package_id or '').strip()
        resolved_variant_id = str(variant_id or '').strip()
        package_info = copy.deepcopy(library.get('packages', {}).get(resolved_package_id))
        if not package_info:
            raise ValueError('美化包不存在')

        variant = copy.deepcopy(package_info.get('variants', {}).get(resolved_variant_id))
        if not variant:
            raise ValueError('变体不存在')

        return library, package_info, variant

    def _build_unique_filename(self, target_dir: str, filename: str):
        base_name, ext = os.path.splitext(filename or '')
        safe_base = base_name.strip() or 'wallpaper'
        safe_ext = ext or '.png'
        candidate = f'{safe_base}{safe_ext}'
        if not os.path.exists(os.path.join(target_dir, candidate)):
            return candidate

        index = 1
        while True:
            candidate = f'{safe_base}-{index}{safe_ext}'
            if not os.path.exists(os.path.join(target_dir, candidate)):
                return candidate
            index += 1

    def _wallpaper_index_for_variant(self, variant: Dict, wallpaper_id: str):
        wallpaper_ids = list(variant.get('wallpaper_ids') or [])
        if wallpaper_id in wallpaper_ids:
            return wallpaper_ids.index(wallpaper_id) + 1
        return 1

    def _find_variant_by_platform(self, package_info: Dict, platform: str):
        for variant in (package_info.get('variants') or {}).values():
            if variant.get('platform') == platform:
                return copy.deepcopy(variant)
        return None

    def _load_theme_data(self, theme_file: str):
        path = self._resolve_project_relative_path(theme_file)
        if not path or not os.path.exists(path):
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception as e:
            logger.warning(f'读取美化主题失败: {e}')
            return {}


class PathLike:
    @staticmethod
    def basename_without_ext(path: str):
        return os.path.splitext(os.path.basename(path or ''))[0].strip()
