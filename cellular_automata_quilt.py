#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "numpy",
#   "matplotlib",
#   "pillow",
# ]
# ///

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

SEED = 11
N = 110
FRAMES = 180
INTERVAL_MS = 55
FPS = 18
OUT_GIF = "cellular_automata_quilt.gif"

def life_step(g):
    neigh = sum(np.roll(np.roll(g, i, axis=0), j, axis=1)
                for i in (-1, 0, 1) for j in (-1, 0, 1)
                if not (i == 0 and j == 0))
    return ((neigh == 3) | ((g == 1) & (neigh == 2))).astype(int)

def main() -> None:
    rng = np.random.default_rng(SEED)
    grid = np.zeros((N, N), dtype=int)
    grid[N // 2 - 8 : N // 2 + 8, N // 2 - 8 : N // 2 + 8] = rng.integers(0, 2, size=(16, 16))

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.axis("off")
    fig.tight_layout(pad=0)

    trail = np.zeros_like(grid, dtype=float)
    age = np.zeros_like(grid, dtype=float)
    img = ax.imshow(np.zeros((N, N, 3), dtype=float), interpolation="nearest")

    def update(frame):
        nonlocal grid, trail, age
        if frame % 8 == 0:
            cx, cy = rng.integers(15, N - 15, size=2)
            patch = rng.integers(0, 2, size=(9, 9))
            grid[cx - 4 : cx + 5, cy - 4 : cy + 5] = np.maximum(
                grid[cx - 4 : cx + 5, cy - 4 : cy + 5], patch
            )

        grid = life_step(grid)
        age = np.where(grid == 1, np.minimum(age + 1.0, 50.0), age * 0.84)
        trail = 0.90 * trail + 1.35 * grid

        blur = (
            np.roll(trail, 1, 0)
            + np.roll(trail, -1, 0)
            + np.roll(trail, 1, 1)
            + np.roll(trail, -1, 1)
        ) * 0.1
        tone = 0.72 * trail + 0.35 * age + blur
        phase = 0.10 * frame

        rgb = np.empty((N, N, 3), dtype=float)
        rgb[..., 0] = 0.5 + 0.5 * np.sin(1.15 * tone + phase + 0.0)
        rgb[..., 1] = 0.5 + 0.5 * np.sin(1.05 * tone + phase + 2.2)
        rgb[..., 2] = 0.5 + 0.5 * np.sin(1.25 * tone + phase + 4.4)

        glow = np.clip(0.20 + 0.80 * np.tanh(0.9 * trail), 0.0, 1.0)
        rgb *= glow[..., None]
        img.set_data(np.clip(rgb, 0.0, 1.0))
        return [img]

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=INTERVAL_MS, blit=False)
    anim.save(OUT_GIF, writer=PillowWriter(fps=FPS))


if __name__ == "__main__":
    main()
