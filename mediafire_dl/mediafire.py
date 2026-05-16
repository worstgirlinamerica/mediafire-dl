from __future__ import annotations

import logging
import re
from pathlib import PurePosixPath
from urllib.parse import unquote, urlparse

from .errors import MediafireAPIError, UnsupportedLinkError
from .http import HttpClient, encoded_path_segment
from .models import DownloadPlan, MediafireItem

LOGGER = logging.getLogger(__name__)

FOLDER_RE = re.compile(r"/folder/([^/?#]+)")
FILE_RE = re.compile(r"/file/([^/?#]+)")


class MediafireClient:
    def __init__(self, http: HttpClient | None = None) -> None:
        self.http = http or HttpClient()

    def build_plan(self, link: str) -> DownloadPlan:
        kind, key = parse_mediafire_link(link)
        if kind == "folder":
            return self._build_folder_plan(key)
        return self._build_file_plan(key, link)

    def _build_folder_plan(self, folder_key: str) -> DownloadPlan:
        folder_name = self._folder_name(folder_key) or "MediaFire Folder"
        files = tuple(self._walk_folder(folder_key, PurePosixPath()))
        return DownloadPlan(display_name=folder_name, files=files, is_folder=True)

    def _build_file_plan(self, quick_key: str, original_link: str) -> DownloadPlan:
        info = self._file_info(quick_key)
        filename = info.get("filename") or filename_from_url(original_link) or "MediaFire File"
        page_url = info.get("links", {}).get("normal_download") or original_link
        size = parse_int(info.get("size"))
        item = MediafireItem(name=filename, page_url=page_url, size=size)
        return DownloadPlan(display_name=filename, files=(item,), is_folder=False)

    def _walk_folder(
        self,
        folder_key: str,
        relative_folder: PurePosixPath,
    ) -> list[MediafireItem]:
        items: list[MediafireItem] = []

        chunk = 1
        while True:
            response = self.http.api_get(
                "folder/get_content.php",
                {
                    "folder_key": folder_key,
                    "content_type": "files",
                    "chunk_number": str(chunk),
                    "chunk_size": "100",
                },
            )
            content = response.get("folder_content", {})
            for entry in content.get("files", []):
                links = entry.get("links", {})
                page_url = links.get("normal_download")
                filename = entry.get("filename")
                if not page_url or not filename:
                    LOGGER.debug("Skipping incomplete MediaFire file entry: %r", entry)
                    continue
                items.append(
                    MediafireItem(
                        name=filename,
                        page_url=page_url,
                        size=parse_int(entry.get("size")),
                        relative_folder=relative_folder,
                    )
                )
            if content.get("more_chunks") != "yes":
                break
            chunk += 1

        chunk = 1
        while True:
            response = self.http.api_get(
                "folder/get_content.php",
                {
                    "folder_key": folder_key,
                    "content_type": "folders",
                    "chunk_number": str(chunk),
                    "chunk_size": "100",
                },
            )
            content = response.get("folder_content", {})
            for entry in content.get("folders", []):
                child_key = entry.get("folderkey")
                child_name = entry.get("name") or entry.get("foldername") or "Untitled Folder"
                if not child_key:
                    LOGGER.debug("Skipping incomplete MediaFire folder entry: %r", entry)
                    continue
                items.extend(self._walk_folder(child_key, relative_folder / safe_name(child_name)))
            if content.get("more_chunks") != "yes":
                break
            chunk += 1

        return items

    def _folder_name(self, folder_key: str) -> str | None:
        try:
            response = self.http.api_get("folder/get_info.php", {"folder_key": folder_key})
        except MediafireAPIError:
            LOGGER.debug("Could not fetch folder name for %s", folder_key, exc_info=True)
            return None
        info = response.get("folder_info", {})
        return info.get("name") or info.get("foldername")

    def _file_info(self, quick_key: str) -> dict:
        response = self.http.api_get("file/get_info.php", {"quick_key": quick_key})
        return response.get("file_info", {})


def parse_mediafire_link(link: str) -> tuple[str, str]:
    parsed = urlparse(link.strip())
    if not parsed.netloc or "mediafire.com" not in parsed.netloc.lower():
        raise UnsupportedLinkError("Please provide a MediaFire file or folder link.")

    path = unquote(parsed.path)
    folder_match = FOLDER_RE.search(path)
    if folder_match:
        return "folder", folder_match.group(1)

    file_match = FILE_RE.search(path)
    if file_match:
        return "file", file_match.group(1)

    raise UnsupportedLinkError("Please provide a MediaFire file or folder link.")


def filename_from_url(link: str) -> str | None:
    parsed = urlparse(link)
    pieces = [piece for piece in unquote(parsed.path).split("/") if piece]
    if len(pieces) >= 3 and pieces[0] == "file":
        return pieces[2].replace("_", " ")
    return None


def safe_name(name: str) -> str:
    return name.replace("/", "-").replace("\\", "-").strip() or "Untitled"


def page_url_for_item(item: MediafireItem) -> str:
    return item.page_url


def api_file_page(quick_key: str, filename: str) -> str:
    return f"https://www.mediafire.com/file/{quick_key}/{encoded_path_segment(filename)}/file"


def parse_int(value: object) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None
