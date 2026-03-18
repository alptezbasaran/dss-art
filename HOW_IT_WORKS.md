# How It Works

This is not a painting. It is not a photograph or a generative texture brushed on by hand. Every pixel you see is the output of math — rules applied to a grid, numbers fed through functions, color computed rather than chosen. The art is in the rules. Everything else follows.

---

## The Game of Life — life from four rules

The foundation is Conway's Game of Life, a cellular automaton invented in 1970. The canvas is a grid of cells, each either alive (1) or dead (0). At every tick, the entire grid advances one generation simultaneously according to four rules:

1. A live cell with **fewer than 2** live neighbors dies (underpopulation).
2. A live cell with **2 or 3** live neighbors survives.
3. A live cell with **more than 3** live neighbors dies (overcrowding).
4. A dead cell with **exactly 3** live neighbors is born.

That's it. Four sentences, and from them emerge gliders, oscillators, self-replicating patterns — behaviors that nobody explicitly programmed.

The grid wraps at the edges (toroidal topology), so a glider that drifts off the right side reappears on the left. There are no walls; the space folds back on itself.

**Seeding** is how you start. Clicking or dragging doesn't place a single cell — it plants a probabilistic cluster, a radial burst where cells near the center are more likely to be born and cells at the edge trail off. The probability of birth at distance $d$ from the click is approximately $P(d) \approx 0.56 - 0.01\, d^2$. You're not drawing; you're igniting.

---

## Color as data — how math paints each cell

The Game of Life produces a binary grid: alive or dead. The color you see is a separate computation layered on top. Three quantities accumulate for every cell, and together they determine its pixel color.

### Trail and age — cellular memory

Each cell carries two running values:

- **trail** — a leaky integrator that charges when the cell is alive and decays when it's dead:

  $$\text{trail}[i] = 0.93\cdot\text{trail}[i] + 1.35\cdot\text{cell}[i] \qquad \in [0,\ \approx 19.3]$$

  $\text{cell}[i]$ is 1 when alive, 0 when dead. At steady state (always alive), trail converges to $\frac{1.35}{1 - 0.93} \approx 19.3$. When the cell dies, trail decays by $\times 0.93$ each frame — half-life of about 10 frames (~550 ms). Here is what that decay looks like starting from steady state:

  <svg xmlns="http://www.w3.org/2000/svg" width="700" height="180" style="background:#111;border-radius:6px">
    <line x1="48" y1="144.0" x2="684" y2="144.0" stroke="#333" stroke-width="1"/>
    <line x1="48" y1="110.7" x2="684" y2="110.7" stroke="#333" stroke-width="1"/>
    <line x1="48" y1="77.3" x2="684" y2="77.3" stroke="#333" stroke-width="1"/>
    <line x1="48" y1="44.0" x2="684" y2="44.0" stroke="#333" stroke-width="1"/>
    <line x1="48" y1="16.0" x2="684" y2="16.0" stroke="#333" stroke-width="1"/>
    <line x1="48.0" y1="16" x2="48.0" y2="144" stroke="#333" stroke-width="1"/>
    <line x1="209.0" y1="16" x2="209.0" y2="144" stroke="#333" stroke-width="1"/>
    <line x1="370.0" y1="16" x2="370.0" y2="144" stroke="#333" stroke-width="1"/>
    <line x1="531.0" y1="16" x2="531.0" y2="144" stroke="#333" stroke-width="1"/>
    <line x1="684.0" y1="16" x2="684.0" y2="144" stroke="#333" stroke-width="1"/>
    <line x1="48" y1="16" x2="48" y2="144" stroke="#555" stroke-width="1.5"/>
    <line x1="48" y1="144" x2="684" y2="144" stroke="#555" stroke-width="1.5"/>
    <text x="42" y="148.0" text-anchor="end" font-family="monospace" font-size="11" fill="#888">0</text>
    <text x="42" y="114.7" text-anchor="end" font-family="monospace" font-size="11" fill="#888">5</text>
    <text x="42" y="81.3" text-anchor="end" font-family="monospace" font-size="11" fill="#888">10</text>
    <text x="42" y="48.0" text-anchor="end" font-family="monospace" font-size="11" fill="#888">15</text>
    <text x="42" y="20.0" text-anchor="end" font-family="monospace" font-size="11" fill="#888">19.2</text>
    <text x="48.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">0</text>
    <text x="209.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">20</text>
    <text x="370.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">40</text>
    <text x="531.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">60</text>
    <text x="684.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">79</text>
    <text x="366.0" y="178" text-anchor="middle" font-family="monospace" font-size="11" fill="#666">frames after cell dies</text>
    <path d="M 48.0,16.0 L 56.1,23.7 L 64.1,30.9 L 72.2,37.7 L 80.2,44.1 L 88.3,50.1 L 96.3,55.7 L 104.4,61.0 L 112.4,66.0 L 120.5,70.7 L 128.5,75.1 L 136.6,79.2 L 144.6,83.1 L 152.7,86.7 L 160.7,90.2 L 168.8,93.4 L 176.8,96.4 L 184.9,99.3 L 192.9,102.0 L 201.0,104.5 L 209.0,106.9 L 217.1,109.1 L 225.1,111.2 L 233.2,113.2 L 241.2,115.0 L 249.3,116.7 L 257.3,118.4 L 265.4,119.9 L 273.4,121.4 L 281.5,122.7 L 289.5,124.0 L 297.6,125.2 L 305.6,126.3 L 313.7,127.4 L 321.7,128.4 L 329.8,129.3 L 337.8,130.2 L 345.9,131.0 L 353.9,131.8 L 362.0,132.5 L 370.0,133.2 L 378.1,133.9 L 386.1,134.5 L 394.2,135.1 L 402.2,135.6 L 410.3,136.1 L 418.3,136.6 L 426.4,137.0 L 434.4,137.4 L 442.5,137.8 L 450.5,138.2 L 458.6,138.5 L 466.6,138.9 L 474.7,139.2 L 482.7,139.5 L 490.8,139.7 L 498.8,140.0 L 506.9,140.2 L 514.9,140.5 L 523.0,140.7 L 531.0,140.9 L 539.1,141.1 L 547.1,141.2 L 555.2,141.4 L 563.2,141.6 L 571.3,141.7 L 579.3,141.8 L 587.4,142.0 L 595.4,142.1 L 603.5,142.2 L 611.5,142.3 L 619.6,142.4 L 627.6,142.5 L 635.7,142.6 L 643.7,142.7 L 651.8,142.8 L 659.8,142.8 L 667.9,142.9 L 675.9,143.0 L 684.0,143.0" stroke="#ff7755" stroke-width="2" fill="none" opacity="0.9"/>
  </svg>

