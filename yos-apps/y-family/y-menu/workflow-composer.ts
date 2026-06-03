// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Workflow Composer
// Chains actions into complete publishing workflows
// ─────────────────────────────────────────────────────────────────────────────

import { WorkflowComposition, WorkflowStep } from './types';
import { StateManager } from './state-manager';

// Pre-defined workflow chains
const WORKFLOW_CHAINS: Record<string, (state: StateManager) => WorkflowComposition> = {

  full_edition: (state) => {
    const bf = state.getBookFactory();
    const isVisual = ['illustrated', 'visual_essay', 'children_book', 'comic', 'artbook'].includes(bf?.book_type || '');
    const missing = state.getMissingInputs();

    const steps: WorkflowStep[] = [
      { step: 1, action: 'Validate manuscript', tool: 'pandoc --check', produces: 'manuscript.validated' },
      { step: 2, action: 'Build Typst print PDF', tool: 'typst compile', produces: 'print_pdf' },
      { step: 3, action: 'Build digital PDF', tool: 'typst compile (screen profile)', produces: 'digital_pdf' },
      { step: 4, action: 'Build Pandoc EPUB', tool: 'pandoc', produces: 'epub_reflowable' },
    ];

    if (isVisual) {
      steps.push({ step: 5, action: 'Build fixed-layout EPUB', tool: 'html-css-svg-fxl-engine', produces: 'epub_fixed_layout' });
    }

    steps.push(
      { step: steps.length + 1, action: 'Generate cover checklist', tool: 'book-factory/cover-brief', produces: 'cover_checklist' },
      { step: steps.length + 2, action: 'Generate KDP package', tool: 'kdp-checklist', produces: 'kdp_package' },
      { step: steps.length + 3, action: 'Generate Draft2Digital package', tool: 'd2d-adapter', produces: 'd2d_package' },
      { step: steps.length + 4, action: 'Generate Lovable mini-site prompt', tool: 'lovable-prompt-generator', produces: 'lovable_site_prompt' },
      { step: steps.length + 5, action: 'Archive release', tool: 'git tag', produces: 'release_archive' },
      { step: steps.length + 6, action: 'Sync release summary to Notion', tool: 'n8n / github-to-notion-sync', produces: 'notion_page' },
    );

    return {
      goal: 'Publish full edition',
      recommended_workflow: 'book-factory/release-edition.md',
      why: 'Full publication chain: all formats + all distribution platforms + web presence + archive.',
      required_inputs: ['manuscript', 'cover', 'metadata', 'typst_template'],
      missing_inputs: missing,
      steps,
      tools: ['typst', 'pandoc', 'epubcheck', 'html-css-svg-fxl-engine', 'kdp-checklist', 'lovable-prompt-generator', 'n8n'],
      expected_outputs: ['print_pdf', 'digital_pdf', 'epub_reflowable', 'epub_fixed_layout', 'kindle_package', 'lovable_site_prompt', 'release_archive'],
      risks: [
        'Typst template must exist before PDF build.',
        'Fixed-layout EPUB requires all images at final resolution.',
        'KDP cover must meet exact dimension specs.',
      ],
      next_menu: 'book-factory.release',
    };
  },

  kindle_package: (state) => {
    const bf = state.getBookFactory();
    const bookType = bf?.book_type || 'text_only';
    const isVisual = ['illustrated', 'children_book', 'comic', 'artbook', 'visual_essay'].includes(bookType);
    const missing = state.getMissingInputs();

    if (isVisual) {
      return {
        goal: 'Produce Kindle-ready package (visual book)',
        recommended_workflow: 'book-factory/build-epub-fxl.md',
        why: `Book type "${bookType}" requires fixed-layout EPUB for Kindle.`,
        required_inputs: ['manuscript', 'cover', 'images', 'metadata'],
        missing_inputs: missing,
        steps: [
          { step: 1, action: 'Prepare HTML/CSS/SVG page layouts', tool: 'html-css-svg-fxl-engine' },
          { step: 2, action: 'Generate fixed-layout EPUB', tool: 'epub-fxl-builder', produces: 'epub_fixed_layout' },
          { step: 3, action: 'Validate EPUB', tool: 'epubcheck', produces: 'epub_validated' },
          { step: 4, action: 'Preview in Kindle Previewer', tool: 'kindle-previewer' },
          { step: 5, action: 'Generate KDP upload checklist', tool: 'kdp-checklist', produces: 'kdp_package' },
        ],
        tools: ['html-css-svg-fxl-engine', 'epubcheck', 'kindle-previewer', 'kdp-checklist'],
        expected_outputs: ['epub_fixed_layout', 'kdp_package'],
        risks: ['Kindle FXL support varies by device. Test on Kindle Paperwhite + Fire.'],
        next_menu: 'book-factory.distribution',
      };
    }

    return {
      goal: 'Produce Kindle-ready package (text book)',
      recommended_workflow: 'book-factory/build-epub-pandoc.md',
      why: 'Text-only book → reflowable EPUB via Pandoc is the optimal Kindle path.',
      required_inputs: ['manuscript', 'cover', 'metadata'],
      missing_inputs: missing,
      steps: [
        { step: 1, action: 'Convert manuscript to EPUB with Pandoc', tool: 'pandoc', produces: 'epub_reflowable' },
        { step: 2, action: 'Validate EPUB', tool: 'epubcheck', produces: 'epub_validated' },
        { step: 3, action: 'Generate KDP metadata', tool: 'kdp-metadata-generator', produces: 'kdp_metadata' },
        { step: 4, action: 'Generate KDP upload checklist', tool: 'kdp-checklist', produces: 'kdp_package' },
      ],
      tools: ['pandoc', 'epubcheck', 'kdp-checklist'],
      expected_outputs: ['epub_reflowable', 'kdp_package'],
      risks: ['Pandoc EPUB requires clean Markdown structure.'],
      next_menu: 'book-factory.distribution',
    };
  },

  lovable_site: (_state) => ({
    goal: 'Generate Lovable mini-site',
    recommended_workflow: 'book-factory/generate-lovable-site.md',
    why: 'One book, simple landing page, speed matters → Lovable is optimal.',
    required_inputs: ['book_title', 'book_description', 'cover', 'author_bio'],
    missing_inputs: [],
    steps: [
      { step: 1, action: 'Generate Lovable prompt package', tool: 'lovable-prompt-generator', produces: 'lovable_site_prompt' },
      { step: 2, action: 'Generate assets package (cover, bio, blurb)', tool: 'asset-packager', produces: 'lovable_assets' },
      { step: 3, action: 'Generate purchase/download section copy', tool: 'copywriter', produces: 'purchase_copy' },
      { step: 4, action: 'Generate SEO metadata', tool: 'seo-generator', produces: 'seo_metadata' },
    ],
    tools: ['lovable-prompt-generator', 'asset-packager'],
    expected_outputs: ['lovable_site_prompt', 'lovable_assets', 'seo_metadata'],
    risks: ['Lovable is best for single-book sites. Use Astro for catalogues.'],
    next_menu: 'book-factory.website',
  }),

  astro_site: (_state) => ({
    goal: 'Generate Astro industrial site spec',
    recommended_workflow: 'book-factory/generate-astro-site-spec.md',
    why: 'Multi-book catalogue or interactive edition → Astro content collections are optimal.',
    required_inputs: ['book_catalogue', 'design_system', 'content_structure'],
    missing_inputs: [],
    steps: [
      { step: 1, action: 'Define content collections schema', tool: 'astro-schema-generator', produces: 'content_schema' },
      { step: 2, action: 'Generate Astro site spec document', tool: 'spec-generator', produces: 'astro_site_spec' },
      { step: 3, action: 'Generate interactive edition spec', tool: 'interactive-spec-generator', produces: 'interactive_spec' },
      { step: 4, action: 'Generate SEO and metadata strategy', tool: 'seo-generator', produces: 'seo_strategy' },
    ],
    tools: ['astro-schema-generator', 'spec-generator'],
    expected_outputs: ['astro_site_spec', 'content_schema', 'seo_strategy'],
    risks: ['Astro requires dev setup. Lovable is faster for simple landing pages.'],
    next_menu: 'book-factory.website',
  }),
};

