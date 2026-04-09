export async function downloadFileFromApi({
  url,
  method = "POST",
  body,
  headers = {},
  defaultFilename = "download.json",
  showToast,
  successMessage,
}) {
  const response = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  const contentDisposition =
    response.headers.get("Content-Disposition") ||
    response.headers.get("content-disposition") ||
    "";
  const contentType = response.headers.get("content-type") || "";
  const isAttachment = contentDisposition.toLowerCase().includes("attachment");

  if (
    !response.ok ||
    (!isAttachment && contentType.includes("application/json"))
  ) {
    const payload = await response.json().catch(() => null);
    const message =
      payload?.msg || payload?.message || `下载失败 (${response.status})`;
    throw new Error(message);
  }

  const filenameMatch = contentDisposition.match(
    /filename\*=UTF-8''([^;]+)|filename="?([^";]+)"?/i,
  );
  const filename = decodeURIComponent(
    filenameMatch?.[1] || filenameMatch?.[2] || defaultFilename,
  );
  const blob = await response.blob();
  const blobUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = blobUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(blobUrl);

  if (successMessage && typeof showToast === "function") {
    showToast(successMessage, 1800);
  }
}
