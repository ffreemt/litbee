"""Prep Settings/Options page."""
# pylint: disable=invalid-name
from functools import partial

import streamlit as st
from loguru import logger as loggu
from logzero import logger
from streamlit import session_state as state


def settings():
    """Prep Settings/Options page.

    Refer to options.py
    """
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
    _ = "ezbee: english-chinese; dzbee: german-chinese, debee: german-english; xbee: other language pairs (slow, approx.1000 pairs/3 min) | ezbee: 英/中; dzbee: 德/中, debee: 德/英; xbee: 其他语言对（慢, 约1000对/3分钟）"
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
        help=_,
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
        help="2: two separate sources (files/pastes/urls), each containing one language; 1: one mixed source (file/paste/url) containing both languages",
        disabled=True,
    )
    state.ns.sourcecount = sourcecount

    sentali_list = [None, "fast", "slow"]
    try:
        index = sentali_list.index(state.ns.sentali)
    except Exception as e:
        logger.error("sentali index error: %s, setting to 0", e)
        index = 0
    sentali = st.radio(
        "Sent Align",
        sentali_list,
        index=index,
        format_func=lambda x: f"{str(x):<4} |",
        help="None: no sent align; fast: gale-church; slow: machine-learning",
        disabled=True,
    )
    state.ns.sentali = sentali

    # show state.ns[:6]
    loggu.debug(f" state.ns.list: {state.ns.list}")

    # beetype, sourcetype, sourcecount, filename1, filename2
    _ = map(partial(getattr, state.ns), state.ns.list[:6])
    logger.debug(" state.ns.list[:3]: %s", str([*_]))

    # st.write(f"run: {state.ns.count}")
    # loggu.debug(f"run: {state.ns.count}")
