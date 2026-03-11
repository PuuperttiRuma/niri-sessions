import subprocess
import json


def get_json(target):
    process = subprocess.run(
        ["niri", "msg", "--json", target], capture_output=True, text=True
    )
    data = json.loads(process.stdout)
    return data


def save(target):
    local_folder = "/home/puupertti/.local/state/niri-sessions"
    data = get_json(target)
    with open(f"{local_folder}/{target}.state.json", "w") as f:
        json.dump(data, f)


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


def main():
    # move_window("37", "3")
    save("workspaces")
    save("windows")


if __name__ == "__main__":
    main()
