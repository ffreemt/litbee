import streamlit as st
from install import install

install("logzero")
from logzero import logzero

logger.info("streamlit version: %s", st.__version__)

x = st.slider('Select a value')
st.write(x, 'squared is', x * x)
st.write(" streamlit version", st.__version__)
