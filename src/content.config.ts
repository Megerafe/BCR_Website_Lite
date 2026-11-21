/**
 * Content model for the one-page Lite website.
 *
 * All editable text and images live in the YAML files inside `src/content/`.
 * This file only describes what fields each YAML file must contain, so that a
 * typo (e.g. a missing image) shows a clear error when you run `npm run dev`.
 */
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { file } from 'astro/loaders';
import { parse } from 'yaml';

/** Loads a YAML file that describes ONE thing (not a list), e.g. site.yaml. */
const single = (path: string) =>
  file(path, { parser: (text) => [{ id: 'main', ...(parse(text) ?? {}) }] });

const link = z.object({ label: z.string(), href: z.string() });

/* ------------------------------------------------------------------ site */
const site = defineCollection({
  loader: single('src/content/site.yaml'),
  schema: z.object({
    name: z.string(),
    tagline: z.string(),
    description: z.string(),
    founder: z.string(),
    location: z.string().default(''),
    serviceArea: z.string().default(''),
    email: z.string().default(''),
    phone: z.string().default(''),
    businessId: z.string().default(''),
    instagram: z.object({ handle: z.string(), url: z.string() }).partial().default({}),
    tiktok: z.object({ handle: z.string(), url: z.string() }).partial().default({}),
    formspreeId: z.string(),
    announcement: z.array(z.string()).default([]),
    nav: z.array(link),
    cta: link,
  }),
});

/* ------------------------------------------------------------------ home */
const home = defineCollection({
  loader: single('src/content/home.yaml'),
  schema: ({ image }) =>
    z.object({
      seo: z.object({ title: z.string(), description: z.string() }),
      hero: z.object({
        eyebrow: z.string(),
        title: z.string(),
        text: z.string(),
        primary: link,
        secondary: link,
        image: image(),
        imageAlt: z.string(),
        secondImage: image().optional(),
        secondImageAlt: z.string().default(''),
      }),
      services: z.object({ title: z.string(), text: z.string(), cta: link }),
      split: z.object({
        eyebrow: z.string(),
        title: z.string(),
        text: z.string(),
        cta: link,
        image: image(),
        imageAlt: z.string(),
      }),
      packages: z.object({
        title: z.string(),
        text: z.string(),
        customTitle: z.string(),
        customText: z.string(),
        customCta: link,
      }),
      process: z.object({
        title: z.string(),
        text: z.string(),
        steps: z.array(z.object({ title: z.string(), text: z.string() })),
      }),
      about: z.object({
        eyebrow: z.string(),
        title: z.string(),
        text: z.string(),
        cta: link,
        image: image(),
        imageAlt: z.string(),
      }),
    }),
});

/* -------------------------------------------------------------- services */
const services = defineCollection({
  loader: file('src/content/services.yaml'),
  schema: ({ image }) =>
    z.object({
      word: z.string(),
      title: z.string(),
      short: z.string(),
      description: z.string(),
      includes: z.array(z.string()).default([]),
      price: z.string().default(''),
      image: image(),
      imageAlt: z.string(),
    }),
});

/* -------------------------------------------------------------- packages */
const packages = defineCollection({
  loader: file('src/content/packages.yaml'),
  schema: z.object({
    name: z.string(),
    subtitle: z.string(),
    description: z.string(),
    includes: z.array(z.string()),
    price: z.string().default(''),
    badge: z.string().default(''),
    featured: z.boolean().default(false),
  }),
});

/* ------------------------------------------------------------------- faq */
const faq = defineCollection({
  loader: file('src/content/faq.yaml'),
  schema: z.object({ question: z.string(), answer: z.string() }),
});

/* ----------------------------------------------------------------- pages */
const pages = defineCollection({
  loader: file('src/content/pages.yaml'),
  schema: z.object({
    eyebrow: z.string().default(''),
    title: z.string(),
    intro: z.string().default(''),
    formTitle: z.string().default(''),
    formIntro: z.string().default(''),
    body: z.array(z.object({ heading: z.string(), text: z.string() })).default([]),
  }),
});

export const collections = { site, home, services, packages, faq, pages };
