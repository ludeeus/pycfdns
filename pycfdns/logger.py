"""Common logger for pycfdns."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)
__all__ = ["LOGGER"]