- **age** — counts consecutive frames alive, capped at 50, decaying at 84%/frame when dead:

  $$\text{age}[i] = \begin{cases} \min(\text{age}[i] + 1,\ 50) & \text{if alive} \\ 0.84\cdot\text{age}[i] & \text{if dead} \end{cases} \qquad \in [0,\ 50]$$

- **tail** — a slow-decaying afterglow accumulator. While a cell is alive it mirrors `trail`; when the cell dies it decays at $\times 0.975$ per frame — roughly 2.5× slower than `trail`. It contributes a dim multiplicative glow on top of the main color, extending the visible trace after death without altering the alive-cell appearance.

Together they form a composite activity signal:

$$t = 0.72\cdot\text{trail} + 0.35\cdot\text{age} \qquad \in [0,\ \approx 31.5]$$

This is the single number that drives color. A freshly born cell has $t \approx 0$; a cell that has been alive continuously approaches $t \approx 31.5$.

### Glow via tanh — a nonlinear brightness curve

Raw trail values would produce either flat brightness or harsh edges. Instead, brightness is compressed through a hyperbolic tangent:

$$\text{glow} = \text{clamp}\!\left(0.2 + 0.8\cdot\tanh(0.9\cdot\text{trail})\right) \qquad \in [0.20,\ 1.0]$$

