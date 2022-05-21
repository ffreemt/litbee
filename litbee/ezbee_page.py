"""Display ezbee page."""
import streamlit as st
import pandas as pd

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


def ezbee_page():
    """Display ezbee page."""
    # st.title('ezbee')
    # st.write('### ezbee')
    # st.write('Welcome to app1')

    try:
        df = st.session_state.ns.df
    except Exception as exc:
        logger.error(exc)
        df = pd.DataFrame([[""]])

    # st.table(df)  # looks alright

    # stlyed pd dataframe?
    # bigger, no pagination
    # st.markdown(df.to_html(), unsafe_allow_html=True)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    options = {
        "resizable": True,
        "autoHeight": True,
        "wrapText": True,
        "editable": True,
    }
    gb.configure_default_column(**options)
    gridOptions = gb.build()

    # ag_grid smallish, editable, probably slower

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

    st.write("double-click a cell to edit")
    agdf = AgGrid(
        df,
        # fit_columns_on_grid_load=True,
        editable=True,
        gridOptions=gridOptions,
        key="outside"
    )