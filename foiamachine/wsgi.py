import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "/home/ubuntu/foiamachine/lib/python2.7/site-packages")))

os.environ["DJANGO_SETTINGS_MODULE"] = "foiamachine.settings"

from django.core.wsgi import WSGIHandler
application = WSGIHandler()
