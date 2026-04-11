import { Link } from "react-router-dom";

export default function TopNav() {
  return (
    <header className="h-20 border-b border-slate-200 bg-white px-6 flex items-center justify-between">
      <div>
        <h1 className="text-4xl font-semibold tracking-tight text-slate-950">
          ClauseIQ
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          AI-powered legal document analysis with grounded evidence
        </p>
      </div>

      <div className="flex items-center gap-3">
        <Link
          to="/upload"
          className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
        >
          Upload Document
        </Link>
      </div>
    </header>
  );
}