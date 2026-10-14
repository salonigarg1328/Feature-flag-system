import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="app">
      <header className="topbar">
        <span className="brand">Feature Flags</span>
        <div className="topbar-right">
          <span className="topbar-user">{user?.name}</span>
          <button className="btn btn-quiet" onClick={logout}>
            Sign out
          </button>
        </div>
      </header>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
