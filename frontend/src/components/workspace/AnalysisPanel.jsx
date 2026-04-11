import OverviewTab from "./OverviewTab";
import KeyFieldsTab from "./KeyFieldsTab";
import ClausesTab from "./ClausesTab";
import RisksTab from "./RisksTab";
import AskAITab from "./AskAITab";
import SearchTab from "./SearchTab";

const tabLabels = [
  { id: "overview", label: "Overview" },
  { id: "fields", label: "Key Fields" },
  { id: "clauses", label: "Clauses" },
  { id: "risks", label: "Risks" },
  { id: "ask-ai", label: "Ask AI" },
  { id: "search", label: "Search" },
];

export default function AnalysisPanel({ activeTab, setActiveTab, analysis }) {
  const isLoading = analysis === null;

  return (
    <aside className="h-full rounded-2xl border border-slate-200 bg-white p-5 shadow-sm overflow-hidden">
      <div className="border-b border-slate-200 pb-4">
        <h3 className="text-2xl font-semibold text-slate-950">Analysis</h3>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          Review structured results, risks, and grounded answers.
        </p>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {tabLabels.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`rounded-xl px-3.5 py-2 text-sm font-semibold transition ${
              activeTab === tab.id
                ? "bg-slate-950 text-white shadow-sm"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="mt-5 h-[calc(100%-9rem)] overflow-y-auto pr-1">
        {isLoading ? (
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
            Loading analysis...
          </div>
        ) : (
          <>
            {activeTab === "overview" && <OverviewTab analysis={analysis} />}
            {activeTab === "fields" && <KeyFieldsTab analysis={analysis} />}
            {activeTab === "clauses" && <ClausesTab analysis={analysis} />}
            {activeTab === "risks" && <RisksTab analysis={analysis} />}
            {activeTab === "ask-ai" && <AskAITab analysis={analysis} />}
            {activeTab === "search" && <SearchTab analysis={analysis} />}
          </>
        )}
      </div>
    </aside>
  );
}