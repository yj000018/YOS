# Y-Menu v0

Y-Menu is the universal cognitive orchestration interface for Y-OS. It serves as a zero-UI command cockpit that translates user intent into actionable workflows.

## Mission

Y-Menu hides tool complexity. Instead of remembering which tool or script to run, the user states an objective (e.g., "Produce a Kindle-ready version"), and Y-Menu orchestrates the required capabilities, decision rules, and workflows.

## Features

- **Dynamic Chat Menus**: Beautiful, state-aware text menus.
- **Intent Routing**: Natural language processing to match goals with capabilities.
- **Workflow Composer**: Chains actions for complex tasks.
- **Capability Registry**: A structured database of Y-OS skills and tools.
- **Agent Suggestions**: Allows AI agents to inject contextual recommendations.

## The First Module: Book-Factory

The first instantiation of Y-Menu is the **Y-Publishing Factory** (Book-Factory), an AI-native book production cockpit. It handles manuscript import, Typst PDF generation, Pandoc EPUB creation, distribution packaging, and website generation.

## Running the Demo

```bash
# Install dependencies
npm install

# Run the full interactive demo
npm run demo

# Show the Book-Factory menu
npm run menu:book

# Test intent routing
npm run intent:kindle
npm run intent:site

# Show Y-OS status
npm run status
```

## Repository Structure

- `src/core/`: The core engine (router, renderer, state manager).
- `menus/`: YAML definitions for all menus.
- `capabilities/`: YAML registry of what Y-OS can do.
- `workflows/`: Markdown documentation of specific workflows.
- `prompts/`: AI prompt templates.
- `examples/`: Example states and sessions.
- `docs/`: Architecture and design principles.

## Future Roadmap

Phase 1: Zero-UI chat launcher (Current)
Phase 2: Raycast-like cockpit
Phase 3: Web dashboard / Lovable prototype
Phase 4: Tauri / local-first app
