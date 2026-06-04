import {
  Focus,
  Workflow,
  Palette,
  Layout,
  MessageCircle,
  Target,
  BarChart,
  Zap,
  Shield,
  Brain,
} from "lucide-react";
import type { FeatureData } from "@/types/sanity";

interface FeaturesSectionProps {
  features: FeatureData[];
  title?: string;
  subtitle?: string;
}

const iconMap: Record<string, React.ElementType> = {
  focus: Focus,
  workflow: Workflow,
  palette: Palette,
  layout: Layout,
  "message-circle": MessageCircle,
  target: Target,
  "bar-chart": BarChart,
  zap: Zap,
  shield: Shield,
  brain: Brain,
};

export function FeaturesSection({ features, title, subtitle }: FeaturesSectionProps) {
  return (
    <section className="py-24 md:py-32 bg-cream-100/50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-display font-bold text-charcoal-900 mb-4">
            {title || "Everything you need, nothing you don\u2019t"}
          </h2>
          <p className="text-charcoal-700/60 text-lg max-w-xl mx-auto">
            {subtitle || "Designed with intention. Every feature serves your creative flow."}
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => {
            const IconComponent = iconMap[feature.icon] || Focus;
            return (
              <div
                key={feature._key || index}
                className="group p-8 rounded-2xl bg-cream-50 border border-cream-200 hover:border-accent/20 hover:shadow-lg hover:shadow-accent/5 transition-all duration-300"
              >
                <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mb-6 group-hover:bg-accent/20 transition-colors">
                  <IconComponent className="w-6 h-6 text-accent" />
                </div>
                <h3 className="text-xl font-display font-semibold text-charcoal-800 mb-3">
                  {feature.title}
                </h3>
                <p className="text-charcoal-700/60 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
