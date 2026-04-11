import StatsOverview from "../components/dashboard/StatsOverview";
import UploadCard from "../components/dashboard/UploadCard";
import RecentDocumentsTable from "../components/dashboard/RecentDocumentsTable";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">Dashboard</h2>
        <p className="text-sm text-slate-600 mt-1">
          Review uploaded legal documents, processing status, and recent analyses.
        </p>
      </div>

      <StatsOverview />
      <UploadCard />
      <RecentDocumentsTable />
    </div>
  );
}
