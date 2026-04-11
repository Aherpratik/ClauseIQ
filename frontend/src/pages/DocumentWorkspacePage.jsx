import { useEffect, useState } from "react";
import DocumentHeader from "../components/workspace/DocumentHeader";
import WorkspaceSidebar from "../components/workspace/WorkspaceSidebar";
import DocumentViewer from "../components/workspace/DocumentViewer";
import AnalysisPanel from "../components/workspace/AnalysisPanel";
import { getExtract, getSummary, getAnalysis } from "../services/api";
import { useParams, useLocation } from "react-router-dom";

function formatDateTime(value) {
  if (!value) return "Unknown";
  return new Date(value).toLocaleString();
}

export default function DocumentWorkspacePage() {
  const [activeTab, setActiveTab] = useState("overview");
  const [document, setDocument] = useState(null);
  const [pages, setPages] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  const location = useLocation();
  const { id: documentId } = useParams();

  useEffect(() => {
    async function loadDocumentData() {
      try {
        setError("");

        const extractData = await getExtract(documentId);
        const summaryData = await getSummary(documentId);

        setPages(extractData.pages || []);

        try {
          const analysisData = await getAnalysis(documentId);
          setAnalysis(analysisData);
        } catch (analysisErr) {
          console.warn("Analysis failed, continuing without it:", analysisErr);
          setAnalysis(null);
        }

        setDocument({
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
      <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">
        {error}
      </div>
    );
  }

  if (!document) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-6 text-slate-600 shadow-sm">
        Loading document...
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-slate-50">
      <DocumentHeader document={document} />

      <div className="flex-1 min-h-0 p-4">
        <div className="flex h-full gap-4">
          <div className="w-[260px] shrink-0 h-full">
            <WorkspaceSidebar
              activeTab={activeTab}
              setActiveTab={setActiveTab}
            />
          </div>

          <div className="flex-1 min-w-0 h-full max-w-none">
            <DocumentViewer pages={pages} />
          </div>

          <div className="w-[300px] shrink-0 h-full">
            <AnalysisPanel
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              analysis={analysis}
            />
          </div>
        </div>
      </div>
    </div>
  );
}