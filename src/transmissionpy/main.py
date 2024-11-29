from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from time import sleep
import typing as t

from transmissionpy import rpc_client
from transmissionpy.core import setup
from transmissionpy.core.constants import (
    CSV_OUTPUT_DIR,
    DATA_DIR,
    JSON_OUTPUT_DIR,
    OUTPUT_DIR,
    PQ_OUTPUT_DIR,
    SNAPSHOT_DIR,
)
from transmissionpy.core.settings import LOGGING_SETTINGS
from transmissionpy.core.utils import df_utils, path_utils
from transmissionpy.domain.Transmission import (
    TORRENT_INT_DATETIME_FIELDNAMES,
    TorrentFileStatIn,
    TorrentFileStatOut,
    TorrentMetadataIn,
    TorrentMetadataOut,
    torrent_df_dtypes_mapping,
)

from loguru import logger as log


def main():
    pass


if __name__ == "__main__":
    setup.setup_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))