export const siteSettings = {
  name: "siteSettings",
  title: "Site Settings",
  type: "document",
  fields: [
    {
      name: "title",
      title: "Site Title",
      type: "string",
      validation: (Rule: any) => Rule.required(),
    },
    {
      name: "description",
      title: "Site Description",
      type: "text",
      validation: (Rule: any) => Rule.required().max(160),
    },
    {
      name: "url",
      title: "Site URL",
      type: "url",
    },
  ],
};
