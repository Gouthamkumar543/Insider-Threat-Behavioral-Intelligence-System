import { useEffect, useState } from "react";
import "./RiskAnalysis.css";
import api from "../../services/api";

function RiskAnalysis() {
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRiskData();
  }, []);

  const loadRiskData = async () => {
    try {
      const response = await api.get("/risk/");
      setRiskData(response.data);
    } catch (error) {
      console.error("Unable to load risk analysis:", error);
      setRiskData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Risk Analysis</h1>
          <p>Analyze employee behavior and insider threat risk levels</p>
        </div>
      </div>

      {loading ? (
        <div className="page-card loading-state">
          Loading risk analysis...
        </div>
      ) : (
        <>
          <div className="risk-summary-grid">
            <div className="risk-summary-card critical-card">
              <span>Critical Risk</span>
              <strong>{riskData?.critical || 0}</strong>
            </div>

            <div className="risk-summary-card high-card">
              <span>High Risk</span>
              <strong>{riskData?.high || 0}</strong>
            </div>

            <div className="risk-summary-card medium-card">
              <span>Medium Risk</span>
              <strong>{riskData?.medium || 0}</strong>
            </div>

            <div className="risk-summary-card low-card">
              <span>Low Risk</span>
              <strong>{riskData?.low || 0}</strong>
            </div>
          </div>

          <div className="page-card risk-explanation">
            <h2>Behavioral Risk Assessment</h2>

            <p>
              The system analyzes employee activity patterns, login behavior,
              file access events, and unusual activities to identify potential
              insider threats.
            </p>

            <div className="risk-progress">
              <div>
                <span>Behavioral Anomalies</span>
                <strong>Monitoring</strong>
              </div>

              <div className="progress-bar">
                <div className="progress-fill"></div>
              </div>
            </div>

            <div className="risk-progress">
              <div>
                <span>Access Pattern Analysis</span>
                <strong>Active</strong>
              </div>

              <div className="progress-bar">
                <div className="progress-fill"></div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default RiskAnalysis;