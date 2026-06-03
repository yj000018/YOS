# Y-Menu Architecture

Y-Menu is the cognitive orchestration interface for Y-OS. It translates user intent into capabilities, workflows, and actionable menus.

## Core Components

### 1. Capability Registry
The living memory of what Y-OS can do. It maps user goals to specific actions, tools, and workflows. Capabilities are defined in YAML files under `/capabilities`.

### 2. Intent Router
Translates natural language inputs (e.g., "produce kindle version") into capability matches and decision paths. It uses fuzzy matching against user phrases and predefined decision rules.

### 3. Dynamic Menus
Menus are not static. They are defined in YAML under `/menus` but are dynamically rendered by the `MenuRenderer`. The renderer merges:
- Static menu items
- Current project state
- Agent suggestions
- Scoring algorithms to recommend the best next action

### 4. Workflow Composer
Chains multiple actions together to achieve a high-level goal (e.g., "Publish full edition"). It outputs a recommended workflow, missing inputs, and required tools.

### 5. State Model
Maintains the current context of the session and the active project (e.g., Book-Factory). State includes active menus, navigation history, available assets, and generated outputs.

### 6. Agent Suggestions
Allows external Y-OS agents to inject high-priority recommendations into the menu (e.g., "Cover is missing, generate cover brief").

## Interaction Flow

1. **User Input**: User selects a menu number, types a command, or enters natural language.
2. **Action Router**: Determines the type of input.
3. **Intent / Workflow**: If natural language, the Intent Router or Workflow Composer processes it.
4. **State Update**: The state is updated based on the action taken.
5. **Menu Render**: The MenuRenderer generates the next visual menu, highlighting the recommended action.
