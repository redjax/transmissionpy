from __future__ import annotations

from dataclasses import dataclass, field
import typing as t

from dynaconf import Dynaconf

TRANSMISSION_SETTINGS = Dynaconf(environments=True, env="transmission", envvar_prefix="TRANSMISSION", settings_files=["settings.toml", ".secrets.toml"])

@dataclass
class TransmissionClientSettings:
    
    host: t.Optional[str] = field(default=None)
    ip: t.Optional[str] = field(default="127.0.0.1")
    port: t.Union[str, int] = field(default=9091)
    protocol: str = field(default="http")
    rpc_url: str = field(default="/transmission/")
    username: str = field(default=None)
    password: str = field(default=None, repr=False)

transmission_settings: TransmissionClientSettings = TransmissionClientSettings(
    host=TRANSMISSION_SETTINGS.get("TRANSMISSION_HOST", default=None),
    ip=TRANSMISSION_SETTINGS.get("TRANSMISSION_IP", default="127.0.0.1"),
    port=TRANSMISSION_SETTINGS.get("TRANSMISSION_PORT", default=9091),
    protocol=TRANSMISSION_SETTINGS.get("TRANSMISSION_PROTOCOL", default="http"),
    username=TRANSMISSION_SETTINGS.get("TRANSMISSION_USERNAME", default=None),
    password=TRANSMISSION_SETTINGS.get("TRANSMISSION_PASSWORD", default=None),
    rpc_url=TRANSMISSION_SETTINGS.get("TRANSMISSION_RPC_URL", default="/transmission/")
)
