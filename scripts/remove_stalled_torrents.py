from transmissionpy import cli
from loguru import logger as log

command = ["torrent", "rm", "--status", "stalled", "--log-file"]


if __name__ == "__main__":
    print("Removing stalled torrents...")
    cli.app.meta(command)