$\tanh$ is S-shaped: it rises steeply near zero, then saturates. At $\text{trail} = 0$, $\text{glow} = 0.20$ (dim but not black). At $\text{trail} = 2$, $\text{glow} \approx 0.90$. Beyond that, it barely moves. The result: cells snap to near-full brightness within a couple of frames of birth, then fade in a long smooth tail after death — nothing blinks on and off like a switch.

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="180" style="background:#111;border-radius:6px">
  <line x1="48" y1="144.0" x2="684" y2="144.0" stroke="#333" stroke-width="1"/>
  <line x1="48" y1="118.4" x2="684" y2="118.4" stroke="#333" stroke-width="1"/>
  <line x1="48" y1="80.0" x2="684" y2="80.0" stroke="#333" stroke-width="1"/>
  <line x1="48" y1="41.6" x2="684" y2="41.6" stroke="#333" stroke-width="1"/>
  <line x1="48" y1="16.0" x2="684" y2="16.0" stroke="#333" stroke-width="1"/>
  <line x1="48.0" y1="16" x2="48.0" y2="144" stroke="#333" stroke-width="1"/>
  <line x1="207.0" y1="16" x2="207.0" y2="144" stroke="#333" stroke-width="1"/>
  <line x1="366.0" y1="16" x2="366.0" y2="144" stroke="#333" stroke-width="1"/>
  <line x1="525.0" y1="16" x2="525.0" y2="144" stroke="#333" stroke-width="1"/>
  <line x1="684.0" y1="16" x2="684.0" y2="144" stroke="#333" stroke-width="1"/>
  <line x1="48" y1="16" x2="48" y2="144" stroke="#555" stroke-width="1.5"/>
  <line x1="48" y1="144" x2="684" y2="144" stroke="#555" stroke-width="1.5"/>
  <text x="42" y="148.0" text-anchor="end" font-family="monospace" font-size="11" fill="#888">0</text>
  <text x="42" y="122.4" text-anchor="end" font-family="monospace" font-size="11" fill="#888">0.2</text>
  <text x="42" y="84.0" text-anchor="end" font-family="monospace" font-size="11" fill="#888">0.5</text>
  <text x="42" y="45.6" text-anchor="end" font-family="monospace" font-size="11" fill="#888">0.8</text>
  <text x="42" y="20.0" text-anchor="end" font-family="monospace" font-size="11" fill="#888">1</text>
  <text x="48.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">0</text>
  <text x="207.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">5</text>
  <text x="366.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">10</text>
  <text x="525.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">15</text>
  <text x="684.0" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">20</text>
  <text x="366.0" y="178" text-anchor="middle" font-family="monospace" font-size="11" fill="#666">trail</text>
  <path d="M 48.0,118.4 L 51.2,109.2 L 54.4,100.2 L 57.5,91.4 L 60.7,83.1 L 63.9,75.2 L 67.1,67.9 L 70.3,61.3 L 73.4,55.2 L 76.6,49.8 L 79.8,45.1 L 83.0,40.8 L 86.2,37.2 L 89.3,34.0 L 92.5,31.3 L 95.7,28.9 L 98.9,26.9 L 102.1,25.2 L 105.2,23.7 L 108.4,22.5 L 111.6,21.4 L 114.8,20.6 L 118.0,19.8 L 121.1,19.2 L 124.3,18.7 L 127.5,18.3 L 130.7,17.9 L 133.9,17.6 L 137.0,17.3 L 140.2,17.1 L 143.4,16.9 L 146.6,16.8 L 149.8,16.6 L 152.9,16.5 L 156.1,16.4 L 159.3,16.4 L 162.5,16.3 L 165.7,16.3 L 168.8,16.2 L 172.0,16.2 L 175.2,16.2 L 178.4,16.1 L 181.6,16.1 L 184.7,16.1 L 187.9,16.1 L 191.1,16.1 L 194.3,16.1 L 197.5,16.0 L 200.6,16.0 L 203.8,16.0 L 207.0,16.0 L 210.2,16.0 L 213.4,16.0 L 216.5,16.0 L 219.7,16.0 L 222.9,16.0 L 226.1,16.0 L 229.3,16.0 L 232.4,16.0 L 235.6,16.0 L 238.8,16.0 L 242.0,16.0 L 245.2,16.0 L 248.3,16.0 L 251.5,16.0 L 254.7,16.0 L 257.9,16.0 L 261.1,16.0 L 264.2,16.0 L 267.4,16.0 L 270.6,16.0 L 273.8,16.0 L 277.0,16.0 L 280.1,16.0 L 283.3,16.0 L 286.5,16.0 L 289.7,16.0 L 292.9,16.0 L 296.0,16.0 L 299.2,16.0 L 302.4,16.0 L 305.6,16.0 L 308.8,16.0 L 311.9,16.0 L 315.1,16.0 L 318.3,16.0 L 321.5,16.0 L 324.7,16.0 L 327.8,16.0 L 331.0,16.0 L 334.2,16.0 L 337.4,16.0 L 340.6,16.0 L 343.7,16.0 L 346.9,16.0 L 350.1,16.0 L 353.3,16.0 L 356.5,16.0 L 359.6,16.0 L 362.8,16.0 L 366.0,16.0 L 369.2,16.0 L 372.4,16.0 L 375.5,16.0 L 378.7,16.0 L 381.9,16.0 L 385.1,16.0 L 388.3,16.0 L 391.4,16.0 L 394.6,16.0 L 397.8,16.0 L 401.0,16.0 L 404.2,16.0 L 407.3,16.0 L 410.5,16.0 L 413.7,16.0 L 416.9,16.0 L 420.1,16.0 L 423.2,16.0 L 426.4,16.0 L 429.6,16.0 L 432.8,16.0 L 436.0,16.0 L 439.1,16.0 L 442.3,16.0 L 445.5,16.0 L 448.7,16.0 L 451.9,16.0 L 455.0,16.0 L 458.2,16.0 L 461.4,16.0 L 464.6,16.0 L 467.8,16.0 L 470.9,16.0 L 474.1,16.0 L 477.3,16.0 L 480.5,16.0 L 483.7,16.0 L 486.8,16.0 L 490.0,16.0 L 493.2,16.0 L 496.4,16.0 L 499.6,16.0 L 502.7,16.0 L 505.9,16.0 L 509.1,16.0 L 512.3,16.0 L 515.5,16.0 L 518.6,16.0 L 521.8,16.0 L 525.0,16.0 L 528.2,16.0 L 531.4,16.0 L 534.5,16.0 L 537.7,16.0 L 540.9,16.0 L 544.1,16.0 L 547.3,16.0 L 550.4,16.0 L 553.6,16.0 L 556.8,16.0 L 560.0,16.0 L 563.2,16.0 L 566.3,16.0 L 569.5,16.0 L 572.7,16.0 L 575.9,16.0 L 579.1,16.0 L 582.2,16.0 L 585.4,16.0 L 588.6,16.0 L 591.8,16.0 L 595.0,16.0 L 598.1,16.0 L 601.3,16.0 L 604.5,16.0 L 607.7,16.0 L 610.9,16.0 L 614.0,16.0 L 617.2,16.0 L 620.4,16.0 L 623.6,16.0 L 626.8,16.0 L 629.9,16.0 L 633.1,16.0 L 636.3,16.0 L 639.5,16.0 L 642.7,16.0 L 645.8,16.0 L 649.0,16.0 L 652.2,16.0 L 655.4,16.0 L 658.6,16.0 L 661.7,16.0 L 664.9,16.0 L 668.1,16.0 L 671.3,16.0 L 674.5,16.0 L 677.6,16.0 L 680.8,16.0 L 684.0,16.0" stroke="#ffcc44" stroke-width="2" fill="none" opacity="0.9"/>
