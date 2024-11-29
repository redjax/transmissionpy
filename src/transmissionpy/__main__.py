from __future__ import annotations

from transmissionpy.cli import app as cli_app

from cyclopts import App
from loguru import logger as log

def start_cli():
    try:
        cli_app.meta()
    except Exception as exc:
        msg = f"({type(exc)}) Error starting CLI. Details: {exc}"
        log.error(msg)
        
        raise exc
    

if __name__ == "__main__":
    start_cli()
