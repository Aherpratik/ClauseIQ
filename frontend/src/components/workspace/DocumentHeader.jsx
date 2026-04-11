export default function DocumentHeader({ document }) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-start justify-between gap-6">
          <div>
            <h2 className="text-4xl font-semibold tracking-tight text-slate-950">
              {document.name}
            </h2>
  
            <div className="mt-2 flex items-center gap-3 text-sm text-slate-500">
              <span>Uploaded: {document.uploadedAt}</span>
              <span>•</span>
              <span>Pages: {document.pages}</span>
              <span>•</span>
              <span>Last analyzed: {document.lastAnalyzed}</span>
            </div>
  
            <p className="mt-4 max-w-3xl text-base leading-7 text-slate-600">
              {document.summary}
            </p>
          </div>
  
          <div className="flex flex-col items-end gap-3">
            <div className="flex gap-2">
              <button className="rounded-xl border border-slate-300 bg-white px-5 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">
                Re-run Analysis
              </button>
  
              <button className="rounded-xl border border-slate-300 bg-white px-5 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">
                Export JSON
              </button>
            </div>
  
            <button className="rounded-xl bg-slate-950 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-slate-800">
              Export Report
            </button>
          </div>
        </div>
      </div>
    );
  }