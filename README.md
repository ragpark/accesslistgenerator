# accesslistgenerator

Web app to generate unique 5-character access codes suitable for an access code datasheet.

## Features

- Web UI (no CLI)
- Generates **5-character alphabetic** codes (letters only, no numbers)
- Uses a consonant-only alphabet to favor **non-word** strings
- Filters blocked rude sequences for **safe-for-work** output
- Guarantees **no repeats** in each generated batch
- Optional deterministic seed for reproducible batches
- Download generated codes as CSV
- Runs with Python standard library only

## Run locally

```bash
python app.py
```

Then open `http://localhost:8080`.

## Deploy to Railway

This repo is ready for Railway deployment:

- `Procfile` start command: `web: python app.py`
- `railway.json` includes basic deploy defaults
- No external dependencies are required

### Steps

1. Push this repo to GitHub.
2. In Railway, create a **New Project** → **Deploy from GitHub repo**.
3. Select this repository.
4. Railway will run the `Procfile` start command.
5. Open the generated Railway domain URL.
