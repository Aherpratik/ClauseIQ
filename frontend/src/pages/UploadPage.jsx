import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadDocument } from "../services/api";

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleUpload() {
    if (!selectedFile) {
      setError("Please select a PDF file first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const result = await uploadDocument(selectedFile);

      if (!result.document_id) {
        throw new Error("No document_id returned from backend");
      }

      navigate(`/documents/${result.document_id}`,{
        state: {
            uploadedAt: new Date().toISOString(),
            lastAnalyzed: new Date().toISOString(),
        },
      });
    } catch (err) {
      console.error(err);
      setError("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">Upload Document</h2>
        <p className="text-sm text-slate-600 mt-1">
          Upload a legal PDF and begin extraction, indexing, and structured analysis.
        </p>
      </div>

      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-10 shadow-sm">
        <div className="text-center">
          <h3 className="text-lg font-semibold">Select a legal PDF</h3>
          <p className="mt-2 text-sm text-slate-500">Supported format: PDF</p>

          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
            className="mt-5 block w-full text-sm text-slate-600"
          />

          {selectedFile && (
            <p className="mt-3 text-sm text-slate-700">
              Selected: {selectedFile.name}
            </p>
          )}

          {error && (
            <p className="mt-3 text-sm text-red-600">{error}</p>
          )}

          <button
            onClick={handleUpload}
            disabled={loading}
            className="mt-5 rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
          >
            {loading ? "Uploading..." : "Upload and Analyze"}
          </button>
        </div>
      </div>
    </div>
  );
}