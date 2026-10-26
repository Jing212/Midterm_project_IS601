
"""Register commands and maintain the command registry."""
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class CommandInfo:
    """Store metadata and handler for a registered command."""
    name: str
    description: str
    handler: Callable


COMMAND_REGISTRY: dict[str, CommandInfo] = {}


def register_command(name: str, description: str):
    """Register a command using a decorator."""

    def decorator(func):
        if name in COMMAND_REGISTRY:
            raise ValueError(
                f"Command '{name}' is already registered."
            )

        COMMAND_REGISTRY[name] = CommandInfo(
            name=name,
            description=description,
            handler=func,
        )

        return func

    return decorator
