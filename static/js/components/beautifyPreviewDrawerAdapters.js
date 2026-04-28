import {
    CHARACTER_DRAWER_VENDOR_MARKUP,
    FORMATTING_DRAWER_VENDOR_MARKUP,
    SETTINGS_DRAWER_VENDOR_MARKUP,
} from '../../vendor/sillytavern/preview-drawers.js';


function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}


function replaceTextareaValue(markup, id, value) {
    const escapedValue = escapeHtml(value);
    const pattern = new RegExp(`(<textarea[^>]*id="${id}"[^>]*>)([\\s\\S]*?)(</textarea>)`);
    return markup.replace(pattern, `$1${escapedValue}$3`);
}


function replaceInputValue(markup, id, value) {
    const escapedValue = escapeHtml(value);
    const pattern = new RegExp(`(<input[^>]*id="${id}"[^>]*value=")(.*?)("[^>]*>)`);
    if (pattern.test(markup)) {
        return markup.replace(pattern, `$1${escapedValue}$3`);
    }

    const openingTagPattern = new RegExp(`(<input[^>]*id="${id}"[^>]*)(>)`);
    return markup.replace(openingTagPattern, `$1 value="${escapedValue}"$2`);
}


function addAttributesToOpeningTag(markup, selector, attributes) {
    const pattern = new RegExp(`(<[^>]*${selector}[^>]*)(>)`);
    return markup.replace(pattern, (_, openingTagStart, tagEnd) => {
        for (const [name, value] of Object.entries(attributes)) {
            const attributePattern = new RegExp(`\\s${name}="[^"]*"`);
            if (attributePattern.test(openingTagStart)) {
                openingTagStart = openingTagStart.replace(attributePattern, ` ${name}="${escapeHtml(value)}"`);
                continue;
            }

            const classMatch = openingTagStart.match(/ class="[^"]*"/);
            if (classMatch) {
                openingTagStart = openingTagStart.replace(classMatch[0], `${classMatch[0]} ${name}="${escapeHtml(value)}"`);
                continue;
            }

            openingTagStart += ` ${name}="${escapeHtml(value)}"`;
        }

        return `${openingTagStart}${tagEnd}`;
    });
}


function replaceBetween(markup, startToken, endToken, content) {
    const startIndex = markup.indexOf(startToken);
    if (startIndex === -1) {
        return markup;
    }

    const contentStartIndex = startIndex + startToken.length;
    const endIndex = markup.indexOf(endToken, contentStartIndex);
    if (endIndex === -1) {
        return markup;
    }

    return `${markup.slice(0, contentStartIndex)}${content}${markup.slice(endIndex)}`;
}


function insertBefore(markup, token, content) {
    const index = markup.indexOf(token);
    if (index === -1) {
        return markup;
    }

    return `${markup.slice(0, index)}${content}${markup.slice(index)}`;
}


export function buildSettingsDrawerPreviewMarkupFromVendor({ theme = {}, vendorMarkup = SETTINGS_DRAWER_VENDOR_MARKUP } = {}) {
    void theme;

    let markup = vendorMarkup;

    markup = addAttributesToOpeningTag(markup, 'id="ai_response_configuration"', {
        style: 'display: flex; flex-direction: column; gap: 10px;',
    });
    markup = addAttributesToOpeningTag(markup, 'id="ai_module_block_novel"', { style: 'display: none;' });
    markup = addAttributesToOpeningTag(markup, 'id="prompt_cost_block"', { style: 'display: none;' });

    for (const selector of [
        'data-preset-manager-import="kobold"',
        'data-preset-manager-export="kobold"',
        'data-preset-manager-delete="kobold"',
        'data-preset-manager-update="kobold"',
        'data-preset-manager-rename="kobold"',
        'data-preset-manager-new="kobold"',
        'data-preset-manager-restore="kobold"',
    ]) {
        markup = addAttributesToOpeningTag(markup, selector, { 'data-preview-disabled': 'true' });
    }

    return markup;
}


