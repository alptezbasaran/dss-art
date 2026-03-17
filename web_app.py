#!/usr/bin/env python3
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Cellular Art")
_HTML = Path(__file__).parent / "index.html"


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return _HTML.read_text()
