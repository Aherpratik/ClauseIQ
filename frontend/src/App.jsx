import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AppShell from "/src/components/layout/AppShell.jsx";
import DashboardPage from "./pages/DashboardPage";
import UploadPage from "./pages/UploadPage";
import DocumentsPage from "./pages/DocumentsPage";
import DocumentWorkspacePage from "./pages/DocumentWorkspacePage";

export default function App() {
  return (
    <Router>
      <AppShell>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/documents/:id" element={<DocumentWorkspacePage />} />
        </Routes>
      </AppShell>
    </Router>
  );
}