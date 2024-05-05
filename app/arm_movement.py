"""
Moving arm:
           - Motor
           - Encoder : 0 or 1 every 5 degree
           - Switch : is 1 at the end of each direction
"""

import asyncio
from typing import Literal
from contextlib import asynccontextmanager
from app.arm_parts import ArmMotor, ArmEncoder, ArmMicroSwitch
from app.logger import get_logger
from app.exceptions import EncoderError, MotorError

logger = get_logger(__name__)
arm_lock = asyncio.Lock()

MAX_RETRIES = 3


@asynccontextmanager
async def motor_work(direction: Literal[1, 2]):
    """
    Context manager to on and off the motor.
    """
    try:
        await ArmMotor.on(direction)
        yield ArmMotor
    except MotorError as e:
        raise MotorError() from e
    finally:
        await ArmMotor.off()


async def check_encoder_status(
    encoder_status: Literal[0, 1],
    encoder_previous_status: Literal[0, 1],
    motor_distance: int,
) -> int:
    """
    Check the encoder status.
    """
    if encoder_status != encoder_previous_status:
        motor_distance += 5
        logger.debug("Motor distance: %s", motor_distance)
    else:
        raise EncoderError()
    return motor_distance


async def distance_travel(motor_target_distance: int) -> None:
    """
    Check the distance travelled by the motor.
    """

    encoder_previous_status = await ArmEncoder.status()
    motor_distance = 0

    while motor_distance < motor_target_distance:
        await asyncio.sleep(0.1)
        encoder_status = await ArmEncoder.status()
        motor_distance = await check_encoder_status(
            encoder_status, encoder_previous_status, motor_distance
        )

        if await ArmMicroSwitch.status() == 1:
            logger.debug("Switch status is 1: end of the direction")
            return

        encoder_previous_status = encoder_status


async def moving_arm(direction: Literal[1, 2], distance: int) -> None:
    """
    Every 20 degrees of motor turn, the distance traveled is 1 unit of range.

    Arm_lock is used to prevent the simultaneous execution of the Arm which
    can lead to race condition.
    """
    async with arm_lock:

        motor_target_distance = 20 * distance

        async with motor_work(direction):
            logger.info("Arm movement is started")
            await distance_travel(motor_target_distance)

        logger.info("Arm movement is stopped")
