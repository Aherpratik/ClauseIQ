const tabs = [
    { id: "overview", label: "Overview" },
    { id: "fields", label: "Key Fields" },
    { id: "clauses", label: "Clauses" },
    { id: "risks", label: "Risks" },
    { id: "ask-ai", label: "Ask AI" },
    { id: "search", label: "Search" },
  ];
  
  const clauseLinks = [
    "Confidential Information",
    "Exclusions",
    "Obligations",
    "Return / Destruction",
    "Term / Survival",
    "Governing Law",
  ];
  
  export default function WorkspaceSidebar({ activeTab, setActiveTab }) {
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
            {clauseLinks.map((item) => (
              <div
                key={item}
                className="rounded-md border border-slate-200 px-3 py-2 text-sm text-slate-600"
              >
                {item}
              </div>
            ))}
          </div>
        </div>
  
        <div className="mt-8">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            Risk Summary
          </h3>
          <div className="mt-3 space-y-2 text-sm">
            <div className="rounded-md bg-red-50 border border-red-200 px-3 py-2 text-red-700">
              1 High
            </div>
            <div className="rounded-md bg-amber-50 border border-amber-200 px-3 py-2 text-amber-700">
              2 Medium
            </div>
            <div className="rounded-md bg-slate-50 border border-slate-200 px-3 py-2 text-slate-700">
              3 Low
            </div>
          </div>
        </div>
      </aside>
    );
  }