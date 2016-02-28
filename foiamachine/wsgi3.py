import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "/home/ubuntu/foiamachine/lib/python2.7/site-packages")))

os.environ["DJANGO_SETTINGS_MODULE"] = "foiamachine.settings"

from django.core.wsgi import WSGIHandler


class Debugger:

    def __init__(self, object):
        self.__object = object

    def __call__(self, *args, **kwargs):
        import pdb
        debugger = pdb.Pdb()
        debugger.use_rawinput = 0
        debugger.reset()
        sys.settrace(debugger.trace_dispatch)

        try:
            return self.__object(*args, **kwargs)
        finally:
            debugger.quitting = 1
            sys.settrace(None)


application = Debugger(WSGIHandler())
