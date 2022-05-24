"""Fetch content from upload.

org ezbee_page.py.
"""
from functools import partial
from itertools import zip_longest

import logzero
import pandas as pd
import streamlit as st
from ezbee import ezbee
from dzbee import dzbee
from ezbee.gen_pairs import gen_pairs  # aset2pairs?
from loguru import logger as loggu
from logzero import logger
from set_loglevel import set_loglevel
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit import session_state as state

logzero.loglevel(set_loglevel())


def fetch_upload():
    """Fetch content from upload."""

    # src_fileio tgt_fileio
    sb_pick_files = st.sidebar.expander("Pick two files", expanded=True)
    with sb_pick_files:
        src_fileio = st.file_uploader(
            "Choose source file (utf8 txt)",
            type=[
                "txt",
            ],
            key="src_text",
            # accept_multiple_files=True,
            # accept_multiple_files=False,
        )

        tgt_fileio = st.file_uploader(
            "Choose target file (utf8 txt)",
            type=[
                "txt",
            ],
            key="tgt_text",
            # accept_multiple_files=True,
        )

    # logger.debug(" len(src_fileio): %s", len(src_fileio))
    # logger.debug(" len(tgt_fileio): %s", len(tgt_fileio))

    if src_fileio:
        logger.debug(" type(src_fileio): %s", type(src_fileio))
        if isinstance(src_fileio, list):
            logger.debug(" len(src_fileio): %s", len(src_fileio))
            logger.debug("src_fileio[-1].name: [%s]", src_fileio[-1].name)
            filenames = [elm.name for elm in src_fileio]
            logger.debug("src_fileio  names: %s", filenames)

            # state.ns.src_fileio = src_fileio
            state.ns.src_file = src_fileio[-1].getvalue().decode()
            state.ns.src_filename = src_fileio[-1].name
        else:
            logger.debug("src_fileio.name: [%s]", src_fileio.name)
            filenames = [src_fileio.name]
            logger.debug("src_fileio  names: %s", filenames)

            # state.ns.src_fileio = src_fileio
            state.ns.src_file = src_fileio.getvalue().decode()
            state.ns.src_filename = src_fileio.name

    if tgt_fileio:
        if isinstance(tgt_fileio, list):
            logger.warning("not set to handle multiple files")
            logger.warning("set accept_multiple_files=False in the meantime")
        else:
            state.ns.tgt_file = tgt_fileio.getvalue().decode()
            state.ns.tgt_filename = tgt_fileio.name

    try:
        _ = state.ns.src_file.splitlines()
        list1 = [elm.strip() for elm in _ if elm.strip()]
        _ = state.ns.tgt_file.splitlines()
        list2 = [elm.strip() for elm in _ if elm.strip()]
    except Exception as exc:
        logger.error(exc)
        list1 = [""]
        list2 = [""]
    state.ns.list1 = list1[:]
    state.ns.list2 = list2[:]

    df = pd.DataFrame(zip_longest(list1, list2, fillvalue=""))
    try:
        df.columns = ["text1", "text2"]
    except Exception as exc:
        logger.debug("df: \n%s", df)
        logger.error("%s", exc)

    state.ns.df = df
    logger.debug("df: %s", df)

    # st.table(df)  # looks alright

    # stlyed pd dataframe?
    # bigger, no pagination
    # st.markdown(df.to_html(), unsafe_allow_html=True)

    # ag_grid smallish, editable, probably slower

    # if "df" not in globals() or "df" not in locals():
    if "df" not in locals():
        logger.debug(" df not defined, return")

    if df.empty:
        logger.debug(" df.empty, return")
        return None

    # df = pd.DataFrame([["", "", ""]], columns=["text1", "text2", "llh"])

    df_exp = st.expander("to be aligned", expanded=False)
    with df_exp:
        st.write(df)  # too small

    _ = """
    ag_exp = st.expander("done aligned")  # , expanded=False
    with ag_exp:
        agdf = AgGrid(
            df,
            # fit_columns_on_grid_load=True,
            editable=True,
            gridOptions=gridOptions,
            key="ag_exp",
        )
    # """

    list1 = [elm.strip() for elm in df.text1 if elm.strip()]
    list2 = [elm.strip() for elm in df.text2 if elm.strip()]
    logger.debug("list1[:3]: %s", list1[:3])
    logger.debug("list2[:3]: %s", list2[:3])

    logger.info("Processing data... %s", state.ns.beetype)
    if state.ns.beetype in ["ezbee", "dzbee"]:
        try:
            # aset = ezbee(
            aset = globals()[state.ns.beetype](
                list1,
                list2,
                # eps=eps,
                # min_samples=min_samples,
            )
        except Exception as e:
            # logger.error("aset = ezbee(...) exc: %s", e)
            logger.error("aset = globals()[state.ns.beetype](...) exc: %s", e)
            aset = ""
            # st.write(e)
            st.write("Collecting inputs...")
            return None
    else:
        st.write(f"{state.ns.beetype} coming soon...")
        return None

    # fastlid changed logger.level is changed to 20
    # turn back to loglevel
    logzero.loglevel(set_loglevel())
    if aset:
        logger.debug("aset: %s...%s", aset[:3], aset[-3:])
        # logger.debug("aset[:10]: %s", aset[:10])

    # st.write(aset)

    aligned_pairs = gen_pairs(list1, list2, aset)
    if aligned_pairs:
        logger.debug("%s...%s", aligned_pairs[:3], aligned_pairs[-3:])
        # logger.debug("aligned_pairs[:20]: \n%s", aligned_pairs[:20])

    df_a = pd.DataFrame(aligned_pairs, columns=["text1", "text2", "llh"])

    # insert seq no
    df_a.insert(0, "sn", range(len(df_a)))

    gb = GridOptionsBuilder.from_dataframe(df_a)
    gb.configure_pagination(paginationAutoPageSize=True)
    options = {
        "resizable": True,
        "autoHeight": True,
        "wrapText": True,
        "editable": True,
    }
    gb.configure_default_column(**options)
    gridOptions = gb.build()

    st.write("aligned (double-click a cell to edit, drag column header to adjust widths)")
    agdf = AgGrid(
        # df,
        df_a,
        gridOptions=gridOptions,
        key="outside",
        editable=True,
        # width="100%",  # width parameter is deprecated
        height=500,
        # fit_columns_on_grid_load=True,
    )
