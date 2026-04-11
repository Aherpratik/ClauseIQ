import { NavLink } from "react-router-dom";

const navItemClass = ({ isActive }) =>
  `block rounded-xl px-4 py-3 text-sm font-medium transition ${
    isActive
      ? "bg-slate-950 text-white shadow-sm"
      : "text-slate-700 hover:bg-slate-100 hover:text-slate-900"
  }`;

export default function Sidebar() {
  return (
    <aside className="w-56 min-h-[calc(100vh-5rem)] border-r border-slate-200 bg-white p-4">
      <nav className="space-y-2">
        <NavLink to="/" className={navItemClass}>
          Dashboard
        </NavLink>
        <NavLink to="/upload" className={navItemClass}>
          Upload
        </NavLink>
        <NavLink to="/documents" className={navItemClass}>
          Documents
        </NavLink>
      </nav>
    </aside>
  );
}