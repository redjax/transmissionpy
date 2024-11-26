from __future__ import annotations

from . import utils, snapshot

from .methods import (
    list_all_torrents,
    list_finished_torrents,
    list_paused_torrents,
    list_stalled_torrents,
    start_torrent,
    stop_torrent,
    write_torrent_to_json,
    snapshot_torrents, delete_torrent, delete_torrent_by_transmission_id
)
from .snapshot import SnapshotManager
