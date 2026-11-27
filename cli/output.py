from collections.abc import Iterable
from rich.console import Console, RenderableType
from rich.table import Table

console = Console()


def display(content: RenderableType):
    console.print(content)


def build_table(title, columns, rows) -> Table:
    table = Table(title=title, show_header=True, header_style="bold cyan")

    for col in columns:
        table.add_column(col)

    for row in rows:
        table.add_row(*row)

    return table