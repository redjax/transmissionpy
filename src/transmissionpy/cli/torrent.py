from loguru import logger as log
import typing as t

from cyclopts import App, Parameter, Group, validators

from transmissionpy import rpc_client


torrent_app = App(name="torrent", help="Torrent management commands.")

@torrent_app.command(name="count")
def count_torrents(status: t.Annotated[str, Parameter(name="status", show_default=True)] = "all"):
    """Count torrents by status.
    
    Params:
        status (str): Status of torrents to count. default: 'all'. Options: ["all", "finished", "stalled"]
    """    
    if status not in ["all", "finished", "stalled"]:
        raise ValueError(f"Invalid status: {status}. Must be one of ['all', 'finished', 'stalled']")

    log.info(f"Counting {status} torrents...")
    
    match status:
        case "all":
            count = len(rpc_client.list_all_torrents()) or 0
        case "finished":
            count = len(rpc_client.list_finished_torrents()) or 0
        case "stalled":
            count = len(rpc_client.list_stalled_torrents()) or 0
    
    if status == "all":
        log.info(f"Found {count} torrent(s)")
    else:
        log.info(f"Found {count} {status} torrent(s)")
