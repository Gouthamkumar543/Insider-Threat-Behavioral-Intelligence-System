import { useEffect, useState } from "react";
import "./Dashboard.css";
import api from "../../services/api";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/dashboard/summary", {
        timeout: 120000,
      });

      console.log("Dashboard API Response:", response.data);

      setDashboard(response.data);
    } catch (error) {
      console.error("Dashboard API Error:", error);

      if (error.code === "ECONNABORTED") {
        setError("Dashboard request timed out.");
      } else {
        setError("Unable to load dashboard data.");
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="status-message">
          <h2>Loading Dashboard...</h2>
          <p>Processing security analytics data...</p>
        </div>
      </div>
    );
  }

  if (error || !dashboard) {
    return (
      <div className="dashboard">
        <div className="status-message error-message">
          <h2>{error || "Unable to load dashboard data."}</h2>

          <button onClick={loadDashboard}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const {
    stats = {},
    riskDistribution = {},
    anomalyDistribution = {},
    topRiskUsers = [],
    recentLogins = [],
    recentFileAccess = [],
  } = dashboard;

  const riskChartData = [
    {
      name: "Critical",
      value: Number(riskDistribution.critical || 0),
    },
    {
      name: "High",
      value: Number(riskDistribution.high || 0),
    },
    {
      name: "Medium",
      value: Number(riskDistribution.medium || 0),
    },
    {
      name: "Low",
      value: Number(riskDistribution.low || 0),
    },
  ];

  const anomalyChartData = [
    {
      name: "Anomalies",
      value: Number(
        anomalyDistribution.anomalies ||
        stats.totalAnomalies ||
        0
      ),
    },
    {
      name: "Normal",
      value: Number(
        anomalyDistribution.normal ||
        Math.max(
          Number(stats.totalEmployees || 0) -
          Number(stats.totalAnomalies || 0),
          0
        )
      ),
    },
  ];

  const activityChartData = [
    {
      name: "Logins",
      value: Number(stats.loginActivities || 0),
    },
    {
      name: "File Access",
      value: Number(stats.fileAccessEvents || 0),
    },
    {
      name: "Anomalies",
      value: Number(stats.totalAnomalies || 0),
    },
  ];

  return (
    <div className="dashboard">

      <div className="dashboard-header">

        <div>
          <h1>Insider Threat Dashboard</h1>

          <p>
            Behavioral intelligence and security monitoring overview
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={loadDashboard}
        >
          Refresh Data
        </button>

      </div>

      <div className="stats-grid">

        <div className="stat-card">
          <span>Total Users</span>

          <strong>
            {Number(
              stats.totalEmployees || 0
            ).toLocaleString()}
          </strong>
        </div>

        <div className="stat-card">
          <span>Login Activities</span>

          <strong>
            {Number(
              stats.loginActivities || 0
            ).toLocaleString()}
          </strong>
        </div>

        <div className="stat-card">
          <span>File Access Events</span>

          <strong>
            {Number(
              stats.fileAccessEvents || 0
            ).toLocaleString()}
          </strong>
        </div>

        <div className="stat-card">
          <span>Total Anomalies</span>

          <strong>
            {Number(
              stats.totalAnomalies || 0
            ).toLocaleString()}
          </strong>
        </div>

        <div className="stat-card critical-card">
          <span>Critical Risk</span>

          <strong>
            {Number(
              stats.criticalRisk || 0
            ).toLocaleString()}
          </strong>
        </div>

        <div className="stat-card high-card">
          <span>High Risk</span>

          <strong>
            {Number(
              stats.highRisk || 0
            ).toLocaleString()}
          </strong>
        </div>

        <div className="stat-card">
          <span>Medium Risk</span>

          <strong>
            {Number(
              stats.mediumRisk || 0
            ).toLocaleString()}
          </strong>
        </div>

        <div className="stat-card">
          <span>Low Risk</span>

          <strong>
            {Number(
              stats.lowRisk || 0
            ).toLocaleString()}
          </strong>
        </div>

      </div>

      <div className="charts-grid">

        <div className="dashboard-box chart-box">

          <div className="box-header">
            <h2>Risk Distribution</h2>
          </div>

          <div className="chart-container">

            <ResponsiveContainer
              width="100%"
              height={320}
            >

              <PieChart>

                <Pie
                  data={riskChartData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={105}
                  label
                >

                  {riskChartData.map(
                    (entry, index) => (
                      <Cell
                        key={`risk-cell-${index}`}
                      />
                    )
                  )}

                </Pie>

                <Tooltip />

                <Legend />

              </PieChart>

            </ResponsiveContainer>

          </div>

        </div>

        <div className="dashboard-box chart-box">

          <div className="box-header">
            <h2>Activity Overview</h2>
          </div>

          <div className="chart-container">

            <ResponsiveContainer
              width="100%"
              height={320}
            >

              <BarChart
                data={activityChartData}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="name"
                />

                <YAxis />

                <Tooltip />

                <Bar
                  dataKey="value"
                  name="Events"
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

        <div className="dashboard-box chart-box">

          <div className="box-header">
            <h2>Anomaly Detection</h2>
          </div>

          <div className="chart-container">

            <ResponsiveContainer
              width="100%"
              height={320}
            >

              <PieChart>

                <Pie
                  data={anomalyChartData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={105}
                  label
                >

                  {anomalyChartData.map(
                    (entry, index) => (
                      <Cell
                        key={`anomaly-cell-${index}`}
                      />
                    )
                  )}

                </Pie>

                <Tooltip />

                <Legend />

              </PieChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>

      <div className="dashboard-box">

        <div className="box-header">
          <h2>Risk Distribution Summary</h2>
        </div>

        <div className="risk-list">

          <div className="risk-item critical">
            <span>Critical</span>

            <strong>
              {riskDistribution.critical || 0}
            </strong>
          </div>

          <div className="risk-item high">
            <span>High</span>

            <strong>
              {riskDistribution.high || 0}
            </strong>
          </div>

          <div className="risk-item medium">
            <span>Medium</span>

            <strong>
              {riskDistribution.medium || 0}
            </strong>
          </div>

          <div className="risk-item low">
            <span>Low</span>

            <strong>
              {riskDistribution.low || 0}
            </strong>
          </div>

        </div>

      </div>

      <div className="dashboard-box">

        <div className="box-header">
          <h2>Top Risk Users</h2>
        </div>

        <div className="table-container">

          <table>

            <thead>

              <tr>
                <th>User</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Login Count</th>
              </tr>

            </thead>

            <tbody>

              {topRiskUsers.length === 0 ? (

                <tr>
                  <td
                    colSpan="4"
                    className="empty-message"
                  >
                    No risk data available
                  </td>
                </tr>

              ) : (

                topRiskUsers.map(
                  (user, index) => (

                    <tr
                      key={`${user.user}-${index}`}
                    >

                      <td>
                        {user.user}
                      </td>

                      <td>
                        {Number(
                          user.risk_score || 0
                        ).toFixed(2)}
                      </td>

                      <td>

                        <span
                          className={`risk-badge ${
                            user.risk_level?.toLowerCase() || "low"
                          }`}
                        >
                          {user.risk_level || "Low"}
                        </span>

                      </td>

                      <td>
                        {user.login_count || 0}
                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>

      <div className="dashboard-box">

        <div className="box-header">
          <h2>Recent Login Activity</h2>
        </div>

        <div className="table-container">

          <table>

            <thead>

              <tr>
                <th>User</th>
                <th>Computer</th>
                <th>Date</th>
                <th>Activity</th>
              </tr>

            </thead>

            <tbody>

              {recentLogins.length === 0 ? (

                <tr>
                  <td
                    colSpan="4"
                    className="empty-message"
                  >
                    No login activity available
                  </td>
                </tr>

              ) : (

                recentLogins.map(
                  (login, index) => (

                    <tr
                      key={`${login.id}-${index}`}
                    >

                      <td>
                        {login.user}
                      </td>

                      <td>
                        {login.pc}
                      </td>

                      <td>
                        {login.date}
                      </td>

                      <td>
                        {login.activity}
                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>

      <div className="dashboard-box">

        <div className="box-header">
          <h2>Recent File Access</h2>
        </div>

        <div className="table-container">

          <table>

            <thead>

              <tr>
                <th>User</th>
                <th>Computer</th>
                <th>Date</th>
                <th>Filename</th>
              </tr>

            </thead>

            <tbody>

              {recentFileAccess.length === 0 ? (

                <tr>
                  <td
                    colSpan="4"
                    className="empty-message"
                  >
                    No file access activity available
                  </td>
                </tr>

              ) : (

                recentFileAccess.map(
                  (file, index) => (

                    <tr
                      key={`${file.id}-${index}`}
                    >

                      <td>
                        {file.user}
                      </td>

                      <td>
                        {file.pc}
                      </td>

                      <td>
                        {file.date}
                      </td>

                      <td>
                        {file.filename}
                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;