import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000/api/v1";

async function parseResponse(response) {
  const text = await response.text();
  try {
    return text ? JSON.parse(text) : {};
  } catch {
    return { raw: text };
  }
}

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [documentId, setDocumentId] = useState("");

  const [searchQuery, setSearchQuery] = useState("confidential information");
  const [question, setQuestion] = useState(
    "What is considered confidential information in this agreement?"
  );
  const [topK, setTopK] = useState(5);

  const [uploadResult, setUploadResult] = useState(null);
  const [extractResult, setExtractResult] = useState(null);
  const [searchResult, setSearchResult] = useState(null);
  const [qaResult, setQaResult] = useState(null);
  const [summaryResult, setSummaryResult] = useState(null);
  const [analyzeResult, setAnalyzeResult] = useState(null);

  const [loading, setLoading] = useState("");
  const [error, setError] = useState("");

  const clearError = () => setError("");

  async function handleUpload() {
    if (!selectedFile) {
      setError("Please select a PDF file first.");
      return;
    }

    clearError();
    setLoading("upload");
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await parseResponse(response);

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setUploadResult(data);
      if (data.document_id) {
        setDocumentId(data.document_id);
      }
    } catch (err) {
      setError(err.message || "Upload failed.");
    } finally {
      setLoading("");
    }
  }

  async function handleExtract() {
    if (!documentId.trim()) {
      setError("Document ID is required.");
      return;
    }

    clearError();
    setLoading("extract");
    setExtractResult(null);

    try {
      const response = await fetch(`${API_BASE}/extract/${documentId}`);
      const data = await parseResponse(response);

      if (!response.ok) {
        throw new Error(data.detail || "Extract failed.");
      }

      setExtractResult(data);
    } catch (err) {
      setError(err.message || "Extract failed.");
    } finally {
      setLoading("");
    }
  }

  async function handleSearch() {
    if (!documentId.trim()) {
      setError("Document ID is required.");
      return;
    }

    clearError();
    setLoading("search");
    setSearchResult(null);

    try {
      const params = new URLSearchParams({
        query: searchQuery,
        top_k: String(topK),
      });

      const response = await fetch(
        `${API_BASE}/search/${documentId}?${params.toString()}`
      );
      const data = await parseResponse(response);

      if (!response.ok) {
        throw new Error(data.detail || "Search failed.");
      }

      setSearchResult(data);
    } catch (err) {
      setError(err.message || "Search failed.");
    } finally {
      setLoading("");
    }
  }

  async function handleQA() {
    if (!documentId.trim()) {
      setError("Document ID is required.");
      return;
    }

    clearError();
    setLoading("qa");
    setQaResult(null);

    try {
      const response = await fetch(`${API_BASE}/qa/${documentId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          top_k: topK,
        }),
      });

      const data = await parseResponse(response);

      if (!response.ok) {
        throw new Error(data.detail || "QA failed.");
      }

      setQaResult(data);
    } catch (err) {
      setError(err.message || "QA failed.");
    } finally {
      setLoading("");
    }
  }

  async function handleSummary() {
    if (!documentId.trim()) {
      setError("Document ID is required.");
      return;
    }

    clearError();
    setLoading("summary");
    setSummaryResult(null);

    try {
      const response = await fetch(`${API_BASE}/summary/${documentId}`);
      const data = await parseResponse(response);

      if (!response.ok) {
        throw new Error(data.detail || "Summary failed.");
      }

      setSummaryResult(data);
    } catch (err) {
      setError(err.message || "Summary failed.");
    } finally {
      setLoading("");
    }
  }

  async function handleAnalyze() {
    if (!documentId.trim()) {
      setError("Document ID is required.");
      return;
    }

    clearError();
    setLoading("analyze");
    setAnalyzeResult(null);

    try {
      const response = await fetch(`${API_BASE}/analyze/${documentId}`);
      const data = await parseResponse(response);

      if (!response.ok) {
        throw new Error(data.detail || "Analyze failed.");
      }

      setAnalyzeResult(data);
    } catch (err) {
      setError(err.message || "Analyze failed.");
    } finally {
      setLoading("");
    }
  }

  function ResultBlock({ title, data }) {
    if (!data) return null;

    return (
      <div className="result-block">
        <h3>{title}</h3>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>ClauseIQ Testing UI</h1>
        <p>Test upload, extract, search, QA, summary, and analyze from one place.</p>
      </header>

      {error && <div className="error-box">{error}</div>}

      <div className="layout">
        <div className="panel">
          <section className="card">
            <h2>1. Upload PDF</h2>
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
            />
            <button onClick={handleUpload} disabled={loading !== ""}>
              {loading === "upload" ? "Uploading..." : "Upload"}
            </button>
          </section>

          <section className="card">
            <h2>2. Document Control</h2>
            <label>Document ID</label>
            <input
              type="text"
              value={documentId}
              onChange={(e) => setDocumentId(e.target.value)}
              placeholder="Document ID will appear here after upload"
            />
            <div className="button-row">
              <button onClick={handleExtract} disabled={loading !== ""}>
                {loading === "extract" ? "Extracting..." : "Extract + Index"}
              </button>
              <button onClick={handleSummary} disabled={loading !== ""}>
                {loading === "summary" ? "Summarizing..." : "Summary"}
              </button>
              <button onClick={handleAnalyze} disabled={loading !== ""}>
                {loading === "analyze" ? "Analyzing..." : "Analyze"}
              </button>
            </div>
          </section>

          <section className="card">
            <h2>3. Search</h2>
            <label>Search Query</label>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />

            <label>Top K</label>
            <input
              type="number"
              min="1"
              max="10"
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value) || 5)}
            />

            <button onClick={handleSearch} disabled={loading !== ""}>
              {loading === "search" ? "Searching..." : "Run Search"}
            </button>
          </section>

          <section className="card">
            <h2>4. QA</h2>
            <label>Question</label>
            <textarea
              rows="5"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <button onClick={handleQA} disabled={loading !== ""}>
              {loading === "qa" ? "Asking..." : "Ask Question"}
            </button>
          </section>
        </div>

        <div className="results">
          <ResultBlock title="Upload Result" data={uploadResult} />
          <ResultBlock title="Extract Result" data={extractResult} />
          <ResultBlock title="Search Result" data={searchResult} />
          <ResultBlock title="QA Result" data={qaResult} />
          <ResultBlock title="Summary Result" data={summaryResult} />
          <ResultBlock title="Analyze Result" data={analyzeResult} />
        </div>
      </div>
    </div>
  );
}