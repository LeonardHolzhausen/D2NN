# D²NN project — design document

A DIY diffractive optical neural network at 532 nm, designed in a
computer simulation and then checked against real hardware.

Last updated: September 2026. Stages 1 and 2 are done, Stage 3 is next.

## 1. Goal

Build a small optical system that recognises simple shapes using green
laser light, and test whether the real device behaves the way the
simulation says it should.

Speed is not the point. At 16x16 pixels and four classes a laptop does
the same arithmetic in microseconds, and no home-built optics will beat
that. The claim being tested is narrower: a network designed entirely in
simulation, then built with cheap equipment, does what it was designed
to do.

```
shape dataset (16x16)
    -> software reference models (linear, polynomial kernel, CNN)
    -> simulation of light travelling between layers
    -> layer patterns trained directly in that simulation
    -> patterns converted into a fabrication recipe
    -> photoresist layers on glass + 532 nm bench + camera
    -> compare hardware against simulation
```

## 2. Question and hypotheses

Can an optical network, trained in a light simulation and built as
two-level phase layers with DIY equipment, reproduce its simulated
behaviour at 532 nm?

These should be fixed in writing before any physical measurement:

- H1: the simulated network lands at or below the polynomial-kernel
  limit for the same dataset, and clearly above the linear baseline.
  Anything above that limit means the simulation is wrong.
- H2: allowing only two delay values instead of freely chosen ones costs
  less than 10 percentage points of simulated accuracy, if the training
  takes the restriction into account.
- H3: on the same test images, the four measured brightness values of
  the real device match the simulated ones with a correlation of at
  least 0.8, and the predicted class agrees in at least 80% of cases.
  Both numbers are proposals and must be fixed before measuring.
- H4: the optical system beats a simple linear classifier on the raw
  input image and on a blurred copy of it. Otherwise the optics is not
  contributing anything.

## 3. Scope

Stages 1 to 4 (dataset, reference models, working simulation, trained
network in simulation, plus the analysis of what this kind of optics can
and cannot do) are a complete result on their own. (See section 13 for
the full stage-by-stage breakdown and what has to pass before each stage
counts as done.)

Stages 5 to 7 (fabrication, bench, measurement) are the open-ended part.
If they take much longer than planned, the first block still stands.

## 4. Background

### 4.1 How a D²NN works

Laser light passes through several thin layers. Each layer delays the
light a little differently at every point, and in the gaps between
layers the light spreads out and mixes. A camera looks at the output
plane, each class owns a small region there, and the brightest region is
the answer. The layer patterns are designed by a computer and then made
physically (Lin et al., 2018).

### 4.2 What such a network can compute

The layers only delay light, they never make decisions, so several
layers behind each other still add up to one linear operation. The only
non-linear step is the camera, which measures brightness, and brightness
is the square of the light wave:

```math
I_k = \sum_{x \in R_k} \bigl| (W E_{\mathrm{in}})(x) \bigr|^2
```

where W describes the whole optical stack and R_k is the camera region
for class k.

Two consequences:

- A normal trained neural network cannot be converted into optics,
  because a normal network applies a non-linear step after every layer
  and the optics has none. The original plan was exactly this
  conversion, and it was dropped. The same objection was published as a
  comment on the 2018 paper, and the original authors accepted the maths.
- A classifier using the pixels and all products of pixel pairs, here a
  support vector machine with a degree-2 polynomial kernel, is an upper
  limit for the optical network on the same data. The optics can only
  reach part of what that classifier expresses, so the limit does not
  have to be reachable, but nothing goes above it.

### 4.3 Which tasks fit

From the pilot study (report, section 4.1): a yes/no question that comes
down to multiplying coordinates and checking signs is partly learnable.
A continuous value such as an angle is not, because getting an angle
needs an arctangent and no polynomial matches that over a wide range. A
yes/no answer also only has to land on the right side of a boundary,
while a predicted number has to be correct. That is why the project now
uses classification.

### 4.4 Is the light doing anything?

