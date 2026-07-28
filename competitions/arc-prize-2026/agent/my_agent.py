"""Lead.AI ARC Prize 2026 baseline agent.

Self-contained by design: the official ARC Kaggle starter splices this file into
its generated submission notebook. Keep external dependencies out of this file.
"""
from __future__ import annotations

import hashlib
import math
import random
from collections import Counter, defaultdict, deque
from typing import Any, Iterable, Sequence

from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent


Grid = list[list[int]]
Point = tuple[int, int]


def _screen(frame: FrameData) -> Grid:
    """Return the latest 2-D screen from a possibly stacked frame payload."""
    raw = getattr(frame, "frame", None) or []
    if not raw:
        return []
    candidate = raw[-1]
    if not isinstance(candidate, Sequence):
        return []
    out: Grid = []
    for row in candidate:
        if isinstance(row, Sequence):
            out.append([int(value) for value in row])
    return out


def _grid_signature(grid: Grid) -> str:
    """Stable compact state key independent of Python's randomized hash seed."""
    digest = hashlib.blake2b(digest_size=12)
    digest.update(len(grid).to_bytes(2, "little", signed=False))
    digest.update((len(grid[0]) if grid else 0).to_bytes(2, "little", signed=False))
    for row in grid:
        digest.update(bytes(max(0, min(255, value)) for value in row))
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
    """Return 4-connected same-color components as ``(color, points)``."""
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
                for nx, ny in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
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
        except Exception:
            try:
                return GameAction.from_name(item.upper())
            except Exception:
                return None
    if isinstance(item, int):
        try:
            return GameAction.from_id(item)
        except Exception:
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
    if raw:
        for item in raw:
            action = _safe_action_from_item(item)
            if action is not None and action is not GameAction.RESET and action not in actions:
                actions.append(action)
    if actions:
        return actions
    return [action for action in GameAction if action is not GameAction.RESET]


