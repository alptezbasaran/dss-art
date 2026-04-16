#!/usr/bin/env python3
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Cellular Art")
_ROOT = Path(__file__).parent
_HTML = _ROOT / "index.html"

app.mount("/assets", StaticFiles(directory=_ROOT / "assets"), name="assets")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return _HTML.read_text()
