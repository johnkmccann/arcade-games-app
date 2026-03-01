import { defineConfig, loadEnv, type ServerOptions } from "vite";
import react from "@vitejs/plugin-react";

/**
 * Configure proxy only if VITE_API_URL is set to an absolute URL.
 * This allows:
 * - Development with .env.local: VITE_API_URL=http://localhost:5001 → proxy enabled
 * - Development without env var: no hardcoded defaults → uses relative /api paths
 * - Production: uses relative /api paths (same domain as frontend)
 */
const getProxyConfig = (env: Record<string, string>): Record<string, any> => {
  const apiUrl = env.VITE_API_URL;

  // Only proxy if VITE_API_URL is an absolute URL (http/https)
  if (apiUrl && apiUrl.startsWith("http")) {
    return {
      "/api": {
        target: apiUrl,
        changeOrigin: true,
        rewrite: (path: string) => path,
      },
    };
  }

  // No proxy configured - relative paths will be used
  return {};
};

export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode`
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [react()],
    server: {
      host: "0.0.0.0",
      port: 5173,
      open: false,
      proxy: getProxyConfig(env),
    } satisfies ServerOptions,
    build: {
      outDir: "dist",
    },
  };
});
