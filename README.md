# Quick Start

TODO: Description

## Dependencies

- [python3](https://www.python.org/downloads) version 3.9 up to 3.12.

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-erpc
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-erpc.git
cd ape-erpc
python3 setup.py install
```

## Quick Usage

Configure via `ape-config.yaml`:
```yaml
erpc: 
  host: https://my-erpc.domain...
```

or `pyproject.toml`
```toml
[tool.ape.erpc] 
host = "https://my-erpc.domain..." 
```

and then launch using any network combo your erpc instance supports via `--network <eco>:<net>:erpc`

## Development

Please see the [contributing guide](CONTRIBUTING.md) to learn more how to contribute to this project.
Comments, questions, criticisms and pull requests are welcomed.
