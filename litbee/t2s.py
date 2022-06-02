"""Convert list to simlified Chinese for traditional Chinese, do nothing otherwise."""
# pylint: disable=invalid-name
from typing import List
import hanzidentifier
from logzero import logger
from opencc import OpenCC

convert = OpenCC('t2s').convert


def t2s(lst: List[str]) -> List[str]:
    """Convert list to simlified Chinese for traditional Chinese, do nothing otherwise.

    Args:
        list of strings

    Returns:
        list of strings
    """
    try:
        # lst[:1000] strim down for extremely large docs
        _ = hanzidentifier.identify(" ".join(lst[:1000]))
    except Exception as e:
        logger.warning("hanzidentifier.is_traditional error: %s, settin to simplified.", e)
        _ = hanzidentifier.SIMP  # 2: simplified

    if _ not in [hanzidentifier.TRAD, hanzidentifier.MIXED]:
        return lst

    res = []
    for line in lst:
        try:
            _ = convert(line)
        except Exception as e:
            logger.warning("ts2 error: %s, setting to original", e)
            _ = line
        res.append(_)

    return res
