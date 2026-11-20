// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// Change this to the real domain once it is bought (e.g. https://www.beautycontentroom.fi).
// On Cloudflare Pages you can also set an environment variable called SITE_URL.
const SITE_URL = process.env.SITE_URL ?? 'https://beautycontentroom.pages.dev';

export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
    server: {
      cors: true,
      allowedHosts: true,
    },
    preview: {
      cors: true,
      allowedHosts: true,
    },
  },
});
