"""Display dzbee page."""
import streamlit as st
import pandas as pd


def dzbee_page():
    """Display dzbee page."""
    # st.title('dzbee')
    # st.write('Welcome to app1')

    try:
        df = st.session_state.ns.df
    except Exception as exc:
        logger.error(exc)
        df = pd.DataFrame([[""]])

    st.table(df)
