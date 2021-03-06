"""Fetch content from upload.

org ezbee_page.py.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-locals, too-many-return-statements, too-many-branches, too-many-statements
import base64
import inspect
import io

# pylint: disable=invalid-name
from functools import partial
from itertools import zip_longest

import hanzidentifier
import logzero
import numpy as np
import pandas as pd
import streamlit as st
from about_time import about_time

# from ezbee.gen_pairs import gen_pairs  # aset2pairs?
from aset2pairs import aset2pairs
from debee import debee  # noqa
from dzbee import dzbee  # noqa
from ezbee import ezbee  # noqa
from fastlid import fastlid
from icecream import ic
from loguru import logger as loggu
from logzero import logger
from set_loglevel import set_loglevel
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit import session_state as state

from litbee.color_map import color_map
from litbee.fetch_paste import fetch_paste
from litbee.fetch_upload import fetch_upload
from litbee.fetch_urls import fetch_urls
from litbee.t2s import t2s


def home():  # noqa
    """Run tasks.

    beetype

    sourcetype
        fetch_upload/fetch_paste, fetch_url
            sourcecount

    align: para-align/sent-align

    save xlsx/tsv
    """
    if state.ns.sourcetype not in ["upload", "paste", "urls"]:
        st.write("Coming soooooooon...")
        return None

    if state.ns.beetype not in ["ezbee", "dzbee", "debee"]:
        st.write("Coming soon...")
        return None

    # process sourcetype and fetch list1/list2
    list1 = list2 = []
    # fetch_upload/fetch_paste
    if state.ns.sourcetype in ["upload"]:
        fetch_upload()
    elif state.ns.sourcetype in ["paste"]:
        fetch_paste()
    elif state.ns.sourcetype in ["urls"]:
        fetch_urls()
    else:
        st.warning(f"{state.ns.sourcetype}: Not implemented")
        return None

    logger.debug("state.ns.updated: %s", state.ns.updated)

    # if not updated, quit: this does not quite work
    # only prevents the first run/missing upload
    if not state.ns.updated:
        logger.debug(" not updated, early exit.")
        return None

    list1 = state.ns.list1[:]
    list2 = state.ns.list2[:]

    logger.debug("list1[:3]: %s", list1[:3])
    logger.debug("list2[:3]: %s", list2[:3])

    df = pd.DataFrame(zip_longest(list1, list2, fillvalue=""))
    try:
        # df.columns = ["text1", "text2"]
        df.columns = [f"text{i + 1}" for i in range(len(df.columns))]
    except Exception as exc:
        logger.debug("df: \n%s", df)
        logger.error("%s", exc)

    state.ns.df = df
    logger.debug("df: %s", df)

    # st.table(df)  # looks alright
    # equiv to st.markdown(df.to_markdown())?

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

    # only show this for upload
    if state.ns.sourcetype in ["upload"]:
        _ = st.expander("to be aligned", expanded=False)
        with _:
            st.write(df)

    logger.info("Processing data... %s", state.ns.beetype)
    # if state.ns.beetype in ["ezbee", "dzbee"]:
    if state.ns.beetype in ["ezbee", "dzbee", "debee"]:
        # bug in json_de2zh.gen_cmat for dzbee and
        # fast_scores.gen_cmat  for ezbee
        # temp fix:
        if state.ns.beetype in ["dzbee"]:
            fastlid.set_languages = ["de", "zh"]
        elif state.ns.beetype in ["ezbee"]:
            fastlid.set_languages = ["en", "zh"]
        elif state.ns.beetype in ["debee"]:
            fastlid.set_languages = ["de", "en"]
        else:
            fastlid.set_languages = None

        fn = globals()[state.ns.beetype]
        # logger.debug("type(fn): %s", fn)
        # logger.debug("dir(fn): %s", dir(fn))
        # logger.debug("fn.__doc__: %s", fn.__doc__)
        logger.debug("fn.__name__: %s", fn.__name__)

        # from inspect import getabsfile
        # logger.debug("getabsfile(fn): %s", getabsfile(fn))

        # convert to simplified chinese if is_tranditional
        with about_time() as t:
            with st.spinner(" diggin..."):
                try:
                    # aset = ezbee/dzbee/debee
                    aset = globals()[state.ns.beetype](
                        t2s(list1),  # t2s, handle trand.chinese
                        t2s(list2),
                        # eps=eps,
                        # min_samples=min_samples,
                    )
                except Exception as e:
                    logger.exception(
                        "aset = globals()[state.ns.beetype](...) exc: %s", e
                    )
                    aset = ""
                    st.write("Collecting inputs...")
                    logger.debug("Collecting inputs...")
                    return None

        st.success(f"Done, took {t.duration_human}")

    else:
        try:
            filename = inspect.currentframe().f_code.co_filename  # type: ignore
        except Exception as e:
            logger.error(e)
            filename = ""
        try:
            lineno = inspect.currentframe().f_lineno  # type: ignore
        except Exception as e:
            logger.error(e)
            lineno = ""
        st.write(f"{state.ns.beetype} coming soon...{filename}:{lineno}")
        return None

    # fastlid changed logger.level to 20
    # turn back to loglevel
    logzero.loglevel(set_loglevel())
    if aset:
        logger.debug("aset: %s...%s", aset[:3], aset[-3:])
        # logger.debug("aset[:10]: %s", aset[:10])

    # st.write(aset)

    # aligned_pairs = gen_pairs(list1, list2, aset)
    aligned_pairs = aset2pairs(list1, list2, aset)
    if aligned_pairs:
        # logger.debug("%s...%s", aligned_pairs[:1], aligned_pairs[-1:])
        logger.debug("%s...s", aligned_pairs[:1])

    df_a = pd.DataFrame(
        aligned_pairs, columns=["text1", "text2", "llh"], dtype="object"
    )

    if set_loglevel() <= 10:
        _ = st.expander("done aligned")
        with _:
            st.table(df_a.astype(str))
            # st.markdown(df_a.astype(str).to_markdown())
            # st.markdown(df_a.astype(str).to_numpy().tolist())

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

    # st.write("editable aligned (double-click a cell to edit, drag column header to adjust widths)")
    _ = "editable aligned (double-click a cell to edit, drag column header to adjust widths)"
    with st.expander(_, expanded=False):
        ag_df = AgGrid(
            # df,
            df_a,
            gridOptions=gridOptions,
            key="outside",
            reload_data=True,
            editable=True,
            # width="100%",  # width parameter is deprecated
            height=750,
            # fit_columns_on_grid_load=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
        )

    # ### prep download

    # taken from vizbee cb_save_xlsx
    # subset = list(df_a.columns[2:3])  # 3rd col
    subset = list(df_a.columns[2:])  # 3rd col

    # pop("sn"): remove sn column
    df_a.pop("sn")
    s_df = df_a.astype(str).style.applymap(color_map, subset=subset)

    if set_loglevel() <= 10:
        logger.debug(" showing styled aligned")
    with st.expander("styled aligned"):
        # st.dataframe(s_df)  # can't handle styleddf
        st.table(s_df)

    output = io.BytesIO()
    with pd.ExcelWriter(
        output, engine="xlsxwriter"
    ) as writer:  # pylint: disable=abstract-class-instantiated
        s_df.to_excel(writer, index=False, header=False, sheet_name="Sheet1")
        writer.sheets["Sheet1"].set_column("A:A", 70)
        writer.sheets["Sheet1"].set_column("B:B", 70)
    output.seek(0)

    val = output.getvalue()
    b64 = base64.b64encode(val)
    filename = ""
    if state.ns.src_filename:
        filename = f"{state.ns.src_filename}-"

    dl_xlsx = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}aligned_paras.xlsx">Download aligned paras xlsx</a>'

    _ = """
    output = io.BytesIO()
    # df_a.astype(str).to_csv(output, sep="\t", index=False, header=False, encoding="gbk")
    df_a.astype(object).to_csv(output, sep="\t", index=False, header=False, encoding="gbk")
    output.seek(0)

    val = output.getvalue()
    b64 = base64.b64encode(val)
    dl_tsv = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}aligned_paras.tsv">Download aligned paras tsv</a>'
    # """

    col1_dl, col2_dl = st.columns(2)
    with col1_dl:
        st.markdown(dl_xlsx, unsafe_allow_html=True)
    _ = """
    with col2_dl:
        st.markdown(dl_tsv, unsafe_allow_html=True)
    # """

    # reset
    state.ns.updated = False

    return None
