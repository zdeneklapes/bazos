# BAZOS-API

Current functionality supports removing and adding items to bazos.cz and .sk

## Installation:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```shell
python3 bazos --help
python3 bazos -b --country cz sk --path $HOME/Documents/photos-archive # Remove all items from bazos.cz and bazos.sk and add new items from $HOME/Documents/photos-archive
python3 bazos -b --country cz sk --add-only --path $HOME/Documents/photos-archive # Add new items from $HOME/Documents/photos-archive
```

### `--path` argument

The folder structure of directory passed to `--path` argument should look like this:

```shell
$HOME/Documents/photos-archive
$HOME/Documents/photos-archive/folder1/photos/photo1.jpg
$HOME/Documents/photos-archive/folder1/info.txt
```

### `info.txt` file structure

Must follow this format:

```shell
>>RUBRIC
PC

>>CATEGORY
Notebooky

>>TITLE
Macbook Pro 2019 16

>>PRICE
25000

>>DESCRIPTION
Your sentences1.
Your sentences2.
```
