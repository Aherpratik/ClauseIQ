export default function AskAITab() {
    return (
      <div className="space-y-4">
        <div className="rounded-lg border border-slate-200 p-4">
          <label className="text-sm font-medium text-slate-700">
            Ask a question about this document
          </label>
          <textarea
            rows={4}
            placeholder="What is considered confidential information in this agreement?"
            className="mt-3 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
          />
          <button className="mt-3 rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800">
            Ask ClauseIQ
          </button>
        </div>
  
        <div className="rounded-lg border border-slate-200 p-4">
          <h4 className="text-sm font-semibold text-slate-900">Answer</h4>
          <p className="mt-3 text-sm leading-6 text-slate-700">
            The agreement defines confidential information as non-public,
            proprietary, business, financial, technical, and operational
            information disclosed by the Disclosing Party.
          </p>
  
          <div className="mt-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              Evidence
            </p>
            <div className="mt-2 rounded-md bg-slate-50 p-3 text-sm text-slate-700 border border-slate-200">
              Page 1: “Confidential Information includes all non-public,
              proprietary, or sensitive business, financial, technical, and
              operational information...”
            </div>
          </div>
        </div>
      </div>
    );
  }