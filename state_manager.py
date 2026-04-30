from dataclasses import dataclass, field

from niri_ipc import (
    NiriTarget,
    get_niri_state,
    load_state_from_file,
    move_window_to_workspace,
    move_workspace_to_index,
    set_workspace_name,
)


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

    def parse_windows(self, windows_json: dict):
        windows = []
        for item in windows_json:
            new_window = Window(
                item["id"], item["title"], item["app_id"], item["workspace_id"]
            )
            windows.append(new_window)
        return windows

    def restore_state(self):
        # Create an object depicting the saved desktop state
        saved_workspaces_state = load_state_from_file(NiriTarget.WORKSPACES)
        saved_windows_state = load_state_from_file(NiriTarget.WINDOWS)

        self.saved_workspaces = self.parse_workspaces(saved_workspaces_state)
        saved_windows = self.parse_windows(saved_windows_state)
        for window in saved_windows:
            for workspace in self.saved_workspaces:
                if workspace.id == window.workspace_id:
                    workspace.windows.append(window)
                    continue

        # Create an object depicting the current desktop state
        current_workspaces_state = get_niri_state(target=NiriTarget.WORKSPACES)
        current_windows_state = get_niri_state(target=NiriTarget.WINDOWS)

        self.current_workspaces = self.parse_workspaces(current_workspaces_state)
        current_windows = self.parse_windows(current_windows_state)
        # for window in saved_windows:
        #     for workspace in self.saved_workspaces:
        #         if workspace.id == window.workspace_id:
        #             workspace.windows.append(window)
        #             continue

        # Recreate the old state by modifying the desktop
        self.saved_workspaces.sort(key=(lambda workspace: workspace.index))
        self.current_workspaces.sort(key=(lambda workspace: workspace.index))

        max_index = self.current_workspaces[-1].index

        print("Recreating Workspace layouts")
        for saved_workspace in self.saved_workspaces:
            print(f"Recreating workspace in index {saved_workspace.index}.")
            # If the workspace has a name:
            if saved_workspace.name is not None:
                # Check if there is already a workspace with same name
                found = False
                for current_workspace in self.current_workspaces:
                    if current_workspace.name == saved_workspace.name:
                        print(
                            f"Found workspace with same name {saved_workspace.name}, moving it to index {saved_workspace.index}."
                        )
                        move_workspace_to_index(
                            current_workspace.name, saved_workspace.index
                        )
                        found = True
                        break
                # If not, give the workspace in the current index a name:
                if not found:
                    print(f"Setting workspace name as {saved_workspace.name}")
                    set_workspace_name(saved_workspace.name, saved_workspace.index)

            # Go through all the windows in the workspace
            # Check if there is a window with the same name in any of the current workspaces
            # If there is, put it in the workspace we are going through and jump to next saved window
            print(f"Moving windows to workspace in index {saved_workspace.index}.")
            for saved_window in saved_workspace.windows:
                found = False
                for current_window in current_windows:
                    if (
                        current_window.app_id == saved_window.app_id
                        and current_window.title == saved_window.title
                    ):
                        print(
                            f"Found '{saved_window.title}', moving to workspace at index {saved_workspace.index}"
                        )
                        move_window_to_workspace(
                            current_window.id, saved_workspace.index
                        )
                        found = True
                        break
                if not found:
                    print(f"Window '{saved_window.title}' not found.")

        # Mutta mitenkäs tää nyt sitten tapahtuu?
        # Ruvetaan käymään savedia läpi, yksi workspace kerrallaan, indexistä 1 lähtien.
        # Etsitään currentista löytyykö sieltä sen nimistä workspacea?
        #   Jos löytyy, siirretään indeksiin yks.
        #   Jos ei löydy, luodaan uusi nimetty ws indexiin yksi
        # Käydään savedin workspacen windowit läpi
        #   siirretään kaikki sinne kuuluvat windowit currentista paikalleen
        #   ne mitä ei löydy, all is fine, kirjataan ylös ja printataan lopussa lista niistä jotka ei löytäneet paikalleen
        # Tarviiko currenttia ollenkaan?

    def recreate_state(self):
        pass
        # But how? Mulla on vanha ja uusi. Me halutaan muokata uutta niin, että se on tismalleen samanlainen kuin vanha.
        # Eli aina kun tehdään muutoksia IPC:llä, tehdään sama muutos myös currenttiin, mutta vanhaan ei kosketa koskaan.
        # Se pysyy immutablena. Pitäiskö luoda current kokoajan uusiksi? Sillon näkee oikean tilanteen... ehkä ei tarvii?
        # Mutta mitenkäs tää nyt sitten tapahtuu?
        # Ruvetaan käymään savedia läpi, yksi workspace kerrallaan, indexistä 1 lähtien.
        # Etsitään currentista löytyykö sieltä sen nimistä workspacea?
        #   Jos löytyy, siirretään indeksiin yks.
        #   Jos ei löydy, luodaan uusi nimetty ws indexiin yksi
        # Käydään savedin workspacen windowit läpi
        #   siirretään kaikki sinne kuuluvat windowit currentista paikalleen
        #   ne mitä ei löydy, all is fine, kirjataan ylös ja printataan lopussa lista niistä jotka ei löytäneet paikalleen
        # Tarviiko currenttia ollenkaan?


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
