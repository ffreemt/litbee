"""Present info about litbee."""
from textwrap import dedent

import debee
import dzbee
import ezbee
import streamlit as st

from litbee import __version__

# from litbee.utils import style_css

msg = dedent(
    f"""
    (ezbee {ezbee.__version__}, dzbee {dzbee.__version__}, debee {debee.__version__})
    <div class="text">
    <ul>
    <li> ezbee: english-chinese, fast para-align

    <li> dzbee: german-chinese, fast para-align

    <li> debee: german-english, fast para-align

    <li> xbee/bumblebee: other language pairs, normal para-align
    </ul>

    The algorithm for fast para-align is home-brewn. Two
    sent-align algorithms are used: one based on Gale-Church,
    the other machine learning.
    </div>
    """
).strip()


def info():
    """Prep info page."""
    _ = """
    st.markdown(f"### litbee {__version__} ")

    # sb_tit_expander = st.sidebar.expander("More info (click to toggle)", expanded=False)
    # _ = st.expander("More info (click to toggle)", expanded=False)
    _ = st.expander("Click to toggle", expanded=True)
    with _:
        st.markdown(msg)
    # """

    # st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # st.markdown(f"<style>{style_css}</style>", unsafe_allow_html=True)

    # st.subheader("Intro")

    st.subheader(f"litbee {__version__}")

    st.markdown(msg, unsafe_allow_html=True)
