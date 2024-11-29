from cyclopts import App, Group, Parameter
import typing as t
import sys

from loguru import logger as log

from .torrent import torrent_app

app = App(name="transmissionpy_cli", help="CLI for transmissionpy Transmission RPC controller client.")

app.meta.group_parameters = Group("Session Parameters", sort_key=0)

## Mount torrent app
app.command(torrent_app)

@app.meta.default
def cli_launcher(*tokens: t.Annotated[str, Parameter(show=False, allow_leading_hyphen=True, help="Enable debug logging")], debug: bool = False):
    log.remove(0)
    
    if debug:
        log.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | {name}.{function}:{line} | > {message}", level="DEBUG")
    else:
        log.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} [{level}] : {message}", level="INFO")
        
    log.debug("START transmissionpy CLI")
    
    app(tokens)
    

if __name__ == "__main__":
    app()
