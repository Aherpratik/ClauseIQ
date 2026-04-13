export default function OverviewTab({ analysis }) {
  if (!analysis) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4 text-slate-500 shadow-sm">
        Loading analysis...
      </div>
    );
  }

  const baseItems = [
    { label: "Document Type", value: analysis.document_type || "Not found" },
    {
      label: "Parties",
      value:
        Array.isArray(analysis.parties) && analysis.parties.length > 0
          ? analysis.parties.join(", ")
          : "Not found",
    },
    { label: "Effective Date", value: analysis.effective_date || "Not found" },
    { label: "Governing Law", value: analysis.governing_law || "Not found" },
  ];

  const ndaItems = [
    {
      label: "Confidentiality Term",
      value: analysis.term || "Not found",
    },
    {
      label: "Return / Destruction",
      value: analysis.return_or_destruction_of_materials || "Not found",
    },
  ];

  const inventionItems = [
    {
      label: "Assignment Scope",
      value: analysis.term || "Not found",
    },
    {
      label: "Work Product / IP",
      value:
        analysis.permitted_use ||
        analysis.non_disclosure_obligations ||
        "Not found",
    },
  ];

  let items = baseItems;

  if (analysis.document_type === "NDA") {
    items = [...baseItems, ...ndaItems];
  } else if (analysis.document_type === "Invention Assignment Agreement") {
    items = [...baseItems, ...inventionItems];
  }

  return (
    <div className="space-y-3">
      {items.map((item) => (
        <div
          key={item.label}
          className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
        >
          <p className="text-sm text-slate-500">{item.label}</p>
          <p className="mt-1 text-sm font-semibold text-slate-900">
            {item.value}
          </p>
        </div>
      ))}
    </div>
  );
}