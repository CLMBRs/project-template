"""Utilities for making experiments reproducible."""

import importlib
import importlib.util
import logging
import random

logger = logging.getLogger(__name__)


def set_seed(seed: int) -> None:
    """Seed every available random number generator.

    Seeds Python's `random` module, plus NumPy and PyTorch if they are installed, so
    that this works whether or not the project depends on them.

    Args:
        seed: the random seed to use
    """
    random.seed(seed)
    # import optional libraries dynamically so they aren't required dependencies
    if importlib.util.find_spec("numpy") is not None:
        numpy = importlib.import_module("numpy")
        numpy.random.seed(seed)
    if importlib.util.find_spec("torch") is not None:
        torch = importlib.import_module("torch")
        torch.manual_seed(seed)
    logger.debug("Set random seed to %d", seed)
