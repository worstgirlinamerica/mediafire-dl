from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class MediafireItem:
    name: str
    page_url: str
    size: int | None = None
    relative_folder: PurePosixPath = PurePosixPath()

    @property
    def relative_path(self) -> PurePosixPath:
        return self.relative_folder / self.name


@dataclass(frozen=True)
class MediafireFolder:
    name: str
    key: str
    files: tuple[MediafireItem, ...]


@dataclass(frozen=True)
class DownloadPlan:
    display_name: str
    files: tuple[MediafireItem, ...]
    is_folder: bool
