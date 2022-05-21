"""Prep __main__.py."""
# pylint: disable=invalid-name
import os
from pathlib import Path
from typing import Optional

import pandas as pd

import streamlit as st
from streamlit import session_state as state
from types import SimpleNamespace

import logzero
from logzero import logger
from set_loglevel import set_loglevel

from litbee import __version__, litbee
from litbee.files2df import files2df
from litbee.utils import sb_front_cover, instructions, menu_items
from litbee.ezbee_page import ezbee_page
from litbee.dzbee_page import dzbee_page
from litbee.xbee_page import xbee_page

os.environ["TZ"] = "Asia/Shanghai"
os.environ["LOGLEVEL"] = "10"
logzero.loglevel(set_loglevel())

st.set_page_config(
    page_title=f"litbee v{__version__}",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",  # "auto" or "expanded" or "collapsed",
    menu_items=menu_items,
)

pd.set_option("precision", 2)
pd.options.display.float_format = "{:,.2f}".format


if "ns" not in state:
    state.ns = SimpleNamespace()


def main():
    # instructions()

    sb_front_cover()

    try:
        _ = state.ns.df
        state.ns.count += 1
        logger.debug(" run: %s", state.ns.count)
    except AttributeError:
        logger.debug("first run")
        # df = files2df("data/en.txt", "data/zh.txt")
        df = files2df("data/test_en.txt", "data/test_zh.txt")
        state.ns.count = 1
        state.ns.df = df

    # multi-page setup
    menu = {
        "ezbee": ezbee_page,
        "dzbee": dzbee_page,
        "xbee": xbee_page,
    }
    selection = st.sidebar.radio("", menu)
    page = menu[selection]

    # page.app()
    page()

    # 'items', 'keys', values, 'to_dict', 'update', 'values'
    # logger.debug("state.ns: %s", state.ns)

    st.write(f"run: {state.ns.count}")
    # st.dataframe(state.ns.df)

    # st.markdown(html_string, unsafe_allow_html=True)
    # st.markdown(state.ns.df.to_html(), unsafe_allow_html=True)


main()
