import os
from pathlib import Path

ROOT_DIR = Path(os.getcwd())
BASE_DIR = Path(__file__)


TOKENS_DIR = os.path.join(ROOT_DIR, 'tokens')
if not os.path.exists(TOKENS_DIR):
    os.makedirs(TOKENS_DIR)


COOKIES_FILE = 'cookies'
LOCAL_STORAGE_FILE = 'local_storage'

if __name__ == '__main__':
    print('run')