export class WorkflowComposer {
  constructor(private state: StateManager) {}

  compose(goal: string): WorkflowComposition | null {
    const normalised = goal.toLowerCase().trim();

    if (normalised.includes('full') || normalised.includes('all') || normalised.includes('publish')) {
      return WORKFLOW_CHAINS.full_edition(this.state);
    }
    if (normalised.includes('kindle') || normalised.includes('amazon') || normalised.includes('kdp')) {
      return WORKFLOW_CHAINS.kindle_package(this.state);
    }
    if (normalised.includes('lovable') || (normalised.includes('mini') && normalised.includes('site'))) {
      return WORKFLOW_CHAINS.lovable_site(this.state);
    }
    if (normalised.includes('astro') || (normalised.includes('industrial') && normalised.includes('site'))) {
      return WORKFLOW_CHAINS.astro_site(this.state);
    }
    if (normalised.includes('site') || normalised.includes('website') || normalised.includes('web')) {
      // Default: ask Lovable vs Astro decision
      return WORKFLOW_CHAINS.lovable_site(this.state);
    }

    return null;
  }

  format(composition: WorkflowComposition): string {
    const lines: string[] = [];
    lines.push('╭────────────────────────────────────────────╮');
    lines.push('│         WORKFLOW COMPOSER                  │');
    lines.push('╰────────────────────────────────────────────╯');
    lines.push('');
    lines.push(`Goal: ${composition.goal}`);
    lines.push(`Why: ${composition.why}`);
    lines.push('');

    if (composition.missing_inputs.length > 0) {
      lines.push('⚠️  Missing inputs: ' + composition.missing_inputs.join(', '));
      lines.push('');
    }

    lines.push('Steps:');
    for (const step of composition.steps) {
      const tool = step.tool ? ` [${step.tool}]` : '';
      const produces = step.produces ? ` → ${step.produces}` : '';
      lines.push(`  ${step.step}. ${step.action}${tool}${produces}`);
    }
    lines.push('');

    lines.push('Expected outputs: ' + composition.expected_outputs.join(', '));

    if (composition.risks && composition.risks.length > 0) {
      lines.push('');
      lines.push('Risks:');
      composition.risks.forEach(r => lines.push(`  ⚠️  ${r}`));
    }

    return lines.join('\n');
  }
}
