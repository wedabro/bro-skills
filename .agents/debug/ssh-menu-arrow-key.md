# SSH menu arrow-key investigation

## Symptom

On a VPS accessed over SSH, pressing an arrow key in `bro-skills init` can end
or corrupt the interactive selection flow. The user requested a comma-separated
numeric entry option as a reliable fallback.

## Evidence

- `bro_skills/cli.py:215-277` uses POSIX raw-terminal input and parses an ANSI
  arrow sequence one character at a time, with a 350 ms timeout between bytes.
- A regular SSH terminal is a TTY, so it does not take the existing numeric
  `input()` fallback at `bro_skills/cli.py:94-142`.
- Raw mode only handles one digit at a time (`bro_skills/cli.py:238-249`), so
  it cannot accept comma-separated selections or indexes above 9.

## Hypothesis

SSH latency or packet fragmentation delays bytes in `ESC [ B` / `ESC O B`
sequences past the parser timeout. The menu then consumes an incomplete escape
sequence and leaves the remaining bytes to be treated as ordinary input.

## Proposed resolution

Add an explicit `--menu-mode numeric` (or equivalent) for `init` that bypasses
raw key reading and accepts `1,2,10`; keep the existing interactive menu as the
default for local terminals. Add tests for parsing and the opt-in mode.
