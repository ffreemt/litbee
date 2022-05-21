# pip install pipx
# pipx install poetry
# pipx ensurepath
# source ~/.bashrc

# curl -sSL https://install.python-poetry.org | python3 -
# -C- continue -S show error -o output
curl -sSL -C- -o install-poetry.py  https://install.python-poetry.org
python install-poetry.py
~/.local/bin/poetry install
