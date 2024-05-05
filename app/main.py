"""
Start of the code execution.
"""

import asyncio
from app.arm_movement import moving_arm
from app.logger import get_logger
from app.exceptions import EncoderError, MotorError

logger = get_logger(__name__)


async def main():
    """
    Create a coroutine that moves the arm in the specific direction and distance.

    As moving_arm  should have only distance and direction as function arguments,
    I assume that the system has only 1 arm, otherwise it should have some kind of
    arm identification as a function argument.
    """
    try:
        task1 = asyncio.create_task(moving_arm(1, 5))
        await task1
    except (EncoderError, MotorError) as e:
        logger.error(e)


if __name__ == "__main__":
    asyncio.run(main())
