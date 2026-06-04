"use client";

import { useState } from "react";

interface WaitlistFormProps {
  formFields?: {
    firstNameLabel: string;
    firstNamePlaceholder: string;
    emailLabel: string;
    emailPlaceholder: string;
    submitText: string;
    submittingText: string;
  };
  successMessage?: {
    headline: string;
    body: string;
  };
  // Legacy props
  submitButtonText?: string;
  confirmationTitle?: string;
  confirmationDescription?: string;
}

export function WaitlistForm({
  formFields,
  successMessage,
  submitButtonText,
  confirmationTitle,
  confirmationDescription,
}: WaitlistFormProps) {
  const [firstName, setFirstName] = useState("");
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  const labels = {
    firstName: formFields?.firstNameLabel || "First name",
    firstNamePlaceholder: formFields?.firstNamePlaceholder || "Your first name",
    email: formFields?.emailLabel || "Email",
    emailPlaceholder: formFields?.emailPlaceholder || "you@example.com",
    submit: formFields?.submitText || submitButtonText || "Join the Waitlist",
    submitting: formFields?.submittingText || "Joining...",
  };

  const success = {
    headline: successMessage?.headline || confirmationTitle || "You're on the list!",
    body: successMessage?.body || confirmationDescription || "Thank you for joining. We'll be in touch soon.",
  };

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");

    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ firstName, email }),
      });

      if (res.ok) {
        setStatus("success");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <div className="text-center py-12 animate-in fade-in duration-500">
        <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6">
          <svg
            className="w-8 h-8 text-green-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-display font-bold text-charcoal-900 mb-3">
          {success.headline}
        </h2>
        <p className="text-charcoal-700/60 max-w-md mx-auto">
          {success.body}
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-4">
      <div>
        <label
          htmlFor="firstName"
          className="block text-sm font-medium text-charcoal-700 mb-1.5"
        >
          {labels.firstName}
        </label>
        <input
          id="firstName"
          type="text"
          required
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          placeholder={labels.firstNamePlaceholder}
          className="w-full px-4 py-3 rounded-xl bg-cream-50 border border-cream-200 text-charcoal-800 placeholder:text-charcoal-700/30 focus:outline-none focus:ring-2 focus:ring-accent/30 focus:border-accent/50 transition-all"
        />
      </div>
      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-charcoal-700 mb-1.5"
        >
          {labels.email}
        </label>
        <input
          id="email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder={labels.emailPlaceholder}
          className="w-full px-4 py-3 rounded-xl bg-cream-50 border border-cream-200 text-charcoal-800 placeholder:text-charcoal-700/30 focus:outline-none focus:ring-2 focus:ring-accent/30 focus:border-accent/50 transition-all"
        />
      </div>
      <button
        type="submit"
        disabled={status === "loading"}
        className="w-full px-6 py-3.5 bg-charcoal-800 text-cream-50 rounded-xl text-base font-medium hover:bg-charcoal-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-charcoal-800/20"
      >
        {status === "loading" ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            {labels.submitting}
          </span>
        ) : (
          labels.submit
        )}
      </button>
      {status === "error" && (
        <p className="text-red-500 text-sm text-center">
          Something went wrong. Please try again.
        </p>
      )}
    </form>
  );
}
