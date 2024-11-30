from transmissionpy import cli
from loguru import logger as log

command = ["torrent", "rm", "--status", "finished"]


if __name__ == "__main__":
    print("Removing finished torrents...")
    cli.app(command)
