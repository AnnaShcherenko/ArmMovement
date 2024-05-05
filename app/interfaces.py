"""
Interfaces for Motor, Encoder and Switch
"""

from typing import Literal, Protocol, runtime_checkable


@runtime_checkable
class Motor(Protocol):
    """
    Interface defines the motor rotation in different directions:
    1 - left;
    2 - right.
    """

    async def on(self, direction: int) -> None:
        """
        Motor begins to rotate in the specific direction.
        """

    async def off(self) -> None:
        """
        Motor stops behaviour
        """


@runtime_checkable
class Encoder(Protocol):
    """
    Interface defines the encoder reading
    """

    async def status(self) -> Literal[0, 1]:
        """
        Returns the current state of the encoder.
        The changing fom 0 to 1 and vice versa means that the motor has rotated 5 degrees.
        """


@runtime_checkable
class MicroSwitch(Protocol):
    """
    Interface defines the switch behaviour
    """

    async def status(self) -> Literal[0, 1]:
        """
        Returns the current state of the switch.
        The changing fom 0 to 1 means that the motor has reached the end of the direction.
        """
