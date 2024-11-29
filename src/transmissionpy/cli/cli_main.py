import argparse
import pandas as pd
import sys

from transmissionpy.core.constants import SNAPSHOT_DIR
from transmissionpy.rpc_client.snapshot import SnapshotManager
from transmissionpy import rpc_client
from transmissionpy.domain.Transmission import TorrentMetadataIn
from transmissionpy.core.utils import df_utils

from loguru import logger as log

import argparse
import pandas as pd

from transmissionpy.rpc_client import SnapshotManager
from transmissionpy.domain.Transmission import TorrentMetadataIn, TorrentSnapshotMetadataIn


def parse_args():
    # Create the main parser
    parser = argparse.ArgumentParser("transmissionpy", description='Transmission CLI control interface')

    # Add a global --debug flag
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for detailed logging')

    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Torrent subcommand
    torrent_parser = subparsers.add_parser('torrent', help='Manage torrents')
    torrent_parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)  # Suppress duplicate help
    torrent_subparsers = torrent_parser.add_subparsers(dest='subcommand', required=True)

    # Count subcommand
    count_parser = torrent_subparsers.add_parser('count', help='Count torrents')
    count_parser.add_argument('type', choices=['all', 'finished', 'stalled'], help='Type of torrents to count')

    # List subcommand
    list_parser = torrent_subparsers.add_parser('list', help='List torrents')
    list_parser.add_argument('type', choices=['all', 'finished', 'stalled'], help='Type of torrents to list')

    # Snapshot subcommand
    snapshot_parser = subparsers.add_parser('snapshot', help='Manage snapshots')
    snapshot_parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
    snapshot_subparsers = snapshot_parser.add_subparsers(dest='subcommand', required=True)

    # List subcommand for snapshots
    snapshot_list_parser = snapshot_subparsers.add_parser('list', help='List snapshots')
    snapshot_list_parser.add_argument('type', choices=['all', 'finished', 'stalled'], help='Type of snapshots to list')

    # Parse arguments
    args = parser.parse_args()

    # Ensure global flags like `--debug` are accessible
    if args.debug:
        # Setup loguru logging
        log.remove()
        log.add(sys.stdout, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | ({module}.{function}:{line}) | > {message}")
        log.debug("DEBUG MODE ENABLED")
    else:
        log.remove()
        log.add(sys.stdout, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} [{level}]: {message}")

    return parser, args

def main(parser: argparse.ArgumentParser, args: argparse.Namespace):
    if args.command == 'torrent':
        if args.subcommand == 'count':
            if args.type == 'all':
                # print("Counting all torrents")
                count = len(rpc_client.list_all_torrents()) or 0
            elif args.type == 'finished':
                # print("Counting finished torrents")
                count = len(rpc_client.list_finished_torrents()) or 0
            elif args.type == 'stalled':
                # print("Counting stalled torrents")
                count = len(rpc_client.list_stalled_torrents()) or 0
            else:
                log.warning("No valid torrent type specified.")
                parser.print_help()
                return
            
            log.info(f"Number of torrents: {count}")

        elif args.subcommand == 'list':
            torrents = []
            
            if args.type == 'all':
                print("Getting list of all torrents")
                torrents = rpc_client.list_all_torrents()
            elif args.type == 'finished':
                print("Getting list of finished torrents")
                torrents = rpc_client.list_finished_torrents()
            elif args.type == 'stalled':
                print("Getting list of stalled torrents")
                torrents = rpc_client.list_stalled_torrents()
            else:
                log.warning("No valid torrent type specified.")
                parser.print_help()
                return
            
            log.debug(f"Converting [{len(torrents)}] torrent objects to TorrentMetadataIn objects")
            torrent_list = []
            for torrent in torrents:
                torrent_list.append(TorrentMetadataIn(**torrent.__dict__))
            
            log.debug(f"Building dataframe...")
            df = rpc_client.utils.convert_torrents_to_df(torrents=torrent_list)
            
            print_df = df[["name", "addedDate", "startDate", "finished", "secondsDownloading"]]
            log.info(f"Torrents:\n\n{print_df.head(5)}")

    elif args.command == 'snapshot':
        if args.subcommand == 'list':
            if args.type == 'all':
                print("Getting list of all snapshots")
                snapshot_manager = SnapshotManager(snapshot_dir=SNAPSHOT_DIR, snapshot_filename="all_torrents_snapshot")
            elif args.type == 'finished':
                print("Getting list of finished snapshots")
                snapshot_manager = SnapshotManager(snapshot_dir=SNAPSHOT_DIR, snapshot_filename="finished_torrents_snapshot")
            elif args.type == 'stalled':
                print("Getting list of stalled snapshots")
                snapshot_manager = SnapshotManager(snapshot_dir=SNAPSHOT_DIR, snapshot_filename="deleted_torrents_snapshot")
            else:
                log.warning("No valid snapshot type specified.")
                parser.print_help()
                return
            
            log.debug(f"Getting snapshot dicts...")
            snapshot_dicts = snapshot_manager.get_snapshots()
            
            snapshots: list[TorrentSnapshotMetadataIn] = []
            
            log.debug(f"Convert snapshot_dict objects into TorrentSnapshotMetadataIn objects")
            for snapshot_dict in snapshot_dicts:
                snapshot_date = str(snapshot_dict['snapshot_date'])
                snapshot_torrents = [t["fields"] for t in snapshot_dict['torrents']]
                
                snapshot = TorrentSnapshotMetadataIn(snapshot_date=snapshot_date, torrents=snapshot_torrents)
                snapshots.append(snapshot)
            
            log.debug(f"Rebuilding dicts from TorrentMetadataIn objects...")
            snapshot_dicts = [t.model_dump() for t in snapshots]
            
            log.debug("Building dataframe...")
            df = pd.DataFrame(snapshot_dicts)
            
            print(df.head(5))


if __name__ == '__main__':
    parser, args = parse_args()
    
    main(parser, args=args)