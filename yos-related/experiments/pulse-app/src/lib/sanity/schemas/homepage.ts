export const homepage = {
  name: "homepage",
  title: "Homepage",
  type: "document",
  fields: [
    {
      name: "hero",
      title: "Hero Section",
      type: "object",
      fields: [
        {
          name: "headline",
          title: "Headline",
          type: "string",
          validation: (Rule: any) => Rule.required().max(80),
        },
        {
          name: "subheadline",
          title: "Subheadline",
          type: "text",
          validation: (Rule: any) => Rule.required().max(200),
        },
        {
          name: "ctaText",
          title: "CTA Button Text",
          type: "string",
          validation: (Rule: any) => Rule.required().max(30),
        },
      ],
    },
    {
      name: "valueProposition",
      title: "Value Proposition",
      type: "object",
      fields: [
        {
          name: "title",
          title: "Section Title",
          type: "string",
          validation: (Rule: any) => Rule.required().max(60),
        },
        {
          name: "description",
          title: "Description",
          type: "text",
          validation: (Rule: any) => Rule.required().max(300),
        },
      ],
    },
    {
      name: "features",
      title: "Features",
      type: "array",
      of: [
        {
          type: "object",
          fields: [
            {
              name: "title",
              title: "Feature Title",
              type: "string",
              validation: (Rule: any) => Rule.required().max(50),
            },
            {
              name: "description",
              title: "Feature Description",
              type: "text",
              validation: (Rule: any) => Rule.required().max(150),
            },
            {
              name: "icon",
              title: "Icon Name",
              type: "string",
              description: "Lucide icon name (focus, workflow, palette)",
            },
          ],
        },
      ],
      validation: (Rule: any) => Rule.max(6),
    },
    {
      name: "finalCta",
      title: "Final CTA Section",
      type: "object",
      fields: [
        {
          name: "title",
          title: "CTA Title",
          type: "string",
          validation: (Rule: any) => Rule.required().max(60),
        },
        {
          name: "description",
          title: "CTA Description",
          type: "text",
          validation: (Rule: any) => Rule.max(200),
        },
        {
          name: "buttonText",
          title: "Button Text",
          type: "string",
          validation: (Rule: any) => Rule.required().max(30),
        },
      ],
    },
  ],
};
