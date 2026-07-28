"""Lead.AI ARC Prize 2026 production baseline agent.

The official ARC Kaggle starter splices this file into the generated submission
notebook. Keep this module self-contained: standard library plus the official
``arcengine`` and ``agents`` packages only.
"""
from __future__ import annotations

import hashlib
import math
import random
from collections import Counter, defaultdict, deque
from collections.abc import Iterable, Sequence
from typing import Any

from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent

Grid = list[list[int]]
Point = tuple[int, int]

_MAX_COORDINATE = 63
_DIRECTION_TO_ACTION = {
    (0, -1): "ACTION1",
    (0, 1): "ACTION2",
    (-1, 0): "ACTION3",
    (1, 0): "ACTION4",
}


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _screen(frame: FrameData) -> Grid:
    """Return the latest 2-D screen from a possibly stacked frame payload.

    Malformed rows are rejected instead of being silently skipped because a
    partially decoded grid can create invalid state hashes and unsafe actions.
    """
    raw = getattr(frame, "frame", None) or []
    if not _is_sequence(raw) or not raw:
        return []
    candidate = raw[-1]
    if not _is_sequence(candidate):
        return []

    output: Grid = []
    expected_width: int | None = None
    for row in candidate:
        if not _is_sequence(row):
            return []
        try:
            normalized = [int(value) for value in row]
        except (TypeError, ValueError):
            return []
        if expected_width is None:
            expected_width = len(normalized)
        elif len(normalized) != expected_width:
            return []
        output.append(normalized)
    return output


def _grid_signature(grid: Grid) -> str:
    """Return a stable state key, including every row boundary."""
    digest = hashlib.blake2b(digest_size=16)
    digest.update(len(grid).to_bytes(2, "little", signed=False))
    for row in grid:
        digest.update(len(row).to_bytes(2, "little", signed=False))
        digest.update(bytes(max(0, min(255, int(value))) for value in row))
    return digest.hexdigest()


def _changed_cells(before: Grid, after: Grid) -> int:
    """Count changed cells, including shape changes."""
    if not before and not after:
        return 0
    height = max(len(before), len(after))
    width = max(
        max((len(row) for row in before), default=0),
        max((len(row) for row in after), default=0),
    )
    changed = 0
    for y in range(height):
        for x in range(width):
            left = before[y][x] if y < len(before) and x < len(before[y]) else None
            right = after[y][x] if y < len(after) and x < len(after[y]) else None
            changed += left != right
    return changed


def _centroid(points: Iterable[Point]) -> Point | None:
    items = list(points)
    if not items:
        return None
    return (
        round(sum(x for x, _ in items) / len(items)),
        round(sum(y for _, y in items) / len(items)),
    )


def _find_colors(grid: Grid, colors: set[int]) -> list[Point]:
    return [
        (x, y)
        for y, row in enumerate(grid)
        for x, value in enumerate(row)
        if value in colors
    ]


def _connected_components(grid: Grid) -> list[tuple[int, list[Point]]]:
    """Return four-connected same-color components as ``(color, points)``."""
    if not grid:
        return []
    seen: set[Point] = set()
    components: list[tuple[int, list[Point]]] = []
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            origin = (x, y)
            if origin in seen:
                continue
            queue: deque[Point] = deque([origin])
            seen.add(origin)
            points: list[Point] = []
            while queue:
                px, py = queue.popleft()
                points.append((px, py))
                for nx, ny in (
                    (px + 1, py),
                    (px - 1, py),
                    (px, py + 1),
                    (px, py - 1),
                ):
                    if ny < 0 or ny >= len(grid) or nx < 0 or nx >= len(grid[ny]):
                        continue
                    if (nx, ny) in seen or grid[ny][nx] != color:
                        continue
                    seen.add((nx, ny))
                    queue.append((nx, ny))
            components.append((color, points))
    return components


