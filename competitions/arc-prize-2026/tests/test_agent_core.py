from __future__ import annotations

import importlib.util
import sys
import types
from enum import Enum
from pathlib import Path


class DummyState(Enum):
    NOT_PLAYED = 0
    PLAYING = 1
    GAME_OVER = 2
    WIN = 3


class DummyAction(Enum):
    RESET = 0
    ACTION1 = 1
    ACTION2 = 2
    ACTION3 = 3
    ACTION4 = 4
    ACTION6 = 6

    @classmethod
    def from_name(cls, name: str) -> "DummyAction":
        return cls[name]

    @classmethod
    def from_id(cls, value: int) -> "DummyAction":
        return cls(value)

    def is_complex(self) -> bool:
        return self is DummyAction.ACTION6

    def set_data(self, data: dict[str, int]) -> None:
        self.action_data = data


class DummyFrame:
    def __init__(
        self,
        frame: list[list[list[int]]] | None = None,
        state: DummyState = DummyState.PLAYING,
        levels_completed: int = 0,
        available_actions: list[object] | None = None,
    ) -> None:
        self.frame = frame or []
        self.state = state
        self.levels_completed = levels_completed
        self.available_actions = available_actions


class DummyAgent:
    def __init__(self, *args: object, **kwargs: object) -> None:
        self.game_id = str(kwargs.get("game_id", "unit-test"))

    @property
    def name(self) -> str:
        return f"{self.game_id}.dummy"


arcengine = types.ModuleType("arcengine")
arcengine.FrameData = DummyFrame
arcengine.GameAction = DummyAction
arcengine.GameState = DummyState
sys.modules["arcengine"] = arcengine

agents = types.ModuleType("agents")
agent_module = types.ModuleType("agents.agent")
agent_module.Agent = DummyAgent
sys.modules["agents"] = agents
sys.modules["agents.agent"] = agent_module

MODULE_PATH = Path(__file__).parents[1] / "agent" / "my_agent.py"
spec = importlib.util.spec_from_file_location("lead_ai_arc_agent", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_grid_signature_is_stable_and_sensitive() -> None:
    grid = [[0, 1], [2, 3]]
    assert module._grid_signature(grid) == module._grid_signature([row[:] for row in grid])
    assert module._grid_signature(grid) != module._grid_signature([[0, 1], [2, 4]])


def test_changed_cells_counts_values_and_shape() -> None:
    assert module._changed_cells([[0, 1]], [[0, 2]]) == 1
    assert module._changed_cells([[0]], [[0, 1]]) == 1
    assert module._changed_cells([], []) == 0


def test_connected_components_uses_four_connectivity() -> None:
    components = module._connected_components([[1, 0, 1], [1, 0, 0]])
    sizes = sorted((color, len(points)) for color, points in components)
    assert sizes == [(0, 3), (1, 1), (1, 2)]


def test_screen_returns_latest_layer() -> None:
    frame = DummyFrame(frame=[[[1]], [[2]]])
    assert module._screen(frame) == [[2]]


def test_legal_actions_normalizes_names_ids_and_dicts() -> None:
    frame = DummyFrame(
        available_actions=["ACTION1", 2, {"name": "ACTION4"}, "RESET", "UNKNOWN"]
    )
    assert module._legal_actions(frame) == [
        DummyAction.ACTION1,
        DummyAction.ACTION2,
        DummyAction.ACTION4,
    ]


def test_click_target_prefers_small_rare_goal_component() -> None:
    agent = module.MyAgent(game_id="click-test")
    grid = [
        [0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0],
        [0, 9, 0, 6, 0],
        [0, 0, 0, 0, 0],
    ]
    target = agent._click_target(grid, module._grid_signature(grid))
    assert target == (3, 2)


def test_goal_directed_movement_moves_right_toward_goal() -> None:
    agent = module.MyAgent(game_id="movement-test")
    grid = [
        [0, 0, 0, 0, 0],
        [0, 9, 0, 0, 6],
        [0, 0, 0, 0, 0],
    ]
    legal = [DummyAction.ACTION1, DummyAction.ACTION2, DummyAction.ACTION3, DummyAction.ACTION4]
    assert agent._movement_action(grid, legal) is DummyAction.ACTION4
