function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function escapeCssText(value) {
  return String(value ?? "").replace(/<\/style/gi, "<\\/style");
}

function escapeCssUrl(value) {
  return String(value ?? "")
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/[\r\n\f]/g, " ");
}

function normalizeNumber(value, fallback) {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : fallback;
}

function clampMin(value, minimum) {
  return Math.max(value, minimum);
}

function clampRange(value, minimum, maximum) {
  return Math.min(Math.max(value, minimum), maximum);
}

function serializeCssVars(vars) {
  return Object.entries(vars)
    .filter(
      ([, value]) => value !== "" && value !== null && value !== undefined,
    )
    .map(([key, value]) => `${key}:${escapeCssText(value)}`)
    .join(";");
}

function buildTopBarAction(label, panelTarget, icon) {
  const iconClass =
    panelTarget === "character"
      ? "fa-solid fa-address-card"
      : "fa-solid fa-sliders";
  const iconFallback = panelTarget === "character" ? "⋯" : "≡";
  return `
    <button
      type="button"
      class="drawer-icon closedIcon st-preview-topbar-action ${iconClass}"
      data-panel-target="${escapeHtml(panelTarget)}"
      data-icon-fallback="${escapeHtml(iconFallback)}"
      aria-pressed="false"
      title="${escapeHtml(label)}"
    ></button>
  `;
}

function buildMessageActions() {
  return `
    <div class="mes_buttons">
      <div class="mes_button extraMesButtonsHint fa-solid fa-ellipsis" data-icon-fallback="⋯" title="Message Actions"></div>
      <div class="mes_button mes_bookmark fa-solid fa-flag" data-icon-fallback="⚑" title="Bookmark"></div>
      <div class="mes_button mes_edit fa-solid fa-pencil" data-icon-fallback="✎" title="Edit"></div>
    </div>
  `;
}

function buildReasoningBlock() {
  return `
    <details class="mes_reasoning_details">
      <summary class="mes_reasoning_summary">
        <div class="mes_reasoning_header_block flex-container">
          <div class="mes_reasoning_header flex-container">
            <span class="mes_reasoning_header_title">Thought for some time</span>
            <div class="mes_reasoning_arrow">^</div>
          </div>
        </div>
        <div class="mes_reasoning_actions flex-container">
          <div class="mes_reasoning_copy mes_button fa-solid fa-copy" data-icon-fallback="⧉" aria-label="Copy reasoning"></div>
          <div class="mes_reasoning_edit mes_button fa-solid fa-pencil" data-icon-fallback="✎" aria-label="Edit reasoning"></div>
        </div>
      </summary>
      <div class="mes_reasoning">${escapeHtml("🌿 梧桐絮语：这条预览消息保留了思维链容器，便于主题命中相关选择器。")}</div>
    </details>
  `;
}

function buildMessage({
  mesId,
  name,
  avatarLabel,
  messageHtml,
  timestamp,
  tokenCounter,
  isUser = false,
  isSystem = false,
  includeReasoning = false,
  extraClass = "",
}) {
  const classes = ["mes"];
  if (extraClass) {
    classes.push(extraClass);
  }

  return `
    <div class="${classes.join(" ")}" mesid="${escapeHtml(mesId)}" ch_name="${escapeHtml(name)}" is_user="${isUser ? "true" : "false"}" is_system="${isSystem ? "true" : "false"}">
      <div class="mesAvatarWrapper">
        <div class="avatar">
          <img alt="${escapeHtml(name)}" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='96' height='96' viewBox='0 0 96 96'%3E%3Crect width='96' height='96' rx='24' fill='%23d8e8c8'/%3E%3Ctext x='50%25' y='55%25' font-size='30' text-anchor='middle' fill='%233c5a2a' font-family='Arial'%3E${encodeURIComponent(avatarLabel)}%3C/text%3E%3C/svg%3E">
        </div>
        <div class="mesIDDisplay">#${escapeHtml(mesId)}</div>
        <div class="mes_timer">${escapeHtml(timestamp)}</div>
        <div class="tokenCounterDisplay">${escapeHtml(tokenCounter)}</div>
      </div>
      <div class="mes_block">
        <div class="ch_name flex-container justifySpaceBetween">
          <div class="flex-container flex1 alignitemscenter">
            <div class="flex-container alignItemsBaseline">
              <span class="name_text">${escapeHtml(name)}</span>
              <small class="timestamp">${escapeHtml(timestamp)}</small>
            </div>
          </div>
          ${buildMessageActions()}
        </div>
        ${includeReasoning ? buildReasoningBlock() : ""}
        <div class="mes_text">${messageHtml}</div>
        <div class="mes_media_wrapper"></div>
        <div class="mes_file_wrapper"></div>
        <div class="mes_bias"></div>
      </div>
      <div class="flex-container swipeRightBlock flexFlowColumn flexNoGap">
        <div class="swipe_right">></div>
        <div class="swipes-counter">1/1</div>
      </div>
    </div>
  `;
}

