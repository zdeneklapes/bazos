import os
from os import path
import sys
from typing import Optional, Union, Dict
import time
from threading import Timer
import random
import yaml


def parse_yaml(filename: str) -> Optional[Union[Dict[str, str], FileNotFoundError]]:
    with open(filename, "r") as stream:
        yaml_parsed = yaml.safe_load(stream)
        # yaml_parsed |= yaml_parsed['default']
        # del yaml_parsed['default']
        return yaml_parsed


def wait_random_time():
    time.sleep(random.random() * 1)


def wait_n_seconds(seconds: int):
    for i in range(seconds):
        time.sleep(1)
        sys.stdout.write(f"\rwaiting {i + 1}s, until {seconds}s")


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def refactor_info_txt(_path: str):
  for dir in next(os.walk(_path))[1]:  # loop through all directories
    file = path.join(_path, dir, 'info.txt')

    assert path.isfile(file), 'File not exist: info.txt'

    with open(file=file, mode='r') as f:
      lines = f.readlines()

    try:
      idx_rubric = lines.index('>>RUBRIKA\n')
      idx_category = lines.index('>>KATEGORIE\n')
      # lines[idx_rubric] = '>>RUBRIC\n'
      # lines[idx_category] = '>>CATEGORY\n'
      # with open(file=file, mode='w') as f:
      #     f.writelines(lines)
    except:
      pass
