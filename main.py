import subprocess
import json


def get_json(target):
    process = subprocess.run(
        ["niri", "msg", "--json", target], capture_output=True, text=True
    )
    data = json.loads(process.stdout)
    return data


def niri_action(action, *args):
    command = ["niri", "msg", "action", action]
    for arg in args:
        command.append(str(arg))
    print(command)
    return subprocess.run(command)


def move_window(window_id, workspace_id):
    niri_action("focus-window", "--id", window_id)
    niri_action("move-window-to-workspace", workspace_id)


def main():
    current_window = get_json("focused-window")
    move_window("37", "2")
    niri_action("focus-window", "--id", current_window["id"])


if __name__ == "__main__":
    main()
