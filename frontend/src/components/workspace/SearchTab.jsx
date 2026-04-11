const results = [
    {
      score: 0.93,
      page: 1,
      text: "Confidential Information includes all non-public, proprietary, or sensitive business, financial, technical, and operational information...",
    },
    {
      score: 0.87,
      page: 2,
      text: "Confidential Information does not include information that is publicly known, independently developed, or rightfully received from another source.",
    },
  ];
  
  export default function SearchTab() {
    return (
      <div className="space-y-4">
        <div className="rounded-lg border border-slate-200 p-4">
          <label className="text-sm font-medium text-slate-700">
            Semantic search
          </label>
          <input
            type="text"
            placeholder="Search for clauses, terms, or obligations"
            className="mt-3 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
          />
          <button className="mt-3 rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800">
            Search
          </button>
        </div>
  
        <div className="space-y-3">
          {results.map((result, index) => (
            <div key={index} className="rounded-lg border border-slate-200 p-4">
              <div className="flex items-center justify-between gap-3">
                <span className="text-xs text-slate-500">Page {result.page}</span>
                <span className="text-xs text-slate-500">
                  Score: {result.score}
                </span>
              </div>
              <p className="mt-3 text-sm leading-6 text-slate-700">{result.text}</p>
            </div>
          ))}
        </div>
      </div>
    );
  }