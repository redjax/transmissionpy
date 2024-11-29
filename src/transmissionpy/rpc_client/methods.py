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
from transmissionpy.domain.Transmission import (
    TorrentMetadataIn,
    TorrentMetadataOut,
    torrent_df_dtypes_mapping,
)

from .snapshot import SnapshotManager
from .utils import (
    convert_multiple_torrents_to_torrentmetadata,
    convert_torrent_to_torrentmetadata,
    convert_torrents_to_df,
    select_random_torrent,
)

from loguru import logger as log
import pandas as pd
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

    log.debug("Getting all torrents")
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

    log.debug(f"Filtering [{len(all_torrents)}] and returning only finished torrents")
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

    log.debug(f"Filtering [{len(all_torrents)}] and returning only stalled torrents")
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


def delete_torrent(torrent: Torrent, transmission_settings: TransmissionClientSettings = transmission_settings, remove_files: bool = False):
    try:
        transmission_controller: TransmissionRPCController = (
            transmission_lib.get_transmission_controller(transmission_settings=transmission_settings)
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting TransmissionRPCController. Details: {exc}"
        log.error(msg)

        raise exc
    
    log.info(f"Deleting torrent '{torrent.name}'")
    try:
        with transmission_controller as torrent_ctl:
            torrent_ctl.delete_torrent(torrent=torrent)
    except Exception as exc:
        msg = f"({type(exc)}) Error deleting torrent '{torrent.name}'. Details: {exc}"
        log.error(msg)

        raise exc
    

def delete_torrent_by_transmission_id(torrent_id: int, transmission_settings: TransmissionClientSettings = transmission_settings, remove_files: bool = False):
    try:
        transmission_controller: TransmissionRPCController = (
            transmission_lib.get_transmission_controller(transmission_settings=transmission_settings)
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting TransmissionRPCController. Details: {exc}"
        log.error(msg)

        raise exc
    
    log.info(f"Deleting torrent by ID: '{torrent_id}'")
    try:
        with transmission_controller as torrent_ctl:
            torrent_ctl.delete_torrent_by_id(torrent_id=torrent_id, remove_files=remove_files)
    except Exception as exc:
        msg = f"({type(exc)}) Error deleting torrent by ID '{torrent_id}'. Details: {exc}"
        log.error(msg)

        raise exc


def snapshot_torrents(transmission_settings: TransmissionClientSettings = transmission_settings) -> list[Torrent]:
    all_torrents: list[Torrent] = list_all_torrents(transmission_settings=transmission_settings)
    
    log.info(f"Snapshotting [{len(all_torrents)}] torrents")
    snapshot_manager = SnapshotManager(snapshot_filename="all_torrents_snapshot")
    try:
        snapshot_manager.save_snapshot(torrents=all_torrents)
    except Exception as exc:
        msg = f"({type(exc)}) Error snapshotting all torrents. Details: {exc}"
        log.error(msg)

    return all_torrents


def delete_oldest_torrents(delete_count: int = 1):
    try:
        all_torrents = snapshot_torrents()
        all_torrents_df = convert_torrents_to_df(torrents=all_torrents)
    except Exception as exc:
        msg = f"({type(exc)}) Error getting all torrents with a snapshot. Details: {exc}"
    
    log.info("Sorting torrents by date ascending (oldest first)")
    sorted_df = all_torrents_df.sort_values(by=["addedDate", "startDate", "secondsDownloading"], ascending=[True, True, False])
    sorted_df = df_utils.convert_df_col_dtypes(df=sorted_df, dtype_mapping=torrent_df_dtypes_mapping)
    
    log.debug(f"Sorted all_torrents_df:\n{sorted_df[['id', 'name', 'isStalled', 'isFinished', 'addedDate', 'startDate', 'secondsDownloading']]}")
    sorted_df = df_utils.convert_df_datetimes_to_timestamp(df=sorted_df)
    
    log.info(f"Deleting [{delete_count}] oldest torrent(s)")
    
    deleted_torrents: list[dict] = []
    loop_count: int = 0
    
    while loop_count <= delete_count:
        ## Find the oldest stalled torrent and delete
        for index, row in sorted_df.iterrows():
            if row["isStalled"] and not row["isFinished"]:
                torrent_id = row["id"]
                log.debug(f"Deleting oldest stalled torrent: [id:{row['id']}] {row['name']}")
                
                try:
                    # delete_torrent_by_transmission_id(torrent_id=torrent_id, remove_files=True)
                
                    # deleted_snapshot = SnapshotManager(snapshot_filename="deleted_torrents_snapshot")
                    # deleted_snapshot.save_snapshot(torrents=[row.to_dict()])
                
                    deleted_row = row
                    
                    ## Add deleted row to deleted torrents list
                    deleted_torrents.append(deleted_row.to_dict())
                    
                    ## Remove deleted row from sorted_df
                    sorted_df.drop(index, inplace=True)
                    
                    break
                
                except Exception as exc:
                    msg = f"({type(exc)}) Error deleting torrent ID '{torrent_id}'. Details: {exc}"
                    log.error(msg)
                    
                    raise exc
                
            
            else:
                log.debug(f"Torrent [id:{row['id']}] {row['name']} is not stalled, finding next...")
                continue
            
        log.debug(f"Deleted torrent:\n{deleted_row[['id', 'name', 'isStalled', 'isFinished', 'addedDate', 'startDate', 'secondsDownloading', 'percentDone']]}")
        
        loop_count += 1
        
    log.info(f"Deleted [{len(deleted_torrents)}] torrent(s)")
    
    return deleted_torrents


def delete_finished_torrents():
    finished_torrents = list_finished_torrents()
    finished_torrents_df = convert_torrents_to_df(torrents=finished_torrents)
    
    log.info(f"Deleting [{len(finished_torrents)}] finished torrent(s)")
    
    deleted_torrents: list[dict] = []
    loop_count: int = 0
    
    while loop_count < len(finished_torrents):
        for index, row in finished_torrents_df.iterrows():
            ## Ensure torrent is finished
            if row["isFinished"]:
                torrent_id = row["id"]
                log.debug(f"Deleting finished torrent: [id:{row['id']}] {row['name']}")
                
                try:
                    # delete_torrent_by_transmission_id(torrent_id=torrent_id, remove_files=True)
                
                    # deleted_snapshot = SnapshotManager(snapshot_filename="deleted_torrents_snapshot")
                    # deleted_snapshot.save_snapshot(torrents=[row.to_dict()])
                
                    deleted_row = row
                    
                    ## Add deleted row to deleted torrents list
                    deleted_torrents.append(deleted_row.to_dict())
                    
                    ## Remove deleted row from sorted_df
                    finished_torrents_df.drop(index, inplace=True)
                    
                    log.debug(f"Deleted torrents:\n{deleted_row[['id', 'name', 'isStalled', 'isFinished', 'addedDate', 'startDate', 'secondsDownloading', 'percentDone']]}")
                    loop_count += 1
                    
                    break
                except Exception as exc:
                    msg = f"({type(exc)}) Error deleting torrent ID '{torrent_id}'. Details: {exc}"
                    log.error(msg)
                    
                    raise exc
                
            else:
                continue
        
    log.info(f"Deleted [{len(deleted_torrents)}] torrent(s)")
    
    return deleted_torrents
