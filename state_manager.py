from dataclasses import dataclass, field


class StateManager:
    def __init__(self) -> None:
        self.workspaces = []

    def parse_workspaces(self, workspaces_json: dict):
        for item in workspaces_json:
            new_workspace = Workspace(
                item["id"], item["idx"], item["name"], item["output"]
            )
            self.workspaces.append(new_workspace)

    def parse_windows(self, windows_json: dict):
        for item in windows_json:
            new_window = Window(
                item["id"], item["title"], item["app_id"], item["workspace_id"]
            )
            for workspace in self.workspaces:
                if workspace.id == new_window.workspace_id:
                    workspace.windows.append(new_window)
                    continue

    def parse_saved_jsons(self, workspaces_json: dict, windows_json: dict):
        self.parse_workspaces(workspaces_json)
        self.parse_windows(windows_json)


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
