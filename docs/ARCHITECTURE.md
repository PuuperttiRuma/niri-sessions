# ARCHITECTURE

## Technology

### Language

**Decision (11.3.2026):** Python will be used for the application logic.

*Reasoning:*
- Niri IPC exports window state as JSON and Python has ergonomic JSON-parsing compared to BASH
- Python handles shell commands through `subprocess`

*Alternatives considered:*
- Bash: Rejected due to JSON parsing considerations.
- Go: Faster and easier distribution, but I don't yet handle it. Version 2 of this will be in Go (or Rust)

### State save folder

**Decision (11.3.2026)**: The app will use ~/.local/state/niri-sessions folder save the state of the windows.

*Reasoning*: The .local/state is the linux default for saving application state.
