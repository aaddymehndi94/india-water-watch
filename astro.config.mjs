import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';

const base = process.env.PUBLIC_BASE_PATH || '/';

export default defineConfig({
  site: process.env.PUBLIC_SITE_URL || 'https://aaddymehndi94.github.io',
  base,
  output: 'static',
  trailingSlash: 'always',
  integrations: [react()],
  vite: { plugins: [tailwindcss()] },
});
