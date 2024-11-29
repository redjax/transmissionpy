from __future__ import annotations

import json
import random
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    torrent_df_dtypes_mapping,
)

from loguru import logger as log
import pandas as pd
from transmission_rpc import Torrent

from methods import demo_delete_finished,demo_all_torrents,demo_convert_to_df,demo_convert_to_metadata,demo_delete_oldest,demo_finished_torrents,demo_pause_torrent,demo_paused_torrents,demo_stalled_torrents


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
    torrent_df_dtypes_mapping = {"activityDate": "datetime64[s]", "addedDate": "datetime64[s]", "dateCreated": "datetime64[s]", "doneDate": "datetime64[s]", "editDate": "datetime64[s]", "startDate": "datetime64[s]"}
    
    all_torrents_df = df_utils.convert_df_col_dtypes(df=all_torrents_df, dtype_mapping=torrent_df_dtypes_mapping)
    ## Convert column dtypes
    torrents_by_seconds_downloading_df = df_utils.convert_df_col_dtypes(df=torrents_by_seconds_downloading_df, dtype_mapping=torrent_df_dtypes_mapping)

    log.info(f"Top 5 longest downloading torrents:\n{torrents_by_seconds_downloading_df[['name', 'secondsDownloading', 'addedDate', 'startDate', 'activityDate', 'error']].head(5)}")


def main(run_delete: bool = False):
    # demo()
    # rpc_client.snapshot_torrents()
    
    if run_delete:
        log.warning("Deleting oldest Torrent")
        # demo_delete_oldest()
        demo_delete_finished()


if __name__ == "__main__":
    setup.setup_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    setup.create_app_paths()
    df_utils.set_pandas_display_opts()
    
    # log.debug(f"Transmission settings: {transmission_lib.transmission_settings}")
    
    RUN_DELETE_DEMO = True

    main(run_delete=RUN_DELETE_DEMO)
