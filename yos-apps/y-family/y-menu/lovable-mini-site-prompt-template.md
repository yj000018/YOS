# Lovable Mini-Site Generation Prompt

## System Context
You are an expert React/Tailwind/Vite developer generating a prompt for Lovable to build a single-page book landing site.

## Inputs
- **Book Title**: {{book_title}}
- **Subtitle**: {{book_subtitle}}
- **Author**: {{author}}
- **Description**: {{book_description}}
- **Cover Image Path**: {{cover_path}}

## Prompt to send to Lovable

```text
Build a premium, modern, high-converting landing page for a book.

Book Title: {{book_title}}
Author: {{author}}

Design Requirements:
- Clean, minimalist aesthetic (black, white, and one accent colour)
- Large hero section with the book cover on the right, title and value proposition on the left
- "Buy Now" CTA buttons that are highly visible
- Section for "What you will learn"
- Section for "About the Author"
- Section for "Testimonials" or reviews
- Fully responsive (mobile first)

Tech Stack:
- React
- Tailwind CSS
- Vite
- Lucide React for icons

Content:
{{book_description}}

Please implement this as a complete, working single-page application.
```