</svg>

### Hue via sine triplet — color as rotation (Original mode)

In the default **Original** mode, the three color channels are computed as phase-shifted sine waves of the activity signal `t`, multiplied by `glow`:

$$\begin{aligned}
R &= \text{glow}\cdot\bigl(0.5 + 0.5\sin(1.15\,t + \varphi + 0.0)\bigr) \\
G &= \text{glow}\cdot\bigl(0.5 + 0.5\sin(1.05\,t + \varphi + 2.2)\bigr) \\
B &= \text{glow}\cdot\bigl(0.5 + 0.5\sin(1.25\,t + \varphi + 4.4)\bigr)
\end{aligned}$$

Each channel oscillates between 0 and 1. The phase offsets — 0, 2.2, 4.4 radians — are spaced approximately 120° apart ($2\pi/3 \approx 2.09$), so at any given $t$ the three channels are roughly a third of a cycle out of phase. As $t$ grows, the channels sweep through the hue wheel at slightly different rates (1.15, 1.05, 1.25), so the color rotates and never simply repeats.

The full colormap — what you'd see scanning across `t = 0 → 79` at full brightness:

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="60">
  <defs>
    <linearGradient id="cmap" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0.0%" stop-color="rgb(127,230,6)"/>
    <stop offset="1.3%" stop-color="rgb(243,113,52)"/>
    <stop offset="2.5%" stop-color="rgb(222,10,201)"/>
    <stop offset="3.8%" stop-color="rgb(88,25,249)"/>
    <stop offset="5.1%" stop-color="rgb(0,142,130)"/>
    <stop offset="6.3%" stop-color="rgb(62,244,7)"/>
    <stop offset="7.6%" stop-color="rgb(201,229,48)"/>
    <stop offset="8.9%" stop-color="rgb(252,111,197)"/>
    <stop offset="10.1%" stop-color="rgb(155,9,250)"/>
    <stop offset="11.4%" stop-color="rgb(25,26,134)"/>
    <stop offset="12.7%" stop-color="rgb(15,144,9)"/>
    <stop offset="13.9%" stop-color="rgb(138,245,45)"/>
    <stop offset="15.2%" stop-color="rgb(247,228,194)"/>
    <stop offset="16.5%" stop-color="rgb(215,109,251)"/>
    <stop offset="17.7%" stop-color="rgb(78,9,139)"/>
    <stop offset="19.0%" stop-color="rgb(0,27,10)"/>
    <stop offset="20.3%" stop-color="rgb(72,146,42)"/>
    <stop offset="21.5%" stop-color="rgb(209,246,190)"/>
    <stop offset="22.8%" stop-color="rgb(250,226,252)"/>
    <stop offset="24.1%" stop-color="rgb(145,107,143)"/>
    <stop offset="25.3%" stop-color="rgb(19,8,12)"/>
    <stop offset="26.6%" stop-color="rgb(21,29,39)"/>
    <stop offset="27.8%" stop-color="rgb(148,148,186)"/>
    <stop offset="29.1%" stop-color="rgb(250,247,253)"/>
    <stop offset="30.4%" stop-color="rgb(207,225,147)"/>
    <stop offset="31.6%" stop-color="rgb(69,105,14)"/>
    <stop offset="32.9%" stop-color="rgb(0,7,36)"/>
    <stop offset="34.2%" stop-color="rgb(81,30,183)"/>
    <stop offset="35.4%" stop-color="rgb(217,150,253)"/>
    <stop offset="36.7%" stop-color="rgb(246,247,151)"/>
    <stop offset="38.0%" stop-color="rgb(134,223,16)"/>
    <stop offset="39.2%" stop-color="rgb(14,103,33)"/>
    <stop offset="40.5%" stop-color="rgb(27,6,179)"/>
    <stop offset="41.8%" stop-color="rgb(159,31,254)"/>
    <stop offset="43.0%" stop-color="rgb(253,152,155)"/>
    <stop offset="44.3%" stop-color="rgb(198,248,18)"/>
    <stop offset="45.6%" stop-color="rgb(59,222,30)"/>
    <stop offset="46.8%" stop-color="rgb(1,101,175)"/>
    <stop offset="48.1%" stop-color="rgb(91,6,254)"/>
    <stop offset="49.4%" stop-color="rgb(224,33,159)"/>
    <stop offset="50.6%" stop-color="rgb(242,155,20)"/>
    <stop offset="51.9%" stop-color="rgb(124,249,27)"/>
    <stop offset="53.2%" stop-color="rgb(9,221,171)"/>
    <stop offset="54.4%" stop-color="rgb(34,98,254)"/>
    <stop offset="55.7%" stop-color="rgb(169,5,163)"/>
    <stop offset="57.0%" stop-color="rgb(254,34,23)"/>
    <stop offset="58.2%" stop-color="rgb(189,157,25)"/>
    <stop offset="59.5%" stop-color="rgb(51,249,167)"/>
    <stop offset="60.8%" stop-color="rgb(3,219,254)"/>
    <stop offset="62.0%" stop-color="rgb(102,96,168)"/>
    <stop offset="63.3%" stop-color="rgb(231,4,25)"/>
    <stop offset="64.6%" stop-color="rgb(237,36,22)"/>
    <stop offset="65.8%" stop-color="rgb(113,159,163)"/>
    <stop offset="67.1%" stop-color="rgb(6,250,254)"/>
    <stop offset="68.4%" stop-color="rgb(42,218,172)"/>
    <stop offset="69.6%" stop-color="rgb(179,94,28)"/>
    <stop offset="70.9%" stop-color="rgb(254,4,20)"/>
    <stop offset="72.2%" stop-color="rgb(179,37,159)"/>
    <stop offset="73.4%" stop-color="rgb(42,161,254)"/>
    <stop offset="74.7%" stop-color="rgb(5,250,175)"/>
    <stop offset="75.9%" stop-color="rgb(112,216,30)"/>
    <stop offset="77.2%" stop-color="rgb(237,92,18)"/>
    <stop offset="78.5%" stop-color="rgb(231,3,155)"/>
    <stop offset="79.7%" stop-color="rgb(102,39,254)"/>
    <stop offset="81.0%" stop-color="rgb(3,163,179)"/>
    <stop offset="82.3%" stop-color="rgb(50,251,33)"/>
    <stop offset="83.5%" stop-color="rgb(188,215,15)"/>
    <stop offset="84.8%" stop-color="rgb(254,90,151)"/>
    <stop offset="86.1%" stop-color="rgb(169,3,253)"/>
    <stop offset="87.3%" stop-color="rgb(35,40,183)"/>
    <stop offset="88.6%" stop-color="rgb(9,165,36)"/>
    <stop offset="89.9%" stop-color="rgb(123,251,13)"/>
    <stop offset="91.1%" stop-color="rgb(242,213,146)"/>
    <stop offset="92.4%" stop-color="rgb(225,88,253)"/>
    <stop offset="93.7%" stop-color="rgb(92,2,187)"/>
    <stop offset="94.9%" stop-color="rgb(1,42,39)"/>
    <stop offset="96.2%" stop-color="rgb(59,167,12)"/>
    <stop offset="97.5%" stop-color="rgb(197,252,142)"/>
    <stop offset="98.7%" stop-color="rgb(253,211,252)"/>
    <stop offset="100.0%" stop-color="rgb(159,86,191)"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="700" height="40" fill="url(#cmap)" rx="4"/>
  <text x="0" y="56" font-family="monospace" font-size="11" fill="#888">t = 0</text>
  <text x="350" y="56" font-family="monospace" font-size="11" fill="#888" text-anchor="middle">t = 40</text>
  <text x="700" y="56" font-family="monospace" font-size="11" fill="#888" text-anchor="end">t = 79</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="332" style="background:#111;border-radius:6px">
  <text x="48" y="22" font-family="monospace" font-size="11" fill="#ff5555" font-weight="bold">R  =  0.5 + 0.5·sin(1.15·t + φ + 0.0)</text>
  <line x1="48" y1="98.0" x2="684" y2="98.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="62.0" x2="684" y2="62.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="26.0" x2="684" y2="26.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="26" x2="48" y2="98" stroke="#444" stroke-width="1"/>
  <line x1="48" y1="98" x2="684" y2="98" stroke="#444" stroke-width="1"/>
  <text x="43" y="102.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">0</text>
  <text x="43" y="66.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">0.5</text>
  <text x="43" y="30.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">1</text>
  <path d="M 48.0,62.0 L 56.1,29.1 L 64.1,35.2 L 72.2,72.9 L 80.2,97.8 L 88.3,80.3 L 96.3,41.2 L 104.4,26.7 L 112.4,54.0 L 120.5,90.8 L 128.5,93.5 L 136.6,59.0 L 144.6,28.0 L 152.7,37.3 L 160.7,75.8 L 168.8,98.0 L 176.8,77.6 L 184.9,38.8 L 192.9,27.4 L 201.0,56.9 L 209.0,92.5 L 217.1,92.0 L 225.1,56.0 L 233.2,27.2 L 241.2,39.5 L 249.3,78.5 L 257.3,97.9 L 265.4,74.9 L 273.4,36.6 L 281.5,28.3 L 289.5,59.9 L 297.6,94.0 L 305.6,90.2 L 313.7,53.1 L 321.7,26.5 L 329.8,41.9 L 337.8,81.1 L 345.9,97.7 L 353.9,72.0 L 362.0,34.5 L 370.0,29.5 L 378.1,62.9 L 386.1,95.2 L 394.2,88.2 L 402.2,50.2 L 410.3,26.1 L 418.3,44.5 L 426.4,83.6 L 434.4,97.1 L 442.5,69.1 L 450.5,32.7 L 458.6,30.9 L 466.6,65.9 L 474.7,96.3 L 482.7,86.1 L 490.8,47.4 L 498.8,26.0 L 506.9,47.2 L 514.9,85.9 L 523.0,96.3 L 531.0,66.1 L 539.1,31.0 L 547.1,32.6 L 555.2,68.9 L 563.2,97.1 L 571.3,83.7 L 579.3,44.7 L 587.4,26.1 L 595.4,50.0 L 603.5,88.1 L 611.5,95.3 L 619.6,63.1 L 627.6,29.6 L 635.7,34.4 L 643.7,71.8 L 651.8,97.6 L 659.8,81.3 L 667.9,42.1 L 675.9,26.5 L 684.0,52.9" stroke="#ff5555" stroke-width="1.8" fill="none" opacity="0.9"/>
  <text x="48" y="118" font-family="monospace" font-size="11" fill="#55ff88" font-weight="bold">G  =  0.5 + 0.5·sin(1.05·t + φ + 2.2)</text>
  <line x1="48" y1="194.0" x2="684" y2="194.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="158.0" x2="684" y2="158.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="122.0" x2="684" y2="122.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="122" x2="48" y2="194" stroke="#444" stroke-width="1"/>
  <line x1="48" y1="194" x2="684" y2="194" stroke="#444" stroke-width="1"/>
  <text x="43" y="198.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">0</text>
  <text x="43" y="162.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">0.5</text>
  <text x="43" y="126.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">1</text>
  <path d="M 48.0,128.9 L 56.1,161.9 L 64.1,191.0 L 72.2,186.9 L 80.2,153.8 L 88.3,124.9 L 96.3,129.3 L 104.4,162.5 L 112.4,191.2 L 120.5,186.6 L 128.5,153.2 L 136.6,124.7 L 144.6,129.6 L 152.7,163.1 L 160.7,191.4 L 168.8,186.2 L 176.8,152.6 L 184.9,124.4 L 192.9,130.0 L 201.0,163.7 L 209.0,191.7 L 217.1,185.8 L 225.1,152.0 L 233.2,124.2 L 241.2,130.4 L 249.3,164.3 L 257.3,191.9 L 265.4,185.4 L 273.4,151.4 L 281.5,124.0 L 289.5,130.8 L 297.6,164.9 L 305.6,192.1 L 313.7,185.0 L 321.7,150.8 L 329.8,123.8 L 337.8,131.2 L 345.9,165.5 L 353.9,192.3 L 362.0,184.6 L 370.0,150.2 L 378.1,123.6 L 386.1,131.6 L 394.2,166.1 L 402.2,192.4 L 410.3,184.2 L 418.3,149.6 L 426.4,123.5 L 434.4,132.0 L 442.5,166.7 L 450.5,192.6 L 458.6,183.8 L 466.6,149.0 L 474.7,123.3 L 482.7,132.4 L 490.8,167.2 L 498.8,192.8 L 506.9,183.4 L 514.9,148.5 L 523.0,123.1 L 531.0,132.9 L 539.1,167.8 L 547.1,192.9 L 555.2,182.9 L 563.2,147.9 L 571.3,123.0 L 579.3,133.3 L 587.4,168.4 L 595.4,193.1 L 603.5,182.5 L 611.5,147.3 L 619.6,122.9 L 627.6,133.7 L 635.7,169.0 L 643.7,193.2 L 651.8,182.0 L 659.8,146.7 L 667.9,122.7 L 675.9,134.2 L 684.0,169.6" stroke="#55ff88" stroke-width="1.8" fill="none" opacity="0.9"/>
  <text x="48" y="214" font-family="monospace" font-size="11" fill="#5599ff" font-weight="bold">B  =  0.5 + 0.5·sin(1.25·t + φ + 4.4)</text>
  <line x1="48" y1="290.0" x2="684" y2="290.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="254.0" x2="684" y2="254.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="218.0" x2="684" y2="218.0" stroke="#2a2a2a" stroke-width="1"/>
  <line x1="48" y1="218" x2="48" y2="290" stroke="#444" stroke-width="1"/>
  <line x1="48" y1="290" x2="684" y2="290" stroke="#444" stroke-width="1"/>
  <text x="43" y="294.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">0</text>
  <text x="43" y="258.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">0.5</text>
  <text x="43" y="222.0" text-anchor="end" font-family="monospace" font-size="10" fill="#666">1</text>
  <path d="M 48.0,288.3 L 56.1,275.3 L 64.1,233.2 L 72.2,219.6 L 80.2,253.1 L 88.3,287.9 L 96.3,276.3 L 104.4,234.2 L 112.4,219.2 L 120.5,251.9 L 128.5,287.4 L 136.6,277.2 L 144.6,235.2 L 152.7,218.9 L 160.7,250.7 L 168.8,287.0 L 176.8,278.1 L 184.9,236.2 L 192.9,218.7 L 201.0,249.5 L 209.0,286.5 L 217.1,279.0 L 225.1,237.2 L 233.2,218.5 L 241.2,248.4 L 249.3,286.0 L 257.3,279.8 L 265.4,238.3 L 273.4,218.3 L 281.5,247.2 L 289.5,285.4 L 297.6,280.6 L 305.6,239.4 L 313.7,218.2 L 321.7,246.0 L 329.8,284.8 L 337.8,281.4 L 345.9,240.5 L 353.9,218.1 L 362.0,244.8 L 370.0,284.2 L 378.1,282.2 L 386.1,241.6 L 394.2,218.0 L 402.2,243.7 L 410.3,283.5 L 418.3,282.9 L 426.4,242.7 L 434.4,218.0 L 442.5,242.6 L 450.5,282.8 L 458.6,283.6 L 466.6,243.9 L 474.7,218.0 L 482.7,241.4 L 490.8,282.1 L 498.8,284.3 L 506.9,245.0 L 514.9,218.1 L 523.0,240.3 L 531.0,281.3 L 539.1,284.9 L 547.1,246.2 L 555.2,218.2 L 563.2,239.2 L 571.3,280.5 L 579.3,285.5 L 587.4,247.4 L 595.4,218.3 L 603.5,238.1 L 611.5,279.7 L 619.6,286.0 L 627.6,248.5 L 635.7,218.5 L 643.7,237.1 L 651.8,278.8 L 659.8,286.6 L 667.9,249.7 L 675.9,218.7 L 684.0,236.0" stroke="#5599ff" stroke-width="1.8" fill="none" opacity="0.9"/>
  <line x1="48.0" y1="290" x2="48.0" y2="294" stroke="#555" stroke-width="1"/>
  <text x="48.0" y="306.0" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">0</text>
  <line x1="209.0" y1="290" x2="209.0" y2="294" stroke="#555" stroke-width="1"/>
  <text x="209.0" y="306.0" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">20</text>
  <line x1="370.0" y1="290" x2="370.0" y2="294" stroke="#555" stroke-width="1"/>
  <text x="370.0" y="306.0" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">40</text>
  <line x1="531.0" y1="290" x2="531.0" y2="294" stroke="#555" stroke-width="1"/>
  <text x="531.0" y="306.0" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">60</text>
  <line x1="684.0" y1="290" x2="684.0" y2="294" stroke="#555" stroke-width="1"/>
  <text x="684.0" y="306.0" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">79</text>
  <text x="366.0" y="328" text-anchor="middle" font-family="monospace" font-size="11" fill="#555">t  (activity signal)</text>
