# nodemon -V -w app.py -x python -m streamlit run app.py
LOGLEVEL=10 nodemon -V -w . -x python -m streamlit run $1
