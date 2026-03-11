# Phase 2: State Management

## Goal
Parse the Niri IPC logs, and using the parsed data recreate a window state.

### Description
To achieve that, we need to be able to save the windows-state JSON to 
.local/share/niri-sessions and also load the data from it. WIth the data
we need to be able to parse the JSON data and move windows using the info
saved in the data object.

**What do I need to know to move the window to the right place?**
I need the ID of the window, but the ID's will probably be whatever, as
they are created dynamically by Niri when spawning a new window. 

So, I need to be able to identify which windows are the same in the saved
state and the new state after reboot.
For that, I have *title*, *app_id* and maybe *pid*, but pid is probably also
dependant on boot-session. But *title* and *app_id* should suffice.

Also, I need the id of the workspace. The workspaces are created dynamically,
so the moving has to be done sequentially. And to restore the session properly
I also need to save the workspace names. The workspaces json has the *name* of
the workspace and also *id* and *idx*. According to Niri IPC docs the *id* is
steady and the *idx* is the index on the monitor, so this is the one I want to
save, as it is the one listening to `niri msg action focus-workspace` and which
tells the actual ordering.

#### Useful Niri IPC commands
- `move-column-to-index --idx idx`
- `focus-column --idx idx`
- `focus-window --id id`
- `focus-window-in-column --idx idx`
- `move-window-to-monitor --id --output` Id of the window to move!
- `set-window-width --id change` ja -height- 
- `move-window-to-workspace --window-id id --focus false <reference>`. Ok, it IS possible to move a window without focus! The reference is the idx or name of the workspace.

## Doing

## To Do (Phase backlog)
- [ ] Create a CLI arg for save and restore
- [ ] Create scripts for moving the window to the correct places

## Done
- [x] Save the windows.state.json and workspaces.state.json to .local/state
- [x] Change the window move to use --focus false and --id
- [x] Learn how to parse JSON in Python
- [x] Experiment with JSON
- [x] Parse focus-window


## Braindump

