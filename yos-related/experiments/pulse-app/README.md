# Pulse — Calm Productivity for Creatives

A demo application validating a full production pipeline: **GPT → Claude → v0 → Next.js → Sanity → Vercel**.

## Architecture

| Layer | Role | Tool |
|-------|------|------|
| 0 | Orchestration | Manus |
| 1 | Product Conception | GPT-4o |
| 2 | Technical Specs | Claude Sonnet |
| 3 | UI Generation | v0 by Vercel |
| 4 | Codebase | Next.js 14 + TypeScript + Tailwind |
| 5 | CMS | Sanity v3 |
| 6 | Deployment | Vercel |

## Stack

- **Next.js 14** (App Router, Server Components)
- **TypeScript**
- **Tailwind CSS**
- **Sanity v3** (Headless CMS)
- **Vercel** (Hosting + Preview)

## Pages

- `/` — Homepage (Hero, Value Prop, Features, Testimonials, CTA)
- `/signup` — Waitlist signup form

## Getting Started

```bash
pnpm install
pnpm dev
```

## Environment Variables

```
NEXT_PUBLIC_SANITY_PROJECT_ID=your_project_id
NEXT_PUBLIC_SANITY_DATASET=production
SANITY_API_TOKEN=your_token
```

## Sanity Schemas

- `homepage` — Homepage content
- `signupPage` — Signup page content
- `testimonial` — Testimonial entries
- `siteSettings` — Global site settings
- `waitlistEntry` — Waitlist form submissions
