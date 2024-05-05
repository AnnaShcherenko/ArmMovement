import time
import asyncio

from app.logger import get_logger
from app.arm_movement import moving_arm

logger = get_logger(__name__)


async def mock_function():
    for i in range(5):
        logger.debug("Mock function step %s: ", i)
        await asyncio.sleep(0.1)


async def mock_main():
    try:
        task1 = asyncio.create_task(mock_function())
        task2 = asyncio.create_task(moving_arm(1, 2))
        await task1
        await task2
    except Exception as e:
        logger.error(e)


async def mock_two_arms():
    try:
        task1 = asyncio.create_task(moving_arm(1, 2))
        task2 = asyncio.create_task(moving_arm(2, 2))
        await task1
        await task2
    except Exception as e:
        logger.error(e)


def test_two_arms():
    start_time = time.time()
    asyncio.run(mock_two_arms())
    assert time.time() - start_time > 1.5


def test_two_controllers():
    start_time = time.time()
    asyncio.run(mock_main())

    assert time.time() - start_time < 1.5
