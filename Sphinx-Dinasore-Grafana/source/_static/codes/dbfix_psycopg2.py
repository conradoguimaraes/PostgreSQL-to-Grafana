
import logging
import os

import sys
import argparse
import traceback

try:
    import psycopg2
except:
    try:
        import pip
        pip.main(['install', 'psycopg2'])
        os.system('cls')
    except:
        print(traceback.format_exc())


sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from communication import tcp_server
from core import manager

if __name__ == "__main__":
    print("Running Dinasore...\n")
    ...
    ...
    ...
    ...
    ...