const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Failed to upload document");
  }

  return res.json();
}

export async function getExtract(documentId) {
  const res = await fetch(`${BASE_URL}/extract/${documentId}`);
  if (!res.ok) {
    throw new Error("Failed to fetch extract");
  }
  return res.json();
}

export async function getSummary(documentId) {
  const res = await fetch(`${BASE_URL}/summary/${documentId}`);
  if (!res.ok) {
    throw new Error("Failed to fetch summary");
  }
  return res.json();
}

export async function getAnalysis(documentId) {
    const res = await fetch(`${BASE_URL}/analyze/${documentId}`);
    if (!res.ok) {
      throw new Error("Failed to fetch analysis");
    }
    return res.json();
  }