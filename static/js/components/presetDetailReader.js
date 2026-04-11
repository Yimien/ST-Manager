/**
 * static/js/components/presetDetailReader.js
 * 预设详情阅读器组件
 */

import {
  getPresetDefaultPreview,
  getPresetDetail,
  savePresetExtensions as apiSavePresetExtensions,
} from "../api/presets.js";
import {
  clearActiveRuntimeContext,
  setActiveRuntimeContext,
} from "../runtime/runtimeContext.js";
import { downloadFileFromApi } from "../utils/download.js";
import { formatDate } from "../utils/format.js";

const LONG_TEXT_FIELDS = new Set([
  "content",
  "story_string",
  "example_separator",
  "chat_start",
  "prefix",
  "suffix",
  "separator",
  "negative_prompt",
  "json_schema",
  "grammar",
  "input_sequence",
  "output_sequence",
  "system_sequence",
  "first_output_sequence",
  "last_output_sequence",
  "stop_sequence",
  "activation_regex",
]);

const SECTION_LABELS = {
  sampling: "采样参数",
  penalties: "惩罚参数",
  length_and_output: "长度与终止",
  dynamic_temperature: "动态温度",
  mirostat: "Mirostat",
  guidance: "引导与负面提示",
  formatting: "格式与运行开关",
  schema_and_grammar: "Schema / Grammar",
  bans_and_bias: "禁词与 Bias",
  sampler_ordering: "采样顺序",
  sequences: "输入输出序列",
  wrapping_and_behavior: "包装与行为",
  activation: "激活规则",
  compatibility: "兼容字段",
  story: "故事模板",
  separator_and_chat: "分隔与聊天",
  insertion_behavior: "插入行为",
  formatting_behavior: "格式行为",
  prompt: "提示词内容",
  placement: "插入位置",
  template: "模板字段",
  runtime_notes: "运行说明",
};

