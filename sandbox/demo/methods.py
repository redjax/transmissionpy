import json
import random
import time

from transmissionpy import rpc_client
from transmissionpy.core import setup, transmission_lib
from transmissionpy.core.constants import (
    CSV_OUTPUT_DIR,
    DATA_DIR,
    JSON_OUTPUT_DIR,
    OUTPUT_DIR,
    PQ_OUTPUT_DIR,
    SNAPSHOT_DIR,
)
from transmissionpy.core.settings import LOGGING_SETTINGS
from transmissionpy.core.utils import df_utils, path_utils
from transmissionpy.domain.Transmission import (
    TORRENT_INT_DATETIME_FIELDNAMES,
    TorrentMetadataIn,
    TorrentMetadataOut,
    torrent_df_mapping,
)

from loguru import logger as log
import pandas as pd
from transmission_rpc import Torrent

def demo_all_torrents():
    all_torrents = rpc_client.list_all_torrents()
    log.info(f"Found [{len(all_torrents)}] torrent(s)")
    
    return all_torrents
    

def demo_paused_torrents():
    paused_torrents = rpc_client.list_paused_torrents()
    log.info(f"Found[{len(paused_torrents)}] paused torrent(s)")
    
    return paused_torrents


def demo_stalled_torrents():
    stalled_torrents= rpc_client.list_stalled_torrents()
    log.info(f"Found[{len(stalled_torrents)}] stalled torrent(s)")
    
    return stalled_torrents


def demo_finished_torrents():
    finished_torrents = rpc_client.list_finished_torrents()
    log.info(f"Found[{len(finished_torrents)}] finished torrent(s)")
    
    return finished_torrents


def demo_convert_to_metadata(torrent: Torrent):
    torrent_metadata = rpc_client.utils.convert_torrent_to_torrentmetadata(torrent=torrent)
    log.debug(f"Torrent metadata: {torrent_metadata}")
    
    return torrent_metadata


def demo_pause_torrent(torrent: Torrent):
    log.info(f"Pausing torrent '{torrent.name}'")
    rpc_client.stop_torrent(torrent=torrent)
    
    print("Sleeping 5 seconds, go check your Transmission client...")
    time.sleep(5)
    
    log.info(f"Unpausing torrent '{torrent.name}'")
    rpc_client.start_torrent(torrent=torrent)
    

def demo_convert_to_df(torrents: list[Torrent], title: str = "Unnamed Dataframe", clean_filename: bool = True) -> pd.DataFrame:
    torrent_dicts = [t.__dict__["fields"] for t in torrents]
    df = rpc_client.utils.convert_torrents_to_df(torrents=torrents)
    
    if clean_filename:
        log.info(f"Cleaning filename: '{title}'")
        title = path_utils.sanitize_filename(filename=title).lower()
        log.info(f"Cleaned filenname: '{title}'")
    
    log.info(f"Saving dataframe '{title}'to parquet, json and csv files...")
    df_utils.save_pq(df=df, pq_file=f"{PQ_OUTPUT_DIR}/{title}.parquet")
    df_utils.save_json(df=df, json_file=f"{JSON_OUTPUT_DIR}/{title}.json", indent=4)
    df_utils.save_csv(df=df, csv_file=f"{CSV_OUTPUT_DIR}/{title}.csv")
    
    return df

def demo_delete_oldest():
    deleted_torrents = rpc_client.delete_oldest_torrents(delete_count=2)
    
    return deleted_torrents

def demo_delete_finished():
    deleted_torrents = rpc_client.delete_finished_torrents()
    
    return deleted_torrents
