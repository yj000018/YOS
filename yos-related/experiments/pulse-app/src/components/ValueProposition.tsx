import type { ValuePropositionData } from "@/types/sanity";

interface ValuePropositionProps {
  data: ValuePropositionData;
}

export function ValueProposition({ data }: ValuePropositionProps) {
  return (
    <section className="py-24 md:py-32">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h2 className="text-3xl md:text-5xl font-display font-bold text-charcoal-900 mb-6 text-balance">
          {data.title}
        </h2>
        <p className="text-lg md:text-xl text-charcoal-700/70 max-w-2xl mx-auto leading-relaxed">
          {data.description}
        </p>
      </div>
    </section>
  );
}
