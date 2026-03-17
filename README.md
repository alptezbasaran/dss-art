## Cellular Automata Quilt

Interactive, full‑screen cellular automata art that you can:
- render to animated GIFs with Python/`uv`
- explore live in the browser (click‑to‑seed, reset), either via Docker or GitHub Pages.

### Local development with `uv`

Render the quilt GIF (non‑interactive, same as the original script):

```bash
uv run cellular_automata_quilt.py
```

This writes `cellular_automata_quilt.gif` into the project directory.

### Docker interactive app

Build the image:

```bash
docker build -t cellular-art-web .
```

Run the full‑screen interactive app:

```bash
docker run --rm -p 8000:8000 cellular-art-web
```

Then open `http://localhost:8000` and:
- click/tap anywhere to seed the automaton from that point, or click and drag to draw a continuous trail
- use the **Reset** button in the bottom‑right corner to clear the canvas

### GitHub Pages

The interactive app is also available as a static HTML page:
- `index.html` contains the entire client‑side implementation
- `.github/workflows/deploy.yml` deploys `index.html` to GitHub Pages on each push to `main`

To enable Pages in GitHub:
1. Go to **Settings → Pages** in the `alptezbasaran/dss-art` repo.
2. Set **Source** to **GitHub Actions**.
3. Push to `main` and wait for the `Deploy to GitHub Pages` workflow to succeed.

After that, your live URL will be shown in the Pages settings and in the workflow summary.