</svg>

Because the three sine frequencies (1.15, 1.05, 1.25) are incommensurable, the colormap never exactly repeats — it cycles through different combinations on every pass. The $\varphi$ term ($\varphi = 0.10 \cdot \text{frame}$) shifts the entire spectrum slowly over time, so even a perfectly stable pattern drifts in hue.

### Color modes — backgrounds and palettes

The app offers multiple color modes selectable via buttons. Each mode defines:

1. A **background color** — what dead or empty cells show. This is always spatially uniform (same color across the entire canvas at any moment) and may morph over time.
2. A **cell color** — what live cells display, driven by the activity signal `t` and shaped by `glow`.

The two are combined with a glow-weighted lerp so transitions are smooth:

$$\text{pixel} = \text{bg} \cdot (1 - \text{glow}) + \text{cellColor} \cdot \text{glow}$$

| Mode | Background | Cell color |
|---|---|---|
| **Original** | black | sine triplet (R/G/B at ~120° phase) × glow |
| **Grayscale** | `abs(sin(now))` morph, black→white bell curve | same sine, single channel |
| **Red** | `#CC0000` fixed | cycles from `#CC0000` → white, bell-curve biased toward white |
| **NC State** | linearly sweeps through 7 brand colors | NC State palette lookup, cycles with normalized glow |
| **Rainbow** | full RGB sine triplet at Original's cycling rate | same sine triplet per-cell with normalized glow |
| **Rainbow Slow** _(More)_ | full RGB sine triplet at NC State's slow rate | same sine triplet per-cell with normalized glow |
| **Fire** _(More)_ | black | orange/yellow flickering |
| **Ice** _(More)_ | black | blues and cyans |
| **Ember** _(More)_ | black | deep reds and oranges |
| **Aurora** _(More)_ | black | greens and magentas |
| **Sunset** _(More)_ | black | purples → oranges → yellows |
| **Ocean** _(More)_ | black | deep blues and teals |
| **Diverging** _(More)_ | black | blue → white → red by activity |
| **Viridis** _(More)_ | black | purple → teal → yellow |
| **Inferno** _(More)_ | black | black → purple → orange → yellow |

The **NC State** background uses a wrapping linear sweep through the 7-color extended palette (Reynolds Red → Pyroman Flame → Hunt Yellow → Genomic Green → Carmichael Aqua → Innovation Blue → Bio-Indigo), cycling continuously at a constant rate with no easing. Modes using **normalized glow** (`glowN = (glow − 0.2) / 0.8`) ensure dead cells show only the background color, while alive cells transition smoothly into the cell palette.

---

## What this means for art

The artist defines the rules. The math writes the image.

There is no hand-placed color, no brush, no filter applied after the fact. What you see is the direct visual encoding of a simulation — activity, memory, and time translated into light. Complexity, beauty, and surprise emerge from a handful of arithmetic operations repeated thousands of times per second. The medium is computation.
