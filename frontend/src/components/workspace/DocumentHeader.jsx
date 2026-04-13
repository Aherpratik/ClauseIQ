export default function DocumentHeader({
  document,
  onRerunAnalysis,
  onExportJSON,
  onExportReport,
}) {
  return (
    <section className="w-full min-w-0 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex min-w-0 flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div className="min-w-0 flex-1">
          <h1
            className="truncate text-3xl font-bold tracking-tight text-slate-900"
            title={document.name}
          >
            {document.name}
          </h1>

          <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-slate-500">
            <span className="whitespace-nowrap">Uploaded: {document.uploadedAt}</span>
            <span className="whitespace-nowrap">Pages: {document.pages}</span>
            <span className="whitespace-nowrap">
              Last analyzed: {document.lastAnalyzed}
            </span>
          </div>

          <p className="mt-5 max-w-4xl text-base leading-8 text-slate-700">
            {document.summary}
          </p>
        </div>

        <div className="flex shrink-0 flex-wrap gap-3">
          <button
            type="button"
            onClick={() => {
              console.log("Re-run Analysis clicked");
              onRerunAnalysis?.();
            }}
            className="rounded-xl border border-slate-300 px-5 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            Re-run Analysis
          </button>

          <button
            type="button"
            onClick={() => {
              console.log("Export JSON clicked");
              onExportJSON?.();
            }}
            className="rounded-xl border border-slate-300 px-5 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            Export JSON
          </button>

          <button
            type="button"
            onClick={() => {
              console.log("Export Report clicked");
              onExportReport?.();
            }}
            className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-medium text-white hover:bg-slate-800"
          >
            Export Report
          </button>
        </div>
      </div>
    </section>
  );
}