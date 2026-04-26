// Vendor-derived preview shell assembled from static/vendor/sillytavern/index.html.
// The structure and anchor ids here intentionally track the upstream shell while
// allowing the preview document builder to inject lightweight hydrated fragments.

export function buildVendorFirstPreviewShell({
  activeSceneId = 'daily',
  topBarStaticActionsMarkup = '',
  settingsDrawerContentMarkup = '',
  formattingDrawerContentMarkup = '',
  characterDrawerContentMarkup = '',
  chatMarkup = '',
  sendFormMarkup = '',
} = {}) {
  return `
    <!-- vendor-derived-shell: static/vendor/sillytavern/index.html -->
    <div class="st-preview-root" data-active-panel="none" data-active-scene="${activeSceneId}">
      <div id="bg1"></div>
      <div class="st-preview-shell">
        <div id="top-bar">
          <div class="st-preview-topbar-strip">
            <div class="st-preview-topbar-section st-preview-topbar-section-left">
              ${topBarStaticActionsMarkup}
            </div>
          </div>
        </div>
        <div id="top-settings-holder">
          <div id="ai-config-button" class="drawer closedDrawer">
            <div class="drawer-toggle drawer-header" data-panel-target="settings">
              <div id="leftNavDrawerIcon" class="drawer-icon fa-solid fa-sliders fa-fw closedIcon st-preview-topbar-action" aria-pressed="false" title="AI Response Configuration"></div>
            </div>
            <div id="left-nav-panel" class="drawer-content fillLeft closedDrawer left-drawer st-preview-panel-body st-preview-settings-drawer" data-panel-surface="settings">
              <div id="left-nav-panelheader" class="fa-solid fa-grip drag-grabber"></div>
              <div class="scrollableInner">${settingsDrawerContentMarkup}</div>
            </div>
          </div>
          <div id="advanced-formatting-button" class="drawer closedDrawer">
            <div class="drawer-toggle drawer-header" data-panel-target="formatting">
              <div id="formattingDrawerIcon" class="drawer-icon fa-solid fa-font fa-fw closedIcon st-preview-topbar-action" aria-pressed="false" title="AI Response Formatting"></div>
            </div>
            <div id="AdvancedFormatting" class="drawer-content fillLeft closedDrawer left-drawer st-preview-panel-body st-preview-formatting-drawer" data-panel-surface="formatting">
              <div class="scrollableInner">${formattingDrawerContentMarkup}</div>
            </div>
          </div>
          <div id="rm_button_panel_pin_div" class="alignitemsflexstart" title="Locked = Character Management panel will stay open">
            <label for="rm_button_panel_pin">
              <div class="fa-solid unchecked fa-unlock right_menu_button"></div>
              <div class="fa-solid checked fa-lock right_menu_button"></div>
            </label>
          </div>
          <div id="right-nav-drawer" class="drawer closedDrawer right-drawer-anchor">
            <div class="drawer-toggle drawer-header" data-panel-target="character">
              <div id="rightNavDrawerIcon" class="drawer-icon fa-solid fa-address-card fa-fw closedIcon st-preview-topbar-action" aria-pressed="false" title="Character Management"></div>
            </div>
            <div id="right-nav-panel" class="drawer-content fillRight closedDrawer right-drawer st-preview-panel-body st-preview-character-panel" data-panel-surface="character">
              <div id="right-nav-panelheader" class="fa-solid fa-grip drag-grabber"></div>
              <div class="scrollableInner">${characterDrawerContentMarkup}</div>
            </div>
          </div>
        </div>
        <div id="sheld">
          <div id="sheldheader" class="fa-solid fa-grip drag-grabber"></div>
          <div id="chat">${chatMarkup}</div>
          <div id="form_sheld">${sendFormMarkup}</div>
        </div>
      </div>
    </div>
  `;
}
