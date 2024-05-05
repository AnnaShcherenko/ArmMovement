from app.arm_parts import ArmMotor, ArmEncoder, ArmMicroSwitch
from app.interfaces import Motor, Encoder, MicroSwitch


def test_protocol():
    assert issubclass(ArmMotor, Motor)
    assert issubclass(ArmEncoder, Encoder)
    assert issubclass(ArmMicroSwitch, MicroSwitch)
