import { BrowserRouter, Routes, Route } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";

import Dashboard from "./pages/Dashboard/Dashboard";
import Employees from "./pages/Employees/Employees";
import ActivityLogs from "./pages/ActivityLogs/ActivityLogs";
import Alerts from "./pages/Alerts/Alerts";
import RiskAnalysis from "./pages/RiskAnalysis/RiskAnalysis";
import Investigations from "./pages/Investigations/Investigations";
import Reports from "./pages/Reports/Reports";
import Profile from "./pages/Profile/Profile";
import Settings from "./pages/Settings/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/activity-logs" element={<ActivityLogs />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/risk-analysis" element={<RiskAnalysis />} />
          <Route path="/investigations" element={<Investigations />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;