The test for any setup: could a single linear operation on the raw input
pixels produce the same output? If yes, the optics is decoration. The
practical version is H4 above, including the blurred-input control. That
control catches the usual way optical demos fool themselves, where the
camera sees a slightly blurred copy of the input and software does the
real work.

### 4.5 Position is the hard part

The light spreads the same way no matter where the shape sits, but the
layer patterns are fixed in place, so the network has to learn every
position from examples. The benchmarks show this is the main difficulty:
a CNN, which looks for the same pattern everywhere in the image, reaches
99 to 100%, while models without that property stay far lower unless
they get much more data.

### 4.6 Other optical approaches

| Approach | Does the light compute? | Trained optics | DIY fit |
|---|---|---|---|
| Passive layers, one camera readout (this project) | yes, the whole function | yes | good |
| Extra camera relay between layers | yes, several non-linear steps | yes | moderate |
| Fixed optics plus trained software readout | yes, but nothing task-specific | no | very good |
| Static mask with no mixing | no | no | not worth building |

The third option stays on the list as a cheap side experiment once any
layer exists, as long as it passes the H4 controls.

## 5. Task and dataset

### 5.1 Task

Four classes, one filled shape per image: circle, square, triangle with
random width and height, plus sign. No rotation at the moment.

### 5.2 Current generator (dataset.py)

- Square image, black and white, whole-pixel coordinates.
- Size between `image_size // 8` and `(image_size - 1) // 2`.
- Random position, always fully inside the image.
- Labels stored as `label` (0-3) and `label_name`, classes drawn evenly.
- `seed` argument with its own random generator.

### 5.3 Why this generator has to be replaced

With whole-pixel positions and sizes there are only about 363 different
circles, 364 squares and 383 plus signs at 16x16, against roughly 3000
triangles. That causes three problems:

- Random draws repeat themselves. In one run 83% of the test images were
  exact copies of training images.
- Removing duplicates leaves the classes badly unbalanced, so plain
  accuracy stops meaning much.
- On a duplicate-free, balanced dataset the upper limit is only about
  51%, against 25% for chance.

At 8x8 it is worse: 36 images appeared with two different labels,
because very small shapes of different classes look identical. 8x8 is
not usable.

### 5.4 Dataset v2, the next job

Tested already (report, section 4.5): draw each shape with fractional
size and position on a canvas four times larger, then shrink it to
16x16. The edges become grey instead of hard, and almost every image is
different.

| Training images | Ridge | Upper limit | Fully connected | CNN |
|---|---|---|---|---|
| 1000 | 53.4% | 71.1% | 82.3% | - |
| 4000 | 58.9% | 77.2% | 93.3% | - |
| 12000 | 59.4% | 82.1% | 98.2% | 100% |

Duplicates between training and test drop to about 2%. The upper limit
was still rising at 12000 images, so the point where it stops needs to
be found before Stage 4.

Requirements for v2:

- balanced classes while generating
- store the generation parameters per image, not only the pixels, so any
  resolution can be redrawn from the same dataset
- save as `.npz` plus a JSON file with seed, image size, scale factor,
  generator version and git commit
- remove duplicates before splitting into training and test data

### 5.5 Rotation, if added later

Free rotation pushed the upper limit down to 54%. Turning every shape
into the same orientation first brought it back to 91%. This step has to
stay in software, because working out the rotation angle needs an
arctangent, which the optics cannot do. It happens while preparing the
input image, before any light is involved.

## 6. Reference models (Stage 2)

16x16, duplicate-free, balanced classes. Details in the report, section
4.4.

| Model | Whole-pixel dataset | Improved generator (12k) | Role |
|---|---|---|---|
| Ridge on raw pixels | 25.9% | 59.4% | H4 control, linear floor |
| Degree-2 kernel | 50.8% | 82.1% | upper limit for the optics |
| Fully connected (64, 32) | 51.4% | 98.2% | reference without convolution |
| CNN | 99.2% | 100% | best available reference |

## 7. Light simulation (Stage 3)

### 7.1 Method

