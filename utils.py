from typing import Union


def parse_bool(val: Union[str, bool]) -> bool:
    """Parse a string to a boolean value."""
    if isinstance(val, bool):
        return val

    return val.lower() in ("yes", "true", "t", "y", "1")
