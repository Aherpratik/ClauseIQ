export default function DocumentViewer({ pages = [] }) {
    return (
      <section className="h-full rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-200 pb-4">
          <h3 className="text-2xl font-semibold text-slate-900">
            Document Viewer
          </h3>
  
          <div className="flex items-center gap-2">
            <button className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
              Zoom In
            </button>
            <button className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
              Zoom Out
            </button>
          </div>
        </div>
  
        <div className="mt-5 h-[calc(100%-5.5rem)] overflow-y-auto rounded-xl bg-slate-100 p-6 space-y-6">
          {pages.length === 0 ? (
            <div className="rounded-xl border border-slate-200 bg-white p-6 text-slate-500 shadow-sm">
              No extracted pages available.
            </div>
          ) : (
            pages.map((page, index) => (
              <div
                key={index}
                className="w-full rounded-2xl border border-slate-200 bg-white px-10 py-8 shadow-sm"
              >
                <div className="mb-4 text-xs font-semibold uppercase tracking-[0.12em] text-slate-400">
                  Page {page.page_number}
                </div>
  
                <p className="whitespace-pre-line text-[15px] leading-8 text-slate-700">
                  {page.text}
                </p>
              </div>
            ))
          )}
        </div>
      </section>
    );
  }