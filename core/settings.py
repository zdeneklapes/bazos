import os
from os import path
from pathlib import Path

ROOT_DIR = Path(os.getcwd())
BASE_DIR = Path(__file__)

TOKENS_DIR = os.path.join(ROOT_DIR, 'tokens')

COOKIES_FILE = path.join(ROOT_DIR, 'cookies')
LOCAL_STORAGE_FILE = path.join(ROOT_DIR, 'local_storage')
