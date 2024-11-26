from __future__ import annotations

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

def demo_delete_oldest():
    all_torrents = rpc_client.snapshot_torrents()
    all_torrents_df = demo_convert_to_df(torrents=all_torrents, title="All Torrents")
    
    sorted_df = all_torrents_df.sort_values(by=["addedDate", "startDate", "secondsDownloading"], ascending=[True, True, False])
    sorted_df = df_utils.convert_df_col_dtypes(df=sorted_df, dtype_mapping=torrent_df_mapping)
    
    log.debug(f"Sorted all_torrents_df:\n{sorted_df[['id', 'name', 'isStalled', 'isFinished', 'addedDate', 'startDate', 'secondsDownloading']]}")
    
    sorted_df = df_utils.convert_df_datetimes_to_timestamp(df=sorted_df)
    ## Find the oldest stalled torrent and delete
    for index, row in sorted_df.iterrows():
        if row["isStalled"] and not row["isFinished"]:
            torrent_id = row["id"]
            log.info(f"Deleting oldest stalled torrent: [id:{row['id']}] {row['name']}")
            
            try:
                rpc_client.delete_torrent_by_transmission_id(torrent_id=torrent_id, remove_files=True)
            
                deleted_snapshot = rpc_client.SnapshotManager(snapshot_filename="deleted_torrents_snapshot")
                deleted_snapshot.save_snapshot(torrents=[row.to_dict()])
            
                deleted_row = row
                
                break
            
            except Exception as exc:
                msg = f"({type(exc)}) Error deleting torrent ID '{torrent_id}'. Details: {exc}"
                log.error(msg)
                
                raise exc
            
        
        else:
            log.debug(f"Torrent [id:{row['id']}] {row['name']} is not stalled, finding next...")
            continue
        
    log.info(f"Deleted torrent:\n{deleted_row[['id', 'name', 'isStalled', 'isFinished', 'addedDate', 'startDate', 'secondsDownloading', 'percentDone']]}")

def demo():
    all_torrents = demo_all_torrents()
    paused_torrents = demo_paused_torrents()
    stalled_torrents = demo_stalled_torrents()
    finished_torrents = demo_finished_torrents()
    
    rpc_client.snapshot_torrents()
    
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
    torrent_df_mapping = {"activityDate": "datetime64[s]", "addedDate": "datetime64[s]", "dateCreated": "datetime64[s]", "doneDate": "datetime64[s]", "editDate": "datetime64[s]", "startDate": "datetime64[s]"}
    
    all_torrents_df = df_utils.convert_df_col_dtypes(df=all_torrents_df, dtype_mapping=torrent_df_mapping)
    ## Convert column dtypes
    torrents_by_seconds_downloading_df = df_utils.convert_df_col_dtypes(df=torrents_by_seconds_downloading_df, dtype_mapping=torrent_df_mapping)

    log.info(f"Top 5 longest downloading torrents:\n{torrents_by_seconds_downloading_df[['name', 'secondsDownloading', 'addedDate', 'startDate', 'activityDate', 'error']].head(5)}")


def main(run_delete: bool = False):
    # demo()
    # rpc_client.snapshot_torrents()
    
    if run_delete:
        log.warning("Deleting oldest Torrent")
        demo_delete_oldest()


if __name__ == "__main__":
    setup.setup_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    setup.create_app_paths()
    df_utils.set_pandas_display_opts()
    
    # log.debug(f"Transmission settings: {transmission_lib.transmission_settings}")
    
    RUN_DELETE_DEMO = False

    main(run_delete=RUN_DELETE_DEMO)
