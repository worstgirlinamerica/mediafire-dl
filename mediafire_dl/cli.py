from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from rich.console import Console

from .downloader import Downloader
from .errors import MediafireDLError
from .http import HttpClient
from .mediafire import MediafireClient
from .output import RichUI


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    ui = RichUI(Console())
    link = args.link or ui.ask_link()
    if not link.strip():
        ui.error("Please paste a MediaFire file or folder link.")
        return 1
    destination = Path(args.output or ui.ask_save_dir(str(default_downloads_dir()))).expanduser()

    try:
        cookie_file = Path(args.cookies).expanduser() if args.cookies else None
        http = HttpClient(cookie_file=cookie_file)
        client = MediafireClient(http)
        downloader = Downloader(http)

        ui.status("Finding files...")
        plan = client.build_plan(link)
        if not plan.files:
            ui.warning("No downloadable files were found.")
            return 1

        ui.show_plan(plan)
        ui.status("Preparing downloads...")

        if args.dry_run:
            ui.warning("Dry run: nothing was downloaded.")
            return 0

        ui.status("Downloading...")
        saved_to = downloader.download_plan(plan, destination, ui)
        ui.finished(str(saved_to))
        return 0
    except KeyboardInterrupt:
        ui.error("Download cancelled.")
        return 130
    except MediafireDLError as exc:
        if args.verbose:
            logging.getLogger(__name__).exception("Mediafire-DL failed")
        ui.error(str(exc))
        return 1
    except Exception as exc:
        if args.verbose:
            logging.getLogger(__name__).exception("Unexpected failure")
            ui.error(str(exc))
        else:
            ui.error("Something went wrong. Run again with --verbose for details.")
        return 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mediafire-dl",
        description="Download MediaFire files and folders with a clean progress UI.",
    )
    parser.add_argument("link", nargs="?", help="MediaFire file or folder link")
    parser.add_argument(
        "-o",
        "--output",
        help="Folder to save downloads into. Defaults to your Downloads folder.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files without downloading them.",
    )
    parser.add_argument(
        "--cookies",
        help=(
            "Path to a Netscape/Mozilla cookies.txt file to use for links your browser can access. "
            "Cookies are read locally and are not saved by Mediafire-DL."
        ),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show technical logs and tracebacks for troubleshooting.",
    )
    return parser.parse_args(argv)


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.CRITICAL,
        format="%(levelname)s: %(name)s: %(message)s",
    )


def default_downloads_dir() -> Path:
    downloads = Path.home() / "Downloads"
    return downloads if downloads.exists() else Path.home()


if __name__ == "__main__":
    sys.exit(main())
