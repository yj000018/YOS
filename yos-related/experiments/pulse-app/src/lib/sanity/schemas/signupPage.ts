export const signupPage = {
  name: "signupPage",
  title: "Signup Page",
  type: "document",
  fields: [
    {
      name: "title",
      title: "Page Title",
      type: "string",
      validation: (Rule: any) => Rule.required().max(60),
    },
    {
      name: "description",
      title: "Page Description",
      type: "text",
      validation: (Rule: any) => Rule.max(200),
    },
    {
      name: "form",
      title: "Form Configuration",
      type: "object",
      fields: [
        {
          name: "submitButtonText",
          title: "Submit Button Text",
          type: "string",
          validation: (Rule: any) => Rule.required().max(30),
        },
        {
          name: "confirmationMessage",
          title: "Confirmation Message",
          type: "object",
          fields: [
            {
              name: "title",
              title: "Confirmation Title",
              type: "string",
              validation: (Rule: any) => Rule.required().max(60),
            },
            {
              name: "description",
              title: "Confirmation Description",
              type: "text",
              validation: (Rule: any) => Rule.max(200),
            },
          ],
        },
      ],
    },
  ],
};
