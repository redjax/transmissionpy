from transmissionpy.core import transmission_lib
from transmissionpy.core.utils import df_utils
from transmissionpy.core import setup
from transmissionpy.core.settings import LOGGING_SETTINGS
from transmissionpy import rpc_client
import pandas as pd
import json
from transmission_rpc import Torrent
import random
from transmissionpy.domain.Transmission import TorrentMetadataIn, TorrentMetadataOut
import time
from transmissionpy.core.constants import DATA_DIR, OUTPUT_DIR, PQ_OUTPUT_DIR, JSON_OUTPUT_DIR

from loguru import logger as log

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
    

def demo_convert_to_df(torrents: list[Torrent], title: str = "Unnamed Dataframe") -> pd.DataFrame:
    torrent_dicts = [t.__dict__["fields"] for t in torrents]
    # df = pd.DataFrame(torrent_dicts)
    df = rpc_client.utils.convert_torrents_to_df(torrents=torrents)
    
    # print(f"{title} DataFrame:\n{df.head(5)}")
    
    log.info(f"Saving dataframe '{title}'to parquet, json and csv files...")
    df_utils.df_to_parquet(df=df, parquet_output=f"{PQ_OUTPUT_DIR}/{title}.parquet")
    df_utils.df_to_json(df=df, json_output=f"{JSON_OUTPUT_DIR}/{title}.json")
    df_utils.df_to_csv(df=df, csv_output=f"{OUTPUT_DIR}/{title}.csv")



def demo():
    all_torrents = demo_all_torrents()
    paused_torrents = demo_paused_torrents()
    stalled_torrents = demo_stalled_torrents()
    finished_torrents = demo_finished_torrents()
    
    random_torrent = rpc_client.utils.select_random_torrent(torrents_list=all_torrents)
    random_torrent_metadata = rpc_client.utils.convert_torrent_to_torrentmetadata(torrent=random_torrent)
    
    # demo_pause_torrent(torrent=random_torrent)
    
    log.info("Convering combined all, paused, stalled, and finished torrents to dataframe")
    demo_convert_to_df(torrents=all_torrents, title="All Torrents")
    demo_convert_to_df(torrents=paused_torrents, title="Paused Torrents")
    demo_convert_to_df(torrents=stalled_torrents, title="Stalled Torrents")
    demo_convert_to_df(torrents=finished_torrents, title="Finished Torrents")


def main():
    demo()


if __name__ == "__main__":
    setup.setup_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    setup.create_app_paths()
    df_utils.set_pandas_display_opts()
    
    log.debug(f"Transmission settings: {transmission_lib.transmission_settings}")
    
    main()
