from __future__ import annotations

import json
import logging
from html import unescape
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from .errors import DownloadLinkError, MediafireAPIError

LOGGER = logging.getLogger(__name__)

USER_AGENT = "Mediafire-DL/0.1 (+https://github.com/)"
API_BASE = "https://www.mediafire.com/api/1.5"


class DownloadButtonParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.download_url: str | None = None
        self.title: str | None = None
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "a" and attr_map.get("id") == "downloadButton":
            href = attr_map.get("href")
            if href:
                self.download_url = unescape(href)
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title and data.strip():
            self.title = data.strip()


class HttpClient:
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout

    def api_get(self, endpoint: str, params: dict[str, str]) -> dict[str, Any]:
        params = {**params, "response_format": "json"}
        url = f"{API_BASE}/{endpoint}?{urlencode(params)}"
        data = self.fetch_bytes(url)
        try:
            payload = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as exc:
            LOGGER.debug("Invalid JSON returned by MediaFire API", exc_info=exc)
            raise MediafireAPIError("MediaFire returned an unreadable response.") from exc

        response = payload.get("response", {})
        result = response.get("result")
        if result and result != "Success":
            message = response.get("message") or "MediaFire reported an error."
            raise MediafireAPIError(message)
        return response

    def fetch_text(self, url: str) -> str:
        return self.fetch_bytes(url).decode("utf-8", errors="replace")

    def fetch_bytes(self, url: str) -> bytes:
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except HTTPError as exc:
            LOGGER.debug("HTTP error while fetching %s", url, exc_info=exc)
            raise MediafireAPIError("MediaFire could not be reached right now.") from exc
        except URLError as exc:
            LOGGER.debug("Network error while fetching %s", url, exc_info=exc)
            raise MediafireAPIError("Network connection failed while contacting MediaFire.") from exc

    def open_download(self, url: str):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        return urlopen(request, timeout=self.timeout)

    def find_public_download_url(self, page_url: str) -> str:
        html = self.fetch_text(page_url)
        parser = DownloadButtonParser()
        parser.feed(html)
        if parser.download_url:
            return parser.download_url
        LOGGER.debug("downloadButton link was not found on %s", page_url)
        raise DownloadLinkError("Could not find the public download button for a file.")


def encoded_path_segment(value: str) -> str:
    return quote(value.replace(" ", "_"), safe="")
