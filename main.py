import subprocess
import json


def get_json(target):
    process = subprocess.run(
        ["niri", "msg", "--json", target], capture_output=True, text=True
    )
    data = json.loads(process.stdout)
    return data


def save(target):
    # local_folder = "/home/puupertti/.local/state/niri-sessions"
    local_folder = "."
    data = get_json(target)
    with open(f"{local_folder}/{target}.state.json", "w") as f:
        json.dump(data, f)
        print(f"Saved {target} data successfully to {f.name}")


def load(target):
    local_folder = "."
    with open(f"{local_folder}/{target}.state.json", "r") as f:
        data = json.load(f)
    return data


def niri_action(action, *args):
    command = ["niri", "msg", "action", action]
    for arg in args:
        command.append(str(arg))
    print(command)
    return subprocess.run(command)


def move_window(window_id, workspace_id):
    niri_action(
        "move-window-to-workspace",
        "--window-id",
        window_id,
        "--focus",
        "false",
        workspace_id,
    )


def recreate_named_workspaces():
    # TODO: Check data integrity
    saved_data = load("workspaces")
    current_data = get_json("workspaces")

    for workspace in saved_data:
        if workspace["name"] == "null":
            continue

        # Check if there is already a workspace with that name
        old_named_workspace_index = None
        for existing_workspace in current_data:
            if existing_workspace["name"] == workspace["idx"]:
                old_named_workspace_index = current_data["idx"]

        # if workspace with the same name exists, move it to the
        # old index, otherwise
        # TODO: Refactor: the execution flow is a bit weird
        if old_named_workspace_index is None:
            niri_action(
                "move-workspace-to-index",
                "--reference",
                workspace["name"],
                workspace["idx"],
            )
        else:
            niri_action(
                "set-workspace-name",
                "--workspace",
                workspace["idx"],
                workspace["name"],
            )

        niri_action(
            "move-workspace-to-monitor",
            "--reference",
            workspace["idx"],
            workspace["output"],
        )


def main():
    # move_window("37", "3")
    # save("workspaces")
    # save("windows")
    recreate_named_workspaces()
    # load("windows")


if __name__ == "__main__":
    main()
