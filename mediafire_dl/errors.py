class MediafireDLError(Exception):
    """Base exception for user-facing downloader errors."""


class UnsupportedLinkError(MediafireDLError):
    """Raised when a link is not a supported MediaFire file or folder URL."""


class MediafireAPIError(MediafireDLError):
    """Raised when MediaFire's public API returns an error."""


class DownloadLinkError(MediafireDLError):
    """Raised when a public download URL cannot be extracted."""
