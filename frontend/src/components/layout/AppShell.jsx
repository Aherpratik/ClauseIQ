import TopNav from "./TopNav";
import Sidebar from "./Sidebar";

export default function AppShell({ children }) {
  return (
    <div className="relative min-h-screen text-slate-900 bg-gradient-to-br from-slate-50 via-white to-slate-100">
      
      {/* subtle background pattern */}
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(#f1f5f9_1px,transparent_1px)] [background-size:24px_24px]" />

      <TopNav />

      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}