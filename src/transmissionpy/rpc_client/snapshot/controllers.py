from loguru import logger as log

from pathlib import Path
import typing as t
from transmissionpy.core.utils import df_utils, path_utils
from datetime import datetime

from transmissionpy.domain.Transmission import TorrentMetadataIn, TorrentMetadataOut
from transmissionpy.rpc_client.utils import convert_torrents_to_df, convert_torrent_to_torrentmetadata, convert_multiple_torrents_to_torrentmetadata
from transmissionpy.core.constants import SNAPSHOT_DIR

from transmission_rpc import Torrent
import pandas as pd
import msgpack

class SnapshotManager:
    def __init__(self, snapshot_dir: t.Union[Path, str] = SNAPSHOT_DIR, snapshot_filename: str = "snapshots"):
        self.snapshot_dir = Path(str(snapshot_dir))
        self.snapshot_parquet_file = self.snapshot_dir / f"{snapshot_filename}.parquet"

    def save_snapshot(self, torrents: t.List[t.Union[Torrent, TorrentMetadataIn, dict]]) -> None:
        """Save a snapshot of torrents to the Parquet file."""
        ## Ensure input is a list of dictionaries
        if not any(isinstance(t, dict) for t in torrents) and not any(isinstance(t, Torrent) for t in torrents) and not any(isinstance(t, TorrentMetadataIn)):
            raise TypeError("torrents must be a list of dicts, TorrentMetadataIn, or transmission_rpc.Torrent objects.")
        
        ## Create list of torrent dicts
        torrents = [
            t.__dict__ if isinstance(t, Torrent)
            else t if isinstance(t, dict)
            else t.model_dump() if isinstance(t, TorrentMetadataIn)
            else None
            for t in torrents
        ]

        ## Create snapshot dir if it does not exist
        if not self.snapshot_dir.exists():
            self.snapshot_dir.mkdir(parents=True, exist_ok=True)

        ## Create the snapshot row with msgpack-compressed data
        snapshot_row = {
            "snapshot_date": datetime.now(),
            "count": len(torrents),
            "torrents": msgpack.dumps(torrents),
        }

        ## Load existing snapshots, if the file exists, and append the new one
        if self.snapshot_parquet_file.exists():
            try:
                existing_df = pd.read_parquet(self.snapshot_parquet_file)
                new_df = pd.concat([existing_df, pd.DataFrame([snapshot_row])], ignore_index=True)
            except Exception as e:
                log.error(f"Failed to read existing Parquet file: {e}")
                raise
        else:
            new_df = pd.DataFrame([snapshot_row])

        ## Save the updated DataFrame to Parquet
        try:
            new_df.to_parquet(self.snapshot_parquet_file, index=False)
            log.info(f"Snapshot saved successfully to {self.snapshot_parquet_file}")
        except Exception as e:
            log.error(f"Failed to write snapshot to Parquet file: {e}")
            raise

    def get_snapshots(self) -> t.List[dict]:
        """Retrieve all snapshots from the Parquet file."""
        if not self.snapshot_parquet_file.exists():
            log.warning(f"No snapshots found at {self.snapshot_parquet_file}")
            return []

        try:
            df = pd.read_parquet(self.snapshot_parquet_file)
            snapshots = [
                {
                    "snapshot_date": row["snapshot_date"],
                    "torrents": msgpack.loads(row["torrents"]),
                }
                for _, row in df.iterrows()
            ]
            return snapshots
        except Exception as e:
            log.error(f"Failed to read snapshots from Parquet file: {e}")
            raise
