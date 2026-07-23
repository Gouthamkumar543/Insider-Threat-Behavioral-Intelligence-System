import { useEffect, useState } from "react";
import "./Alerts.css";
import api from "../../services/api";

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      const response = await api.get("/alerts/");
      setAlerts(response.data);
    } catch (error) {
      console.error("Unable to load alerts:", error);
      setAlerts([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Security Alerts</h1>
          <p>Review and manage detected insider threat alerts</p>
        </div>
      </div>

      <div className="alerts-grid">
        {loading ? (
          <div className="loading-state">Loading alerts...</div>
        ) : alerts.length === 0 ? (
          <div className="empty-state">
            <h3>No active alerts</h3>
            <p>New security alerts will appear here.</p>
          </div>
        ) : (
          alerts.map((alert, index) => (
            <div className="alert-card" key={alert.id || index}>
              <div className="alert-top">
                <span
                  className={`severity ${
                    alert.severity?.toLowerCase() || "medium"
                  }`}
                >
                  {alert.severity || "Medium"}
                </span>

                <span className="alert-date">
                  {alert.created_at
                    ? new Date(alert.created_at).toLocaleDateString()
                    : "Recently"}
                </span>
              </div>

              <h3>{alert.title || "Suspicious Activity Detected"}</h3>

              <p>
                {alert.description ||
                  "Potentially suspicious employee behavior has been detected."}
              </p>

              <div className="alert-footer">
                <span>Employee: {alert.employee_id || "Unknown"}</span>

                <button>Investigate</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Alerts;