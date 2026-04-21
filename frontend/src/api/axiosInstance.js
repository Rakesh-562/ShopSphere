import axios from "axios";

// Auth service: Flask app runs on port 5000 by default (confirmed in run.py)
// ⚠️ Product service: FastAPI - your teammate will confirm the port
// ⚠️ Orders service: Django - your teammate will confirm the port
const AUTH_BASE_URL = import.meta.env.VITE_AUTH_URL || "http://localhost:5000";
const PRODUCT_BASE_URL = import.meta.env.VITE_PRODUCT_URL || "http://localhost:8000";
const ORDER_BASE_URL = import.meta.env.VITE_ORDER_URL || "http://localhost:8001";

export const authApi = axios.create({ baseURL: AUTH_BASE_URL });
export const productApi = axios.create({ baseURL: PRODUCT_BASE_URL });
export const orderApi = axios.create({ baseURL: ORDER_BASE_URL });

// Attaches JWT token to every request automatically
const attachToken = (instance) => {
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  // If server returns 401 (token expired or invalid), log the user out
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
      return Promise.reject(error);
    }
  );
};

attachToken(authApi);
attachToken(productApi);
attachToken(orderApi);
