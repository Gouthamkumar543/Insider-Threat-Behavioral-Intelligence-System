import "./Reports.css";

function Reports() {
  const reports = [
    {
      title: "Monthly Threat Intelligence Report",
      type: "Security Analysis",
      date: "Current Month",
    },
    {
      title: "Employee Risk Assessment",
      type: "Risk Analysis",
      date: "Current Month",
    },
    {
      title: "Activity Monitoring Report",
      type: "Activity Logs",
      date: "Current Month",
    },
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Reports</h1>
          <p>Generate and review security intelligence reports</p>
        </div>

        <button className="primary-button">Generate Report</button>
      </div>

      <div className="reports-grid">
        {reports.map((report, index) => (
          <div className="report-card" key={index}>
            <div className="report-icon">📄</div>

            <div className="report-content">
              <h3>{report.title}</h3>
              <p>{report.type}</p>
              <span>{report.date}</span>
            </div>

            <button className="download-button">View</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Reports;