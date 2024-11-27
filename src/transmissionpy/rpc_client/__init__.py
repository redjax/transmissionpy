from __future__ import annotations

from . import snapshot, utils
from .methods import (
    delete_torrent,
    delete_torrent_by_transmission_id,
    list_all_torrents,
    list_finished_torrents,
    list_paused_torrents,
    list_stalled_torrents,
    snapshot_torrents,
    start_torrent,
    stop_torrent,
    write_torrent_to_json,delete_oldest_torrents,delete_finished_torrents
)
from .snapshot import SnapshotManager
