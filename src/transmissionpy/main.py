import argparse
from dataclasses import dataclass, field
from loguru import logger as log
from pathlib import Path
import typing as t
from time import sleep

from transmissionpy.core import setup
from transmissionpy.core.settings import LOGGING_SETTINGS
from transmissionpy.domain.Transmission import torrent_df_mapping, TORRENT_INT_DATETIME_FIELDNAMES, TorrentFileStatIn, TorrentFileStatOut, TorrentMetadataIn, TorrentMetadataOut
from transmissionpy import rpc_client
from transmissionpy.core.constants import DATA_DIR, OUTPUT_DIR, SNAPSHOT_DIR, PQ_OUTPUT_DIR, CSV_OUTPUT_DIR,JSON_OUTPUT_DIR
from transmissionpy.core.utils import df_utils, path_utils

def main():
    pass


if __name__ == "__main__":
    setup.setup_logging(log_level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))