class MyAgent(Agent):
    """Deterministic novelty-driven baseline with visual and episodic memory."""

    MAX_ACTIONS = 240
    STAGNATION_LIMIT = 14
    CLICK_INTERVAL = 7

    # Public ARC documentation identifies these common visual roles. The policy
    # uses them only when detected and otherwise falls back to generic novelty.
    PLAYER_COLORS = {9, 10, 12}  # blue body / light-blue / orange head
    GOAL_COLORS = {6, 7}  # pink / magenta goal or door cues
    WALL_COLORS = {5}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        seed_bytes = hashlib.blake2b(self.game_id.encode("utf-8"), digest_size=8).digest()
        self.rng = random.Random(int.from_bytes(seed_bytes, "little"))
        self.state_visits: Counter[str] = Counter()
        self.action_uses: Counter[str] = Counter()
        self.action_values: defaultdict[str, float] = defaultdict(float)
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
        return f"{super().name}.lead-ai-novelty-v1"

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def _reset_episode_memory(self, keep_values: bool = True) -> None:
        self.state_visits.clear()
        self.dead_clicks.clear()
        self.last_grid = []
        self.last_state_key = ""
        self.last_action_name = None
        self.last_click = None
        self.stagnation = 0
        self.level_step = 0
        if not keep_values:
            self.action_uses.clear()
            self.action_values.clear()

    def _learn_from_transition(self, latest_frame: FrameData, grid: Grid) -> None:
        levels = int(getattr(latest_frame, "levels_completed", 0) or 0)
        if self.last_action_name is None or not self.last_grid:
            self.last_levels = levels
            return

        changed = _changed_cells(self.last_grid, grid)
        level_gain = max(0, levels - self.last_levels)
        died = latest_frame.state is GameState.GAME_OVER
        repeated = self.state_visits[_grid_signature(grid)] > 0

        reward = math.log1p(changed)
        reward += 40.0 * level_gain
        reward -= 8.0 if died else 0.0
        reward -= 1.5 if changed == 0 else 0.0
        reward -= 0.5 if repeated else 0.0

        key = self.last_action_name
        count = self.action_uses[key]
        previous = self.action_values[key]
        self.action_values[key] = previous + (reward - previous) / max(1, count)

        if changed == 0:
            self.stagnation += 1
            if self.last_click is not None:
                self.dead_clicks.add((self.last_state_key, *self.last_click))
        else:
            self.stagnation = max(0, self.stagnation - 2)

    def _movement_action(self, grid: Grid, legal: list[GameAction]) -> GameAction | None:
        player = _centroid(_find_colors(grid, self.PLAYER_COLORS))
        goals = _find_colors(grid, self.GOAL_COLORS)
        goal = _centroid(goals)
        if player is None or goal is None:
            return None

        action_by_name = {action.name: action for action in legal}
        px, py = player
        gx, gy = goal
        ranked: list[str] = []
        if abs(gx - px) >= abs(gy - py):
            ranked.extend(["ACTION4" if gx > px else "ACTION3", "ACTION2" if gy > py else "ACTION1"])
        else:
            ranked.extend(["ACTION2" if gy > py else "ACTION1", "ACTION4" if gx > px else "ACTION3"])

        # Prefer a direction not already proven ineffective in the current state.
        for name in ranked:
            if name in action_by_name and self.action_values[name] > -1.25:
                return action_by_name[name]
        for name in ranked:
            if name in action_by_name:
                return action_by_name[name]
        return None

    def _click_target(self, grid: Grid, state_key: str) -> Point | None:
        if not grid:
            return None
        counts = Counter(value for row in grid for value in row)
        candidates: list[tuple[float, Point]] = []
        for color, points in _connected_components(grid):
            if color in self.WALL_COLORS or color in self.PLAYER_COLORS:
                continue
            size = len(points)
            if size == 0:
                continue
            center = _centroid(points)
            if center is None or (state_key, *center) in self.dead_clicks:
                continue
            # Small, rare, non-background components are more likely to be
            # buttons, symbols, keys, or other interactive objects.
            rarity = 1.0 / max(1, counts[color])
            compactness = 1.0 / math.sqrt(size)
            semantic_bonus = 2.5 if color in self.GOAL_COLORS else 0.0
            background_penalty = 3.0 if counts[color] > 0.45 * sum(counts.values()) else 0.0
            jitter = self.rng.random() * 0.01
            score = 8.0 * rarity + 2.0 * compactness + semantic_bonus - background_penalty + jitter
            candidates.append((score, center))
        return max(candidates, default=(0.0, None), key=lambda item: item[0])[1]

    def _exploration_action(self, legal: list[GameAction]) -> GameAction:
        simple = [action for action in legal if not action.is_complex()]
        pool = simple or legal
        total = 1 + sum(self.action_uses[action.name] for action in pool)

        def score(action: GameAction) -> float:
            uses = self.action_uses[action.name]
            value = self.action_values[action.name]
            curiosity = math.sqrt(2.0 * math.log(total + 1) / (uses + 1))
            return value + curiosity + self.rng.random() * 1e-4

        return max(pool, key=score)

    def choose_action(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        if latest_frame.state in (GameState.NOT_PLAYED, GameState.GAME_OVER):
            self._reset_episode_memory(keep_values=True)
            action = GameAction.RESET
            action.reasoning = {"policy": "reset", "why": f"state={latest_frame.state}"}
            return action

        grid = _screen(latest_frame)
        self._learn_from_transition(latest_frame, grid)

        levels = int(getattr(latest_frame, "levels_completed", 0) or 0)
        if levels > self.last_levels:
            self._reset_episode_memory(keep_values=True)
            self.last_levels = levels

        state_key = _grid_signature(grid)
        self.state_visits[state_key] += 1
        legal = _legal_actions(latest_frame)
        if not legal:
            action = GameAction.RESET
            action.reasoning = {"policy": "safety-reset", "why": "no legal actions resolved"}
            return action

        if self.stagnation >= self.STAGNATION_LIMIT:
            self._reset_episode_memory(keep_values=True)
            action = GameAction.RESET
            action.reasoning = {
                "policy": "stagnation-recovery",
                "why": f"no useful change for {self.STAGNATION_LIMIT} decisions",
            }
            return action

        complex_actions = [action for action in legal if action.is_complex()]
        chosen: GameAction | None = None
        target: Point | None = None

        # Periodically test high-information visual objects when click-like
        # actions are available. Avoid coordinates already shown to be inert.
        if complex_actions and self.level_step % self.CLICK_INTERVAL == self.CLICK_INTERVAL - 1:
            target = self._click_target(grid, state_key)
            if target is not None:
                chosen = min(complex_actions, key=lambda action: self.action_uses[action.name])
                chosen.set_data({"x": int(target[0]), "y": int(target[1])})

        if chosen is None:
            chosen = self._movement_action(grid, legal)
        if chosen is None:
            chosen = self._exploration_action(legal)

        if chosen.is_complex() and target is None:
            target = self._click_target(grid, state_key)
            if target is None:
                width = len(grid[0]) if grid else 64
                height = len(grid) if grid else 64
                target = (self.rng.randrange(max(1, width)), self.rng.randrange(max(1, height)))
            chosen.set_data({"x": int(target[0]), "y": int(target[1])})

        self.action_uses[chosen.name] += 1
        self.last_action_name = chosen.name
        self.last_click = target if chosen.is_complex() else None
        self.last_grid = grid
        self.last_state_key = state_key
        self.last_levels = levels
        self.level_step += 1

        chosen.reasoning = {
            "policy": "lead-ai-novelty-v1",
            "state": state_key,
            "visit": self.state_visits[state_key],
            "stagnation": self.stagnation,
            "action_value": round(self.action_values[chosen.name], 4),
            "click_target": target,
            "why": "goal-directed movement when visible; otherwise novelty/UCB exploration",
        }
        return chosen
