# PyAbsInt

An lightweight abstract interpreter implemented in Python.

## Supported Abstract Domains

1. Boxes (Implementation from [APRON](https://github.com/caterinaurban/apronpy))
2. Octagon (Implementation from [ELINA](https://github.com/eth-sri/ELINA))
3. Zones (Implementation from [ELINA](https://github.com/eth-sri/ELINA))

## Installation

1. Run
```
pip install requirements.txt
```

2. Install and build:
    - [APRON](https://github.com/antoinemine/apron) (for `Boxes` domain)
    - [ELINA](https://github.com/eth-sri/ELINA) (for `Octagon` domain)
    - [My fork of ELINA](https://github.com/sgomber/elina/tree/feature/zones-python-interface) (ELINA does not expose `Zones` as python interface as of now, so I added them it in my fork of ELINA)

