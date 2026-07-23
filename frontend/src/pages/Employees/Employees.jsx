import { useEffect, useState } from "react";
import "./Employees.css";
import api from "../../services/api";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      const response = await api.get("/employees/");
      setEmployees(response.data);
    } catch (error) {
      console.error("Unable to load employees:", error);
      setEmployees([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredEmployees = employees.filter((employee) =>
    `${employee.name || ""} ${employee.email || ""} ${employee.department || ""}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Employees</h1>
          <p>Monitor and manage employee security profiles</p>
        </div>

        <button className="primary-button">+ Add Employee</button>
      </div>

      <div className="page-card">
        <div className="table-toolbar">
          <input
            type="text"
            placeholder="Search employees..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="loading-state">Loading employees...</div>
        ) : filteredEmployees.length === 0 ? (
          <div className="empty-state">
            <h3>No employees found</h3>
            <p>Employee records will appear here.</p>
          </div>
        ) : (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Email</th>
                  <th>Department</th>
                  <th>Role</th>
                  <th>Risk Level</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {filteredEmployees.map((employee, index) => (
                  <tr key={employee.id || index}>
                    <td>
                      <div className="employee-info">
                        <div className="employee-avatar">
                          {(employee.name || "E").charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <strong>{employee.name || "Unknown Employee"}</strong>
                          <span>ID: {employee.id || "N/A"}</span>
                        </div>
                      </div>
                    </td>

                    <td>{employee.email || "Not available"}</td>
                    <td>{employee.department || "Security"}</td>
                    <td>{employee.role || "Employee"}</td>

                    <td>
                      <span
                        className={`risk-badge ${
                          employee.risk_level?.toLowerCase() || "low"
                        }`}
                      >
                        {employee.risk_level || "Low"}
                      </span>
                    </td>

                    <td>
                      <span className="status-badge active">Active</span>
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

export default Employees;