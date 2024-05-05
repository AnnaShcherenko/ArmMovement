import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.arm_movement import moving_arm, distance_travel, check_encoder_status
from app.exceptions import EncoderError, MotorError


@pytest.mark.asyncio
@patch("app.arm_movement.distance_travel")
@patch("app.arm_movement.motor_work")
async def test_arm_movement(mock_motor_work, mock_distance_travel):

    await moving_arm(1, 2)

    mock_motor_work.assert_called_once()
    mock_motor_work.return_value.__aenter__.assert_called_once()
    mock_motor_work.return_value.__aexit__.assert_called_once()
    mock_distance_travel.assert_called_once()


@pytest.mark.asyncio
@patch("app.arm_movement.distance_travel")
@patch("app.arm_movement.motor_work")
async def test_arm_movement_motorerror(mock_motor_work, mock_distance_travel):

    mock_motor_work.side_effect = MotorError

    with pytest.raises(MotorError):
        await moving_arm(1, 2)

        mock_motor_work.assert_called_once()
        mock_motor_work.return_value.__aenter__.assert_called_once()
        mock_motor_work.return_value.__aexit__.assert_not_called()
        mock_distance_travel.assert_not_called()


@pytest.mark.asyncio
@patch("app.arm_movement.distance_travel")
@patch("app.arm_movement.ArmMotor")
async def test_context_manager(mock_motor, mock_distance_travel):

    mock_motor.on = AsyncMock()
    mock_motor.off = AsyncMock()

    mock_distance_travel.side_effect = EncoderError()

    with pytest.raises(EncoderError):
        await moving_arm(1, 2)

    mock_motor.on.assert_called_once()
    mock_motor.off.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "encoder_status, switch_status, motor_distance, target_distance, expected_calls",
    [
        ([0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [5, 10, 15, 20], 20, 4),
        ([0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [5, 10, 15, 20], 15, 3),
        ([0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [5, 10, 15, 20], 20, 3),
    ],
)
@patch("app.arm_movement.check_encoder_status")
@patch("app.arm_movement.ArmMicroSwitch")
@patch("app.arm_movement.ArmEncoder")
async def test_distance_travel(
    mock_encoder,
    mock_switch,
    mock_check_encoder_status,
    encoder_status,
    switch_status,
    motor_distance,
    target_distance,
    expected_calls,
):

    mock_encoder.status = AsyncMock(side_effect=encoder_status)
    mock_switch.status = AsyncMock(side_effect=switch_status)
    mock_check_encoder_status.side_effect = motor_distance

    await distance_travel(target_distance)

    mock_encoder.status.call_count == expected_calls + 1
    mock_switch.status.call_count == expected_calls
    mock_check_encoder_status.call_count == expected_calls


@pytest.mark.asyncio
@patch("app.arm_movement.check_encoder_status")
@patch("app.arm_movement.ArmMicroSwitch")
@patch("app.arm_movement.ArmEncoder")
async def test_distance_travel_encoder_error(
    mock_encoder, mock_switch, mock_check_encoder_status
):

    mock_encoder.status = AsyncMock(return_value=0)
    mock_check_encoder_status.side_effect = EncoderError

    with pytest.raises(EncoderError):
        await distance_travel(20)

    mock_encoder.status.call_count == 2
    mock_switch.status.call_count == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "encoder_status, encoder_previous_status, motor_distance, result",
    [(0, 1, 0, 5), (1, 0, 5, 10), (1, 1, 5, EncoderError)],
)
async def test_check_encoder_status(
    encoder_status, encoder_previous_status, motor_distance, result
):

    if result == EncoderError:
        with pytest.raises(EncoderError):
            await check_encoder_status(
                encoder_status, encoder_previous_status, motor_distance
            )
    else:
        assert (
            await check_encoder_status(
                encoder_status, encoder_previous_status, motor_distance
            )
            == result
        )
