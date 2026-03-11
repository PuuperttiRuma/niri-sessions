import subprocess


def get_json(target):
    process = subprocess.run(
        ["niri", "msg", "--json", target], capture_output=True, text=True
    )
    # TODO: Add JSON parsing so returns a proper JSON object
    return process.stdout


def niri_action(action, *args):
    command = ["niri", "msg", "action", action]
    for arg in args:
        command.append(arg)
    return subprocess.run(command)


def move_window(window_id, workspace_id):
    niri_action("focus-window", "--id", window_id)
    niri_action("move-window-to-workspace", workspace_id)


def main():
    move_window("37", "2")


if __name__ == "__main__":
    main()
