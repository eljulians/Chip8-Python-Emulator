# CHIP-8 emulator

[![Build Status](https://travis-ci.org/julenpardo/Chip8-Python-Emulator.svg?branch=master)](https://travis-ci.org/julenpardo/Chip8-Python-Emulator)
[![Coverage Status](https://coveralls.io/repos/github/julenpardo/Chip8-Python-Emulator/badge.svg?branch=master)](https://coveralls.io/github/julenpardo/Chip8-Python-Emulator?branch=master)
![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)

A CHIP-8 emulator. Based on [Cowgod's CHIP-8 Technichal Reference v1.0](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM).

## Set up

```bash
pipenv install  # --dev for development
```

## Usage

```bash
pipenv shell
python chip8_emulator <path/to/rom>
```

## Run tests with coverage

```bash
pipenv shell
pipenv run tests
pipenv run cov-html  # After having run the tests
pipenv run cov-stdout  # After having run the tests
```
