export const testimonial = {
  name: "testimonial",
  title: "Testimonial",
  type: "document",
  fields: [
    {
      name: "quote",
      title: "Quote",
      type: "text",
      validation: (Rule: any) => Rule.required().max(300),
    },
    {
      name: "author",
      title: "Author",
      type: "object",
      fields: [
        {
          name: "name",
          title: "Name",
          type: "string",
          validation: (Rule: any) => Rule.required().max(50),
        },
        {
          name: "title",
          title: "Job Title",
          type: "string",
          validation: (Rule: any) => Rule.required().max(80),
        },
        {
          name: "company",
          title: "Company",
          type: "string",
          validation: (Rule: any) => Rule.max(50),
        },
      ],
    },
    {
      name: "featured",
      title: "Featured on Homepage",
      type: "boolean",
      description: "Show this testimonial on the homepage",
      initialValue: false,
    },
  ],
};
