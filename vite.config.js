import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/timetablegeneration/",
  test: {
    globals: true,
    environment: 'jsdom',
  },
  alias: {
    '@emotion/styled': '@emotion/styled',
    '@emotion/react': '@emotion/react',
    '@mui/x-date-pickers': '@mui/x-date-pickers',

  }
})
