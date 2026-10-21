import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    fs: {
      // Allow importing the canonical contract types from packages/shared
      // (src/lib/api.ts) — outside the client/ Vite root.
      allow: ['../..'],
    },
  },
});
