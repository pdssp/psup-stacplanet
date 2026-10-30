# PSUP-STACPLANET

PSUP organizer for STACPLANET, per PDSSP's ontology

## Installation

To install the development version, download `uv` and sync with the environment:

```console
uv sync --all-groups --all-extras
```

You can use the CLI right here.

```console
uv run psup-stacplanet --help
```

To mount the browser, you need to have Docker installed beforehand. You'll then need to clone the `.env.example` file, and fill `OUTPUT_DIR` to where you stored the root catalog.

```console
cp .env.example .env
```

Then, build your images and with docker compose:

```console
docker compose up -d
```

Then go to http://localhost:8091/ to see the result.
