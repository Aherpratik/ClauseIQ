export default function RisksTab({ analysis }) {
    if (!analysis) {
      return (
        <div className="rounded-xl border border-slate-200 bg-white p-4 text-slate-500 shadow-sm">
          Loading risks...
        </div>
      );
    }
  
    const risks = analysis.risks || [];
  
    if (risks.length === 0) {
      return (
        <div className="rounded-xl border border-slate-200 bg-white p-4 text-slate-500 shadow-sm">
          No risks detected.
        </div>
      );
    }
  
    return (
      <div className="space-y-3">
        {risks.map((risk, index) => (
          <div
            key={index}
            className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
          >
            <div className="flex items-center justify-between gap-3">
              <h4 className="text-sm font-semibold text-slate-900">
                {risk.title || "Untitled Risk"}
              </h4>
              <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700">
                {risk.severity || "unknown"}
              </span>
            </div>
  
            <p className="mt-3 text-sm text-slate-700">
              {risk.description || "No description available."}
            </p>
  
            {risk.recommendation && (
              <div className="mt-3 rounded-md bg-slate-50 p-3 text-sm text-slate-700 border border-slate-200">
                <span className="font-medium">Recommendation:</span>{" "}
                {risk.recommendation}
              </div>
            )}
          </div>
        ))}
      </div>
    );
  }