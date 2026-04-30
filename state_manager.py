from dataclasses import dataclass, field

from niri_ipc import NiriTarget, get_niri_state, load_state_from_file


class StateManager:
    def __init__(self) -> None:
        self.saved_workspaces = []
        self.current_workspaces = []

    def parse_workspaces(self, workspaces_json: dict):
        workspaces = []
        for item in workspaces_json:
            new_workspace = Workspace(
                item["id"], item["idx"], item["name"], item["output"]
            )
            workspaces.append(new_workspace)
        return workspaces

    def parse_windows(self, windows_json: dict, workspaces: list):
        for item in windows_json:
            new_window = Window(
                item["id"], item["title"], item["app_id"], item["workspace_id"]
            )
            for workspace in workspaces:
                if workspace.id == new_window.workspace_id:
                    workspace.windows.append(new_window)
                    continue

    def restore_state(self):
        # Create an object depicting the saved desktop state
        saved_workspaces_state = load_state_from_file(NiriTarget.WORKSPACES)
        saved_windows_state = load_state_from_file(NiriTarget.WINDOWS)

        self.saved_workspaces = self.parse_workspaces(saved_workspaces_state)
        self.parse_windows(saved_windows_state, self.saved_workspaces)

        # Create an object depicting the current desktop state
        current_workspaces_state = get_niri_state(target=NiriTarget.WORKSPACES)
        current_windows_state = get_niri_state(target=NiriTarget.WINDOWS)

        self.current_workspaces = self.parse_workspaces(current_workspaces_state)
        self.parse_windows(current_windows_state, self.current_workspaces)

        # Recreate the old state by modifying the desktop


@dataclass
class Workspace:
    id: int
    index: int
    name: str
    output: str
    windows: list = field(default_factory=list)


@dataclass
class Window:
    id: int
    title: str
    app_id: str
    workspace_id: int


# def recreate_named_workspaces():
#     # TODO: Check data integrity
#     saved_data = load_state_from_file(NiriTarget.WORKSPACES)
#     current_data = get_niri_state(NiriTarget.WORKSPACES)
#
#     for saved_workspace in saved_data:
#         idx = saved_workspace["idx"]
#         name = saved_workspace["name"]
#         output = saved_workspace["output"]
#
#         print(f"Workspace: {idx}, {name}")
#         if name is None:
#             print(f"Workspace idx {idx}, has no name, skip.")
#             continue
#
#         current_workspace_names = []
#         for current_workspace in current_data:
#             current_workspace_names.append(current_workspace["name"])
#
#         if saved_workspace["name"] in current_workspace_names:
#             move_workspace_to_index(name, idx)
#         else:
#             set_workspace_name(name, idx)
#         move_workspace_to_monitor(output, idx)
