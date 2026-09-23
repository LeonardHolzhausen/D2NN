# D²NN — DIY Diffractive Optical Neural Network at 532 nm

A from-scratch attempt to build a diffractive optical neural network
(D²NN): a classifier that computes with passive glass layers and green
laser light instead of a processor. Light passes through a few thin
layers that each delay it slightly differently at every point; between
layers the light spreads out and mixes; a camera reads out the answer
from where the light ends up. The layer patterns are designed in
simulation first and only then fabricated.

The goal isn't speed — a laptop does the same 16×16 classification in
microseconds and no home-built optics will beat that. The actual
question is narrower: **can a network designed entirely in a light
simulation, then built with cheap DIY equipment, reproduce that
simulated behaviour in hardware?**

**Status (September 2026):** Stages 1–2 (dataset, reference models) are
done, Stage 3 (light simulation) is next. No optical hardware has been
built yet — everything below the fold is software and simulation.

## Why a polynomial classifier caps what's possible

Because the layers only delay light and never make a decision, stacking
several of them is still mathematically one linear operation; the only
non-linear step is the camera measuring brightness. That means a
classifier using every pixel *and* every product of pixel pairs — here a
degree-2 polynomial-kernel SVM — is a hard upper limit for what the
optical network can ever reach on the same data. This is used throughout
to sanity-check results instead of just trusting whatever accuracy a
model reports.

That check caught a real bug: an early CNN benchmark reported 100%
accuracy with a suspiciously tiny loss. It turned out 83% of the test
images were exact duplicates of training images, because the first
dataset generator could only produce a few hundred distinct shapes per
class. After removing duplicates and balancing classes, the CNN still
gets 99.2%, but the honest optical upper limit drops to 50.8% (vs. 25%
chance) on that dataset — and a better image generator raises it to
82.1%. Full details, including the abandoned first task (predicting
continuous line-angle values, which polynomial models can't express),
are in [`report.md`](report.md).

| Model | Test accuracy (16×16, duplicate-free, balanced) |
|---|---|
| Chance | 25.0% |
| Ridge on raw pixels | 25.9% |
| **Degree-2 kernel — optical upper limit** | **50.8%** |
| Fully connected (64, 32) | 51.4% |
| CNN | 99.2% |

## Project structure

| File | What it is |
|---|---|
| [`project.md`](project.md) | Full design document: hypotheses, physical sizing at 532 nm, fabrication route (two-level photoresist lithography), simulation method, stage-by-stage acceptance criteria |
| [`report.md`](report.md) | Interim write-up of Stages 1–2: task selection, the duplicate-data bug, benchmark results |
| `dataset.py` | Synthetic shape dataset generator (circle / square / triangle / plus) |
| `DNN.py` | Reference CNN benchmark on the dataset (dedup + class balancing, then train/test) |
| `visualization.py` | Plotting helpers for dataset samples |
| `old/` | Superseded material from an earlier project direction (mmWave radar / 3D-printed terahertz optics), kept for history only — not part of the current 532 nm / photolithography approach |

## Running it

```bash
python -m venv .venv
source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt
python DNN.py
```

`DNN.py` builds a shape dataset, removes duplicate images before
splitting into train/test, balances the classes, and trains a small CNN
as the accuracy reference described in `report.md`.

## What's next

The light simulation (angular-spectrum propagation) and the trained
optical-layer design come next, followed by fabrication tests. See
`project.md` section 13 for the full stage plan and what has to pass
before each stage counts as done.

## References

- X. Lin et al., "All-optical machine learning using diffractive deep
  neural networks", *Science* 361, 1004–1008 (2018).
- J. Li et al., "Class-specific differential detection in diffractive
  optical neural networks improves inference accuracy", *Advanced
  Photonics* 1, 046001 (2019).

(Full reference list in `project.md` and `report.md`.)
