import argparse
from niri_ipc import (
    NiriTarget,
    save_state_to_file,
)
from state_manager import StateManager


def save_action(args):
    print("Saving desktop state")
    save_state_to_file(NiriTarget.WORKSPACES)
    save_state_to_file(NiriTarget.WINDOWS)


def load_action(args):
    print("Loading previous desktop state")

    manager = StateManager()
    manager.restore_state()

    # For debugging
    # for workspace in manager.saved_workspaces:
    #     print(workspace)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    save_parser = subparsers.add_parser("save", help="Save current desktop state.")
    save_parser.set_defaults(func=save_action)

    load_parser = subparsers.add_parser("load", help="Load desktop state.")
    load_parser.set_defaults(func=load_action)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("No argument given")
        parser.print_help()

    # move_window("37", "3")
    # recreate_named_workspaces()


if __name__ == "__main__":
    main()
