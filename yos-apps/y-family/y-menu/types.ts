// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Core Types
// ─────────────────────────────────────────────────────────────────────────────

// ── Action Types ──────────────────────────────────────────────────────────────

export type ActionType =
  | 'submenu'
  | 'workflow'
  | 'prompt'
  | 'skill'
  | 'script'
  | 'tool'
  | 'decision'
  | 'diagnostic'
  | 'external_link'
  | 'documentation'
  | 'noop';

// ── Menu Item ─────────────────────────────────────────────────────────────────

export interface MenuItem {
  id: string;
  label: string;
  emoji?: string;
  description?: string;
  action_type: ActionType;
  target?: string;
  requires?: string[];
  produces?: string[];
  recommended_when?: string[];
  disabled_when?: string[];
  visible_when?: string[];
  next_menu?: string;
  tags?: string[];
  agent_suggestion?: boolean;
  agent_source?: string;
  agent_confidence?: number;
  agent_reason?: string;
}

// ── Menu Definition ───────────────────────────────────────────────────────────

export interface MenuDefinition {
  id: string;
  title: string;
  subtitle?: string;
  module?: string;
  parent?: string;
  items: MenuItem[];
  commands?: string[];
  footer?: string;
}

// ── Capability ────────────────────────────────────────────────────────────────

export interface DecisionRule {
  condition: string;
  recommend: string;
}

export interface Capability {
  id: string;
  title: string;
  module: string;
  user_phrases: string[];
  required_inputs?: string[];
  optional_inputs?: string[];
  decision_rules?: DecisionRule[];
  tools?: string[];
  outputs?: string[];
  limitations?: string[];
  fallbacks?: string[];
  next_actions?: string[];
  workflow?: string;
  tags?: string[];
}

// ── State ─────────────────────────────────────────────────────────────────────

export interface OutputStatus {
  print_pdf?: string;
  digital_pdf?: string;
  epub_reflowable?: string;
  epub_fixed_layout?: string;
  kindle_package?: string;
  lovable_site_prompt?: string;
  astro_site_spec?: string;
  [key: string]: string | undefined;
}

export interface ManuscriptState {
  status: 'missing' | 'imported' | 'cleaned' | 'validated';
  source_format?: string;
  path?: string;
}

export interface AssetsState {
  cover?: string;
  images?: string;
}

export interface DistributionState {
  kdp?: string;
  ingram?: string;
  draft2digital?: string;
}

export interface BookFactoryState {
  active_book_id?: string;
  active_book_title?: string;
  publisher?: string;
  edition?: string;
  book_type?: string;
  manuscript?: ManuscriptState;
  assets?: AssetsState;
  outputs?: OutputStatus;
  distribution?: DistributionState;
  recommendations?: string[];
}

export interface UserPreferences {
  preferred_interaction_style?: string;
  preferred_output_style?: string;
  default_language?: string;
}

export interface SessionState {
  active_module?: string;
  active_menu?: string;
  navigation_stack?: string[];
  last_action?: string;
  last_result?: string;
  recent_actions?: string[];
}

export interface YMenuState {
  session: SessionState;
  user?: UserPreferences;
  book_factory?: BookFactoryState;
  [key: string]: unknown;
}

// ── Agent Suggestion ──────────────────────────────────────────────────────────

export interface AgentSuggestion {
  id: string;
  source_agent: string;
  title: string;
  reason: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  action_type: ActionType;
  target?: string;
  expires_when?: string[];
}

// ── Workflow ──────────────────────────────────────────────────────────────────

export interface WorkflowStep {
  step: number;
  action: string;
  tool?: string;
  produces?: string;
  requires?: string;
}

export interface WorkflowComposition {
  goal: string;
  recommended_workflow: string;
  why: string;
  required_inputs: string[];
  missing_inputs: string[];
  steps: WorkflowStep[];
  tools: string[];
  expected_outputs: string[];
  risks?: string[];
  next_actions?: string[];
  next_menu?: string;
}

// ── Intent Routing ────────────────────────────────────────────────────────────

export interface IntentMatch {
  capability: Capability;
  score: number;
  matched_phrase?: string;
}

export interface IntentRouterResult {
  intent: string;
  matches: IntentMatch[];
  best_match?: IntentMatch;
  needs_clarification?: boolean;
  clarification_question?: string;
  decision_paths?: string[];
}

// ── Rendered Menu ─────────────────────────────────────────────────────────────

export interface RenderedMenu {
  raw: string;
  menu_id: string;
  item_count: number;
  recommended_action?: string;
}
