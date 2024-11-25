from __future__ import annotations

import random
import typing as t

from transmissionpy.core.utils import list_utils
from transmissionpy.domain.Transmission import TorrentMetadataIn, TorrentMetadataOut

from loguru import logger as log
from transmission_rpc import Torrent

def convert_torrent_to_torrentmetadata(torrent: Torrent):
    if torrent is None:
        raise ValueError("Missing transmission_rpc.Torrent object")
    if not isinstance(torrent, Torrent):
        raise TypeError(f"Invalid type for torrent: ({type(torrent)}). Must be of type transmission_rpc.Torrent")

    try:
        torrent_metadata = TorrentMetadataIn.model_validate(torrent.__dict__["fields"])
        return torrent_metadata
    except Exception as exc:
        msg = f"({type(exc)}) Error validating torrent metadata. Details: {exc}"
        log.error(msg)
        
        raise exc


def convert_multiple_torrents_to_torrentmetadata(torrents: list[Torrent]) -> list[TorrentMetadataIn]:
    if torrents is None or (isinstance(torrents, list) and len(torrents) == 0):
        raise ValueError("torrents list must not be empty")
    if not isinstance(torrents, list):
        raise TypeError(f"Invalid type for torrents: ({type(torrents)}). Must be a list of transmission_rpc.Torrent objects")
    
    torrents_out: list[TorrentMetadataIn] = []
    
    for t in torrents:
        _t: TorrentMetadataIn = convert_torrent_to_torrentmetadata(torrent=t)
        torrents_out.append(_t)
        
    return torrents_out


def select_random_torrent(torrents_list: list[t.Union[Torrent, TorrentMetadataIn, TorrentMetadataOut]]) -> t.Union[Torrent, TorrentMetadataIn, TorrentMetadataOut]:
    if torrents_list is None or (isinstance(torrents_list, list) and len(torrents_list) == 0):
        raise ValueError("torrents list must not be empty")
    if not isinstance(torrents_list, list):
        raise TypeError(f"Invalid type for torrents: ({type(torrents_list)}). Must be a list of transmission_rpc.Torrent objects")
    
    random_torrent = list_utils.get_random_item(torrents_list)
    
    return random_torrent
