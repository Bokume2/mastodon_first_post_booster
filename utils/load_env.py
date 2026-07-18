from datetime import timedelta
from os import environ
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../settings/.env")
load_dotenv(dotenv_path, verbose=True)

BASE_URL = environ["BASE_URL"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]

MAX_FOLLOWERS = int(environ["MAX_FOLLOWERS"])
if MAX_FOLLOWERS < 0:
    raise ValueError("MAX_FOLLOWERSが負の値に設定されています")
MAX_BOOST_DAYS = timedelta(days=int(environ["MAX_BOOST_DAYS"]))
if MAX_BOOST_DAYS < timedelta(days=0):
    raise ValueError("MAX_BOOST_DAYSが負の値に設定されています")

TZ = environ["TZ"]
