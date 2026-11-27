from collections.abc import Iterable
from difflib import get_close_matches


def suggest_commands(
    user_command: str,
    available_commands: Iterable[str],
    *,
    limit: int = 3,
    cutoff: float = 0.55,
) -> list[str]:
    #Suggestion of closest valid commands when user enters an unknown command.
    cleaned = user_command.strip().casefold()
    if not cleaned:
        return []
    return get_close_matches(cleaned, list(available_commands), n=limit, cutoff=cutoff)
