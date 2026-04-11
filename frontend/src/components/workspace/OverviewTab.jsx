export default function OverviewTab({ analysis }) {
    if (!analysis) {
      return (
        <div className="rounded-xl border border-slate-200 bg-white p-4 text-slate-500 shadow-sm">
          Loading analysis...
        </div>
      );
    }
  
    const items = [
      { label: "Document Type", value: analysis.document_type || "Not found" },
      { label: "Parties", value: analysis.parties || "Not found" },
      { label: "Effective Date", value: analysis.effective_date || "Not found" },
      { label: "Governing Law", value: analysis.governing_law || "Not found" },
      {
        label: "Confidentiality Term",
        value: analysis.confidentiality_term || "Not found",
      },
      {
        label: "Return / Destruction",
        value: analysis.return_destruction || "Not found",
      },
    ];
  
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