function buildPreviewBehaviorScript() {
  return `
    (() => {
      const root = document.querySelector('.st-preview-root');
      if (!root) return;
      const buttons = Array.from(document.querySelectorAll('[data-panel-target]'));

      const sync = (panel) => {
        root.dataset.activePanel = panel;
        buttons.forEach((button) => {
          const active = button.dataset.panelTarget === panel;
          button.setAttribute('aria-pressed', active ? 'true' : 'false');
          button.classList.toggle('is-active', active);
          button.classList.toggle('openIcon', active);
          button.classList.toggle('closedIcon', !active);
        });
      };

      buttons.forEach((button) => {
        button.addEventListener('click', () => {
          const nextPanel = button.dataset.panelTarget || 'none';
          sync(root.dataset.activePanel === nextPanel ? 'none' : nextPanel);
        });
      });

      sync(root.dataset.activePanel || 'none');
    })();
  `;
}

export function buildBeautifyPreviewThemeVars(theme = {}, wallpaperUrl = "") {
  const fontScale = (() => {
    const normalized = normalizeNumber(theme.font_scale, 1);
    return normalized > 0 ? normalized : 1;
  })();
  const blurStrength = clampMin(normalizeNumber(theme.blur_strength, 10), 0);
  const shadowWidth = clampMin(normalizeNumber(theme.shadow_width, 2), 0);
  const chatWidth = clampRange(normalizeNumber(theme.chat_width, 50), 25, 100);
  const safeWallpaperUrl = wallpaperUrl
    ? `url("${escapeCssUrl(wallpaperUrl)}")`
    : "none";

  return {
    "--SmartThemeBodyColor": theme.main_text_color || "#f8fafc",
    "--SmartThemeEmColor":
      theme.italics_text_color || theme.main_text_color || "#cbd5e1",
    "--SmartThemeUnderlineColor":
      theme.underline_text_color || theme.quote_text_color || "#38bdf8",
    "--SmartThemeQuoteColor": theme.quote_text_color || "#f59e0b",
    "--SmartThemeBlurTintColor":
      theme.blur_tint_color || "rgba(15, 23, 42, 0.48)",
    "--SmartThemeChatTintColor":
      theme.chat_tint_color || "rgba(15, 23, 42, 0.52)",
    "--SmartThemeUserMesBlurTintColor":
      theme.user_mes_blur_tint_color || "rgba(59, 130, 246, 0.22)",
    "--SmartThemeBotMesBlurTintColor":
      theme.bot_mes_blur_tint_color || "rgba(15, 23, 42, 0.58)",
    "--SmartThemeShadowColor": theme.shadow_color || "rgba(15, 23, 42, 0.35)",
    "--SmartThemeBorderColor":
      theme.border_color || "rgba(148, 163, 184, 0.24)",
    "--fontScale": String(fontScale),
    "--blurStrength": `${blurStrength}px`,
    "--shadowWidth": `${shadowWidth}px`,
    "--SmartThemeBlurStrength": "var(--blurStrength)",
    "--mainFontSize": "calc(var(--fontScale) * 16px)",
    "--sheldWidth": `${chatWidth}vw`,
    "--wallpaperUrl": safeWallpaperUrl,
  };
}

