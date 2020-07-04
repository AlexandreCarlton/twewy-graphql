#!/usr/bin/env python

from twewy.app import app
from twewy.database import init_db
init_db()
app.run()
