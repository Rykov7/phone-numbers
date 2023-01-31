cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"
source .venvu/bin/activate
python3 -O modules/fixer.py
deactivate