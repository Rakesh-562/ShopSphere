import { authApi } from "./axiosInstance";

// ✅ This endpoint EXISTS in authservice/app/accounts/views.py
// POST /api/login → { email, password }
// Returns: { access_token: "...", message: "Login successful" }
export const loginUser = (data) => authApi.post("/api/login", data);

// ⚠️ The backend ONLY has a /register route for HTML forms, not JSON API yet.
// This will fail until your teammate adds a POST /api/register route.
export const registerUser = (data) => authApi.post("/api/register", data);

// ⚠️ The backend has no /api/me endpoint yet.
// We fake it using data saved in localStorage at login time.
export const getMe = () => {
  const user = localStorage.getItem("user");
  return Promise.resolve({ data: user ? JSON.parse(user) : null });
};