The angular spectrum method: transform the light field into spatial
frequencies with an FFT, give each frequency the phase shift it picks up
over the distance z, and transform back.

```math
E(x, y, z) = \mathcal{F}^{-1}\left\{ \mathcal{F}\{E(x, y, 0)\} \cdot e^{\,i z \sqrt{k^2 - k_x^2 - k_y^2}} \right\}
```

Frequencies that would need an imaginary square root do not travel and
are set to zero. Implementation with `tf.signal.fft2d`, so the model can
be trained with the same Keras tools already in use.

### 7.2 Sampling

Each of the 16x16 regions gets several simulation pixels, around 8x8,
and the field is padded with zeros by at least a factor of two on each
side, so light does not wrap around the edge of the FFT.

### 7.3 Tests before trusting it

1. Total brightness stays the same across a propagation step.
2. A single rectangular opening produces the known diffraction pattern,
   and a laser beam widens the way the standard formula says.
3. Propagating forward and then backward returns the original field.
4. A simulated grating sends light into the angles given by
   sin(θ) = m·λ/Λ.
5. Doubling the sampling density and the padding changes the result by
   less than 1%.

## 8. Network design (Stage 4)

- Input: the 16x16 image, encoded as brightness.
- Layers: start with one, then two or three, each with 16x16 adjustable
  regions, so 256 values per layer.
- Delay values: only two allowed (0 and half a wavelength), because only
  two can be made by hand. Train with free values that are pushed
  towards two during training, and report both numbers for H2.
- Output: four camera regions, one per class, placed close together so
  they see the same illumination. Optionally eight regions in pairs,
  where the class score is the difference within a pair (Li et al.,
  2019).
- Loss: cross-entropy over the normalised region brightness values.
- Record all four brightness values per test image, not only the
  predicted class. H3 compares exactly those.

## 9. Physical size at 532 nm

### 9.1 Distance between layers

Light leaving a region of width p spreads at an angle of about λ/p. To
reach across the full width of the next layer (N·p), the gap has to be
roughly

```math
z \approx \frac{N p^2}{\lambda}
```

The distance grows with the square of the region size, and shrinks if
fewer or smaller regions are used. An earlier draft had this backwards.
For N = 16:

| Region size p | Total width | Distance z |
|---|---|---|
| 50 µm | 0.8 mm | 7.5 cm |
| 100 µm | 1.6 mm | 30 cm |
| 150 µm | 2.4 mm | 68 cm |
| 200 µm | 3.2 mm | 1.2 m |

Smaller regions keep the bench short but need sharper masks
(professionally printed film instead of a laser printer) and make the
device very small to handle. This is only a first estimate; the
simulation decides the real distance.

Later option: a lens between the layers does the mixing over a much
shorter distance, at the cost of more alignment work.

### 9.2 Layer thickness is not the same as layer distance

The photoresist pattern is about 0.4 µm thick and sets the delay. The
distance z is centimetres of empty air between layers. The two have
nothing to do with each other, and thinner resist does not shorten the
bench.

### 9.3 Brightness

Filled shapes let much more light through than the thin lines of the
first task. Still to check in simulation: how bright the four output
regions are compared to the camera noise at realistic laser power.

## 10. Laser, coherence, safety

- 532 nm green DPSS laser, chosen because it is visible and the parts
  are cheap. The fabrication route in section 11 does not depend on the
  wavelength.
- The device relies on light waves adding up and cancelling, so the
  laser has to stay "in step" with itself over the length of the setup.
  Cheap modules manage only millimetres to centimetres. Plan: buy two or
  three, measure each one with a simple interferometer, keep the best. A
  single-frequency laser removes the problem and costs hundreds to
  thousands of euros.
- Beam preparation: microscope objective and pinhole to clean the beam,
  then a lens to make it parallel over a few millimetres.
- Safety: the eye is most sensitive around 532 nm. Goggles rated OD 4+
  at 532 nm specifically, closed beam path, no reflective jewellery. The
  German rules for the laser class need checking before buying.

## 11. Fabrication

### 11.1 Why photolithography and not holography

