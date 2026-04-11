import { Link } from "react-router-dom";

export default function UploadCard() {
  return (
    <div className="rounded-xl border border-dashed border-slate-300 bg-white p-8 shadow-sm">
      <h3 className="text-lg font-semibold">Upload a new legal document</h3>
      <p className="mt-2 text-sm text-slate-600">
        Upload PDF agreements, NDAs, leases, and other legal documents for extraction,
        analysis, grounded Q&A, and clause review.
      </p>

      <div className="mt-5">
        <Link
          to="/upload"
          className="inline-flex rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
        >
          Go to Upload
        </Link>
      </div>
    </div>
  );
}