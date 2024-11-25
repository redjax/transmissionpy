from __future__ import annotations

from contextlib import AbstractContextManager
from pathlib import Path
import typing as t

from transmission_rpc.client import Client
from transmission_rpc.torrent import Torrent

class TransmissionRPCController(AbstractContextManager):
    def __init__(
        self,
        host: str | None = None,
        ip: str | None = None,
        port: int = None,
        username: str = None,
        password: str = None,
        path: str = None,
        protocol: str = None,
        timeout: int | float | tuple[int | float, int | float] | None = None,
    ) -> None:
        self.host: str | None = host
        self.ip: str | None = ip
        self.port: int | None = port
        self.username: str | None = username
        self.password: str | None = password
        self.path: str | None = path
        self.protocol: str | None = protocol
        self.timeout: int | float | tuple[int | float, int | float] | None = timeout

        self.client: Client | None = None

    def __enter__(self) -> "TransmissionRPCController":
        self.client = self._create_client()

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            msg = f"Unhandled exception in TransmissionRPCController: {exc_value}"
            # log.error(msg)
            print(f"[ERROR] {msg}")

    def _create_client(self) -> Client:
        """Create and return a configured transmission_rpc.Client object."""
        _conf: dict[str, t.Union[str, int]] = {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "path": self.path,
            "protocol": self.protocol,
        }

        # Remove keys with None values to avoid passing them to Client
        _conf = {k: v for k, v in _conf.items() if v is not None}

        try:
            client = Client(**_conf)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception getting Transmission RPC Client. Details: {exc}"
            )

        return client

    def _move_or_copy(
        self,
        ids: int | str | list[int] | list[str] = None,
        dest: str | Path = None,
        move: bool = False,
    ) -> bool:
        try:
            self.client.move_torrent_data(
                ids=ids, location=dest, timeout=self.timeout, move=move
            )

            return True
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception {'moving' if move else 'copying'} torrent data to dest '{dest}'. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            raise exc

    def get_client(self) -> Client:
        """Return the Transmission RPC client."""
        if self.client is None:
            self.client = self._create_client()

        return self.client

    def get_all_torrents(self) -> list[Torrent]:
        try:
            _torrents: list[Torrent] = self.client.get_torrents()

            return _torrents
        except Exception as exc:
            msg = Exception(f"Unhandled exception getting all torrents. Details: {exc}")
            print(f"[ERROR] {msg}")

            raise exc

    def get_multiple_torrents(self, ids: list[str | int] = None) -> list[Torrent]:

        try:
            _torrents: list[Torrent] = self.client.get_torrents(
                ids=ids, timeout=self.timeout
            )

            return _torrents
        except Exception as exc:
            msg = Exception(f"Unhandled exception getting all torrents. Details: {exc}")
            print(f"[ERROR] {msg}")

            raise exc

    def get_single_torrent(self, torrent_id: str | int = None):
        try:
            _torrent: Torrent = self.client.get_torrent(
                torrent_id=torrent_id, timeout=self.timeout
            )

            return _torrent
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting torrent by ID '{torrent_id}'. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            raise exc

    def move_torrent_data(
        self, ids: int | str | list[int] | list[str] = None, dest: str | Path = None
    ) -> bool:

        try:
            self._move_or_copy(ids=ids, dest=dest, move=True)
            return True
        except Exception as exc:
            return False

        # try:
        #     self.client.move_torrent_data(
        #         ids=ids, location=dest, timeout=self.timeout, move=True
        #     )

        #     return True
        # except Exception as exc:
        #     msg = Exception(
        #         f"Unhandled exception moving torrent data to dest '{dest}'. Details: {exc}"
        #     )
        #     print(f"[ERROR] {msg}")

        #     raise exc

    def copy_torrent_data(
        self, ids: int | str | list[int] | list[str] = None, dest: str | Path = None
    ) -> bool:
        try:
            self._move_or_copy(ids=ids, dest=dest, move=False)
            return True
        except Exception as exc:
            return False
        # try:
        #     self.client.move_torrent_data(
        #         ids=ids, location=dest, timeout=self.timeout, move=False
        #     )

        #     return True
        # except Exception as exc:
        #     msg = Exception(
        #         f"Unhandled exception moving torrent data to dest '{dest}'. Details: {exc}"
        #     )
        #     print(f"[ERROR] {msg}")

        #     raise exc

    def get_free_space(self, remote_path: str = "/") -> int | None:
        try:
            free_space: int | None = self.client.free_space(path=remote_path)

            return free_space
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting free space at transmission remote. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            raise exc

    def get_recently_active(self) -> t.Tuple[t.List[Torrent] | t.List[int]]:
        recently_active: t.Tuple[t.List[Torrent] | t.List[int]] = (
            self.client.get_recently_active_torrents()
        )

        return recently_active
