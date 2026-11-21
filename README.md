# BeautyContentRoom – Lite website

A lighter, **one-page** version of the **BeautyContentRoom** website built with the exact same design system, colours, fonts, and editable YAML structure as [`BCR_Website`](https://github.com/Megerafe/BCR_Website).

- **Single-page flow:** Full-width Hero · Hero text · Palvelut · Bränditarina · Paketit · Prosessi · Tietoa · **Ota yhteyttä (form + contact details)** · Usein kysyttyä (FAQ) + in-page Tietosuojaseloste modal.
- **Smooth anchor navigation:** Every header link, hero button, service card, and package card scrolls smoothly to the relevant section — clicking a service or package automatically pre-selects it in the contact form.
- **Contact form:** Sends enquiries to Formspree (`xljdyznw`), with Finnish validation, honeypot spam protection, and service/package selection.

> 🇫🇮 **Pikaohje suomeksi** löytyy tämän tiedoston lopusta.

---

## Tech stack

| Part | Choice | Why |
| --- | --- | --- |
| Framework | [Astro 7](https://astro.build) (static site) | Fastest possible site, minimal JavaScript, simple to host anywhere |
| Styling | Tailwind CSS 4 + design tokens in `src/styles/global.css` | Same brand palette, fonts and sizing as `BCR_Website` |
| Content | YAML files in `src/content/` (Astro content collections) | Easy to edit in GitHub's web editor; typos give clear errors |
| Images | `astro:assets` | JPG/PNG files are automatically resized and converted to WebP |
| Form | [Formspree](https://formspree.io) | No backend server needed |
| Hosting | Cloudflare Pages (free) | Auto-deploys on push to GitHub |

---

## Run it locally

Requirements: **Node.js 22** (LTS) – check with `node -v`. With nvm: `nvm use` (reads `.nvmrc`).

```bash
npm install        # once
npm run dev        # → http://localhost:4321  (live reload while you edit)
npm run build      # production build into dist/
npm run preview    # serve the built dist/ locally
npm run check      # type/content check
```

---

## Where to edit what

Everything you normally change lives in **`src/content/`** (texts) and **`src/assets/images/`** (photos).

| File | Controls |
| --- | --- |
| `src/content/site.yaml` | Business name, email, phone, Instagram/TikTok, location, Y-tunnus, Formspree ID, top announcement strip, anchor navigation |
| `src/content/home.yaml` | Hero, services heading, brand story panel, packages heading, process steps, about teaser |
| `src/content/services.yaml` | Service cards (carousel + contact form checkboxes + footer quick-select links) |
| `src/content/packages.yaml` | Packages Start / Glow / Signature (cards + contact form options) |
| `src/content/faq.yaml` | Frequently asked questions at the bottom of the page |
| `src/content/pages.yaml` | Contact section intro (`yhteys`) and privacy notice modal (`tietosuoja`) |
| `src/styles/global.css` | Brand colours, fonts, sizes (the `@theme { … }` block at the top) |

### Link straight to the form with options pre-selected

`/?paketti=glow#yhteys` · `/?palvelu=ugc#yhteys` · `/?paketti=oma#yhteys` – the IDs come from the YAML files.

---

## 🇫🇮 Pikaohje sisällön muokkaamiseen

**Tekstit** ovat kansiossa `src/content/` ja **kuvat** kansiossa `src/assets/images/`.

1. Avaa tiedosto GitHubissa, esim. `src/content/home.yaml`.
2. Paina kynä-ikonia (_Edit this file_).
3. Muuta tekstiä kaksoispisteen `:` jälkeen. Älä muuta rivien alussa olevia sisennyksiä.
4. Paina _Commit changes…_ → kirjoita lyhyt kuvaus → _Commit changes_.

**Hinnat:** jätä `price: ""`, niin sivulla lukee "Pyydä tarjous". Kun haluat näyttää hinnan, kirjoita esim. `price: "alk. 290 €"`.

**Tärkeää ennen julkaisua:** osta Yellow Peas -fontin verkkolisenssi, vaihda kuvat omiin töihin ja tarkista yhteystiedot (`site.yaml`) sekä tietosuojaseloste (`pages.yaml`).
