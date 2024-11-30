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

def torrents_to_df(torrents: list[TorrentMetadataIn], dtype_mapping: dict = torrent_df_dtypes_mapping, col_rename_mapping: dict | None = None) -> pd.DataFrame:
    try:
        converted_torrents: list[TorrentMetadataIn] = rpc_client.utils.convert_multiple_torrents_to_torrentmetadata(torrents=torrents)
        torrents_df: pd.DataFrame = rpc_client.utils.convert_torrents_to_df(torrents=converted_torrents)
    
        torrents_df = df_utils.convert_df_col_dtypes(df=torrents_df, dtype_mapping=dtype_mapping)
        
        if col_rename_mapping:
            try:
                torrents_df = df_utils.rename_df_cols(df=torrents_df, col_rename_map=col_rename_mapping)
            except Exception as exc:
                msg = f"({type(exc)}) Error renaming columns: {exc}"
                log.error(msg)
                log.warning("Continuing without renaming DataFrame columns.")
        
        return torrents_df

    except Exception as exc:
        msg = f"({type(exc)}) Error creating dataframe from torrent list. Details: {exc}"
        log.error(msg)
        
        raise exc
    
def df_float_to_percent(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy[col_name].apply(lambda x: "{:.2f}%".format(round(x * 100, 2)))
    
    return df_copy


def select_df_cols(df: pd.DataFrame, cols: list[str] | None = None):
    if not cols:
        return df

    df_copy = df.copy()
    df_copy = df_copy[cols]
    
    return df_copy


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


def print_torrent_df(torrent_df: pd.DataFrame, dtype_mapping: dict = torrent_df_dtypes_mapping, rename_columns: t.Mapping[str, str] | None = {"id": "torrentId", "name": "torrent", "isFinished": "finished", "isStalled": "stalled", "addedDate": "date added", "activityDate": "last active", "percentDone": "done", "timeDownloading": "download time"}, status: str = "all", max_print_rows: int = 300, df_preview_rows: int = 5,  show_columns: list[str] = ["id", "name", "isFinished", "isStalled", "addedDate", "activityDate", "downloadedEver", "error", "percentDone", "timeDownloading"]):
    print_df: pd.DataFrame = torrent_df.copy(deep=True)
    
    ## Hide pandas index so transmission ID is less confusing
    print_df = df_utils.hide_df_index(df=print_df)
    
    ## Convert datatypes
    print_df: pd.DataFrame = df_utils.convert_df_col_dtypes(df=print_df, dtype_mapping=dtype_mapping)
    ## Convert secondsDownloading column to timedelta
    print_df["timeDownloading"] = print_df["secondsDownloading"].apply(time_utils.convert_seconds_to_timedelta)
    
    ## Select subset of columns to display
    print_df = select_df_cols(df=print_df, cols=show_columns)
    ## Convert percentDone column to percentage string
    print_df = df_float_to_percent(df=print_df, col_name="percentDone")
    
    ## Rename columns
    print_df.rename(columns=rename_columns, inplace=True)
    
    if status == "all":
        log.info(f"All torrent count: {print_df.shape[0]}")
        log.info("Torrents:")
    else:
        log.info(f"{status.title()} torrent count: {print_df.shape[0]}")
        log.info(f"{status.title()} torrents:")
    
    with pd.option_context("display.max_rows", max_print_rows or 100):
        print(print_df.head(df_preview_rows or 5))
    
    

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
    
    match status.lower():
        case "all":
            torrents = rpc_client.list_all_torrents()
        case "finished":
            torrents = rpc_client.list_finished_torrents()
        case "stalled":
            torrents = rpc_client.list_stalled_torrents()
    
    if torrents is None or len(torrents) == 0:
        log.warning("No torrents found at remote")

        return
    
    torrents_df: pd.DataFrame = torrents_to_df(torrents=torrents)
    
    if isinstance(torrents_df, pd.DataFrame) and torrents_df.empty:
        if status == "all": 
            log.warning("No torrents found at remote")
        else:
            log.warning(f"No {status.title()} torrents found at remote")
        return
    
    ## Display torrents dataframe in CLI
    print_torrent_df(torrent_df=torrents_df, status=status, max_print_rows=limit, df_preview_rows=preview)
    
    return torrents_df

@torrent_app.command(name=["rm", "remove"])
def remove_torrent(torrent_id: t.Annotated[int, Parameter(name=["--id"])] | None = None, status: t.Annotated[str, Parameter(name=["-s", "--status"])] | None = None):
    """Remove a torrent, or multiple torrents by state.
    
    Params:
        torrent_id (int): ID of torrent to remove.
        status (str): State of torrents to remove. Options: ["all", "finished", "stalled"]
    """
    if torrent_id:
        try:
            rm_torrent = rpc_client.get_torrent_by_id(torrent_id=torrent_id)
            log.debug(f"Found torrent: {rm_torrent.name}")
        except Exception as exc:
            msg = f"({type(exc)}) Error getting torrent by ID '{torrent_id}'. Details: {exc}"
            log.error(msg)
            
            return
        
        log.info(f"Deleting torrent: {rm_torrent.name}")
        try:
            rpc_client.delete_torrent_by_transmission_id(torrent_id=torrent_id)
            log.success(f"Deleted torrent [id: {torrent_id}]: {rm_torrent.name}")
        except Exception as exc:
            msg = f"({type(exc)} Error deleting torrent '{rm_torrent.name}'. Details: {exc})"
            log.error(msg)
            
            raise exc
        
    if status:
        log.info(f"Getting list of {status.title()} torrents...")
        
        match status.lower():
            case "all":
                torrents = rpc_client.list_all_torrents()
            case "finished":
                torrents = rpc_client.list_finished_torrents()
            case "stalled":
                torrents = rpc_client.list_stalled_torrents()

        if torrents is None or len(torrents) == 0:
            log.warning("No torrents found at remote")
            return
        
        for torrent in torrents:
            log.info(f"Deleting torrent: {torrent.name}")
            try:
                rpc_client.delete_torrents_by_transmission_id(torrent_ids=torrent.id)
                log.success(f"Deleted torrent [id: {torrent.id}]: {torrent.name}")
            except Exception as exc:
                msg = f"({type(exc)} Error deleting torrent '{torrent.name}'. Details: {exc})"
                log.error(msg)
                
                raise exc
