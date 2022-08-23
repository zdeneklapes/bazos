from os import path
import os


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

