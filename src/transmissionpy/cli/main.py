from __future__ import annotations

import sys
import typing as t

from transmissionpy.core.utils import df_utils

from .torrent import torrent_app

from cyclopts import App, Group, Parameter
from loguru import logger as log
import pandas as pd

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
    
#     max_rows=100
#     max_columns=10
#     max_colwidth=10
#     max_width=None

#     log.debug(f"""Setting Pandas options:
# max_rows: {max_rows}
# max_columns: {max_columns}
# max_colwidth: {max_colwidth}
# max_width: {max_width}
# """)
    
    ## Set Pandas display options
    # pd.set_option("display.max_rows", 300)
    # pd.set_option("display.max_columns", 5)
    # pd.set_option("display.max_colwidth", 20)
    
    app(tokens)
    

if __name__ == "__main__":
    app()
