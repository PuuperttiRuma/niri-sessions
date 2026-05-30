import subprocess
import json
from enum import Enum
from pathlib import Path


class NiriTarget(str, Enum):
    WINDOWS = ("windows",)
    WORKSPACES = ("workspaces",)
    OUTPUTS = "outputs"


SESSION_DIR = Path.home() / ".local/state/niri-sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)


def get_niri_state(target: NiriTarget) -> dict:
    process = subprocess.run(
        ["niri", "msg", "--json", target], capture_output=True, text=True
    )
    data = json.loads(process.stdout)
    return data


def save_state_to_file(target: NiriTarget) -> None:
    data = get_niri_state(target)
    with open(SESSION_DIR / f"{target.value}.state.json", "w") as f:
        json.dump(data, f)
        print(f"Saved {target.value} data successfully to {f.name}")


def load_state_from_file(target: NiriTarget) -> dict:
    with open(SESSION_DIR / f"{target.value}.state.json", "r") as f:
        data = json.load(f)
    return data


def niri_action(action, *args):
    command = ["niri", "msg", "action", action]
    for arg in args:
        command.append(str(arg))
    # print(command)
    return subprocess.run(command)


def move_window_to_workspace(window_id, workspace_ref):
    """Move a window to a workspace

    window_id: Id of the window to move.
    reference: Index or name of the workspace to move the window to.
    """
    niri_action(
        "move-window-to-workspace",
        "--window-id",
        window_id,
        "--focus",
        "false",
        workspace_ref,
    )


def move_workspace_to_index(workspace_name, index):
    niri_action("move-workspace-to-index", "--reference", workspace_name, index)


def set_workspace_name(workspace_name, index):
    niri_action(
        "set-workspace-name",
        "--workspace",
        index,
        workspace_name,
    )


def move_workspace_to_monitor(output, index):
    niri_action("move-workspace-to-monitor", "--reference", index, output)