The hard part at 532 nm is thickness, not width. A useful delay accuracy
means controlling the layer thickness to about 100 nm, while features of
50 to 200 µm across are easy. Holographic recording at home only
produces regular stripe patterns, not arbitrary ones. Two-level
lithography turns the problem into "resist or no resist" at each region,
plus a single thickness to calibrate once.

### 11.2 Main route: two-level photoresist layers

The delay depends on thickness T:

```math
\varphi = \frac{2\pi (n-1)}{\lambda} T, \qquad T_{\pi} = \frac{\lambda}{2(n-1)} \approx 380\text{–}440\ \text{nm}
```

for a refractive index n of about 1.6 to 1.7. Procedure, one glass slide
per layer:

1. Make the black-and-white layer pattern and print it as a mask.
   A laser-printed transparency is enough for 100 µm regions and larger.
2. Clean a glass microscope slide with isopropanol or acetone.
3. Spin-coat a thin positive photoresist at roughly 4000 to 5000 rpm,
   which gives about 0.4 to 0.5 µm. Check against the manufacturer's
   spin curve.
4. Bake for about a minute at 110 to 115 °C, following the datasheet.
5. Press the mask against the slide and expose with a UV LED. Run a test
   series of exposure times first, since a home lamp is not calibrated.
6. Develop, rinse, dry. Exposed areas wash down to bare glass, unexposed
   areas keep the full thickness.
7. Check under a microscope, estimate the thickness from the
   interference colours, and test a calibration grating with the 532 nm
   laser before making real layers.

No etching, no wavelength-sensitive holographic material, and the UV
exposure needs no laser. If more than two delay values are wanted later,
the same process works with grey masks and a measured dose curve.

### 11.3 Side route: holographic grating, for calibration only

Recording a simple stripe pattern with two crossing laser beams, with
spacing Λ = λ / (2·sin θ), so a 10 µm spacing needs about 1.5 degrees.
This checks the laser, the stability of the bench and the diffraction
angles. It is not used for network layers.

### 11.4 What professional equipment would add

A mask aligner with chrome-on-glass masks reaches features of about a
micrometre, and university cleanrooms also have maskless UV writers.
That would allow smaller regions, more delay levels and more regions per
layer. None of it is needed for a first device.

## 12. Input and output

### 12.1 Input, which changes for every image

Option A, to start with: one printed transparency per test image,
swapped by hand in a slide holder. Grey levels can be faked with small
dot patterns, since a 1200 dpi printer puts about 7x7 dots into a 150 µm
region.

Option B, later: a small LCD panel with the backlight removed, driven
over HDMI. Caveats: the colour filters mean using green only and
grouping several LCD pixels per region, the panel scatters laser light,
and removing the backlight may destroy the panel.

### 12.2 Output

A camera at the output plane, four (or eight) regions added up in
software, a dark frame subtracted, and the normalised brightness values
stored for every image. Photodiodes would be simpler later, but the
camera works and switching would only add calibration work.

## 13. Stages and their tests

| Stage | Content | Status |
|---|---|---|
| 1 | Dataset generator | v1 done, v2 next |
| 2 | Reference models | done on v1, repeat on v2 |
| 3 | Light simulation | next |
| 4 | Network trained in simulation | planned |
| 5 | Fabrication tests | planned |
| 6 | Make the trained layers | planned |
| 7 | Bench and measurement | planned |

What has to pass before a stage counts as done:

Stage 1, dataset
- every class fits fully inside the image, for all seeds and sizes
- class balance within 5%
- the same seed gives the same dataset, different seeds do not
- count of different images, and of images that appear with more than
  one label, which must be zero
- a picture grid of at least 16 labelled samples

Stage 2, reference models
- duplicates removed before splitting, and the remaining overlap
  reported, which should be about zero
- balanced accuracy, averaged over at least three seeds
- a curve showing where the upper limit stops rising

Stage 3, simulation
- the five tests in section 7.3

Stage 4, simulated network
- accuracy at or below the upper limit and above the linear baseline
  (H1)
