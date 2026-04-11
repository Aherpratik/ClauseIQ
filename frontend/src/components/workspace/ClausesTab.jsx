const clauses = [
    {
      title: "Confidential Information Definition",
      page: 1,
      text: "Confidential Information includes all non-public, proprietary, or sensitive business, financial, technical, and operational information...",
    },
    {
      title: "Exclusions",
      page: 2,
      text: "Confidential Information does not include information that is publicly known, independently developed, or rightfully received from another source.",
    },
    {
      title: "Non-Disclosure Obligations",
      page: 2,
      text: "The Receiving Party shall protect such Confidential Information...",
    },
    {
      title: "Return / Destruction",
      page: 2,
      text: "The Receiving Party shall return or destroy materials upon request.",
    },
  ];
  
  export default function ClausesTab() {
    return (
      <div className="space-y-3">
        {clauses.map((clause) => (
          <div key={clause.title} className="rounded-lg border border-slate-200 p-4">
            <div className="flex items-center justify-between gap-3">
              <h4 className="text-sm font-semibold text-slate-900">
                {clause.title}
              </h4>
              <span className="text-xs text-slate-500">Page {clause.page}</span>
            </div>
  
            <p className="mt-3 text-sm leading-6 text-slate-700">{clause.text}</p>
  
            <button className="mt-3 text-sm font-medium text-slate-900 underline underline-offset-4">
              View in document
            </button>
          </div>
        ))}
      </div>
    );
  }