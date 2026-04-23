class StateManager:
    def __init__(self) -> None:
        self.workspaces = []

    def parse_workspaces(self, workspaces_json: dict):
        for data in workspaces_json:
            new_workspace = Workspace(
                data["id"], data["idx"], data["name"], data["output"]
            )
            self.workspaces.append(new_workspace)


class Workspace:
    def __init__(self, id, index, name, output) -> None:
        self.windows = []
        self.id = id
        self.index = index
        self.name = name
        self.output = output


class Window:
    def __init__(self, id, title, app_id, workspace_id) -> None:
        self.id = id
        self.title = title
        self.app_id = app_id
        self.workspace_id = workspace_id


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
