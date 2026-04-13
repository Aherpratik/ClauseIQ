export default function KeyFieldsTab({ analysis }) {
  if (!analysis) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4 text-slate-500 shadow-sm">
        Loading key fields...
      </div>
    );
  }

  const baseFields = [
    ["Document Type", analysis.document_type],
    [
      "Parties",
      Array.isArray(analysis.parties) && analysis.parties.length > 0
        ? analysis.parties.join(", ")
        : "",
    ],
    ["Effective Date", analysis.effective_date],
    ["Governing Law", analysis.governing_law],
  ];

  const ndaFields = [
    ["Confidentiality Term", analysis.term],
    ["Return / Destruction", analysis.return_or_destruction_of_materials],
  ];

  const inventionFields = [
    ["Assignment Scope", analysis.term],
    [
      "Work Product / IP",
      analysis.permitted_use || analysis.non_disclosure_obligations,
    ],
  ];

  let fields = baseFields;

  if (analysis.document_type === "NDA") {
    fields = [...baseFields, ...ndaFields];
  } else if (analysis.document_type === "Invention Assignment Agreement") {
    fields = [...baseFields, ...inventionFields];
  }

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