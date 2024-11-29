import logging
import typing as t
import argparse

from loguru import logger as log

from transmissionpy import cli
from transmissionpy.core.settings import LOGGING_SETTINGS

log = logging.getLogger(__name__)

if __name__ == "__main__":
    parser, args = cli.parse_args()
    
    # logging.basicConfig(level="DEBUG" if args.debug else "ERROR", format="%(asctime)s | [%(levelname)s] | (%(module)s.%(funcName)s:%(lineno)d) | > %(message)s" if args.debug else "%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    
    log.debug("Calling CLI main")
    cli.main(parser=parser, args=args)