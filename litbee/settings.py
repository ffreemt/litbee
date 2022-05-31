"""Prep Settings/Options page."""
# pylint: disable=invalid-name
from functools import partial
import streamlit as st
from loguru import logger as loggu
from logzero import logger
from streamlit import session_state as state


def settings():
    """Prep  Settings/Options page.

    Refer to options.py"""
    # horizotal radio
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )

    sourcetype_list = ["upload", "paste", "urls"]
    beetype_list = ["ezbee", "dzbee", "debee", "xbee"]

    # col1, col2 = st.columns([24, 21])  # 4*6, 3*7
    # col1, col2 = st.columns(2)

    # with col1:
    try:
        index = beetype_list.index(state.ns.beetype)
    except Exception as e:
        logger.error("beetype index error: %s, setting to 0", e)
        index = 0
    beetype = st.radio(
        "Pick a bee",
        beetype_list,
        index=index,
        format_func=lambda x: f"{x:<7} |",
        help="ezbee: english-chinese; dzbee: german-chinese, debee: german-english",
    )
    state.ns.beetype = beetype

    # with col2:
    try:
        index = sourcetype_list.index(state.ns.sourcetype)
    except Exception as e:
        logger.error("sourcetype index error: %s, setting to 0", e)
        index = 0
    sourcetype = st.radio(
        "Source",
        sourcetype_list,
        index=index,
        format_func=lambda x: f"{x:<8} |",
        help="upload: one or two files; paste: from clipboard; urls: from the net",
        disabled=True,
    )
    state.ns.sourcetype = sourcetype

    sourcecount_list = [2, 1]
    try:
        index = sourcecount_list.index(state.ns.sourcecount)
    except Exception as e:
        logger.error("sourcecount index error: %s, setting to 0", e)
        index = 0
    sourcecount = st.radio(
        "Source Count",
        sourcecount_list,
        index=index,
        format_func=lambda x: f"{x:<3} |",
        help="2: two separate sources (files/paste/urls), each containing one language; 1: one mixed source (file/pate/url) containing both languages",
        disabled=True,
    )
    state.ns.sourcecount = sourcecount

    # show state.ns[:6]
    loggu.debug(f" state.ns.list: {state.ns.list}")

    # beetype, sourcetype, sourcecount, filename1, filename2
    _ = map(partial(getattr, state.ns), state.ns.list[:5])
    logger.debug(" state.ns.list[:3]: %s", str([*_]))

    # st.write(f"run: {state.ns.count}")
    # loggu.debug(f"run: {state.ns.count}")
