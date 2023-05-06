# BAZOS-API

## Authors:

- Zdeněk Lapeš <lapes.zdenek@gmail.com>

## Description:

Current stuff in this repository is just used to remove and add new items to bazos.cz and .sk

## Installation:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```shell
python3 main.py --help
python3 main.py -b --country cz sk --path $HOME/Documents/photos-archive # Remove all items from bazos.cz and bazos.sk and add new items from $HOME/Documents/photos-archive
python3 main.py -b --country cz sk --add-only --path $HOME/Documents/photos-archive # Add new items from $HOME/Documents/photos-archive
```

### `--path` argument

The folder structure of directory passed to `--path` argument should look like this:

```shell
$HOME/Documents/photos-archive
$HOME/Documents/photos-archive/folder1/photos/photo1.jpg
$HOME/Documents/photos-archive/folder1/info.txt
```

### `info.txt` file

Must follow this format:

```shell
>>RUBRIC
PC

>>CATEGORY
Notebooky

>>TITLE
Iphone X 64GB

>>PRICE
1000

>>DESCRIPTION
Your sentences1.
Your sentences2.
```

## TODO:

- make API class, that user can connect to bazos, get all their items, and then add new items, remove old items,
  update items, etc...
- Then create some example scripts, that show how to use this API class
- change "our own" file structure that describes items to yaml syntax
