from typing import Callable


def input_error(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            name = e.args[0] if e.args else ""
            return f"Contact {name} does not exist"
        except IndexError:
            return "Please enter the required arguments"

    return inner