def _safe_action_from_item(item: Any) -> GameAction | None:
    if isinstance(item, GameAction):
        return item
    if isinstance(item, str):
        try:
            return GameAction.from_name(item)
        except (KeyError, TypeError, ValueError):
            return None
    if isinstance(item, int):
        try:
            return GameAction.from_id(item)
        except (TypeError, ValueError):
            return None
    if isinstance(item, dict):
        for key in ("name", "action", "id"):
            if key in item:
                return _safe_action_from_item(item[key])
    return None


def _legal_actions(latest_frame: FrameData) -> list[GameAction]:
    """Normalize the framework's optional legal-action payload."""
    raw = getattr(latest_frame, "available_actions", None)
    actions: list[GameAction] = []
    if raw and _is_sequence(raw):
        for item in raw:
            action = _safe_action_from_item(item)
            if (
                action is not None
                and action is not GameAction.RESET
                and action not in actions
            ):
                actions.append(action)
    if actions:
        return actions
    return [action for action in GameAction if action is not GameAction.RESET]


def _shortest_direction(
    grid: Grid,
    start: Point,
    goals: set[Point],
    blocked_colors: set[int],
) -> tuple[int, int] | None:
    """Find the first four-neighbor step on a shortest traversable path."""
    if not grid or start in goals:
        return None
    sx, sy = start
    if sy < 0 or sy >= len(grid) or sx < 0 or sx >= len(grid[sy]):
        return None

    queue: deque[Point] = deque([start])
    parent: dict[Point, Point | None] = {start: None}
    found: Point | None = None

    while queue:
        current = queue.popleft()
        if current in goals:
            found = current
            break
        x, y = current
        for neighbor in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            nx, ny = neighbor
            if ny < 0 or ny >= len(grid) or nx < 0 or nx >= len(grid[ny]):
                continue
            if neighbor in parent or grid[ny][nx] in blocked_colors:
                continue
            parent[neighbor] = current
            queue.append(neighbor)

    if found is None:
        return None

    step = found
    while parent[step] is not None and parent[step] != start:
        step = parent[step]  # type: ignore[assignment]
    if parent[step] is None:
        return None
    return step[0] - sx, step[1] - sy


def _clamp_point(point: Point) -> Point:
    return (
        max(0, min(_MAX_COORDINATE, int(point[0]))),
        max(0, min(_MAX_COORDINATE, int(point[1]))),
    )


