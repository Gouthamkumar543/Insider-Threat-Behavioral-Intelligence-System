import { useState } from "react";
import "./Settings.css";

function Settings() {
  const [notifications, setNotifications] = useState(true);
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p>Configure your Insider AI security system</p>
        </div>
      </div>

      <div className="settings-card">
        <h2>Notification Settings</h2>

        <div className="setting-row">
          <div>
            <strong>Security Notifications</strong>
            <p>Receive notifications for important security events.</p>
          </div>

          <label className="switch">
            <input
              type="checkbox"
              checked={notifications}
              onChange={() => setNotifications(!notifications)}
            />
            <span></span>
          </label>
        </div>

        <div className="setting-row">
          <div>
            <strong>Email Alerts</strong>
            <p>Receive critical threat alerts through email.</p>
          </div>

          <label className="switch">
            <input
              type="checkbox"
              checked={emailAlerts}
              onChange={() => setEmailAlerts(!emailAlerts)}
            />
            <span></span>
          </label>
        </div>

        <h2>Appearance</h2>

        <div className="setting-row">
          <div>
            <strong>Dark Mode</strong>
            <p>Enable dark mode for the dashboard.</p>
          </div>

          <label className="switch">
            <input
              type="checkbox"
              checked={darkMode}
              onChange={() => setDarkMode(!darkMode)}
            />
            <span></span>
          </label>
        </div>

        <button className="save-button">Save Settings</button>
      </div>
    </div>
  );
}

export default Settings;