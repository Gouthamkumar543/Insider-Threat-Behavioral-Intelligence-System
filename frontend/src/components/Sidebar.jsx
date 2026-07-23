import "./Sidebar.css";
import {
  LayoutDashboard,
  Users,
  Activity,
  ShieldAlert,
  BarChart3,
  Search,
  FileText,
  User,
  Settings,
  LogOut,
} from "lucide-react";
import { NavLink } from "react-router-dom";

function Sidebar() {
  const menuItems = [
    {
      title: "Dashboard",
      path: "/dashboard",
      icon: <LayoutDashboard size={20} />,
    },
    {
      title: "Employees",
      path: "/employees",
      icon: <Users size={20} />,
    },
    {
      title: "Activity Logs",
      path: "/activity-logs",
      icon: <Activity size={20} />,
    },
    {
      title: "Alerts",
      path: "/alerts",
      icon: <ShieldAlert size={20} />,
    },
    {
      title: "Risk Analysis",
      path: "/risk-analysis",
      icon: <BarChart3 size={20} />,
    },
    {
      title: "Investigations",
      path: "/investigations",
      icon: <Search size={20} />,
    },
    {
      title: "Reports",
      path: "/reports",
      icon: <FileText size={20} />,
    },
    {
      title: "Profile",
      path: "/profile",
      icon: <User size={20} />,
    },
    {
      title: "Settings",
      path: "/settings",
      icon: <Settings size={20} />,
    },
  ];

  return (
    <aside className="sidebar">

      <div className="logo">
        <h2>🛡️ Insider AI</h2>
      </div>

      <nav className="menu">
        {menuItems.map((item, index) => (
          <NavLink
            key={index}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "menu-item active" : "menu-item"
            }
          >
            {item.icon}
            <span>{item.title}</span>
          </NavLink>
        ))}
      </nav>

      <div className="logout">
        <button>
          <LogOut size={18} />
          Logout
        </button>
      </div>

    </aside>
  );
}

export default Sidebar;