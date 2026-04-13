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
          console.log("FULL API RESPONSE:", analysisData);
          setAnalysis(analysisData.analysis || null);
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
      <div className="w-full p-6">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (!document) {
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
          <DocumentHeader document={document} />

          <div className="mt-6 grid grid-cols-1 gap-4 xl:grid-cols-[260px_minmax(0,1fr)_300px]">
            <div className="min-w-0">
              <WorkspaceSidebar
                activeTab={activeTab}
                setActiveTab={setActiveTab}
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
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}