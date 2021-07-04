import sys

from pymodm import connect

from server.config import CONFIG

config_name = "prod"

if len(sys.argv) > 1:
    config_name = sys.argv[1]

database_url = CONFIG[config_name].DATABASE_URI

connect(database_url)