export function buildFormattingDrawerPreviewMarkupFromVendor({
    scenePromptContent = '',
    vendorMarkup = FORMATTING_DRAWER_VENDOR_MARKUP,
} = {}) {
    let markup = vendorMarkup;

    markup = replaceTextareaValue(markup, 'context_story_string', scenePromptContent);
    markup = addAttributesToOpeningTag(markup, 'id="af_master_import"', { 'data-preview-disabled': 'true' });
    markup = addAttributesToOpeningTag(markup, 'id="af_master_export"', { 'data-preview-disabled': 'true' });

    return markup;
}


export function buildCharacterDrawerPreviewMarkupFromVendor({
    identities = {},
    detail = {},
    vendorMarkup = CHARACTER_DRAWER_VENDOR_MARKUP,
} = {}) {
    const packageName = detail.packageName || '';
    const name = identities.character?.name || packageName || 'Preview Character';
    const description = detail.description || '';
    const firstMessage = detail.firstMessage || '';
    const personality = detail.personality || '';
    const creatorNotes = detail.notes || '';
    const tags = Array.isArray(detail.tags) ? detail.tags : [];

    let markup = vendorMarkup;

    markup = replaceBetween(
        markup,
        '<div id="rm_button_selected_ch">',
        '</div>',
        `
                            <h2 class="interactable">${escapeHtml(name)}</h2>
                        `,
    );
    markup = replaceInputValue(markup, 'character_name_pole', name);
    markup = replaceTextareaValue(markup, 'description_textarea', description);
    markup = replaceTextareaValue(markup, 'firstmessage_textarea', firstMessage);

    markup = insertBefore(
        markup,
        '                            <!-- these divs are invisible and used for server communication purposes -->',
        `                            <div id="personality_div" class="title_restorable"><span>Personality</span></div>
                            <textarea id="personality_textarea" name="personality">${escapeHtml(personality)}</textarea>
                            <div id="creator_notes_divider" class="title_restorable"><span>Creator Notes</span></div>
                            <textarea id="creator_notes_textarea" name="creator_notes">${escapeHtml(creatorNotes)}</textarea>
`,
    );

    const tagMarkup = tags
        .map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`)
        .join('');
    markup = replaceBetween(markup, '<div id="tagList" class="tags">', '</div>', tagMarkup);

    const cardMarkup = `
                            <div class="menu_button" data-preview-character-card="primary" data-preview-action="show-detail">
                                <div class="character_name">${escapeHtml(name)}</div>
                                <div class="character_package">${escapeHtml(packageName)}</div>
                                <div class="character_description">${escapeHtml(description)}</div>
                            </div>`;
    markup = replaceBetween(markup, '<div id="rm_print_characters_block" class="flexFlowColumn">', '</div>', cardMarkup);

    markup = addAttributesToOpeningTag(markup, 'id="rm_button_search"', { 'data-preview-action': 'toggle-search' });
    markup = addAttributesToOpeningTag(markup, 'id="charListGridToggle"', { 'data-preview-action': 'toggle-grid' });
    markup = addAttributesToOpeningTag(markup, 'id="rm_button_back"', { 'data-preview-action': 'show-list' });

    for (const selector of [
        'id="rm_button_create"',
        'id="character_import_button"',
        'id="external_import_button"',
        'id="rm_button_group_chats"',
        'id="create_button_label"',
        'id="export_button"',
        'id="delete_button"',
        'id="bulkEditButton"',
        'id="bulkSelectAllButton"',
        'id="bulkDeleteButton"',
    ]) {
        markup = addAttributesToOpeningTag(markup, selector, { 'data-preview-disabled': 'true' });
    }

    markup = addAttributesToOpeningTag(markup, 'id="rm_ch_create_block"', { style: 'display: none;' });
    markup = addAttributesToOpeningTag(markup, 'id="rm_characters_block"', { style: 'display: block;' });

    return markup;
}
