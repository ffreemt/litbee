"""Prep __main__.py."""
# pylint: disable=invalid-name
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

import logzero
import streamlit as st
from logzero import logger
from set_loglevel import set_loglevel
from streamlit import session_state as state

from litbee import __version__, litbee
from litbee.files2df import files2df

os.environ["TZ"] = "Asia/Shanghai"
os.environ["LOGLEVEL"] = "10"
logzero.loglevel(set_loglevel())

if "ns" not in state:
    state.ns = SimpleNamespace()


def main():
    logger.debug("state: %s", state)

    df = files2df("data/test_en.txt", "data/test_zh.txt")
    state.ns.df = df
    logger.debug("state: %s", state)


main()
