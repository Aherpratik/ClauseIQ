import { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";
import DocumentHeader from "../components/workspace/DocumentHeader";
import WorkspaceSidebar from "../components/workspace/WorkspaceSidebar";
import DocumentViewer from "../components/workspace/DocumentViewer";
import AnalysisPanel from "../components/workspace/AnalysisPanel";
import { getExtract, getSummary, getAnalysis } from "../services/api";

function formatDateTime(value) {
  if (!value) return "Unknown";
  return new Date(value).toLocaleString();
}

export default function DocumentWorkspacePage() {
  const [activeTab, setActiveTab] = useState("overview");
  const [documentMeta, setDocumentMeta] = useState(null);
  const [pages, setPages] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  const location = useLocation();
  const { id: documentId } = useParams();

  async function loadAnalysisOnly() {
    try {
      console.log("Re-running analysis for:", documentId);

      const analysisData = await getAnalysis(documentId);
      setAnalysis(analysisData.analysis || null);

      setDocumentMeta((prev) =>
        prev
          ? {
              ...prev,
              lastAnalyzed: new Date().toLocaleString(),
            }
          : prev
      );
    } catch (err) {
      console.error("Failed to rerun analysis:", err);
      alert("Failed to re-run analysis.");
    }
  }

  function handleExportJSON() {
    try {
      if (!analysis) {
        alert("No analysis available to export.");
        return;
      }

      const blob = new Blob([JSON.stringify(analysis, null, 2)], {
        type: "application/json",
      });

      const url = window.URL.createObjectURL(blob);
      const a = window.document.createElement("a");
      a.href = url;
      a.download = `${(documentMeta?.name || "document-analysis").replace(
        /\.pdf$/i,
        ""
      )}.json`;

      window.document.body.appendChild(a);
      a.click();
      window.document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export JSON failed:", err);
      alert("Failed to export JSON.");
    }
  }

  function handleExportReport() {
    try {
      if (!documentMeta || !analysis) {
        alert("No report data available to export.");
        return;
      }

      const report = `
Document: ${documentMeta.name}
Uploaded: ${documentMeta.uploadedAt}
Pages: ${documentMeta.pages}
Last analyzed: ${documentMeta.lastAnalyzed}

Summary:
${documentMeta.summary}

Analysis:
${JSON.stringify(analysis, null, 2)}
      `.trim();

      const blob = new Blob([report], { type: "text/plain" });
      const url = window.URL.createObjectURL(blob);
      const a = window.document.createElement("a");
      a.href = url;
      a.download = `${(documentMeta.name || "document-report").replace(
        /\.pdf$/i,
        ""
      )}-report.txt`;

      window.document.body.appendChild(a);
      a.click();
      window.document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export report failed:", err);
      alert("Failed to export report.");
    }
  }

  useEffect(() => {
    async function loadDocumentData() {
      try {
        setError("");

        const extractData = await getExtract(documentId);
        const summaryData = await getSummary(documentId);

        setPages(extractData.pages || []);

        try {
          const analysisData = await getAnalysis(documentId);
          console.log("FULL API RESPONSE:", analysisData);
          setAnalysis(analysisData.analysis || null);
        } catch (analysisErr) {
          console.warn("Analysis failed, continuing without it:", analysisErr);
          setAnalysis(null);
        }

        setDocumentMeta({
          name: (extractData.filename || "Untitled Document").replace(
            /^[a-f0-9-]+_/,
            ""
          ),
          uploadedAt: formatDateTime(location.state?.uploadedAt),
          pages: extractData.pages?.length || 0,
          lastAnalyzed: formatDateTime(location.state?.lastAnalyzed),
          summary:
            summaryData.summary ||
            "No summary available for this document yet.",
        });
      } catch (err) {
        console.error("Failed to load document data:", err);
        setError("Failed to load document data.");
      }
    }

    loadDocumentData();
  }, [documentId, location.state]);

  if (error) {
    return (
      <div className="w-full p-6">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (!documentMeta) {
    return (
      <div className="w-full p-6">
        <div className="rounded-xl border border-slate-200 bg-white p-6 text-slate-600 shadow-sm">
          Loading document...
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-x-hidden bg-slate-50">
      <main className="h-full overflow-y-auto overflow-x-hidden p-6">
        <div className="w-full min-w-0">
          <DocumentHeader
            document={documentMeta}
            onRerunAnalysis={loadAnalysisOnly}
            onExportJSON={handleExportJSON}
            onExportReport={handleExportReport}
          />

          <div className="mt-6 grid grid-cols-1 gap-4 xl:grid-cols-[260px_minmax(0,1fr)_300px]">
            <div className="min-w-0">
              <WorkspaceSidebar
                activeTab={activeTab}
                setActiveTab={setActiveTab}
                analysis={analysis}
              />
            </div>

            <div className="min-w-0">
              <DocumentViewer pages={pages} />
            </div>

            <div className="min-w-0">
              <AnalysisPanel
                activeTab={activeTab}
                setActiveTab={setActiveTab}
                analysis={analysis}
                documentId={documentId}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}