import { Link } from "react-router-dom";



export default function RecentDocumentsTable({ documents = []}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white/80 backdrop-blur-sm shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden">
      <div className="border-b border-slate-200 px-5 py-4">
        <h3 className="text-lg font-semibold">Recent documents</h3>
      </div>

      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-left text-slate-500">
          <tr>
            <th className="px-5 py-3 font-medium">Document</th>
            <th className="px-5 py-3 font-medium">Type</th>
            <th className="px-5 py-3 font-medium">Status</th>
            <th className="px-5 py-3 font-medium">Updated</th>
            <th className="px-5 py-3 font-medium">Open</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((doc) => (
            <tr
            key={doc.document_id}
            className="border-t border-slate-100 hover:bg-slate-50 transition"
            >
              <td className="px-5 py-4">{doc.filename}</td>
              <td className="px-5 py-4">{doc.document_type || "Unknown"}</td>
              <td className="px-5 py-4">{doc.status}</td>
              <td className="px-5 py-4">{doc.updated_at || "-"}</td>
              <td className="px-5 py-4">
                <Link
                  to={`/documents/${doc.document_id}`}
                  className="text-slate-900 underline underline-offset-4"
                >
                  Open
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}