cd "$( dirname $0 )"
source .venvu/bin/activate
python3 -O modules/comparer.py
deactivate