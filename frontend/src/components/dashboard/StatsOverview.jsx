function StatCard({ title, value, subtitle }) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
        <p className="text-sm text-slate-500">{title}</p>
        <h3 className="mt-2 text-2xl font-semibold">{value}</h3>
        <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
      </div>
    );
  }
  
  export default function StatsOverview() {
    return (
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Total Documents" value="12" subtitle="Across all uploads" />
        <StatCard title="Processed" value="9" subtitle="Ready for review" />
        <StatCard title="Flagged Risks" value="5" subtitle="Across analyzed documents" />
        <StatCard title="Needs Review" value="3" subtitle="Missing key fields" />
      </div>
    );
  }