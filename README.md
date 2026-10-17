# Buffon's Needle with Manim

A mathematical animation of Buffon's needle problem, from the crossing
geometry and probability calculation to a Monte Carlo estimate of pi.

The presentation is written for **Manim Community 0.19.0**, using the Cairo
renderer. It contains an introduction, the crossing rule, three example needle
positions, a probability derivation, and a 10,000-drop simulation.

## The Mathematics

For parallel lines separated by distance $d$ and a needle of length
$0 < \ell \leq d$, assume the center's position modulo the line spacing and the
needle's orientation are uniform and independent.

Let $X$ be the distance from the needle's center to the nearest line, and let
$\Theta$ be its acute angle to the horizontal. A crossing occurs when

$$
X \leq \frac{\ell}{2}\sin\Theta.
$$

Since $X \sim U(0,d/2)$ and $\Theta \sim U(0,\pi/2)$, the crossing probability is

$$
p = \frac{2\ell}{\pi d}.
$$

If $C_N$ of the first $N$ independent drops cross a line, the running estimate is

$$
\widehat{\pi}_N = \frac{2\ell}{d}\frac{N}{C_N}, \qquad C_N > 0.
$$

The estimate is undefined before the first crossing. As the sample size grows,
it converges to pi under these assumptions, but it need not get closer after
every drop. The probability formula above is not valid unchanged for needles
longer than the line spacing.

## Requirements

The development environment used:

| Component | Tested version |
| --- | --- |
| Python | 3.13.3 |
| Manim Community | 0.19.0 |
| NumPy | 2.2.5 |
| tqdm | 4.67.1 |
| Renderer | Cairo |
| Operating system | Windows |
| LaTeX distribution | MiKTeX |

The direct Python dependencies are pinned in `requirements.txt`. This is not a
complete lockfile for transitive dependencies. Other platforms have not been
validated for this project.

Install a LaTeX distribution with `latex` and `dvisvgm` available on your
`PATH`, because the presentation uses `Tex` and `MathTex`. On Windows, the
tested distribution is [MiKTeX](https://miktex.org/download). Allow its package
manager to install missing packages; first-time formula rendering can take
longer. LaTeX is a system dependency, not a pip package.

For other platforms or system-dependency problems, consult the
[Manim installation guide](https://docs.manim.community/en/stable/installation.html).
Keep this project's pinned Python package versions when following newer guides.
Manim 0.19.0 uses PyAV for video writing, so a separate FFmpeg executable is not
required for this silent presentation; see the
[0.19.0 release notes](https://docs.manim.community/en/stable/changelog/0.19.0-changelog.html).

## Installation

Clone the repository and enter it:

```sh
git clone https://github.com/4blue0/buffons-needle-manim.git
cd buffons-needle-manim
```

On Windows, create an environment with Python 3.13:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If you use Anaconda Prompt or Command Prompt, activate it with:

```bat
.venv\Scripts\activate.bat
```

In PowerShell, use:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activation is optional: if PowerShell blocks the activation script, use
`.\.venv\Scripts\python.exe` in place of `python` in all commands below.
There is no need to change the machine-wide execution policy.

Check the tools:

```sh
python -m manim --version
latex --version
dvisvgm --version
```

## Render the Presentation

From the repository directory, using the environment above:

```sh
python -m manim -pql needles_presentation.py FullScene
```

This renders a low-quality preview at 480p and 15 FPS, then opens the result.
For the presentation-quality render at 1080p and 60 FPS:

```sh
python -m manim -pqh needles_presentation.py FullScene
```

Omit `-p` to render without opening the video player. These commands create
video files even when previewing. Press `Ctrl+C` in the terminal to interrupt
a render.

The default output locations are:

```text
media/videos/needles_presentation/480p15/FullScene.mp4
media/videos/needles_presentation/1080p60/FullScene.mp4
```

Generated videos, temporary clips, and LaTeX cache files remain local and are
ignored by Git.

### Individual Scenes

Replace `FullScene` in the command with any of these scene names:

| Scene | Content |
| --- | --- |
| `IntroScene` | Opening title and introduction |
| `CrossingRuleScene` | Parallel lines, needle geometry, and crossing rule |
| `ThreeNeedlesScene` | Three example positions and rotating needles |
| `ProbCalcScene` | Probability distributions and integral derivation |
| `MonteCarloScene` | Simulation and running estimate of pi |
| `FullScene` | All five sections in sequence |

For example:

```sh
python -m manim -pql needles_presentation.py MonteCarloScene
```

### Preview a Range

```sh
python -m manim -pql -n 100,150 needles_presentation.py MonteCarloScene
```

The numbers are **zero-based animation indices**, not seconds or needle
numbers. Both endpoints are included, so this selects 51 animation steps.
Earlier steps are processed without rendering their frames to establish the
correct starting state. Indices change when animation calls are added or removed.

The custom `ProgressScene` shows one progress bar. A bounded range skips the
full-scene counting pass and counts only selected steps. Without an end limit,
the scene first runs a counting pass, which can take some time before rendering
begins. The times in the bar are `[elapsed | estimated remaining]`; they are
rendering times, not the video's playback duration.

## Simulation Details

- Needle length: 4; line spacing: 5; sample size: 10,000.
- NumPy seed: 42. Keeping the seed and sampling code unchanged makes comparisons
  between renders reproducible.
- Orientations are sampled on $[0,\pi)$; using the absolute vertical projection
  is equivalent to folding them into the acute-angle convention above.
- The first 100 drops are shown individually. Later updates use batches of 20
  through 1,000 drops, then batches of 250 through 10,000.
- All 10,000 drops contribute to the crossing count and estimate. The drawing
  shows only the newest 20 needles from each batch and keeps at most 80 visible.
- Green means a crossing; gray means no crossing. Needles are white during the
  drop and bounce, and counters update after landing.
- The bounce returns to the sampled landing position and angle; it does not
  change the crossing result.
- The yellow curve is the running estimate, and the teal dashed line marks pi.
  The graph changes scale at sample-count milestones. Values outside a stage's
  vertical range are omitted from the visible curve, not from the calculation.

With the pinned environment and default seed, the simulation produces 5,145
crossings and a final estimate of approximately 3.10982. This is a finite-sample
result, not a guarantee of a particular accuracy.

## Editing

All animation code is in `needles_presentation.py`. The functions
`intro_animation`, `draw_parallel_lines`, `different_needles`,
`probability_calculations`, and `monte_carlo_simulation` define the five sections.
`needle_drop_animation` handles the landing effect, and `ProgressScene` handles
terminal progress.

The booleans in `FullScene.construct` select the sections for a combined render.
The separate scene classes are convenient for testing without changing those
booleans.

The simulation is authored for the default 10,000-drop layout. Changing
`total_throws` requires reviewing `checkpoints` and the graph milestones as well.
Changing physical dimensions or the center sampling region also requires
reviewing the displayed line positions and the crossing assumptions; these are
not yet general-purpose configuration options.

## Troubleshooting

- **`manim` is not recognized:** use `python -m manim` with the project
  environment, or use its Python executable by full path.
- **LaTeX fails:** check `latex` and `dvisvgm`, then inspect the relevant log
  under `media/Tex/` for missing packages or errors.
- **A pydub warning mentions FFmpeg:** this environment can emit that warning
  while successfully rendering this silent presentation. Inspect the actual
  exception if rendering fails; audio workflows may require additional tools.
- **A duration is too short:** animations cannot be shorter than one frame.
  At 15 FPS, one frame is about 0.0667 seconds.

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 Papias Periklis.
