import axios from "axios";

/**
 * Determine the API base URL based on environment:
 * - Development with VITE_API_URL env var: use explicit override (e.g., different backend server)
 * - Production: use relative paths (e.g., /api -> same domain)
 * - Development fallback: use localhost:5001 (local Darts backend)
 */
const getBaseURL = (): string => {
  const envApiUrl = import.meta.env.VITE_API_URL;

  if (envApiUrl) {
    // Explicit override via environment variable
    return envApiUrl;
  }

  // Relative paths work in production (same domain)
  // In development, Vite proxy catches /api/* and forwards to localhost:5001
  return "/api";
};

// Create an Axios instance with base configuration
const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000, // 10 seconds for game operations
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
