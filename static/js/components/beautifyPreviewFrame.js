import { buildBeautifyPreviewAssetUrl } from "../api/beautify.js";
import {
  clearIsolatedHtml,
  renderIsolatedHtml,
} from "../runtime/renderRuntime.js";
import { buildBeautifyPreviewDocument } from "./beautifyPreviewDocument.js";

let previewBaseCssPromise = null;

async function loadPreviewBaseCss() {
  if (!previewBaseCssPromise) {
    previewBaseCssPromise = fetch("/static/css/modules/st-preview-base.css")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to load preview base CSS: ${res.status}`);
        }
        return res.text();
      })
      .catch((error) => {
        previewBaseCssPromise = null;
        throw error;
      });
  }
  return previewBaseCssPromise;
}

async function resolvePreviewBaseCss() {
  try {
    return await loadPreviewBaseCss();
  } catch (error) {
    console.warn(
      "Beautify preview base CSS unavailable, using inline preview styles only.",
      error,
    );
    return "";
  }
}

export default function beautifyPreviewFrame() {
  return {
    previewBaseCss: "",

    get previewHostEl() {
      if (this.$refs?.previewHost) {
        return this.$refs.previewHost;
      }
      return this.$el?.querySelector(".beautify-preview-host") || null;
    },

    get previewShellMode() {
      return this.$store.global.beautifyPreviewDevice || "pc";
    },

    get previewApproximateNoticeVisible() {
      const variant = this.$store.global.beautifyActiveVariant || {};
      const hint = variant.preview_hint || {};
      return hint.preview_accuracy === "approx";
    },

    init() {
      this.$watch("$store.global.beautifyActiveDetail", (detail) => {
        if (!detail) {
          this.destroy();
          return;
        }
        this.$nextTick(() => {
          this.renderPreview();
        });
      });
      this.$watch("$store.global.beautifyActiveVariant", () =>
        this.renderPreview(),
      );
      this.$watch("$store.global.beautifyActiveWallpaper", () =>
        this.renderPreview(),
      );
      this.$watch("$store.global.beautifyPreviewDevice", () =>
        this.renderPreview(),
      );
      this.renderPreview();
      this.$nextTick(() => {
        this.renderPreview();
      });
      resolvePreviewBaseCss().then((css) => {
        this.previewBaseCss = css;
        this.renderPreview();
      });
    },

    resolvePreviewState() {
      const variant = this.$store.global.beautifyActiveVariant || {};
      const wallpaper = this.$store.global.beautifyActiveWallpaper || {};
      return {
        platform: this.previewShellMode === "mobile" ? "mobile" : "pc",
        theme: variant.theme_data || {},
        wallpaperUrl: wallpaper.file
          ? buildBeautifyPreviewAssetUrl(wallpaper.file)
          : "",
      };
    },

    renderPreview() {
      const host = this.previewHostEl;
      if (!host) {
        return;
      }

      const state = this.resolvePreviewState();
      const documentHtml = buildBeautifyPreviewDocument({
        ...state,
        baseCss: this.previewBaseCss,
      });

      renderIsolatedHtml(host, {
        htmlPayload: documentHtml,
        minHeight: state.platform === "mobile" ? 760 : 900,
        maxHeight: state.platform === "mobile" ? 3200 : 4800,
      });
    },

    destroy() {
      const host = this.previewHostEl;
      if (host) {
        clearIsolatedHtml(host, { clearShadow: true });
      }
    },
  };
}
