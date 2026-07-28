from __future__ import annotations

import importlib.util
import json
import sys
import types
from enum import Enum
from pathlib import Path


class DummyState(str, Enum):
    NOT_PLAYED = "NOT_PLAYED"
    NOT_FINISHED = "NOT_FINISHED"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"


class DummyAction(Enum):
    RESET = 0
    ACTION1 = 1
    ACTION2 = 2
    ACTION3 = 3
    ACTION4 = 4
    ACTION5 = 5
    ACTION6 = 6
    ACTION7 = 7

    @classmethod
    def from_name(cls, name: str) -> "DummyAction":
        return cls[name.upper()]

    @classmethod
    def from_id(cls, value: int) -> "DummyAction":
        return cls(value)

    def is_complex(self) -> bool:
        return self is DummyAction.ACTION6

    def set_data(self, data: dict[str, int]) -> None:
        x = int(data["x"])
        y = int(data["y"])
        if not 0 <= x <= 63 or not 0 <= y <= 63:
            raise ValueError("complex coordinates out of bounds")
        self.action_data = {"x": x, "y": y}


class DummyFrame:
    def __init__(
        self,
        frame: list[list[list[int]]] | None = None,
        state: DummyState = DummyState.NOT_FINISHED,
        levels_completed: int = 0,
        available_actions: list[object] | None = None,
        full_reset: bool = False,
    ) -> None:
        self.frame = frame or []
        self.state = state
        self.levels_completed = levels_completed
        self.available_actions = available_actions
        self.full_reset = full_reset


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


def frame(grid: list[list[int]], **kwargs: object) -> DummyFrame:
    return DummyFrame(frame=[grid], **kwargs)


def test_grid_signature_is_stable_sensitive_and_row_aware() -> None:
    grid = [[0, 1], [2, 3]]
    assert module._grid_signature(grid) == module._grid_signature([row[:] for row in grid])
    assert module._grid_signature(grid) != module._grid_signature([[0, 1], [2, 4]])
    assert module._grid_signature([[1], [2, 3]]) != module._grid_signature([[1], [2], [3]])


def test_changed_cells_counts_values_and_shape() -> None:
    assert module._changed_cells([[0, 1]], [[0, 2]]) == 1
    assert module._changed_cells([[0]], [[0, 1]]) == 1
    assert module._changed_cells([], []) == 0


def test_connected_components_uses_four_connectivity() -> None:
    components = module._connected_components([[1, 0, 1], [1, 0, 0]])
    sizes = sorted((color, len(points)) for color, points in components)
    assert sizes == [(0, 3), (1, 1), (1, 2)]


def test_screen_returns_latest_layer_and_rejects_ragged_rows() -> None:
    assert module._screen(DummyFrame(frame=[[[1]], [[2]]])) == [[2]]
    assert module._screen(DummyFrame(frame=[[[1], [2, 3]]])) == []


def test_screen_rejects_malformed_values() -> None:
    malformed = DummyFrame(frame=[[['not-an-integer']]])  # type: ignore[list-item]
    assert module._screen(malformed) == []


def test_legal_actions_normalizes_names_ids_and_dicts() -> None:
    test_frame = DummyFrame(
        available_actions=["ACTION1", 2, {"name": "ACTION4"}, "RESET", "UNKNOWN"]
    )
    assert module._legal_actions(test_frame) == [
        DummyAction.ACTION1,
        DummyAction.ACTION2,
        DummyAction.ACTION4,
    ]


def test_shortest_direction_routes_around_walls() -> None:
    grid = [
        [0, 0, 0, 0, 0],
        [0, 9, 5, 6, 0],
        [0, 0, 0, 0, 0],
    ]
    direction = module._shortest_direction(grid, (1, 1), {(3, 1)}, {5})
    assert direction in {(0, -1), (0, 1)}


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


def test_goal_directed_movement_uses_shortest_path() -> None:
    agent = module.MyAgent(game_id="movement-test")
    grid = [
        [0, 0, 0, 0, 0],
        [0, 9, 0, 0, 6],
        [0, 0, 0, 0, 0],
    ]
    legal = [
        DummyAction.ACTION1,
        DummyAction.ACTION2,
        DummyAction.ACTION3,
        DummyAction.ACTION4,
    ]
    state_key = module._grid_signature(grid)
    assert agent._movement_action(grid, legal, state_key) is DummyAction.ACTION4


def test_full_reset_clears_learned_values() -> None:
    agent = module.MyAgent(game_id="reset-test")
    agent.action_values["ACTION1"] = 9.0
    action = agent.choose_action(
        [],
        frame([[0]], full_reset=True, available_actions=[1, 2, 3, 4]),
    )
    assert action is DummyAction.RESET
    assert agent.action_values == {}


def test_game_over_resets_but_keeps_global_action_values() -> None:
    agent = module.MyAgent(game_id="death-test")
    agent.action_values["ACTION1"] = 2.0
    action = agent.choose_action(
        [],
        frame(
            [[0]],
            state=DummyState.GAME_OVER,
            available_actions=[1, 2, 3, 4],
        ),
    )
    assert action is DummyAction.RESET
    assert agent.action_values["ACTION1"] == 2.0


def test_choose_action_is_deterministic_for_same_game_and_state() -> None:
    grid = [[0, 0], [0, 0]]
    available = [1, 2, 3, 4, 5, 7]
    first = module.MyAgent(game_id="deterministic")
    second = module.MyAgent(game_id="deterministic")
    action_one = first.choose_action([], frame(grid, available_actions=available))
    action_two = second.choose_action([], frame(grid, available_actions=available))
    assert action_one is action_two


