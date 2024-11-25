from loguru import logger as log

from pydantic import BaseModel, Field, field_validator, ValidationError, computed_field, ConfigDict
import typing as t

class TorrentMetadataBase(BaseModel):
    pass


class TorrentMetadataIn(BaseModel):
    pass


class TorrentMetadataOut(BaseModel):
    id: int
