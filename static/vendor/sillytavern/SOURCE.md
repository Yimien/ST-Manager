# SillyTavern Vendor Source

- Upstream project: SillyTavern
- Upstream local source used for sync: `D:\Workspace\SillyTavern`
- Upstream revision for current vendor snapshot: `004f1336e6e59d476c1043f1dc94c92d028ac5d0`
- License: AGPL-3.0
- Purpose: beautify native ST preview only
- Vendoring strategy: keep `index.html` as a faithful upstream copy and vendor every direct local `href`/`src` dependency it references so the subtree is internally consistent at the file-reference level.
- Scope boundary: this baseline intentionally covers direct `index.html` dependencies first; transitive dependencies referenced deeper by vendored scripts or stylesheets can be added by later tasks if the preview runtime starts consuming them.

## Copied Paths

- `LICENSE`
- `public/index.html`
- `public/manifest.json`
- `public/script.js`
- `public/style.css`
- `public/css/animations.css`
- `public/css/bright.min.css`
- `public/css/fontawesome.min.css`
- `public/css/cropper.min.css`
- `public/css/extensions-panel.css`
- `public/css/group-avatars.css`
- `public/css/jquery-ui.min.css`
- `public/css/macros.css`
- `public/css/solid.min.css`
- `public/css/brands.min.css`
- `public/css/rm-groups.css`
- `public/css/select2-overrides.css`
- `public/css/select2.min.css`
- `public/css/st-tailwind.css`
- `public/css/toastr.min.css`
- `public/css/toggle-dependent.css`
- `public/css/user.css`
- `public/css/world-info.css`
- `public/css/popup.css`
- `public/css/popup-safari-fix.css`
- `public/css/promptmanager.css`
- `public/css/loader.css`
- `public/css/character-group-overlay.css`
- `public/css/file-form.css`
- `public/css/logprobs.css`
- `public/css/accounts.css`
- `public/css/tags.css`
- `public/css/scrollable-button.css`
- `public/css/welcome.css`
- `public/css/data-maid.css`
- `public/css/secrets.css`
- `public/css/backgrounds.css`
- `public/css/chat-backups.css`
- `public/css/mobile-styles.css`
- `public/scripts/i18n.js`
- `public/lib/dialog-polyfill.css`
- `public/lib/cropper.min.js`
- `public/lib/eventemitter.js`
- `public/lib/jquery-3.5.1.min.js`
- `public/lib/jquery-cookie-1.4.1.min.js`
- `public/lib/jquery-cropper.min.js`
- `public/lib/jquery-ui.min.js`
- `public/lib/jquery.izoomify.js`
- `public/lib/jquery.transit.min.js`
- `public/lib/jquery.ui.touch-punch.min.js`
- `public/lib/pagination.js`
- `public/lib/polyfill.js`
- `public/lib/select2-search-placeholder.js`
- `public/lib/select2.min.js`
- `public/lib/structured-clone/monkey-patch.js`
- `public/lib/swiped-events.js`
- `public/lib/toastr.min.js`
- `public/lib/toolcool-color-picker.js`
- `public/favicon.ico`
- `public/img/ai4.png`
- `public/img/apple-icon-57x57.png`
- `public/img/apple-icon-72x72.png`
- `public/img/apple-icon-114x114.png`
- `public/img/apple-icon-144x144.png`
- `public/img/down-arrow.svg`
- `public/img/times-circle.svg`
- `public/sounds/message.mp3`
- `public/webfonts/*`
- `public/index.html` derived shell extraction: `static/vendor/sillytavern/preview-shell.js`

## Local Notes

- Files in this directory are vendored upstream assets unless explicitly marked otherwise.
- Project-authored preview glue should live outside copied upstream files whenever possible.
- The baseline includes `style.css` top-level imports plus directly referenced nested CSS and image assets needed for a self-contained preview runtime.
- `tests/test_beautify_preview_document_contracts.py` verifies the direct local dependencies declared in the vendored `index.html`; keep this list and the copied subtree in sync when refreshing upstream files.
- `preview-shell.js` is a vendor-derived extraction of the preview shell anchors and drawer/frame relationships from `index.html`, kept separate so preview assembly can stay vendor-first without booting upstream runtime scripts.

## Shell Anchors

- `preview-shell.js` preserves these vendor-owned shell anchors from upstream `public/index.html`: `bg1`, `top-bar`, `top-settings-holder`, `leftNavDrawerIcon`, `left-nav-panel`, `rightNavDrawerIcon`, `right-nav-panel`, `sheld`, `chat`, and `form_sheld`.
- The shell module only exposes preview-owned fragment slots for settings drawer content, formatting drawer content, character drawer content, chat markup, and send-form class names.
- The Character Management shell strip is kept aligned with current upstream anchors, including `rightNavHolder` as the drawer root plus `rm_button_characters` and `HotSwapWrapper` inside `CharListButtonAndHotSwaps`.
- Scene switching stays outside the isolated ST frame for Task 2; do not add host-owned scene-switcher markup into `preview-shell.js`.

## Refresh Guidance

- Refresh upstream files from `D:\Workspace\SillyTavern` at a known commit and record the new revision here.
- Re-extract `preview-shell.js` from upstream `public/index.html` without changing shell ownership of the anchor structure.
- Keep preview-specific adaptations in `static/js/components/beautifyPreviewDocument.js` limited to slot fragment assembly.
- Re-run `pytest tests/test_beautify_preview_document_contracts.py -v` after any vendor refresh.
