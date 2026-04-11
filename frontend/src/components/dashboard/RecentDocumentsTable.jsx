import { Link } from "react-router-dom";

const docs = [
  {
    id: "1",
    name: "Basic-Non-Disclosure-Agreement.pdf",
    type: "NDA",
    status: "Analysis Ready",
    updated: "Apr 10, 2026",
  },
  {
    id: "2",
    name: "Vendor-Service-Agreement.pdf",
    type: "Service Agreement",
    status: "Processing",
    updated: "Apr 9, 2026",
  },
  {
    id: "3",
    name: "Office-Lease.pdf",
    type: "Lease",
    status: "Needs Review",
    updated: "Apr 8, 2026",
  },
];

export default function RecentDocumentsTable() {
  return (
    <div className="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
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
          {docs.map((doc) => (
            <tr key={doc.id} className="border-t border-slate-100">
              <td className="px-5 py-4">{doc.name}</td>
              <td className="px-5 py-4">{doc.type}</td>
              <td className="px-5 py-4">{doc.status}</td>
              <td className="px-5 py-4">{doc.updated}</td>
              <td className="px-5 py-4">
                <Link
                  to={`/documents/${doc.id}`}
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