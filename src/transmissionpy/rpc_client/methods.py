from loguru import logger as log

import typing as t

from transmissionpy.core import transmission_lib
from transmissionpy.core.utils import df_utils
from transmissionpy.core.transmission_lib import transmission_settings, TransmissionClientSettings, TransmissionRPCController

from transmission_rpc import Torrent

def list_all_torrents(transmission_settings: TransmissionClientSettings = transmission_settings):
    try:
        transmission_controller: TransmissionRPCController = transmission_lib.get_transmission_controller(transmission_settings=transmission_settings)
    except Exception as exc:
        msg = f"({type(exc)}) Error getting TransmissionRPCController. Details: {exc}"
        log.error(msg)
        
        raise exc
    
    try:
        with transmission_controller as torrent_ctl:
            all_torrents: list[Torrent] = torrent_ctl.get_all_torrents()
            
        return all_torrents
    except Exception as exc:
        msg = f"({type(exc)}) Error getting all torrents. Details: {exc}"
        log.error(msg)
        
        return []

def list_finished_torrents():
    pass

def list_paused_torrents():
    pass