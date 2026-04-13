const tabs = [
  { id: "overview", label: "Overview" },
  { id: "fields", label: "Key Fields" },
  { id: "clauses", label: "Clauses" },
  { id: "risks", label: "Risks" },
  { id: "ask-ai", label: "Ask AI" },
  { id: "search", label: "Search" },
];

export default function WorkspaceSidebar({
  activeTab,
  setActiveTab,
  analysis,
}) {
  const clauses = analysis?.clauses || [];
  const risks = analysis?.risks || [];

  const highCount = risks.filter((r) => r.severity === "high").length;
  const mediumCount = risks.filter((r) => r.severity === "medium").length;
  const lowCount = risks.filter((r) => r.severity === "low").length;

  return (
    <aside className="col-span-12 lg:col-span-2 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div>
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Review Workspace
        </h3>
        <div className="mt-4 space-y-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full rounded-md px-3 py-2 text-left text-sm font-medium transition ${
                activeTab === tab.id
                  ? "bg-slate-900 text-white"
                  : "text-slate-700 hover:bg-slate-100"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-8">
        <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">
          Clause Navigator
        </h3>
        <div className="mt-3 space-y-2">
          {clauses.length > 0 ? (
            clauses.map((item, index) => (
              <div
                key={`${item}-${index}`}
                className="rounded-md border border-slate-200 px-3 py-2 text-sm text-slate-600"
              >
                {item}
              </div>
            ))
          ) : (
            <div className="rounded-md border border-slate-200 px-3 py-2 text-sm text-slate-400">
              No clauses detected
            </div>
          )}
        </div>
      </div>

      <div className="mt-8">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Risk Summary
        </h3>
        <div className="mt-3 space-y-2 text-sm">
          <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-red-700">
            {highCount} High
          </div>
          <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-amber-700">
            {mediumCount} Medium
          </div>
          <div className="rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-slate-700">
            {lowCount} Low
          </div>
        </div>
      </div>
    </aside>
  );
}