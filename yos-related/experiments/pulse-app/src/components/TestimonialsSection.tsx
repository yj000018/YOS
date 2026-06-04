import type { TestimonialData } from "@/types/sanity";

interface TestimonialsSectionProps {
  testimonials: TestimonialData[];
}

export function TestimonialsSection({ testimonials }: TestimonialsSectionProps) {
  if (!testimonials || testimonials.length === 0) return null;

  return (
    <section className="py-24 md:py-32">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-display font-bold text-charcoal-900 mb-4">
            Loved by teams everywhere
          </h2>
          <p className="text-charcoal-700/60 text-lg">
            What early adopters are saying about Pulse.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => {
            const name = testimonial.name || testimonial.author?.name || "Anonymous";
            const role = testimonial.role || testimonial.author?.title || "";
            const company = testimonial.company || testimonial.author?.company || "";

            return (
              <div
                key={testimonial._id || index}
                className="p-8 rounded-2xl bg-cream-100/50 border border-cream-200"
              >
                <svg
                  className="w-8 h-8 text-accent/30 mb-4"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                </svg>
                <blockquote className="text-charcoal-700 leading-relaxed mb-6">
                  &ldquo;{testimonial.quote}&rdquo;
                </blockquote>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center">
                    <span className="text-accent font-semibold text-sm">
                      {name.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-charcoal-800 text-sm">
                      {name}
                    </p>
                    <p className="text-charcoal-700/50 text-xs">
                      {role}
                      {company && ` at ${company}`}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
