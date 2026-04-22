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

        # Check if there is already a workspace with that name
        # and if there is, move it to the correct index
        var = current_workspace_names
        print(type(var))
        print(var)
        if saved_workspace["name"] in var:
            niri_action(
                "move-workspace-to-index",
                "--reference",
                saved_workspace["name"],
                saved_workspace["idx"],
            )
        else:
            niri_action(
                "set-workspace-name",
                "--workspace",
                saved_workspace["idx"],
                saved_workspace["name"],
            )

        niri_action(
            "move-workspace-to-monitor",
            "--reference",
            saved_workspace["idx"],
            saved_workspace["output"],
        )


def main():
    # move_window("37", "3")
    # save("workspaces")
    # save("windows")
    recreate_named_workspaces()
    # load("windows")


if __name__ == "__main__":
    main()