def test_complex_action_coordinates_always_fit_arc_contract() -> None:
    agent = module.MyAgent(game_id="complex")
    action = agent.choose_action(
        [],
        frame([[0]], available_actions=[6]),
    )
    assert action is DummyAction.ACTION6
    assert 0 <= action.action_data["x"] <= 63
    assert 0 <= action.action_data["y"] <= 63


def test_no_available_payload_falls_back_to_all_non_reset_actions() -> None:
    actions = module._legal_actions(frame([[0]], available_actions=[]))
    assert DummyAction.RESET not in actions
    assert set(actions) == set(DummyAction) - {DummyAction.RESET}


def test_reasoning_metadata_is_json_serializable() -> None:
    agent = module.MyAgent(game_id="reasoning")
    action = agent.choose_action(
        [],
        frame([[0, 9, 6]], available_actions=[1, 2, 3, 4]),
    )
    json.dumps(action.reasoning)


def test_state_action_failure_penalty_avoids_repeated_dead_move() -> None:
    agent = module.MyAgent(game_id="failure-penalty")
    grid = [[0, 0], [0, 0]]
    key = module._grid_signature(grid)
    agent.state_action_failures[(key, "ACTION1")] = 10
    legal = [DummyAction.ACTION1, DummyAction.ACTION2]
    assert agent._exploration_action(legal, key) is DummyAction.ACTION2


def test_safe_action_parser_rejects_unknown_payloads() -> None:
    assert module._safe_action_from_item("UNKNOWN") is None
    assert module._safe_action_from_item(999) is None
    assert module._safe_action_from_item({"other": "ACTION1"}) is None
    assert module._safe_action_from_item(None) is None


def test_shortest_direction_handles_terminal_and_blocked_cases() -> None:
    grid = [[9, 5, 6]]
    assert module._shortest_direction(grid, (0, 0), {(0, 0)}, {5}) is None
    assert module._shortest_direction(grid, (0, 0), {(2, 0)}, {5}) is None
    assert module._shortest_direction(grid, (99, 99), {(2, 0)}, {5}) is None


def test_clamp_point_enforces_complex_action_bounds() -> None:
    assert module._clamp_point((-5, 100)) == (0, 63)


def test_dead_click_is_not_selected_again() -> None:
    agent = module.MyAgent(game_id="dead-click")
    grid = [[0, 0, 0], [0, 6, 0], [0, 0, 0]]
    key = module._grid_signature(grid)
    agent.dead_clicks.add((key, 1, 1))
    assert agent._click_target(grid, key) != (1, 1)


def test_unchanged_transition_records_failure_and_dead_click() -> None:
    agent = module.MyAgent(game_id="learn-failure")
    grid = [[0, 0], [0, 0]]
    key = module._grid_signature(grid)
    agent.last_grid = [row[:] for row in grid]
    agent.last_state_key = key
    agent.last_action_name = "ACTION6"
    agent.last_click = (1, 1)
    agent.action_uses["ACTION6"] = 1
    agent._learn_from_transition(frame(grid), grid)
    assert agent.stagnation == 1
    assert agent.state_action_failures[(key, "ACTION6")] == 1
    assert (key, 1, 1) in agent.dead_clicks


def test_changed_transition_reduces_stagnation() -> None:
    agent = module.MyAgent(game_id="learn-success")
    agent.last_grid = [[0]]
    agent.last_state_key = module._grid_signature([[0]])
    agent.last_action_name = "ACTION1"
    agent.action_uses["ACTION1"] = 1
    agent.stagnation = 3
    agent._learn_from_transition(frame([[1]]), [[1]])
    assert agent.stagnation == 1
    assert agent.action_values["ACTION1"] > 0


def test_stagnation_limit_forces_recovery_reset() -> None:
    agent = module.MyAgent(game_id="stagnation")
    agent.stagnation = agent.STAGNATION_LIMIT
    action = agent.choose_action(
        [],
        frame([[0]], available_actions=[1, 2, 3, 4]),
    )
    assert action is DummyAction.RESET
    assert action.reasoning["policy"] == "stagnation-recovery"


def test_periodic_click_uses_complex_action_and_target() -> None:
    agent = module.MyAgent(game_id="periodic-click")
    agent.level_step = agent.CLICK_INTERVAL - 1
    action = agent.choose_action(
        [],
        frame(
            [[0, 0, 0], [0, 6, 0], [0, 0, 0]],
            available_actions=[1, 2, 3, 4, 6],
        ),
    )
    assert action is DummyAction.ACTION6
    assert action.reasoning["strategy"] == "rare-object-click"


def test_level_gain_clears_episode_state_but_keeps_values() -> None:
    agent = module.MyAgent(game_id="level-gain")
    agent.last_grid = [[0]]
    agent.last_state_key = module._grid_signature([[0]])
    agent.last_action_name = "ACTION1"
    agent.action_uses["ACTION1"] = 1
    agent.last_levels = 0
    agent.state_visits["old"] = 3
    agent.choose_action(
        [],
        frame([[1]], levels_completed=1, available_actions=[1, 2, 3, 4]),
    )
    assert "old" not in agent.state_visits
    assert agent.last_levels == 1


def test_is_done_only_on_win() -> None:
    agent = module.MyAgent(game_id="done")
    assert not agent.is_done([], frame([[0]]))
    assert agent.is_done([], frame([[0]], state=DummyState.WIN))
