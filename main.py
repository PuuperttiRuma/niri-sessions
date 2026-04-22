from niri_ipc import (
    NiriTarget,
    get_niri_state,
    load_state_from_file,
    move_workspace_to_index,
    move_workspace_to_monitor,
    save_state_to_file,
    set_workspace_name,
)


def recreate_named_workspaces():
    # TODO: Check data integrity
    saved_data = load_state_from_file(NiriTarget.WORKSPACES)
    current_data = get_niri_state(NiriTarget.WORKSPACES)

    for saved_workspace in saved_data:
        idx = saved_workspace["idx"]
        name = saved_workspace["name"]
        output = saved_workspace["output"]

        print(f"Workspace: {idx}, {name}")
        if name is None:
            print(f"Workspace idx {idx}, has no name, skip.")
            continue

        current_workspace_names = []
        for current_workspace in current_data:
            current_workspace_names.append(current_workspace["name"])

        if saved_workspace["name"] in current_workspace_names:
            move_workspace_to_index(name, idx)
        else:
            set_workspace_name(name, idx)
        move_workspace_to_monitor(output, idx)


def main():
    # move_window("37", "3")
    save_state_to_file(NiriTarget.WORKSPACES)
    save_state_to_file(NiriTarget.WINDOWS)
    # recreate_named_workspaces()
    # load("windows")


if __name__ == "__main__":
    main()
