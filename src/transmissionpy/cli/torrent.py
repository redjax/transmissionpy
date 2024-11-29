from loguru import logger as log
import typing as t

from cyclopts import App, Parameter, Group, validators
import pandas as pd
from transmissionpy import rpc_client
from transmissionpy.domain.Transmission import TorrentMetadataIn
from transmissionpy.core.utils import df_utils


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


@torrent_app.command(name="list")
def list_torrents(status: t.Annotated[str, Parameter(name="status", show_default=True)] = "all", preview: t.Annotated[int, Parameter(name=["-p", "--preview"])] = 5):
    """List torrents by status.
    
    Params:
        status (str): Status of torrents to list. Options: ["all", "finished", "stalled"].
        preview (int): Number of torrents to preview. 0=all results (output will be slow with many results, and may push parts out of the terminal history).
    """    
    if status not in ["all", "finished", "stalled"]:
        raise ValueError(f"Invalid status: {status}. Must be one of ['all', 'finished', 'stalled']")

    log.info(f"Listing {status.title()} torrents...")
    
    match status:
        case "all":
            torrents = rpc_client.list_all_torrents()
        case "finished":
            torrents = rpc_client.list_finished_torrents()
        case "stalled":
            torrents = rpc_client.list_stalled_torrents()
    
    if torrents is None or len(torrents) == 0:
        log.warning("No torrents found at remote")

        return
    
    converted_torrents: list[TorrentMetadataIn] = rpc_client.utils.convert_multiple_torrents_to_torrentmetadata(torrents=torrents)
    torrents_df: pd.DataFrame = rpc_client.utils.convert_torrents_to_df(torrents=converted_torrents)
    torrents_df = df_utils.convert_df_datetimes_to_timestamp(df=torrents_df)
    
    if isinstance(torrents_df, pd.DataFrame) and torrents_df.empty:
        if status == "all": 
            log.warning("No torrents found at remote")
        else:
            log.warning(f"No {status.title()} torrents found at remote")
        return
    
    print_df  = torrents_df[["name", "isFinished", "isStalled", "addedDate", "activityDate", "downloadedEver", "error", "eta", "percentDone", "secondsDownloading"]]
    
    if status == "all":
        log.info(f"All torrent count: {print_df.shape[0]}")
        log.info("Torrents:")
    else:
        log.info(f"{status.title()} torrent count: {print_df.shape[0]}")
        log.info(f"{status.title()} torrents:")
        
    print(print_df.head(preview))
    
    # return torrents_df