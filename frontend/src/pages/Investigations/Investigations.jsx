import { useState } from "react";
import "./Investigations.css";

function Investigations() {
  const [investigations, setInvestigations] = useState([]);

  const createInvestigation = () => {
    const newInvestigation = {
      id: investigations.length + 1,
      title: "New Security Investigation",
      status: "Open",
      priority: "High",
      created: new Date().toLocaleDateString(),
    };

    setInvestigations([...investigations, newInvestigation]);
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Investigations</h1>
          <p>Manage and investigate suspicious insider threat activities</p>
        </div>

        <button className="primary-button" onClick={createInvestigation}>
          + New Investigation
        </button>
      </div>

      <div className="investigation-grid">
        {investigations.length === 0 ? (
          <div className="empty-state">
            <h3>No investigations yet</h3>
            <p>Start an investigation from a security alert.</p>
          </div>
        ) : (
          investigations.map((investigation) => (
            <div className="investigation-card" key={investigation.id}>
              <div className="investigation-header">
                <span className="case-id">
                  CASE-{String(investigation.id).padStart(4, "0")}
                </span>

                <span className="investigation-status">
                  {investigation.status}
                </span>
              </div>

              <h3>{investigation.title}</h3>

              <div className="investigation-details">
                <p>
                  <strong>Priority:</strong> {investigation.priority}
                </p>

                <p>
                  <strong>Created:</strong> {investigation.created}
                </p>
              </div>

              <button className="view-button">View Investigation</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Investigations;