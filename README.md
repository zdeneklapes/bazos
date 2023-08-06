# BAZOS-API

Current functionality supports removing and adding items to bazos.cz, bazos.sk, bazos.at and bazos.pl.

## Goal
Create full-featured API for bazos.cz, bazos.sk, bazos.at and bazos.pl.

## Installation

```shell
pip3 install bazos
```

## Run

```shell
bazos --help
bazos -b --country cz sk --path $HOME/Documents/photos-archive # Remove all items from bazos.cz and bazos.sk and add new items from $HOME/Documents/photos-archive
bazos -b --country cz sk --add-only --path $HOME/Documents/photos-archive # Add new items from $HOME/Documents/photos-archive
```

### `--country` argument
Supported countries: `cz`, `sk`, `at`, `pl`


### `-b|--bazos` argument
This turn on run.

### `--path` argument
The folder where all photos and `user_{country}.yml` file.

How to structure folder defined in `--path` argument:

```yml
# user_${bazos_country}.yml e.g.: user_cz.yml
name: Jmeno
phone_number: '+420123456789'
email: user@example.com
psc: 60200
password: 123456
```


### Example of folder structure

```shell
bazos-ads/
bazos-ads/user_cz.yml
bazos-ads/user_sk.yml
bazos-ads/item1/photos/photo1.jpg
bazos-ads/item1/photos/photo2.jpg
bazos-ads/item1/info.txt
bazos-ads/item2/photos/photo1.jpg
bazos-ads/item2/photos/photo2.jpg
bazos-ads/item2/info.txt
...
```

### `info.txt` syntax

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



## Contribution and Development

Every contribution is welcome!

Please follow rules inside `.pre-commit-config.yml` file.

Before creating pull request, please run `pre-commit run --all-files` to check if there are no errors.

### Install pre-commit hooks

```shell
pre-commit install
```

### Create virtual environment and install dependencies

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
