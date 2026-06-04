export const waitlistEntry = {
  name: "waitlistEntry",
  title: "Waitlist Entry",
  type: "document",
  fields: [
    {
      name: "firstName",
      title: "First Name",
      type: "string",
      validation: (Rule: any) => Rule.required(),
    },
    {
      name: "email",
      title: "Email",
      type: "string",
      validation: (Rule: any) => Rule.required(),
    },
    {
      name: "submittedAt",
      title: "Submitted At",
      type: "datetime",
      validation: (Rule: any) => Rule.required(),
    },
  ],
  orderings: [
    {
      title: "Submitted At (Newest)",
      name: "submittedAtDesc",
      by: [{ field: "submittedAt", direction: "desc" }],
    },
  ],
};
