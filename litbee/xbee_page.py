"""Display xbee page."""
import streamlit as st
import pandas as pd


def xbee_page():
    """Display xbee page."""
    # st.title('dzbee')
    st.write('Coming soon')

    try:
        df = st.session_state.ns.df
    except Exception as exc:
        logger.error(exc)
        df = pd.DataFrame([[""]])

    # st.table(df)
