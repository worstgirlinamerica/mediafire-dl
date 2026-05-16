from __future__ import annotations

import logging
from pathlib import Path

from .errors import DownloadLinkError, MediafireDLError
from .http import HttpClient
from .mediafire import safe_name
from .models import DownloadPlan, MediafireItem
from .output import UserInterface

LOGGER = logging.getLogger(__name__)


class Downloader:
    def __init__(self, http: HttpClient | None = None, chunk_size: int = 1024 * 128) -> None:
        self.http = http or HttpClient()
        self.chunk_size = chunk_size

    def download_plan(self, plan: DownloadPlan, destination: Path, ui: UserInterface) -> Path:
        root = destination / safe_name(plan.display_name) if plan.is_folder else destination
        root.mkdir(parents=True, exist_ok=True)

        total = len(plan.files)
        for index, item in enumerate(plan.files, start=1):
            self._download_item(item, root, ui, index, total)
        return root

    def _download_item(
        self,
        item: MediafireItem,
        root: Path,
        ui: UserInterface,
        index: int,
        total: int,
    ) -> None:
        target = root / Path(*item.relative_folder.parts) / safe_name(item.name)
        target.parent.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(f"{target.name}.part")

        try:
            direct_url = self.http.find_public_download_url(item.page_url)
        except MediafireDLError:
            raise
        except Exception as exc:
            LOGGER.debug("Unexpected error while finding download URL", exc_info=exc)
            raise DownloadLinkError(f"Could not prepare {item.name} for download.") from exc

        with self.http.open_download(direct_url) as response:
            length = response.headers.get("Content-Length")
            total_size = int(length) if length and length.isdigit() else item.size
            progress = ui.start_file(index, total, item, total_size)
            with partial.open("wb") as file:
                while True:
                    chunk = response.read(self.chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
                    progress.update(len(chunk))
            progress.finish()
        partial.replace(target)
