import sys, os

INTERP = "/home/clientsdevs/virtualenv/kaaruj_venv/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

import Config.wsgi
application = Config.wsgi.application