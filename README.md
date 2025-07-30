# Optiland Playground

This project is a wrapper for the [Optiland](https://github.com/HarrisonKramer/optiland) Python optics package, running in a reproducible VS Code Dev Container.

## Features

- Full editable Optiland source (`src/optiland`)
- Docker-based Python environment
- VS Code Dev Container support
- Sample script: `reverse_telephoto_example.py`
- IPOPT optimizer integration (see `ipopt_optimizer_example.py`)

## Quickstart

1. Clone this repo:
   ```bash
   git clone https://github.com/rlepko/optiland-playground.git
   ```
2. Rebuild the dev container so IPOPT and cyipopt are installed.
