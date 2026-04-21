import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

// Wrap any page with this to make it login-only
// Example: <ProtectedRoute><Dashboard /></ProtectedRoute>
export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <div className="loading-screen">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;

  return children;
}
