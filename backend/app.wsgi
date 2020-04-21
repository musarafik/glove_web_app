activate_this = '/home/ubuntu/glove_web_app/backend/venv/bin/activate_this.py'

with open(activate_this) as f:
	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/glove_web_app/backend")

from app import app as application

