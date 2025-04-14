import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    host: true,         // Accept connections from Docker host
    port: 5173,
  },
});


