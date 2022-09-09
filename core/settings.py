import os
from os import path
from pathlib import Path

ROOT_DIR = Path(os.getcwd())
BASE_DIR = Path(__file__)


TOKENS_DIR = os.path.join(ROOT_DIR, 'tokens')
if not os.path.exists(TOKENS_DIR):
    os.makedirs(TOKENS_DIR)


COOKIES_FILE = path.join(TOKENS_DIR, 'cookies')
LOCAL_STORAGE_FILE = path.join(TOKENS_DIR, 'local_storage')

if __name__ == '__main__':
    print('run')
