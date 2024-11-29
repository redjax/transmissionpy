from __future__ import annotations

from datetime import timedelta
import typing as t

from transmissionpy import rpc_client
from transmissionpy.core.utils import df_utils, time_utils
from transmissionpy.domain.Transmission import (
    TorrentMetadataIn,
    torrent_df_dtypes_mapping,
)

from cyclopts import App, Group, Parameter, validators
from loguru import logger as log
import pandas as pd

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
def list_torrents(status: t.Annotated[str, Parameter(name="status", show_default=True)] = "all", preview: t.Annotated[int, Parameter(name=["-p", "--preview"])] = 5, limit: t.Annotated[int, Parameter(name=["-l", "--limit"])] = 300):
    """List torrents by status.
    
    Params:
        status (str): Status of torrents to list. Options: ["all", "finished", "stalled"].
        preview (int): Number of torrents to preview. 0=all results (output will be slow with many results, and may push parts out of the terminal history).
        limit (int): Max number of DataFrame rows to print when displaying in CLI. 0=unlimited (output will be slow with many results, and may push parts out of the terminal history).
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
    # torrents_df = df_utils.convert_df_datetimes_to_timestamp(df=torrents_df)
    torrents_df: pd.DataFrame = df_utils.convert_df_col_dtypes(df=torrents_df, dtype_mapping=torrent_df_dtypes_mapping)
    
    ## Convert secondsDownloading column to timedelta
    torrents_df["timeDownloading"] = torrents_df["secondsDownloading"].apply(time_utils.convert_seconds_to_timedelta)
    
    if isinstance(torrents_df, pd.DataFrame) and torrents_df.empty:
        if status == "all": 
            log.warning("No torrents found at remote")
        else:
            log.warning(f"No {status.title()} torrents found at remote")
        return
    
    print_df: pd.DataFrame = torrents_df[["id", "name", "isFinished", "isStalled", "addedDate", "activityDate", "downloadedEver", "error", "percentDone", "timeDownloading"]]
    ## Convert percentDone column to string for displaying to user
    print_df["percentDone"] = print_df["percentDone"].apply(lambda x: "{:.2f}%".format(round(x * 100, 2)))
    
    if status == "all":
        log.info(f"All torrent count: {print_df.shape[0]}")
        log.info("Torrents:")
    else:
        log.info(f"{status.title()} torrent count: {print_df.shape[0]}")
        log.info(f"{status.title()} torrents:")
        
    print_df = print_df.rename(columns={"id": "torrentId"})
    ## Hide pandas index so transmission ID is less confusing
    print_df = df_utils.hide_df_index(df=print_df)
    
    # with pd.option_context("display.max_columns", 50):
        ## Hide pandas index so transmission ID is less confusing
        # print(print_df.head(preview).to_string(index=False))
    with pd.option_context("display.max_rows", limit):
        print(print_df.head(preview))
    
    # return torrents_df
    

# @torrent_app.command(name="")