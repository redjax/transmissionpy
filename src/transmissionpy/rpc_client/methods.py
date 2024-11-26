from __future__ import annotations

import json
import typing as t

from transmissionpy.core import transmission_lib
from transmissionpy.core.transmission_lib import (
    TransmissionClientSettings,
    TransmissionRPCController,
    transmission_settings,
)
from transmissionpy.core.utils import df_utils, hash_utils
from transmissionpy.domain.Transmission import TorrentMetadataIn, TorrentMetadataOut
from .snapshot import SnapshotManager

from loguru import logger as log
from transmission_rpc import Torrent

def write_torrent_to_json(torrent: Torrent, output: str):
    if torrent is None:
        raise ValueError("Missing a transmission_rpc.Torrent object")
    if output is None:
        output: str = f"{hash_utils.get_hash_from_str(input_str=torrent.name)}.json"

    data = json.dumps(torrent.__dict__, indent=4)

    try:
        with open(output, "w") as f:
            f.write(data)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving torrent '{torrent.name}'. Details: {exc}"
        log.error(msg)

        raise exc


def list_all_torrents(
    transmission_settings: TransmissionClientSettings = transmission_settings,
):
    try:
        transmission_controller: TransmissionRPCController = (
            transmission_lib.get_transmission_controller(
                transmission_settings=transmission_settings
            )
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting TransmissionRPCController. Details: {exc}"
        log.error(msg)

        raise exc

    log.info("Getting all torrents")
    try:
        with transmission_controller as torrent_ctl:
            all_torrents: list[Torrent] = torrent_ctl.get_all_torrents()

        return all_torrents
    except Exception as exc:
        msg = f"({type(exc)}) Error getting all torrents. Details: {exc}"
        log.error(msg)

        return []


def list_finished_torrents(
    transmission_settings: TransmissionClientSettings = transmission_settings,
):
    all_torrents: list[Torrent] = list_all_torrents(
        transmission_settings=transmission_settings
    )

    if all_torrents is None or len(all_torrents) == 0:
        log.warning("No torrents found at remote")
        return []

    log.info(f"Filtering [{len(all_torrents)}] and returning only finished torrents")
    finished_torrents: list[Torrent] = [
        torrent for torrent in all_torrents if torrent.done_date
    ]

    return finished_torrents


def list_stalled_torrents(
    transmission_settings: TransmissionClientSettings = transmission_settings,
):
    all_torrents: list[Torrent] = list_all_torrents(
        transmission_settings=transmission_settings
    )

    if all_torrents is None or len(all_torrents) == 0:
        log.warning("No torrents found at remote")
        return []

    log.info(f"Filtering [{len(all_torrents)}] and returning only stalled torrents")
    stalled_torrents: list[Torrent] = [
        torrent for torrent in all_torrents if torrent.is_stalled
    ]

    return stalled_torrents


def list_paused_torrents(
    transmission_settings: TransmissionClientSettings = transmission_settings,
):
    all_torrents: list[Torrent] = list_all_torrents(
        transmission_settings=transmission_settings
    )

    if all_torrents is None or len(all_torrents) == 0:
        log.warning("No torrents found at remote")
        return []

    log.info(f"Filtering [{len(all_torrents)}] and returning only paused torrents")
    paused_torrents: list[Torrent] = [
        torrent for torrent in all_torrents if torrent.stopped
    ]

    return paused_torrents


def start_torrent(torrent: Torrent, transmission_settings: TransmissionClientSettings = transmission_settings):
    try:
        transmission_controller: TransmissionRPCController = (
            transmission_lib.get_transmission_controller(transmission_settings=transmission_settings)
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting TransmissionRPCController. Details: {exc}"
        log.error(msg)

        raise exc

    log.info(f"Starting torrent '{torrent.name}'")
    try:
        with transmission_controller as torrent_ctl:
            torrent_ctl.start_torrent(torrent=torrent)
    except Exception as exc:
        msg = f"({type(exc)}) Error starting torrent '{torrent.name}'. Details: {exc}"
        log.error(msg)

        raise exc


def stop_torrent(torrent: Torrent, transmission_settings: TransmissionClientSettings = transmission_settings,):
    try:
        transmission_controller: TransmissionRPCController = (
            transmission_lib.get_transmission_controller(transmission_settings=transmission_settings)
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting TransmissionRPCController. Details: {exc}"
        log.error(msg)

        raise exc

    log.info(f"Stopping torrent '{torrent.name}'")
    try:
        with transmission_controller as torrent_ctl:
            torrent_ctl.stop_torrent(torrent=torrent)
    except Exception as exc:
        msg = f"({type(exc)}) Error stopping torrent '{torrent.name}'. Details: {exc}"
        log.error(msg)

        raise exc


def snapshot_torrents(transmission_settings: TransmissionClientSettings = transmission_settings,):
    all_torrents: list[Torrent] = list_all_torrents(transmission_settings=transmission_settings)
    
    log.info(f"Snapshotting [{len(all_torrents)}] torrents")
    snapshot_manager = SnapshotManager(snapshot_filename="all_torrents_snapshot")
    try:
        snapshot_manager.save_snapshot(torrents=all_torrents)
    except Exception as exc:
        msg = f"({type(exc)}) Error snapshotting all torrents. Details: {exc}"
        log.error(msg)

        raise exc