class MyAgent(Agent):
    """Deterministic symbolic baseline with planning and episodic memory."""

    MAX_ACTIONS = 240
    STAGNATION_LIMIT = 14
    CLICK_INTERVAL = 7

    PLAYER_COLORS = {9, 10, 12}
    GOAL_COLORS = {6, 7}
    WALL_COLORS = {5}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        seed_bytes = hashlib.blake2b(
            self.game_id.encode("utf-8"), digest_size=8
        ).digest()
        self.rng = random.Random(int.from_bytes(seed_bytes, "little"))
        self.state_visits: Counter[str] = Counter()
        self.action_uses: Counter[str] = Counter()
        self.action_values: defaultdict[str, float] = defaultdict(float)
        self.state_action_failures: Counter[tuple[str, str]] = Counter()
        self.dead_clicks: set[tuple[str, int, int]] = set()
        self.last_grid: Grid = []
        self.last_state_key = ""
        self.last_action_name: str | None = None
        self.last_click: Point | None = None
        self.last_levels = 0
        self.stagnation = 0
        self.level_step = 0

    @property
    def name(self) -> str:
        return f"{super().name}.lead-ai-symbolic-v2"

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def _reset_episode_memory(
        self,
        *,
        keep_values: bool = True,
        current_levels: int | None = None,
    ) -> None:
        self.state_visits.clear()
        self.state_action_failures.clear()
        self.dead_clicks.clear()
        self.last_grid = []
        self.last_state_key = ""
        self.last_action_name = None
        self.last_click = None
        self.stagnation = 0
        self.level_step = 0
        if current_levels is not None:
            self.last_levels = current_levels
        if not keep_values:
            self.action_uses.clear()
            self.action_values.clear()

    def _learn_from_transition(self, latest_frame: FrameData, grid: Grid) -> None:
        levels = int(getattr(latest_frame, "levels_completed", 0) or 0)
        if self.last_action_name is None or not self.last_grid:
            self.last_levels = levels
            return

        current_key = _grid_signature(grid)
        changed = _changed_cells(self.last_grid, grid)
        level_gain = max(0, levels - self.last_levels)
        died = latest_frame.state is GameState.GAME_OVER
        repeated = self.state_visits[current_key] > 0

        reward = math.log1p(changed)
        reward += 40.0 * level_gain
        reward -= 8.0 if died else 0.0
        reward -= 1.5 if changed == 0 else 0.0
        reward -= 0.5 if repeated else 0.0

        action_name = self.last_action_name
        count = max(1, self.action_uses[action_name])
        previous = self.action_values[action_name]
        self.action_values[action_name] = previous + (reward - previous) / count

        if changed == 0:
            self.stagnation += 1
            self.state_action_failures[(self.last_state_key, action_name)] += 1
            if self.last_click is not None:
                self.dead_clicks.add((self.last_state_key, *self.last_click))
        else:
            self.stagnation = max(0, self.stagnation - 2)

    def _movement_action(
        self,
        grid: Grid,
        legal: list[GameAction],
        state_key: str,
    ) -> GameAction | None:
        player = _centroid(_find_colors(grid, self.PLAYER_COLORS))
        goal_cells = set(_find_colors(grid, self.GOAL_COLORS))
        if player is None or not goal_cells:
            return None

        action_by_name = {action.name: action for action in legal}
        direction = _shortest_direction(
            grid,
            player,
            goal_cells,
            self.WALL_COLORS,
        )
        ranked: list[str] = []
        if direction in _DIRECTION_TO_ACTION:
            ranked.append(_DIRECTION_TO_ACTION[direction])

        goal = _centroid(goal_cells)
        if goal is not None:
            px, py = player
            gx, gy = goal
            if abs(gx - px) >= abs(gy - py):
                ranked.extend(
                    [
                        "ACTION4" if gx > px else "ACTION3",
                        "ACTION2" if gy > py else "ACTION1",
                    ]
                )
            else:
                ranked.extend(
                    [
                        "ACTION2" if gy > py else "ACTION1",
                        "ACTION4" if gx > px else "ACTION3",
                    ]
                )

        seen: set[str] = set()
        for name in ranked:
            if name in seen:
                continue
            seen.add(name)
            action = action_by_name.get(name)
            if action is None:
                continue
            if self.state_action_failures[(state_key, name)] < 2:
                return action
        for name in ranked:
            action = action_by_name.get(name)
            if action is not None:
                return action
        return None

    def _click_target(self, grid: Grid, state_key: str) -> Point | None:
        if not grid:
            return None
        counts = Counter(value for row in grid for value in row)
        total_cells = max(1, sum(counts.values()))
        candidates: list[tuple[float, Point]] = []
        for color, points in _connected_components(grid):
            if color in self.WALL_COLORS or color in self.PLAYER_COLORS:
                continue
            size = len(points)
            if size == 0:
                continue
            center = _centroid(points)
            if center is None:
                continue
            center = _clamp_point(center)
            if (state_key, *center) in self.dead_clicks:
                continue
            rarity = 1.0 / max(1, counts[color])
            compactness = 1.0 / math.sqrt(size)
            semantic_bonus = 2.5 if color in self.GOAL_COLORS else 0.0
            background_penalty = 3.0 if counts[color] > 0.45 * total_cells else 0.0
            jitter = self.rng.random() * 0.01
            score = (
                8.0 * rarity
                + 2.0 * compactness
                + semantic_bonus
                - background_penalty
                + jitter
            )
            candidates.append((score, center))
        return max(candidates, default=(0.0, None), key=lambda item: item[0])[1]

    def _exploration_action(
        self,
        legal: list[GameAction],
        state_key: str,
    ) -> GameAction:
        simple = [action for action in legal if not action.is_complex()]
        pool = simple or legal
        total = 1 + sum(self.action_uses[action.name] for action in pool)

        def score(action: GameAction) -> float:
            uses = self.action_uses[action.name]
            value = self.action_values[action.name]
            curiosity = math.sqrt(2.0 * math.log(total + 1) / (uses + 1))
            failure_penalty = 1.25 * self.state_action_failures[
                (state_key, action.name)
            ]
            return value + curiosity - failure_penalty + self.rng.random() * 1e-4

        return max(pool, key=score)

    def choose_action(
        self,
        frames: list[FrameData],
        latest_frame: FrameData,
    ) -> GameAction:
        levels = int(getattr(latest_frame, "levels_completed", 0) or 0)
        full_reset = bool(getattr(latest_frame, "full_reset", False))
        if full_reset or latest_frame.state in (
            GameState.NOT_PLAYED,
            GameState.GAME_OVER,
        ):
            self._reset_episode_memory(
                keep_values=not full_reset,
                current_levels=levels,
            )
            action = GameAction.RESET
            action.reasoning = {
                "policy": "reset",
                "full_reset": full_reset,
                "state": str(latest_frame.state),
            }
            return action

        grid = _screen(latest_frame)
        self._learn_from_transition(latest_frame, grid)

        if levels > self.last_levels:
            self._reset_episode_memory(
                keep_values=True,
                current_levels=levels,
            )

        state_key = _grid_signature(grid)
        self.state_visits[state_key] += 1
        legal = _legal_actions(latest_frame)
        if not legal:
            action = GameAction.RESET
            action.reasoning = {
                "policy": "safety-reset",
                "why": "no legal actions resolved",
            }
            return action

        if self.stagnation >= self.STAGNATION_LIMIT:
            self._reset_episode_memory(
                keep_values=True,
                current_levels=levels,
            )
            action = GameAction.RESET
            action.reasoning = {
                "policy": "stagnation-recovery",
                "why": f"no useful change for {self.STAGNATION_LIMIT} decisions",
            }
            return action

        complex_actions = [action for action in legal if action.is_complex()]
        chosen: GameAction | None = None
        target: Point | None = None
        strategy = "exploration"

        if (
            complex_actions
            and self.level_step % self.CLICK_INTERVAL == self.CLICK_INTERVAL - 1
        ):
            target = self._click_target(grid, state_key)
            if target is not None:
                chosen = min(
                    complex_actions,
                    key=lambda action: self.action_uses[action.name],
                )
                chosen.set_data({"x": target[0], "y": target[1]})
                strategy = "rare-object-click"

        if chosen is None:
            chosen = self._movement_action(grid, legal, state_key)
            if chosen is not None:
                strategy = "shortest-path-movement"
        if chosen is None:
            chosen = self._exploration_action(legal, state_key)

        if chosen.is_complex() and target is None:
            target = self._click_target(grid, state_key)
            if target is None:
                width = min(_MAX_COORDINATE + 1, len(grid[0]) if grid else 64)
                height = min(_MAX_COORDINATE + 1, len(grid) if grid else 64)
                target = (
                    self.rng.randrange(max(1, width)),
                    self.rng.randrange(max(1, height)),
                )
            target = _clamp_point(target)
            chosen.set_data({"x": target[0], "y": target[1]})
            strategy = "complex-action-exploration"

        self.action_uses[chosen.name] += 1
        self.last_action_name = chosen.name
        self.last_click = target if chosen.is_complex() else None
        self.last_grid = grid
        self.last_state_key = state_key
        self.last_levels = levels
        self.level_step += 1

        chosen.reasoning = {
            "policy": "lead-ai-symbolic-v2",
            "strategy": strategy,
            "state": state_key,
            "visit": self.state_visits[state_key],
            "stagnation": self.stagnation,
            "action_value": round(self.action_values[chosen.name], 4),
            "state_action_failures": self.state_action_failures[
                (state_key, chosen.name)
            ],
            "click_target": target,
        }
        return chosen
