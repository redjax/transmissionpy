from __future__ import annotations

from decimal import Decimal
import typing as t

from loguru import logger as log
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
)

class TorrentFileStatBase(BaseModel):
    bytesCompleted: int = Field(default=0)
    priority: int = Field(default=0)
    wanted: bool = Field(default=False)


class TorrentFileStatIn(TorrentFileStatBase):
    pass

class TorrentFileStatOut(TorrentFileStatBase):
    db_id: int
    

class TorrentFileBase(BaseModel):
    bytesCompleted: int = Field(default=0)
    length: int = Field(default=0)
    name: str = Field(default="")

class TorrentFileIn(TorrentFileBase):
    pass

class TorrentFileOut(TorrentFileStatBase):
    db_id: int

class TorrentPeersFromBase(BaseModel):
    fromCache: int = Field(default=0)
    fromDht: int = Field(default=0)
    fromIncoming: int = Field(default=0)
    fromLpd: int = Field(default=0)
    fromLtep: int = Field(default=0)
    fromPex: int = Field(default=0)
    fromTracker: int = Field(default=0)

class TorrentPeersFromIn(TorrentPeersFromBase):
    pass

class TorrentPeersFromOut(TorrentPeersFromBase):
    db_id: int
    
class TorrentTrackerStatBase(BaseModel):
    announce: str = Field(default="")
    announceState: int = Field(default=0)
    downloadCount: int = Field(default=0)
    hasAnnounced: bool = Field(default=False)
    hasScraped: bool = Field(default=False)
    host: str = Field(default="")
    id: int = Field(default=0)
    isBackup: bool = Field(default=False)
    lastAnnouncePeerCount: int = Field(default=0)
    lastAnnounceResult: str = Field(default="")
    lastAnnounceStartTime: int = Field(default=0)
    lastAnnounceSucceeded: bool = Field(default=False)
    lastAnnounceTime: int = Field(default=0)
    lastAnnounceTimedOut: bool = Field(default=False)
    lastScrapeResult: str = Field(default="")
    lastScrapeStartTime: int = Field(default=0)
    lastScrapeSucceeded: bool = Field(default=False)
    lastScrapeTime: int = Field(default=0)
    lastScrapeTimedOut: bool = Field(default=False)
    leecherCount: int = Field(default=0)
    nextAnnounceTime: int = Field(default=0)
    nextScrapeTime: int = Field(default=0)
    scrape: str = Field(default="")
    scrapeState: int = Field(default=0)
    seederCount: int = Field(default=0)
    tier: int = Field(default=0)


class TorrentTrackerStatIn(TorrentTrackerStatBase):
    pass

class TorrentTrackerStatOut(TorrentTrackerStatBase):
    db_id: int


class TorrentTrackerBase(BaseModel):
    announce: str = Field(default="")
    id: int = Field(default=0)
    scrape: str = Field(default="")
    tier: int = Field(default=0)


class TorrentTrackerIn(TorrentTrackerBase):
    pass

class TorrentTrackerOut(TorrentTrackerBase):
    db_id: int

class TorrentMetadataBase(BaseModel):
    activityDate: int = Field(default=0)
    addedDate: int = Field(default=0)
    bandwidthPriority: int = Field(default=0)
    comment: str = Field(default="")
    corruptEver: int = Field(default=0)
    creator: str = Field(default="")
    dateCreated: int = Field(default=0)
    desiredAvailable: int = Field(default=0)
    doneDate: int = Field(default=0)
    downloadDir: str = Field(default="")
    downloadLimit: int = Field(default=0)
    downloadLimited: bool = Field(default=False)
    downloadedEver: int = Field(default=0)
    editDate: int = Field(default=0)
    error: int = Field(default=0)
    errorString: str = Field(default="")
    eta: int = Field(default=0)
    etaIdle: int = Field(default=0)
    fileStats: list[TorrentFileStatBase] = Field(default_factory=list())
    files: list[TorrentFileBase] = Field(default_factory=list())
    hashString: str = Field(default="")
    haveUnchecked: int = Field(default=0)
    haveValid: int = Field(default=0)
    honorsSessionLimits: bool = Field(default=False)
    id: int = Field(default=0)
    isFinished: bool = Field(default=False)
    isPrivate: bool = Field(default=False)
    isStalled: bool = Field(default=False)
    # labels: list = ...
    leftUntilDone: int = Field(default=0)
    magnetLink: str = Field(default="")
    manualAnnounceTime: int = Field(default=0)
    maxConnectedPeers: int = Field(default=0)
    metadataPercentComplete: int = Field(default=0)
    name: str = Field(default="")
    # peer-limit: int = ...
    # peers: list = ...
    peersConnected: int = Field(default=0)
    peersFrom: TorrentPeersFromBase = Field(default=None)
    peersGettingFromUs: int = Field(default=0)
    peersSendingToUs: int = Field(default=0)
    percentDone: Decimal = Field(default=Decimal(0.0))
    pieceCount: int = Field(default=0)
    pieceSize: int = Field(default=0)
    pieces: str = Field(default="")
    queuePosition: int = Field(default=0)
    rateDownload: int = Field(default=0)
    rateUpload: int = Field(default=0)
    recheckProgress: int = Field(default=0)
    secondsDownloading: int = Field(default=0)
    secondsSeeding: int = Field(default=0)
    seedIdleLimit: int = Field(default=0)
    seedIdleMode: int = Field(default=0)
    seedRatioLimit: int = Field(default=0)
    seedRatioMode: int = Field(default=0)
    sizeWhenDone: int = Field(default=0)
    startDate: int = Field(default=0)
    status: int = Field(default=0)
    torrentFile: str = Field(default="")
    totalSize: int = Field(default=0)
    trackerStats: list[TorrentTrackerStatBase] = Field(default_factory=list())
    trackers: list[TorrentTrackerBase] = Field(default_factory=list())
    uploadLimit: int = Field(default=0)
    uploadLimited: bool = Field(default=False)
    uploadRatio: Decimal = Field(default=Decimal(0.0))
    uploadedEver: int = Field(default=0)

class TorrentMetadataIn(TorrentMetadataBase):
    fileStats: list[TorrentFileStatIn] = Field(default_factory=list())
    files: list[TorrentFileIn] = Field(default_factory=list())
    peersFrom: TorrentPeersFromIn = Field(default=None)
    trackerStats: list[TorrentTrackerStatIn] = Field(default_factory=list())
    trackers: list[TorrentTrackerIn] = Field(default_factory=list())

class TorrentMetadataOut(TorrentMetadataBase):
    db_id: int
    
    fileStats: list[TorrentFileStatOut] = Field(default_factory=list())
    files: list[TorrentFileOut] = Field(default_factory=list())
    peersFrom: TorrentPeersFromOut = Field(default=None)
    trackerStats: list[TorrentTrackerStatOut] = Field(default_factory=list())
    trackers: list[TorrentTrackerOut] = Field(default_factory=list())


class TorrentSnapshotMetadataBase(BaseModel):
    snapshot_date: str = Field(default=None)
    torrents: list[TorrentMetadataBase] = Field(default=None)
    

class TorrentSnapshotMetadataIn(TorrentSnapshotMetadataBase):
    torrents: list[TorrentMetadataIn] = Field(default=None, repr=False)
    
    @computed_field
    def torrent_count(self) -> int:
        return len(self.torrents)

class TorrentSnapshotMetadataOut(TorrentSnapshotMetadataBase):
    id: int
