from os import environ
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../settings/.env")
load_dotenv(dotenv_path, verbose=True)

BASE_URL = environ.get("BASE_URL")
ACCESS_TOKEN = environ.get("ACCESS_TOKEN")
