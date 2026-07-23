import "./Profile.css";

function Profile() {
  const user = JSON.parse(localStorage.getItem("user")) || {};

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>My Profile</h1>
          <p>Manage your account information</p>
        </div>
      </div>

      <div className="profile-card">
        <div className="profile-avatar">
          {(user.name || user.email || "U").charAt(0).toUpperCase()}
        </div>

        <h2>{user.name || "Security Administrator"}</h2>

        <p className="profile-role">
          {user.role || "Security Manager"}
        </p>

        <div className="profile-details">
          <div>
            <span>Email</span>
            <strong>{user.email || "admin@insiderai.com"}</strong>
          </div>

          <div>
            <span>Role</span>
            <strong>{user.role || "Security Manager"}</strong>
          </div>

          <div>
            <span>Account Status</span>
            <strong className="active-text">Active</strong>
          </div>
        </div>

        <button className="primary-button">Edit Profile</button>
      </div>
    </div>
  );
}

export default Profile;