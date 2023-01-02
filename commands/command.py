from typing import Callable, Optional
from discord import interactions

class Command:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.fn: Optional[Callable] = None

    def func(self, fn: Callable[[interactions.Interaction, ], None]):
        self.fn = fn
