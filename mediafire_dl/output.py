from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import PurePosixPath
from typing import Iterable

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from .models import DownloadPlan, MediafireItem

MINT = "#7fffd4"
MINT_DIM = "#5fd6b5"


class ProgressHandle(ABC):
    @abstractmethod
    def update(self, advance: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def finish(self) -> None:
        raise NotImplementedError


class UserInterface(ABC):
    @abstractmethod
    def ask_link(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def ask_save_dir(self, default: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def status(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_plan(self, plan: DownloadPlan) -> None:
        raise NotImplementedError

    @abstractmethod
    def start_file(self, index: int, total: int, item: MediafireItem, size: int | None) -> ProgressHandle:
        raise NotImplementedError

    @abstractmethod
    def finished(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str) -> None:
        raise NotImplementedError


class RichProgressHandle(ProgressHandle):
    def __init__(self, progress: Progress, task_id: TaskID) -> None:
        self.progress = progress
        self.task_id = task_id

    def update(self, advance: int) -> None:
        self.progress.update(self.task_id, advance=advance)

    def finish(self) -> None:
        task = next(task for task in self.progress.tasks if task.id == self.task_id)
        if task.total is not None:
            self.progress.update(self.task_id, completed=task.total)
        self.progress.stop_task(self.task_id)


class RichUI(UserInterface):
    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()
        self.progress = Progress(
            SpinnerColumn(style=MINT),
            TextColumn("[bold #7fffd4]{task.description}"),
            BarColumn(bar_width=None, complete_style=MINT, finished_style=MINT, pulse_style=MINT_DIM),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=self.console,
            transient=False,
        )
        self._progress_started = False

    def ask_link(self) -> str:
        try:
            return Prompt.ask("[#7fffd4]Paste a MediaFire file or folder link[/#7fffd4]").strip()
        except EOFError:
            return ""

    def ask_save_dir(self, default: str) -> str:
        try:
            answer = Prompt.ask(
                "[#7fffd4]Where should files be saved?[/#7fffd4]",
                default=default,
            ).strip()
        except EOFError:
            return default
        return answer or default

    def status(self, message: str) -> None:
        self.console.print(Text(message, style=MINT))

    def show_plan(self, plan: DownloadPlan) -> None:
        kind = "folder" if plan.is_folder else "file"
        self.console.print(f"[#7fffd4]Found {kind}:[/#7fffd4] [bold]{plan.display_name}[/bold]")
        count = len(plan.files)
        label = "file" if count == 1 else "files"
        self.console.print(f"[#7fffd4]Found {count} {label}:[/#7fffd4]")
        self.console.print(build_file_tree(plan.files))

    def start_file(self, index: int, total: int, item: MediafireItem, size: int | None) -> ProgressHandle:
        if not self._progress_started:
            self.progress.start()
            self._progress_started = True
        description = f"Downloading {index} of {total}: {item.name}"
        task_id = self.progress.add_task(description, total=size)
        return RichProgressHandle(self.progress, task_id)

    def finished(self, path: str) -> None:
        if self._progress_started:
            self.progress.stop()
            self._progress_started = False
        table = Table.grid(padding=(0, 1))
        table.add_column(style=MINT)
        table.add_column()
        table.add_row("Finished.", path)
        self.console.print(Panel(table, border_style=MINT, box=box.ROUNDED))

    def warning(self, message: str) -> None:
        self.console.print(f"[yellow]{message}[/yellow]")

    def error(self, message: str) -> None:
        if self._progress_started:
            self.progress.stop()
            self._progress_started = False
        self.console.print(f"[bold red]Error:[/bold red] {message}")


def build_file_tree(files: Iterable[MediafireItem]) -> Tree:
    root = Tree("[bold]Files[/bold]", guide_style=MINT_DIM)
    folder_nodes: dict[PurePosixPath, Tree] = {PurePosixPath(): root}
    for item in sorted(files, key=lambda file: str(file.relative_path).lower()):
        current_path = PurePosixPath()
        current_node = root
        for part in item.relative_folder.parts:
            current_path = current_path / part
            if current_path not in folder_nodes:
                folder_nodes[current_path] = current_node.add(f"[#7fffd4]{part}/[/#7fffd4]")
            current_node = folder_nodes[current_path]
        current_node.add(item.name)
    return root
