from __future__ import annotations

import json
from collections import Counter, deque
from typing import Any

import gradio as gr
import pandas as pd

PLAYER_COLORS = {9, 10, 12}
GOAL_COLORS = {6, 7}
WALL_COLORS = {5}
DIRECTIONS = [
    (0, -1, "ACTION1"),
    (0, 1, "ACTION2"),
    (-1, 0, "ACTION3"),
    (1, 0, "ACTION4"),
]

EXAMPLE_GRID = json.dumps(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 5, 0, 6, 0],
        [0, 10, 0, 5, 0, 7, 0],
        [0, 12, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ],
    indent=2,
)


def _parse_grid(raw: str) -> list[list[int]]:
    try:
        value: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise gr.Error(f"Invalid JSON: {exc.msg}") from exc

    if not isinstance(value, list) or not value:
        raise gr.Error("Grid must be a non-empty JSON list of rows.")
    if len(value) > 64:
        raise gr.Error("Grid height must not exceed 64.")

    grid: list[list[int]] = []
    width: int | None = None
    for row_index, row in enumerate(value):
        if not isinstance(row, list) or not row:
            raise gr.Error(f"Row {row_index} must be a non-empty list.")
        if width is None:
            width = len(row)
            if width > 64:
                raise gr.Error("Grid width must not exceed 64.")
        elif len(row) != width:
            raise gr.Error("Every row must have the same width.")

        parsed_row: list[int] = []
        for column_index, cell in enumerate(row):
            if isinstance(cell, bool) or not isinstance(cell, int):
                raise gr.Error(
                    f"Cell ({column_index}, {row_index}) must be an integer."
                )
            if not 0 <= cell <= 15:
                raise gr.Error(
                    f"Cell ({column_index}, {row_index}) must be between 0 and 15."
                )
            parsed_row.append(cell)
        grid.append(parsed_row)
    return grid


def _centroid(points: list[tuple[int, int]]) -> tuple[int, int] | None:
    if not points:
        return None
    return (
        round(sum(x for x, _ in points) / len(points)),
        round(sum(y for _, y in points) / len(points)),
    )


def _positions(
    grid: list[list[int]], colors: set[int]
) -> list[tuple[int, int]]:
    return [
        (x, y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell in colors
    ]


def _first_path_action(
    grid: list[list[int]],
    start: tuple[int, int],
    goals: set[tuple[int, int]],
) -> tuple[str | None, int | None]:
    if start in goals:
        return "AT_GOAL", 0

    height = len(grid)
    width = len(grid[0])
    queue: deque[tuple[int, int, str, int]] = deque()
    visited = {start}

    for dx, dy, action in DIRECTIONS:
        nx, ny = start[0] + dx, start[1] + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] not in WALL_COLORS:
            queue.append((nx, ny, action, 1))
            visited.add((nx, ny))

    while queue:
        x, y, first_action, distance = queue.popleft()
        if (x, y) in goals:
            return first_action, distance
        for dx, dy, _ in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if (nx, ny) in visited or grid[ny][nx] in WALL_COLORS:
                continue
            visited.add((nx, ny))
            queue.append((nx, ny, first_action, distance + 1))
    return None, None


def inspect_grid(raw_grid: str) -> tuple[dict[str, Any], pd.DataFrame]:
    grid = _parse_grid(raw_grid)
    counts = Counter(cell for row in grid for cell in row)
    player_points = _positions(grid, PLAYER_COLORS)
    goal_points = _positions(grid, GOAL_COLORS)
    player = _centroid(player_points)
    goal = _centroid(goal_points)

    suggested_action: str | None = None
    path_length: int | None = None
    if player is not None and goal_points:
        suggested_action, path_length = _first_path_action(
            grid, player, set(goal_points)
        )

    if suggested_action is None:
        suggested_action = "EXPLORE_LEGAL_ACTIONS"

    report = {
        "valid": True,
        "height": len(grid),
        "width": len(grid[0]),
        "color_counts": dict(sorted(counts.items())),
        "estimated_player_centroid": player,
        "estimated_goal_centroid": goal,
        "wall_cells": sum(counts[color] for color in WALL_COLORS),
        "suggested_action": suggested_action,
        "estimated_path_length": path_length,
        "assumptions": [
            "colors 9, 10, and 12 may represent a player",
            "colors 6 and 7 may represent a goal",
            "color 5 may represent a wall",
            "actual action meanings vary by game",
        ],
        "scope": "Public inspection demo; not a private Kaggle evaluation.",
    }
    return report, pd.DataFrame(grid)


with gr.Blocks(title="Lead.AI ARC Grid Inspector") as demo:
    gr.Markdown(
        "# 🧩 Lead.AI ARC Grid Inspector\n"
        "Validate a 0–15 ARC-style grid and inspect a transparent symbolic "
        "next-action suggestion."
    )
    grid_input = gr.Textbox(
        label="Grid JSON",
        value=EXAMPLE_GRID,
        lines=14,
    )
    inspect_button = gr.Button("Inspect grid", variant="primary")
    report_output = gr.JSON(label="Structured inspection")
    grid_output = gr.Dataframe(label="Validated grid", interactive=False)
    inspect_button.click(
        inspect_grid,
        inputs=grid_input,
        outputs=[report_output, grid_output],
    )
    gr.Examples(
        examples=[[EXAMPLE_GRID]],
        inputs=grid_input,
    )

if __name__ == "__main__":
    demo.launch()
