from os import path
import os


def refactor_info_txt(url: str):
    for dir in next(os.walk(url))[1]:  # loop through all directories
        file = path.join(url, dir, 'info.txt')

        assert path.isfile(file), 'File not exist: info.txt'

        with open(file=file, mode='r') as f:
            lines = f.readlines()
            idx = lines.index('>>PRICE\n') + 1

        with open(file=file, mode='w') as f:
            f.writelines(lines[:idx])
