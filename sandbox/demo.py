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


def demo_convert_to_metadata(torrent: Torrent):
    torrent_metadata = rpc_client.utils.convert_torrent_to_torrentmetadata(torrent=torrent)
    log.debug(f"Torrent metadata: {torrent_metadata}")
    
    return torrent_metadata
    
def demo():
    all_torrents = demo_all_torrents()
    paused_torrents = demo_paused_torrents()
    stalled_torrents = demo_stalled_torrents()
    
    random_torrent = rpc_client.utils.select_random_torrent(torrents_list=all_torrents)
    random_torrent_metadata = rpc_client.utils.convert_torrent_to_torrentmetadata(torrent=random_torrent)
        

def main():
    demo()
    
    # all_torrents = rpc_client.list_all_torrents()
    # if all_torrents is None or len(all_torrents) == 0:
    #     log.warning("List of torrents is empty")
    # else:
    #     rand_index = random.randint(0, len(all_torrents) - 1)
    #     random_torrent = all_torrents[rand_index]
        
    # # debug_torrent(torrent=random_torrent)
    # rand_torrent_metadata = rpc_client.utils.convert_torrent_to_torrentmetadata(torrent=random_torrent)
    # log.debug(f"Converted torrent '{rand_torrent_metadata.name}' to TorrentMetadata object")
    
    # all_torrent_metadata = rpc_client.utils.convert_multiple_torrents_to_torrentmetadata(torrents=all_torrents)
    # log.debug(f"Converted [{len(all_torrent_metadata)}] torrent(s) to TorrentMetadata objects")    


if __name__ == "__main__":
    setup.setup_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    df_utils.set_pandas_display_opts()
    
    log.debug(f"Transmission settings: {transmission_lib.transmission_settings}")
    
    main()
    
    
    
    
    
    # demo_torrent = all_torrents[1]
    # demo_torrent_filename = demo_torrent.name.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(" ","_")
    # with open("ex_torrent.json", "w") as f:
    #     data = json.dumps(demo_torrent.__dict__, indent=4)
    #     f.write(data)
    
    # try:
    #     transmission_controller = transmission_lib.get_transmission_controller(transmission_settings=transmission_lib.transmission_settings)
    # except Exception as exc:
    #     msg = f"({type(exc)}) Error getting TransmissionRPCContro"
        
    # with transmission_controller as torrent_ctl:
    #     log.info("Getting all torrents from remote")
    #     try:
    #         torrents = torrent_ctl.get_all_torrents()
    #     except Exception as exc:
    #         msg = f"({type(exc)}) Error getting torrents from remote. Details: {exc}"
    #         log.error(msg)
            
    #         raise exc

    #     print(f"Retrieved [{len(torrents)}] from remote {torrent_ctl.host}")
        
    # torrent_dicts: list[dict] = []
    
    # for t in torrents:
    #     t_dict = {
    #         "name": t.name,
    #         "status": t.status,
    #         "added": t.added_date,
    #         "last_active": t.activity_date,
    #         "downloading": t.downloading,
    #         "done": True if t.done_date else False,
    #         "done_date": t.done_date,
    #         "percent_downloaded": t.progress,
    #         "total_size": t.total_size,
    #         "ratio": t.ratio,
    #         "seconds_downloading": t.seconds_downloading,
    #         "seconds_seeding": t.seconds_seeding
    #     }
    #     torrent_dicts.append(t_dict)
        
    # done_torrent_dicts = [d for d in torrent_dicts if d["done"]]
    # log.info(f"Found [{len(torrent_dicts)}] torrent(s), [{len(done_torrent_dicts)}] of which are finished downloading.")
        
    # torrent_df = pd.DataFrame(torrent_dicts)
    # print(f"\nAll torrents (first 5 of {torrent_df.shape[0]}):")
    # print(torrent_df.head(5))
    
    # done_torrent_df = pd.DataFrame(done_torrent_dicts)
    # print(f"\nFinished torrents (first 5 of {done_torrent_df.shape[0]}): ")
    # print(done_torrent_df)
    
    # done_torrents = torrent_df.loc[torrent_df["done"] == True]  # noqa: E712
    # print(done_torrents.head(5))
    
        
#         print("First 5 torrents:")
#         for t in torrents[0:5]:
#             print(f"""Torrent: {t.name}
# Status: {t.status}
# Added: {t.added_date}
# Last Active: {t.activity_date}                  
# Downloading: {t.downloading}
# Done: {True if t.done_date else False}
# Done Date: {'NA' if not t.done_date else t.done_date}
# Percent Downloaded: {t.progress}%
# Trackers: {len(t.trackers)}
# Total Size: {t.total_size} bytes
# Ratio: {t.ratio}
# Time spent downloading: {t.seconds_downloading} seconds
# """)
        
#         done_torrents = [t for t in torrents if t.done_date]
        
#         print(f"Found [{len(done_torrents)}] finished torrent(s)")
#         if len(done_torrents) > 0:
#             print("First 5 done torrents:")
#             for t in done_torrents[0:5]:
#                 print(f"""Torrent: {t.name}
# Added: {t.added_date}
# Last Active: {t.activity_date}                  
# Downloading: {t.downloading}
# Done: {True if t.done_date else False}
# Done Date: {'NA' if not t.done_date else t.done_date}
# Percent Downloaded: {t.percent_done}%
# """)

#             partially_downloaded_torrents = [t for t in torrents if t.percent_done > 0.0]
#             print(f"Found [{len(partially_downloaded_torrents)}] partially downloaded torrent(s)")
#             if partially_downloaded_torrents:
#                 print("First 5 partially downloaded torrents:")
#                 for t in partially_downloaded_torrents[0:5]:
#                     print(f"""Torrent: {t.name}
# Added: {t.added_date}
# Last Active: {t.activity_date}                  
# Downloading: {t.downloading}
# Done: {True if t.done_date else False}
# Done Date: {'NA' if not t.done_date else t.done_date}
# Percent Downloaded: {t.percent_done}%
# """)