export default function presetDetailReader() {
  return {
    showModal: false,
    isLoading: false,
    activePresetDetail: null,
    defaultPreviewPath: "",
    defaultPreviewAvailable: false,

    init() {
      window.addEventListener("open-preset-reader", (e) => {
        this.openPreset(e.detail || {});
      });
    },

    get parameterSections() {
      const sections = this.activePresetDetail?.sections || {};
      return Object.entries(sections)
        .filter(([name]) => name !== "compatibility")
        .map(([name, items]) => ({
          name,
          label: this.getSectionLabel(name),
          items: (items || []).filter((item) => !this.isLongTextItem(item)),
        }))
        .filter((section) => section.items.length > 0);
    },

    get templateItems() {
      const sections = this.activePresetDetail?.sections || {};
      return Object.entries(sections).flatMap(([sectionName, items]) =>
        (items || [])
          .filter((item) => this.isLongTextItem(item))
          .map((item) => ({
            ...item,
            sectionName,
            sectionLabel: this.getSectionLabel(sectionName),
          })),
      );
    },

    get compatibilitySections() {
      const sections = this.activePresetDetail?.sections || {};
      return Object.entries(sections)
        .filter(([name]) => name === "compatibility")
        .map(([name, items]) => ({
          name,
          label: this.getSectionLabel(name),
          items: items || [],
        }))
        .filter((section) => section.items.length > 0);
    },

    get extensionSummary() {
      const extensions = this.activePresetDetail?.extensions || {};
      const regexCount = Array.isArray(extensions.regex_scripts)
        ? extensions.regex_scripts.length
        : 0;
      const scriptCount = Array.isArray(extensions?.tavern_helper?.scripts)
        ? extensions.tavern_helper.scripts.length
        : 0;
      return { regexCount, scriptCount, total: regexCount + scriptCount };
    },

    async openPreset(item) {
      if (!item?.id) return;
      this.isLoading = true;
      this.showModal = true;

      try {
        const res = await getPresetDetail(item.id);
        if (!res.success) {
          this.$store.global.showToast(res.msg || "获取详情失败", "error");
          this.closeModal();
          return;
        }

        this.activePresetDetail = res.preset;
        this.defaultPreviewPath = "";
        this.defaultPreviewAvailable = false;
        setActiveRuntimeContext({
          preset: {
            id: res.preset?.id || item.id || "",
            name: res.preset?.name || "",
            type: res.preset?.type || "",
            path: res.preset?.path || "",
          },
        });
        this.loadDefaultPreviewInfo();
      } catch (error) {
        console.error("Failed to load preset detail:", error);
        this.$store.global.showToast("获取详情失败", "error");
        this.closeModal();
      } finally {
        this.isLoading = false;
      }
    },

    async loadDefaultPreviewInfo() {
      if (!this.activePresetDetail?.capabilities?.can_restore_default) return;
      try {
        const res = await getPresetDefaultPreview({
          preset_id: this.activePresetDetail.id,
          preset_kind: this.activePresetDetail.preset_kind,
        });
        if (res.success) {
          this.defaultPreviewPath = res.default_path || "";
          this.defaultPreviewAvailable = true;
        }
      } catch (error) {
        console.warn("Load preset default preview failed:", error);
      }
    },

    closeModal() {
      this.showModal = false;
      this.activePresetDetail = null;
      this.defaultPreviewPath = "";
      this.defaultPreviewAvailable = false;
      clearActiveRuntimeContext("preset");
    },

    openFullscreenEditor(options = {}) {
      if (!this.activePresetDetail) return;
      window.dispatchEvent(
        new CustomEvent("open-preset-editor", {
          detail: {
            presetId: this.activePresetDetail.id,
            activeNav: options.activeNav || "basic",
            restoreDefault: options.restoreDefault === true,
          },
        }),
      );
      this.closeModal();
    },

    openRawViewer() {
      this.openFullscreenEditor({ activeNav: "raw" });
    },

    previewRestoreDefault() {
      this.openFullscreenEditor({ restoreDefault: true });
    },

    async exportActivePreset() {
      const detail = this.activePresetDetail;
      if (!detail) return;

      try {
        await downloadFileFromApi({
          url: "/api/presets/export",
          body: { id: detail.id },
          defaultFilename: detail.filename || `${detail.name || "preset"}.json`,
          showToast: this.$store?.global?.showToast,
        });
      } catch (error) {
        this.$store.global.showToast(error.message || "导出失败", "error");
      }
    },

    openAdvancedExtensions() {
      if (!this.activePresetDetail) return;

      const extensions = this.activePresetDetail.extensions || {};
      const editingData = {
        extensions: {
          regex_scripts: Array.isArray(extensions.regex_scripts)
            ? extensions.regex_scripts
            : [],
          tavern_helper: extensions.tavern_helper || { scripts: [] },
        },
      };

      window.dispatchEvent(
        new CustomEvent("open-advanced-editor", {
          detail: editingData,
        }),
      );

      const saveHandler = async (e) => {
        window.removeEventListener("advanced-editor-save", saveHandler);
        const nextExtensions = e?.detail?.extensions || editingData.extensions;
        await this.savePresetExtensions(nextExtensions);
      };
      window.addEventListener("advanced-editor-save", saveHandler);
    },

    async savePresetExtensions(extensions) {
      if (!this.activePresetDetail) return;
      try {
        const res = await apiSavePresetExtensions({
          id: this.activePresetDetail.id,
          extensions,
        });
        if (!res.success) {
          this.$store.global.showToast(res.msg || "保存失败", "error");
          return;
        }
        this.$store.global.showToast("扩展已保存");
        await this.openPreset({ id: this.activePresetDetail.id });
      } catch (error) {
        console.error("Failed to save preset extensions:", error);
        this.$store.global.showToast("保存失败", "error");
      }
    },

    getSectionLabel(name) {
      return SECTION_LABELS[name] || name;
    },

    getSourceLabel() {
      return this.activePresetDetail?.type === "global"
        ? "全局预设"
        : "资源预设";
    },

    isLongTextItem(item) {
      return Boolean(item && LONG_TEXT_FIELDS.has(item.key));
    },

    formatValue(value) {
      if (value === null || value === undefined || value === "") return "-";
      if (typeof value === "boolean") return value ? "是" : "否";
      if (typeof value === "number") {
        return Number.isInteger(value)
          ? String(value)
          : value.toFixed(4).replace(/0+$/, "").replace(/\.$/, "");
      }
      if (typeof value === "object") {
        try {
          return JSON.stringify(value, null, 2);
        } catch (error) {
          return String(value);
        }
      }
      return String(value);
    },

    formatDate(ts) {
      return formatDate(ts, { includeYear: true });
    },

    formatSize(bytes) {
      const size = Number(bytes) || 0;
      if (!size) return "0 B";
      if (size < 1024) return `${size} B`;
      if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
      return `${(size / 1024 / 1024).toFixed(1)} MB`;
    },

    async copyText(value, label = "内容") {
      try {
        await navigator.clipboard.writeText(String(value ?? ""));
        this.$store.global.showToast(`${label}已复制`);
      } catch (error) {
        console.error(error);
        this.$store.global.showToast(`复制${label}失败`, "error");
      }
    },

    viewLongText(item) {
      if (!item) return;
      window.dispatchEvent(
        new CustomEvent("open-markdown-view", {
          detail: String(item.value || ""),
        }),
      );
    },
  };
}
