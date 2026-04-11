export default function KeyFieldsTab({ analysis }) {
    if (!analysis) {
      return (
        <div className="rounded-xl border border-slate-200 bg-white p-4 text-slate-500 shadow-sm">
          Loading key fields...
        </div>
      );
    }
  
    const fields = [
      ["Document Type", analysis.document_type],
      ["Parties", analysis.parties],
      ["Effective Date", analysis.effective_date],
      ["Governing Law", analysis.governing_law],
      ["Confidentiality Term", analysis.confidentiality_term],
      ["Return / Destruction", analysis.return_destruction],
    ];
  
    return (
      <div className="space-y-3">
        {fields.map(([name, value]) => (
          <div
            key={name}
            className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
          >
            <p className="text-sm text-slate-500">{name}</p>
            <p className="mt-1 text-sm font-semibold text-slate-900">
              {value || "Not found"}
            </p>
          </div>
        ))}
      </div>
    );
  }