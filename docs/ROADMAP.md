# ROADMAP

## MVP
Save firefox window positions and workspace layout at shutdown and restore it on reboot. 

### Phase 1: IPC
Get stuff moving with Python using Niri IPC.

./phase_1_tasks.md

### Phase 2: State Management
Parse the Niri IPC logs, and using the parsed data recreate a window state.

./phase_2_tasks.md

### Phase 3: Automation
Hook the saving to shutdown and to Firefox launch.

## Future Ideas
- Save and restore entire workspaces manually with a launcher like rofi/wofi/fuzzel