export function buildBeautifyPreviewSampleMarkup(platform = "pc") {
  const normalizedPlatform = platform === "mobile" ? "mobile" : "pc";
  const platformLabel = normalizedPlatform === "mobile" ? "Mobile" : "PC";
  const inputHint =
    normalizedPlatform === "mobile"
      ? "🍂 在梧桐树下写点什么..."
      : "Type a message, or /? for help";

  return `
    <div class="st-preview-root" data-platform="${escapeHtml(normalizedPlatform)}" data-active-panel="none">
      <div class="st-preview-wallpaper"></div>
      <div class="st-preview-overlay"></div>
      <div class="st-preview-shell">
        <div id="top-bar">
          <div class="st-preview-brand-block">
            <div class="st-preview-brand">SillyTavern Preview</div>
            <div class="st-preview-chat-meta">Astra · Theme fidelity check · ${escapeHtml(platformLabel)}</div>
          </div>
          <div class="st-preview-platform-chip">${escapeHtml(platformLabel)}</div>
        </div>
        <div id="top-settings-holder">
          <div class="drawer st-preview-topbar-drawer">
            ${buildTopBarAction("Character", "character", "Ch")}
            ${buildTopBarAction("Settings", "settings", "St")}
          </div>
          <div class="drawer-content st-preview-drawer-panel st-preview-settings-drawer" id="table_drawer_content">
            <div class="inline-drawer-header">
              <span class="standoutHeader">Preview Settings</span>
              <span>Panel</span>
            </div>
            <div class="options-content">
              <label class="st-preview-setting-row"><span>Blur Strength</span><input type="range" min="0" max="30" value="10"></label>
              <label class="st-preview-setting-row"><span>Chat Width</span><select><option>Balanced</option></select></label>
              <label class="st-preview-setting-row"><span>Theme Surface</span><input type="text" value="Glass / paper layered shell"></label>
            </div>
          </div>
          <div class="drawer-content st-preview-drawer-panel st-preview-character-panel" id="character_popup">
            <div class="inline-drawer-header">
              <span class="standoutHeader">Character</span>
              <span>Panel</span>
            </div>
            <div class="st-preview-character-card">
              <div class="avatar-container selected">
                <div class="avatar"><img alt="Astra" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='128' height='128' viewBox='0 0 128 128'%3E%3Crect width='128' height='128' rx='24' fill='%23dbead1'/%3E%3Ctext x='50%25' y='54%25' font-size='40' text-anchor='middle' fill='%233c5a2a' font-family='Arial'%3EA%3C/text%3E%3C/svg%3E"></div>
              </div>
              <div class="st-preview-character-copy">
                <div class="ch_name"><span class="name_text">Astra</span></div>
                <div class="st-preview-character-tags">fantasy · guide · preview persona</div>
                <p>角色卡快速面板用于暴露更多主题表面，包括头像、名称、标签与简介容器。</p>
              </div>
            </div>
          </div>
        </div>
        <div id="sheld">
          <div id="chat">
            ${buildMessage({
              mesId: "1",
              name: "SillyTavern System",
              avatarLabel: "ST",
              timestamp: "System",
              tokenCounter: "meta",
              isSystem: true,
              extraClass: "smallSysMes",
              messageHtml:
                '<p>Previewing theme surfaces with fixed sample content.</p><p><a href="#">Example link</a></p><hr>',
            })}
            ${buildMessage({
              mesId: "2",
              name: "Astra",
              avatarLabel: "A",
              timestamp: "08:14",
              tokenCounter: "318 tok",
              includeReasoning: true,
              messageHtml:
                "<p><strong>粗体</strong>、<em>斜体</em>、<u>下划线</u> 和 <code>inline code</code>。</p><blockquote>引用颜色、边框、留白和正文容器应该尽量贴近 ST。</blockquote><p>Welcome back. Theme variables now drive this isolated preview.</p>",
            })}
            ${buildMessage({
              mesId: "3",
              name: "You",
              avatarLabel: "Y",
              timestamp: "08:15",
              tokenCounter: "142 tok",
              isUser: true,
              extraClass: "last_mes",
              messageHtml: `<p>列表、链接和代码块也需要稳定呈现。</p><ul><li>Keep the message shell realistic.</li><li>Make rich text and code samples visible.</li></ul><pre><code>const preview = buildBeautifyPreviewDocument({ platform: '${escapeHtml(normalizedPlatform)}' });</code></pre>`,
            })}
          </div>
          <div id="form_sheld">
            <div id="send_form">
              <div id="nonQRFormItems">
                <div id="leftSendForm" class="alignContentCenter">
                  <div id="options_button" class="fa-solid fa-bars interactable" data-icon-fallback="≡" aria-label="Options"></div>
                </div>
                <textarea id="send_textarea" name="text" class="mdHotkeys" placeholder="${escapeHtml(inputHint)}"></textarea>
                <div id="rightSendForm" class="alignContentCenter">
                  <div id="mes_continue" class="fa-solid fa-arrow-right interactable" data-icon-fallback=">" aria-label="Continue"></div>
                  <div id="send_but" class="fa-solid fa-paper-plane interactable" data-icon-fallback="➤" aria-label="Send"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

export function buildBeautifyPreviewDocument({
  theme = {},
  wallpaperUrl = "",
  platform = "pc",
  baseCss = "",
} = {}) {
  const themeVars = buildBeautifyPreviewThemeVars(theme, wallpaperUrl);
  const serializedVars = serializeCssVars(themeVars);
  const customCss = escapeCssText(theme.custom_css || "");
  const safeBaseCss = escapeCssText(baseCss);
  const markup = buildBeautifyPreviewSampleMarkup(platform);
  const behaviorScript = buildPreviewBehaviorScript();

  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Beautify Preview</title>
    <style>:root{${serializedVars}}</style>
    <style>
      html, body {
        margin: 0;
        min-height: 100%;
        background: #0f172a;
        color: var(--SmartThemeBodyColor);
      }

      body {
        position: relative;
        overflow-x: hidden;
      }

      .st-preview-root {
        min-height: 100vh;
        position: relative;
      }

      .st-preview-wallpaper,
      .st-preview-overlay {
        position: fixed;
        inset: 0;
        pointer-events: none;
      }

      .st-preview-wallpaper {
        background-image: var(--wallpaperUrl);
        background-size: cover;
        background-position: center;
      }

      .st-preview-overlay {
        background: linear-gradient(var(--SmartThemeBlurTintColor), var(--SmartThemeBlurTintColor));
      }

      .st-preview-shell {
        position: relative;
        z-index: 1;
        min-height: 100vh;
        padding: 20px;
      }

      .flex-container {
        display: flex;
      }

      .justifySpaceBetween {
        justify-content: space-between;
      }

      .flex1 {
        flex: 1;
      }

      .alignitemscenter,
      .alignContentCenter,
      .alignItemsBaseline {
        align-items: center;
      }

      .alignItemsBaseline {
        align-items: baseline;
      }

      .flexFlowColumn {
        flex-direction: column;
      }

      .flexNoGap {
        gap: 0;
      }
    </style>
    <style>${safeBaseCss}</style>
    <style>${customCss}</style>
  </head>
  <body>
    ${markup}
    <script>${behaviorScript.replace(/<\/script/gi, "<\\/script")}</script>
  </body>
</html>`;
}
