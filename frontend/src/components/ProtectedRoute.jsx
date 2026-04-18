import { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";

import client from "../api/client";

export default function ProtectedRoute({ allowedRoles = [] }) {
  const location = useLocation();
  const [state, setState] = useState({ loading: true, user: null });

  useEffect(() => {
    let mounted = true;

    const loadUser = async () => {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        if (mounted) {
          setState({ loading: false, user: null });
        }
        return;
      }

      try {
        const { data } = await client.get("/auth/me/");
        if (mounted) {
          setState({ loading: false, user: data?.user || null });
        }
      } catch {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        if (mounted) {
          setState({ loading: false, user: null });
        }
      }
    };

    loadUser();
    return () => {
      mounted = false;
    };
  }, []);

  if (state.loading) {
    return (
      <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-3xl items-center justify-center px-4">
        <p className="text-sm text-core-ink/70">Checking account access...</p>
      </div>
    );
  }

  if (!state.user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (allowedRoles.length && !allowedRoles.includes(state.user.role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
