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
    col1, col2 = st.columns(2)

    with col1:
        try:
            index = beetype_list.index(state.ns.beetype)
        except Exception as e:
            logger.error("beetype index error: %s, setting to 0", e)
            index = 0
        beetype = st.radio(
            "Pick a bee",
            beetype_list,
            index=index,
            format_func=lambda x: f"{x:<7}|",
        )
        state.ns.beetype = beetype
    with col2:
        try:
            index = sourcetype_list.index(state.ns.sourcetype)
        except Exception as e:
            logger.error("sourcetype index error: %s, setting to 0", e)
            index = 0
        sourcetype = st.radio(
            "Source",
            sourcetype_list,
            index=index,
            format_func=lambda x: f"{x:<8}|"
        )
        state.ns.sourcetype = sourcetype

    # show state.ns[:6]
    loggu.debug(f" state.ns.list: {state.ns.list}")

    # beetype, sourcetype, filename1, filename2
    _ = map(partial(getattr, state.ns), state.ns.list[:4])
    logger.debug(" state.ns.list[:3]: %s", str([*_]))

    # st.write(f"run: {state.ns.count}")
    # loggu.debug(f"run: {state.ns.count}")
