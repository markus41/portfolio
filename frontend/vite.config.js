import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  },
  build: {
    rollupOptions: {
      input: {
        editor: resolve(__dirname, 'index.html'),
        dashboard: resolve(__dirname, 'dashboard/index.html')
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom'
  }
});
