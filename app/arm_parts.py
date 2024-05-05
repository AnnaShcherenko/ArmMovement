"""
Classes that simulate the behaviour of the motor, encoder and microswitch of the arm.
Are subclasses of the Motor, Encoder and MicroSwitch interfaces.

As the motor, encoder and microswitch are related to the arm,
the classes are named ArmMotor, ArmEncoder and ArmMicroSwitch and they 
implemnents static methods which characterize all instances of the class.
"""

from typing import Literal
from app.logger import get_logger

logger = get_logger(__name__)


class ArmMotor:
    """
    Class simulates the motor behaviour
    """

    @staticmethod
    async def on(direction: int) -> None:
        """
        Arm motor begins to rotate in the specific direction.
        """
        logger.info("Motor is rotating in direction %s ", direction)

    @staticmethod
    async def off() -> None:
        """
        Arm motor stops rotating.
        """
        logger.info("Motor is stopped")


class ArmEncoder:
    """
    Class simulates the encoder behaviour
    """

    _state: int = 0

    @staticmethod
    async def status() -> Literal[0, 1]:
        """
        Every call change the value from 0 to 1 and vice versa.
        Encoder changes the status 10 times per second.
        """
        ArmEncoder._state = 1 - ArmEncoder._state
        return ArmEncoder._state


class ArmMicroSwitch:
    """
    Class simulates the switch behaviour
    """

    @staticmethod
    async def status() -> Literal[0, 1]:
        """
        As I don't know when the motor reaches the end of the direction,
        it always returns 0 for test purposes.
        """
        # return 0 if random.random() > 0.1 else 1
        return 0
