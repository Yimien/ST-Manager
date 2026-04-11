function escapeCssText(value) {
  return String(value || "").replace(/<\/style/gi, "<\\/style");
}

export function buildBeautifyPreviewStyle(theme = {}, wallpaperUrl = "") {
  const fontScale = Number(theme.font_scale || 1) || 1;
  const blurStrength = Number(theme.blur_strength || 10) || 10;
  const shadowWidth = Number(theme.shadow_width || 2) || 2;
  const chatWidth = Number(theme.chat_width || 50) || 50;
  return {
    "--beautify-main-text": theme.main_text_color || "#f8fafc",
    "--beautify-italics-text":
      theme.italics_text_color || theme.main_text_color || "#dbeafe",
    "--beautify-underline-text": theme.underline_text_color || "#93c5fd",
    "--beautify-quote-text": theme.quote_text_color || "#cbd5f5",
    "--beautify-blur-tint": theme.blur_tint_color || "rgba(15, 23, 42, 0.74)",
    "--beautify-chat-tint": theme.chat_tint_color || "rgba(15, 23, 42, 0.42)",
    "--beautify-user-tint":
      theme.user_mes_blur_tint_color || "rgba(59, 130, 246, 0.2)",
    "--beautify-bot-tint":
      theme.bot_mes_blur_tint_color || "rgba(148, 163, 184, 0.18)",
    "--beautify-shadow-color": theme.shadow_color || "rgba(15, 23, 42, 0.38)",
    "--beautify-border-color":
      theme.border_color || "rgba(148, 163, 184, 0.24)",
    "--beautify-font-scale": `${fontScale}`,
    "--beautify-chat-width": `${Math.max(36, Math.min(100, chatWidth))}%`,
    "--beautify-blur-strength": `${Math.max(0, blurStrength)}px`,
    "--beautify-shadow-width": `${Math.max(0, shadowWidth)}px`,
    "--beautify-wallpaper-url": wallpaperUrl
      ? `url("${wallpaperUrl}")`
      : "none",
  };
}

export default function beautifyPreviewFrame() {
  return {
    injectedCustomCss: "",

    get previewStyleObject() {
      const detail = this.$store.global.beautifyActiveDetail || {};
      const variant = this.$store.global.beautifyActiveVariant || {};
      const wallpaper = this.$store.global.beautifyActiveWallpaper || {};
      const theme = variant.theme_data || {};
      const wallpaperUrl = wallpaper.file
        ? this.buildPreviewAssetUrl(wallpaper.file)
        : "";
      return buildBeautifyPreviewStyle(theme, wallpaperUrl);
    },

    get previewShellMode() {
      return this.$store.global.beautifyPreviewDevice || "pc";
    },

    get previewApproximateNoticeVisible() {
      const variant = this.$store.global.beautifyActiveVariant || {};
      const hint = variant.preview_hint || {};
      return hint.preview_accuracy === "approx";
    },

    get previewCustomCss() {
      const variant = this.$store.global.beautifyActiveVariant || {};
      return String((variant.theme_data || {}).custom_css || "").trim();
    },

    init() {
      this.$watch("$store.global.beautifySelectedVariantId", () => {
        this.injectedCustomCss = this.previewCustomCss;
      });
      this.injectedCustomCss = this.previewCustomCss;
    },

    buildPreviewAssetUrl(relativePath) {
      const normalized = String(relativePath || "").replace(
        /^data\/library\/beautify\//,
        "",
      );
      return `/api/beautify/preview-asset/${normalized.split("/").map(encodeURIComponent).join("/")}`;
    },

    customCssMarkup() {
      if (!this.injectedCustomCss) return "";
      return `<style>${escapeCssText(this.injectedCustomCss)}</style>`;
    },
  };
}
