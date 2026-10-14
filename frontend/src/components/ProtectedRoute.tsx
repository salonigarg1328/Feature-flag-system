import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/** Sirf logged-in user andar aa sakta hai, warna /login par bhej do. */
export default function ProtectedRoute() {
  const { user, loading } = useAuth();

  if (loading) return <p className="page-note">Loading...</p>;
  if (!user) return <Navigate to="/login" replace />;
  return <Outlet />;
}
