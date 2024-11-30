# TransmissionPy

A CLI build with the Python [`cyclopts`](cyclopts.readthedocs.io/) package.

Manage your Transmission torrents with Python!

## Requirements

- [`uv`](https://docs.astral.sh/uv)
  - This project was built using `uv`.
  - If you install `uv`, you can run this app without worrying about dependencies. Just run `uv run transmissionpy <--args>`
- If you are not using `uv`, create a virtualenv (`virtualenv .venv`), activate it with `. .venv/bin/activate` (Linux/Mac) or `. .venv\Scripts\activate` (Windows), then run `pip install -r requirements.txt`

## Usage

Run `uv run transmissionpy --help` to see help menu.

### Help

*Note: This help menu may be out of date. It's a good idea to run `uv run transmissionpy --help` to see the current args.*

```shell
Usage: transmissionpy_cli COMMAND

CLI for transmissionpy Transmission RPC controller client.

╭─ Session Parameters ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug --no-debug  [default: False]                                                                                                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ torrent    Torrent management commands.                                                                                                                                                                          │
│ --help -h  Display this message and exit.                                                                                                                                                                        │
│ --version  Display application version.                                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
