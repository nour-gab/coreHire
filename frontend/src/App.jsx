import { Navigate, Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar";
import DashboardLayout from "./layouts/DashboardLayout";
import AdminDashboard from "./pages/AdminDashboard";
import CandidateDashboard from "./pages/CandidateDashboard";
import CompanyDashboard from "./pages/CompanyDashboard";
import JobsPage from "./pages/JobsPage";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

export default function App() {
  return (
    <div className="min-h-screen bg-core-cloud font-body">
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/jobs" element={<JobsPage />} />

        <Route path="/dashboard/candidate" element={<DashboardLayout role="candidate" />}>
          <Route index element={<CandidateDashboard />} />
        </Route>

        <Route path="/dashboard/company" element={<DashboardLayout role="company" />}>
          <Route index element={<CompanyDashboard />} />
          <Route path="jobs" element={<CompanyDashboard />} />
        </Route>

        <Route path="/dashboard/admin" element={<DashboardLayout role="admin" />}>
          <Route index element={<AdminDashboard />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
