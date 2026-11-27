from typing import Callable


def input_error(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"[bold red]Error:[/bold red] {e}"
        except KeyError as e:
            name = e.args[0] if e.args else ""
            return f"[bold red]Error:[/bold red] Contact '{name}' does not exist."
        except IndexError:
            return "[bold yellow]Warning:[/bold yellow] Please enter the required arguments."

    return inner
