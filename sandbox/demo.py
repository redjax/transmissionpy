from __future__ import annotations

import json
import random
import time

from transmissionpy import rpc_client
from transmissionpy.core import setup, transmission_lib
from transmissionpy.core.constants import (
    DATA_DIR,
    JSON_OUTPUT_DIR,
    OUTPUT_DIR,
    PQ_OUTPUT_DIR,
    CSV_OUTPUT_DIR
)
from transmissionpy.core.settings import LOGGING_SETTINGS
from transmissionpy.core.utils import df_utils, path_utils
from transmissionpy.domain.Transmission import (
    TORRENT_INT_DATETIME_FIELDNAMES,
    TorrentMetadataIn,
    TorrentMetadataOut,
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
    # df = pd.DataFrame(torrent_dicts)
    df = rpc_client.utils.convert_torrents_to_df(torrents=torrents)
    
    # print(f"{title} DataFrame:\n{df.head(5)}")
    
    if clean_filename:
        log.info(f"Cleaning filename: '{title}'")
        # title = title.lower().replace(" ", "_").replace(":", "-")
        title = path_utils.sanitize_filename(filename=title).lower()
        log.info(f"Cleaned filenname: '{title}'")
    
    log.info(f"Saving dataframe '{title}'to parquet, json and csv files...")
    df_utils.save_pq(df=df, pq_file=f"{PQ_OUTPUT_DIR}/{title}.parquet")
    df_utils.save_json(df=df, json_file=f"{JSON_OUTPUT_DIR}/{title}.json", indent=4)
    df_utils.save_csv(df=df, csv_file=f"{CSV_OUTPUT_DIR}/{title}.csv")
    
    return df



def demo():
    all_torrents = demo_all_torrents()
    paused_torrents = demo_paused_torrents()
    stalled_torrents = demo_stalled_torrents()
    finished_torrents = demo_finished_torrents()
    
    random_torrent = rpc_client.utils.select_random_torrent(torrents_list=all_torrents)
    random_torrent_metadata = rpc_client.utils.convert_torrent_to_torrentmetadata(torrent=random_torrent)
    
    # demo_pause_torrent(torrent=random_torrent)
    
    log.info("Convering combined all, paused, stalled, and finished torrents to dataframe")
    all_torrents_df = demo_convert_to_df(torrents=all_torrents, title="All Torrents")
    paused_torrents_df = demo_convert_to_df(torrents=paused_torrents, title="Paused Torrents")
    stalled_torrents_df = demo_convert_to_df(torrents=stalled_torrents, title="Stalled Torrents")
    finished_torrents_df = demo_convert_to_df(torrents=finished_torrents, title="Finished Torrents")
    
    log.debug(f"'All Torrents' columns: {all_torrents_df.columns.tolist()}")
    
    torrents_by_seconds_downloading_df = df_utils.sort_df_by_col(df=all_torrents_df, col_name="secondsDownloading", order="desc")
    
    log.info("Converting datetime fields currently represented as integers to datetimes")
    ## Convert column dtypes
    torrent_df_mapping = {"activityDate": "datetime64[s]", "addedDate": "datetime64[s]", "dateCreated": "datetime64[s]", "doneDate": "datetime64[s]", "editDate": "datetime64[s]", "startDate": "datetime64[s]"}
    torrents_by_seconds_downloading_df = df_utils.convert_df_col_dtypes(df=torrents_by_seconds_downloading_df, dtype_mapping=torrent_df_mapping)

    log.info(f"Top 5 longest downloading torrents:\n{torrents_by_seconds_downloading_df[['name', 'secondsDownloading', 'addedDate', 'startDate', 'activityDate', 'error']].head(5)}")



def main():
    demo()


if __name__ == "__main__":
    setup.setup_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    setup.create_app_paths()
    df_utils.set_pandas_display_opts()
    
    log.debug(f"Transmission settings: {transmission_lib.transmission_settings}")
    
    main()
