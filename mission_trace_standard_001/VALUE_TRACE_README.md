# How to Use the Value Trace Standard

This directory contains the standard assets for generating Y-OS Value Traces.

## Files Provided

1. `VALUE_TRACE_STANDARD.md`: The rules and principles of the standard.
2. `value_trace_schema.json`: The machine-readable JSON schema. Use this to structure your trace data before rendering.
3. `value_trace_template.excalidraw`: A blank, reusable Excalidraw template with the correct layout and color coding.
4. `value_trace_template.md`: A markdown version of the layout for Obsidian use.

## Workflow for Future Missions

When a future mission requires an Excalidraw trace:

1. **Extract Data:** Gather the execution data from the Y-OS runtime (latency, tokens, tools, artifacts).
2. **Structure Data:** Format the data according to `value_trace_schema.json`.
3. **Determine Verdict:** Analyze the input and output to determine if the work was valuable (YES), purely self-referential (NO), or mixed (AMBER).
4. **Generate Excalidraw:** Use a Python script to inject the structured data into the Excalidraw format, following the layout defined in the standard. Do not build a new runtime module for this; use a lightweight script within the mission directory.
5. **Render (Optional):** If requested, render the Excalidraw JSON to PNG/SVG using `cairosvg` or similar tools.

## Important Constraints

* **No Dashboards:** Do not build a web UI or dashboard to view these traces. They are static artifacts.
* **No New Modules:** Do not add a `trace_renderer_v3` to the Y-OS core. Generation must remain a lightweight, on-demand script.
* **Value Focus:** Always fill out the "Without Y-OS vs With Y-OS" section. If you cannot articulate why Y-OS was better than manual work, the trace should highlight a failure in value creation.
