# flit-bumpversion

Updates the `__version__` of a package, commits the changes and tags the commit.


## Installation

flit-bumpversion only works with python 3.7 and upwards.

```sh
python3 -m pip install flit_bumpversion
```


## Usage

You can either provide a single file module or a directory module:

If you want to update the `__version__` string in the `my_package.py` file:

```sh
flit-bumpversion patch my_package.py
```

Or when updating a directory module:

```sh
flit-bumpversion patch my_package
```

This will update `my_package/__init__.py` file.
