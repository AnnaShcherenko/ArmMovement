"""
Exceptions for the app.
"""


class EncoderError(Exception):
    """
    Exception raised when the encoder is not working properly.
    """

    def __init__(self):
        super().__init__("Encoder error: encoder doesn't respond")


class SwitchError(Exception):
    """
    Exception raised when the switch is not working properly.
    """

    def __init__(self):
        super().__init__("Switch error: switch doesn't respond")


class MotorError(Exception):
    """
    Exception raised when the motor is not working properly.
    """

    def __init__(self):
        super().__init__("Motor error: motor doesn't respond")


class ComponentError(Exception):
    """
    Exception raised when components doesn't respond.
    """

    def __init__(self):
        super().__init__("Component error: components doesn't respond during 3 seconds")
