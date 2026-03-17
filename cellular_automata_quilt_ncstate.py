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

SEED = 186
N = 116
FRAMES = 180
INTERVAL_MS = 55
FPS = 18
OUT_GIF = "cellular_automata_quilt_ncstate.gif"


def hex_to_rgb01(value: str) -> np.ndarray:
    value = value.lstrip("#")
    return np.array([int(value[i : i + 2], 16) for i in (0, 2, 4)], dtype=float) / 255.0


def life_step(g: np.ndarray) -> np.ndarray:
    neigh = sum(
        np.roll(np.roll(g, i, axis=0), j, axis=1)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        if not (i == 0 and j == 0)
    )
    return ((neigh == 3) | ((g == 1) & (neigh == 2))).astype(int)


def main() -> None:
    rng = np.random.default_rng(SEED)
    grid = np.zeros((N, N), dtype=int)
    grid[N // 2 - 10 : N // 2 + 10, N // 2 - 10 : N // 2 + 10] = rng.integers(0, 2, size=(20, 20))

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.axis("off")
    fig.tight_layout(pad=0)

    trail = np.zeros_like(grid, dtype=float)
    age = np.zeros_like(grid, dtype=float)
    img = ax.imshow(np.zeros((N, N, 3), dtype=float), interpolation="nearest")

    # NC State-inspired palette with Wolfpack Red as dominant anchor.
    c_black = hex_to_rgb01("#000000")
    c_reynolds = hex_to_rgb01("#990000")
    c_wolfpack = hex_to_rgb01("#CC0000")
    c_flame = hex_to_rgb01("#D14905")
    c_white = hex_to_rgb01("#FFFFFF")

    def update(frame: int):
        nonlocal grid, trail, age

        if frame % 7 == 0:
            cx, cy = rng.integers(16, N - 16, size=2)
            patch = rng.integers(0, 2, size=(9, 9))
            grid[cx - 4 : cx + 5, cy - 4 : cy + 5] = np.maximum(
                grid[cx - 4 : cx + 5, cy - 4 : cy + 5], patch
            )

        if frame % 19 == 0:
            # Occasional stripe burst for a woven/quilt rhythm.
            sx = rng.integers(4, N - 4)
            grid[sx - 1 : sx + 1, :] = np.maximum(grid[sx - 1 : sx + 1, :], rng.integers(0, 2, size=(2, N)))

        grid = life_step(grid)
        age = np.where(grid == 1, np.minimum(age + 1.0, 70.0), age * 0.86)
        trail = 0.91 * trail + 1.30 * grid

        blur = (
            np.roll(trail, 1, 0)
            + np.roll(trail, -1, 0)
            + np.roll(trail, 1, 1)
            + np.roll(trail, -1, 1)
        ) * 0.1

        tone = 0.75 * trail + 0.33 * age + blur + 0.05 * np.sin(0.12 * frame)
        tone_norm = 1.0 - np.exp(-0.14 * tone)
        t = np.clip(tone_norm, 0.0, 1.0)

        rgb = np.empty((N, N, 3), dtype=float)

        seg1 = t < 0.22
        seg2 = (t >= 0.22) & (t < 0.56)
        seg3 = (t >= 0.56) & (t < 0.82)
        seg4 = t >= 0.82

        u1 = np.clip(t / 0.22, 0.0, 1.0)
        u2 = np.clip((t - 0.22) / 0.34, 0.0, 1.0)
        u3 = np.clip((t - 0.56) / 0.26, 0.0, 1.0)
        u4 = np.clip((t - 0.82) / 0.18, 0.0, 1.0)

        for ch in range(3):
            rgb[..., ch] = (
                seg1 * ((1.0 - u1) * c_black[ch] + u1 * c_reynolds[ch])
                + seg2 * ((1.0 - u2) * c_reynolds[ch] + u2 * c_wolfpack[ch])
                + seg3 * ((1.0 - u3) * c_wolfpack[ch] + u3 * c_flame[ch])
                + seg4 * ((1.0 - u4) * c_flame[ch] + u4 * c_white[ch])
            )

        # Keep red dominant while still giving highlights some contrast.
        red_emphasis = 0.85 + 0.25 * np.tanh(1.2 * trail)
        rgb[..., 0] *= red_emphasis
        rgb[..., 1] *= 0.96
        rgb[..., 2] *= 0.95

        img.set_data(np.clip(rgb, 0.0, 1.0))
        return [img]

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=INTERVAL_MS, blit=False)
    anim.save(OUT_GIF, writer=PillowWriter(fps=FPS))


if __name__ == "__main__":
    main()
