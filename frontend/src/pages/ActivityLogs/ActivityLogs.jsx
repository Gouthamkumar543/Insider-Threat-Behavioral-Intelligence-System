import { useEffect, useState } from "react";
import "./ActivityLogs.css";
import api from "../../services/api";

function ActivityLogs() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadActivities();
  }, []);

  const loadActivities = async () => {
    try {
      const response = await api.get("/login-activity/");
      setActivities(response.data);
    } catch (error) {
      console.error("Unable to load activity logs:", error);
      setActivities([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Activity Logs</h1>
          <p>Monitor employee authentication and system activities</p>
        </div>
      </div>

      <div className="page-card">
        {loading ? (
          <div className="loading-state">Loading activity logs...</div>
        ) : activities.length === 0 ? (
          <div className="empty-state">
            <h3>No activity logs found</h3>
            <p>System activities will appear here.</p>
          </div>
        ) : (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Activity</th>
                  <th>IP Address</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th>Date & Time</th>
                </tr>
              </thead>

              <tbody>
                {activities.map((activity, index) => (
                  <tr key={activity.id || index}>
                    <td>{activity.employee_id || activity.user || "Unknown"}</td>
                    <td>{activity.activity || "Login Attempt"}</td>
                    <td>{activity.ip_address || "N/A"}</td>
                    <td>{activity.location || "Unknown"}</td>

                    <td>
                      <span
                        className={`activity-status ${
                          activity.success ? "success" : "failed"
                        }`}
                      >
                        {activity.success ? "Successful" : "Failed"}
                      </span>
                    </td>

                    <td>
                      {activity.login_time
                        ? new Date(activity.login_time).toLocaleString()
                        : "N/A"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default ActivityLogs;