cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"
source .venv/bin/activate
python3 -O modules/fixer.py
deactivate