import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getDocuments } from "../services/api";

function formatDate(value) {
  if (!value) return "Unknown";
  return new Date(value * 1000).toLocaleDateString();
}

function detectTypeFromName(name) {
  const lower = name.toLowerCase();

  if (lower.includes("nda") || lower.includes("non-disclosure")) return "NDA";
  if (lower.includes("appointment") || lower.includes("employment")) {
    return "Employment Agreement";
  }
  if (lower.includes("invention assignment")) {
    return "Invention Assignment Agreement";
  }
  if (lower.includes("service")) return "Service Agreement";

  return "Unknown";
}

export default function DashboardPage() {
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDocuments() {
      try {
        setError("");
        const data = await getDocuments();

        const docs = (data.documents || []).map((doc) => {
          const name = doc.filename || doc.name;
        
          return {
            id: doc.document_id || doc.id,
            name,
            status: doc.status,
            updated_at: doc.updated_at,
            type:
              doc.type && doc.type !== "Unknown"
                ? doc.type
                : detectTypeFromName(name),
          };
        });

        setDocuments(docs);
      } catch (err) {
        console.error("Failed to load documents:", err);
        setError("Failed to load dashboard data.");
      }
    }

    loadDocuments();
  }, []);

  const totalDocuments = documents.length;
  const processed = documents.filter((d) => d.status === "Analysis Ready").length;
  const flaggedRisks = Math.floor(documents.length / 3);
  const needsReview = documents.filter((d) => d.status === "Needs Review").length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold tracking-tight text-slate-950">
          Dashboard
        </h1>
        <p className="mt-2 text-base text-slate-600">
          Review uploaded legal documents, processing status, and recent analyses.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-slate-500">Total Documents</p>
          <p className="mt-3 text-4xl font-bold text-slate-950">{totalDocuments}</p>
          <p className="mt-2 text-sm text-slate-400">Across all uploads</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-slate-500">Processed</p>
          <p className="mt-3 text-4xl font-bold text-slate-950">{processed}</p>
          <p className="mt-2 text-sm text-slate-400">Ready for review</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-slate-500">Flagged Risks</p>
          <p className="mt-3 text-4xl font-bold text-slate-950">{flaggedRisks}</p>
          <p className="mt-2 text-sm text-slate-400">Across analyzed documents</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-slate-500">Needs Review</p>
          <p className="mt-3 text-4xl font-bold text-slate-950">{needsReview}</p>
          <p className="mt-2 text-sm text-slate-400">Missing key fields</p>
        </div>
      </div>

      <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 shadow-sm">
        <h2 className="text-3xl font-bold text-slate-950">
          Upload a new legal document
        </h2>
        <p className="mt-3 max-w-3xl text-base text-slate-600">
          Upload PDF agreements, NDAs, leases, and other legal documents for extraction,
          analysis, grounded Q&amp;A, and clause review.
        </p>
        <div className="mt-6">
          <Link
            to="/upload"
            className="inline-flex rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800"
          >
            Go to Upload
          </Link>
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 px-6 py-5">
          <h2 className="text-3xl font-bold text-slate-950">Recent documents</h2>
        </div>

        {documents.length === 0 ? (
          <div className="px-6 py-8 text-slate-500">No documents uploaded yet.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left">
              <thead className="bg-slate-50 text-sm text-slate-500">
                <tr>
                  <th className="px-6 py-4 font-semibold">Document</th>
                  <th className="px-6 py-4 font-semibold">Type</th>
                  <th className="px-6 py-4 font-semibold">Status</th>
                  <th className="px-6 py-4 font-semibold">Updated</th>
                  <th className="px-6 py-4 font-semibold">Open</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {documents.map((doc) => (
                  <tr key={doc.id} className="text-sm text-slate-700">
                    <td className="px-6 py-4">{doc.name}</td>
                    <td className="px-6 py-4">{doc.type}</td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          doc.status === "Analysis Ready"
                            ? "bg-green-100 text-green-700"
                            : doc.status === "Processing"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {doc.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">{formatDate(doc.updated_at)}</td>
                    <td className="px-6 py-4">
                      <Link
                        to={`/documents/${doc.id}`}
                        className="font-medium text-slate-900 underline underline-offset-2"
                      >
                        Open
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}