- free delay values compared against two allowed values (H2)
- the H4 controls, raw and blurred
- tolerance check: accuracy with 1 mm distance error, one region of
  sideways shift, and 10% thickness error

Stage 5, fabrication tests
- resist thickness within 10% of target
- calibration grating diffracts into the predicted angles

Stage 6, layers
- microscope check that the pattern matches the design

Stage 7, measurement
- H3 numbers written down before measuring
- the same test images measured on hardware and in simulation
- report correlation, class agreement and hardware accuracy

## 14. Decisions

Settled:

- four-class shape classification, continuous values dropped after the
  pilot
- training directly in the simulation, no conversion of an existing
  network
- 16x16 resolution, 8x8 rejected
- 532 nm, same laser for all bench work
- two-level photoresist layers, holography only for calibration
- printed transparencies for input first, LCD later
- success means agreement between hardware and simulation
- always remove duplicates before splitting, always report balanced
  results

Still open:

- dataset v2 details: scale factor, grey or black-and-white input
- number of layers (1 to 3) and region size (50 to 150 µm)
- four camera regions or eight in pairs
- which laser module, after the coherence tests
- whether to add rotation back in

## 15. Risks

| Risk | Likelihood | What can be done |
|---|---|---|
| Upper limit too low for a convincing result | medium | dataset v2, more data, smaller range of positions, paired camera regions |
| Two delay levels cost too much accuracy | medium | take the restriction into account during training, grey masks later |
| Resist thickness off target | medium | calibrate the spin speed, and use the tolerance check to see how much error is acceptable |
| Laser not coherent enough | medium | test several modules, keep path lengths similar |
| Aligning millimetre-sized layers | high | proper mounts, alignment marks on the masks, start with one layer |
| Camera noise against a weak signal | low to medium | check in simulation, longer exposure, averaging |
| Scope creep | high | stages 1 to 4 are defined as the finished core result |

## 16. Rough budget

Order of magnitude only, still to be confirmed.

| Item | Rough cost |
|---|---|
| 532 nm laser modules, 2 to 3 for testing | 20-80 EUR each |
| Laser goggles, OD 4+ at 532 nm | 50-150 EUR |
| Objective, pinhole, lenses, mounts, breadboard | 150-500 EUR, less if used |
| Camera | 30-300 EUR |
| Photoresist and developer | ask supplier |
| UV LED, DIY spin coater, hotplate | 50-150 EUR |
| Masks | 5-50 EUR per batch |
| LCD panel for option B | 20-40 EUR |

## 17. References

These come from secondary reading so far and still need checking against
the originals.

1. X. Lin, Y. Rivenson, N. T. Yardimci, M. Veli, Y. Luo, M. Jarrahi,
   A. Ozcan, "All-optical machine learning using diffractive deep neural
   networks", Science 361, 1004-1008 (2018).
2. H. Wei et al., "Comment on 'All-optical machine learning using
   diffractive deep neural networks'", arXiv (2018), and the authors'
   response.
3. J. Li, D. Mengu, Y. Luo, Y. Rivenson, A. Ozcan, "Class-specific
   differential detection in diffractive optical neural networks
   improves inference accuracy", Advanced Photonics 1, 046001 (2019).
4. J.-F. Morizur et al., "Programmable unitary spatial mode
   manipulation", JOSA A 27, 2524 (2010).
5. G. Labroille et al., "Efficient and mode selective spatial mode
   multiplexer based on multi-plane light conversion", Optics Express
   22, 15599 (2014).
6. G.-B. Huang, Q.-Y. Zhu, C.-K. Siew, "Extreme learning machine: theory
   and applications", Neurocomputing 70, 489-501 (2006).
7. D. Pierangeli, G. Marcucci, C. Conti, "Photonic extreme learning
   machine by free-space optical propagation", Photonics Research 9,
   1446 (2021).
8. J. W. Goodman, "Introduction to Fourier Optics".
9. Covestro Bayfol HX datasheet, and photoresist datasheets for spin
   curves and exposure dose.