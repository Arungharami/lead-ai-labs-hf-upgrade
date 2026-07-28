---
title: Lead.AI ARC Grid Inspector
emoji: 🧩
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
pinned: false
license: mit
short_description: Validate ARC-style grids and inspect a symbolic next-action suggestion.
---

# Lead.AI ARC Grid Inspector

An interactive, educational companion for the Lead.AI ARC-AGI-3 symbolic agent.

Paste a rectangular JSON grid containing integer values from 0 to 15. The app validates the grid, identifies common player/goal/wall color roles, computes a shortest-path suggestion when possible, and returns a structured explanation.

## Scope

- This Space is a public inspection and collaboration demo.
- It does not connect to the private Kaggle evaluation gateway.
- It does not reproduce the full competition agent state or official score.
- Color-role assumptions are heuristics and may not match every ARC-AGI-3 game.

Source and experiment governance are maintained in the GitHub project:

`Arungharami/lead-ai-labs-hf-upgrade/competitions/arc-prize-2026`
