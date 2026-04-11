import TopNav from "./TopNav";
import Sidebar from "./Sidebar";

export default function AppShell({ children }) {
  return (
    <div className="bg-slate-50 min-h-screen text-slate-900">
      <TopNav />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}