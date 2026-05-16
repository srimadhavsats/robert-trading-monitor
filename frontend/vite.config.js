import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(), // Adds Tailwind directly to the build pipeline
  ],
  server: {
    port: 5174,
    host: "127.0.0.1",
    strictPort: true,
  },
});
