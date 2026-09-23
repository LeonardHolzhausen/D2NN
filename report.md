# Towards a DIY diffractive optical neural network at 532 nm

Task selection, reference ceilings, and a data problem found during
benchmarking.

Leo, independent project. Interim report, September 2026.

## Abstract

A diffractive optical neural network (D²NN) does its computation with
passive glass layers and laser light instead of electronics. This report
covers the first two stages of a DIY attempt to build one at 532 nm.

Because such a network can only ever compute a fairly simple class of
functions, a polynomial classifier trained on the same data gives an
upper limit for how well the optical version can possibly do. That upper
limit was used to pick the task. The first idea, predicting six
geometric properties of two line segments, failed the test: the angle
between the lines could not be predicted at all (R² near zero) and even
the yes/no question "do the lines cross" only reached 60-66% against a
52% baseline. The task was changed to classifying four shapes on a 16x16
image.

During benchmarking a network reported 100% accuracy with an
impossibly small loss. The cause was data leakage: 83% of the test
images were exact copies of training images, because the image generator
can only produce about 360 different pictures for three of the four
classes. After removing duplicates and balancing the classes, a CNN
still reaches 99.2%, but the optical upper limit drops to 50.8% against
25% for chance. A test with a better image generator raises that limit
to 82.1%, which defines the next step.

## 1. Introduction

In a D²NN (Lin et al., 2018), laser light passes through several thin
layers that delay the light slightly differently at every point. Between
the layers the light spreads out and mixes. A camera looks at the far
end, where each class has its own small region, and the brightest region
is the answer. The layers are designed on a computer and then made
physically.

Published D²NNs were 3D printed for terahertz radiation, where the
structures are a fraction of a millimetre in size. This project asks
whether the same thing can be done with green laser light at 532 nm and
cheap equipment, and whether the real device then behaves like its
computer model.

The aim is not speed. At 16x16 pixels an ordinary laptop does the same
arithmetic in microseconds. The aim is to check that the physical device
matches the simulation it was designed in.

This report covers everything before the optics: choosing the task,
building the dataset, and measuring what standard software models
achieve on it. It also records two mistakes, because both changed the
plan.

## 2. Background

### 2.1 What the optics can compute

Each layer only delays the light; it never makes a decision. Putting
several such layers behind each other still adds up to one big linear
operation on the light wave. The only step that is not linear is the
camera, which measures brightness, and brightness is the square of the
wave. So the score for class k is

```math
I_k = \sum_{x \in R_k} \bigl| (W E_{\mathrm{in}})(x) \bigr|^2
```

where W is the single matrix that describes the whole optical stack and
R_k is the camera region belonging to class k.

Two things follow from this.

First, a normal trained neural network cannot simply be converted into
optics, because a normal network applies a nonlinear step after every
layer and the optics has none. The original plan was exactly this
conversion, and it was dropped. The same objection was published as a
comment on the 2018 D²NN paper, and the original authors agreed with the
maths while arguing that extra layers still help in practice.

Second, a classifier that uses the input pixels and all products of
pairs of pixels, here a support vector machine with a degree-2
polynomial kernel, is an upper limit for the optical network on the same
data. The optics can only reach part of what that classifier can
express, so the limit does not have to be reachable, but nothing can go
above it.

### 2.2 Controls

To show the optics does anything useful, the network has to beat a
simple linear classifier on the raw input image, and another one on a
blurred copy of the input. Without those controls, a camera seeing a
slightly blurred input plus some software could explain the result.

## 3. Methods

### 3.1 Task A: two line segments (abandoned)

A generator draws two line segments with random angle, length and
position on a black-and-white image, and calculates six labels exactly:
the angle between the lines, the ratio of their lengths, whether they
cross, whether they are parallel, whether they overlap, and their
smallest distance.

An early version always put line 1 in the left half and line 2 in the
right half of the image. That made labels such as the length ratio
depend on where the lines were, not only on the lines themselves. It was
fixed by placing both lines freely and sorting them by length.

### 3.2 Task B: shape classification (current)

A second generator draws one filled shape per image: circle, square,
triangle with random width and height, or plus sign. The size is between
`image_size // 8` and `(image_size - 1) // 2`, and the position is
random but always keeps the shape fully inside the image. Coordinates
are whole pixels and the images are black and white.

### 3.3 How the models were tested

- Duplicate images are removed before the data is split into training
  and test sets, so no test image is also a training image.
- After that, every class is cut down to the size of the smallest class,
  so accuracy is not dominated by one class.
- Every number is an average over three dataset seeds, with the standard
  deviation.
- Models: ridge classifier, logistic regression, support vector machine
  with a degree-2 polynomial kernel (the optical upper limit), a small
  fully connected network (64 and 32 units), and a CNN with two or three
  convolution blocks, a 64-unit dense layer, Adam and early stopping.
- Tools: Python, NumPy, OpenCV, scikit-learn, TensorFlow/Keras.

## 4. Results

### 4.1 Task A: continuous values cannot be predicted

Degree-2 kernel models on 1500 images, 30% test split:

| Resolution | "Do they cross" accuracy | Majority baseline | Angle $`R^2`$ |
|---|---|---|---|
| 8x8 | 66.0% | 51.6% | -0.01 |
| 16x16 | 61.3% | 51.8% | 0.00 |
| 32x32 | 62.2% | 53.8% | -0.01 |
| 128x128 | 63.3% | 51.8% | 0.00 |

An $`R^2`$ of zero means the model does no better than always guessing
the average angle. A purely linear model was at chance level for both
labels.

Counting labels over 300000 random samples showed a second problem. The
lines cross in 48.6% of cases, are parallel in 0.56%, and overlap in
0.0003% (one single case). Three of the six labels are therefore far too
rare to learn.

### 4.2 Task B: first quick tests

These early tests used a separate generator and did not remove
duplicates, so the absolute numbers are probably too high (see 4.3). The
comparisons within each test are still useful:

- Letting the shapes rotate freely pushed the upper limit down to 54% at
  16x16. Turning every shape into the same orientation first, before
  the model sees it, brought it back to 91%.
- Raising the smallest allowed shape size from 1/8 to 1/4 of the image
  raised the limit from 75.6% to 92-94% at 8x8, and from 80.0% to 96-99%
  at 16x16.
- Giving the triangle random corner angles did not hurt accuracy.

### 4.3 Data leakage in the first CNN result

The first CNN on the shape generator (4000 images, 16x16) reported 100%
test accuracy with a loss of $`4 \times 10^{-10}`$. A loss that close to
zero is not realistic for images the model has never seen. Checking the
data showed:

- the 4000 samples contained only 1125 different images
- 664 of the 800 test images, that is 83%, were exact copies of training
  images

The reason is that with whole-pixel coordinates at 16x16 there are only
a few possible sizes and positions per shape. After removing duplicates
the CNN still reached 100%, on 225 test images, but with a realistic
loss of $`2 \times 10^{-4}`$.

Removing duplicates revealed a second issue. Out of 20000 draws at 16x16
there were 363 different circles, 364 squares, 383 plus signs, but 3049
triangles. Without balancing, a model that always answers "triangle"
already scores 56%. At 8x8 it is worse: 36 images appeared with two
different labels, because very small shapes of different classes look
identical. 8x8 is therefore not usable for this task.

### 4.4 Corrected benchmark at 16x16

363 images per class, 25% test split, three seeds:

| Model | Test accuracy |
|---|---|
| Chance | 25.0% |
| Ridge on raw pixels | 25.9 ± 1.4% |
| Degree-2 kernel (optical upper limit) | 50.8 ± 2.1% |
| Fully connected network (64, 32) | 51.4 ± 1.0% |
| CNN (single seed) | 99.2% |

Moving every shape to the middle of the image before training was tried
as a fix. It leaves only 6 to 8 different images per class, so it does
not help.

### 4.5 A better image generator

Shapes were drawn with fractional sizes and positions on a 64x64 canvas
and then shrunk to 16x16, which gives grey edge pixels instead of hard
ones. This makes almost every image different. Classes were balanced
while generating, and the test set used its own seed.

| Training images | Duplicates in test set | Ridge | Upper limit | Fully connected | CNN |
|---|---|---|---|---|---|
| 1000 | 2 / 2000 | 53.4% | 71.1% | 82.3% | - |
| 4000 | 14 / 2000 | 58.9% | 77.2% | 93.3% | - |
| 12000 | 37 / 2000 | 59.4% | 82.1% | 98.2% | 100% |

Converting the same images back to pure black and white gave similar
limits (70.0, 77.5, 82.2%) but many more duplicates, up to 19% of the
test set.

## 5. Discussion

**Why angles fail but crossing partly works.** Whether two segments
cross can be decided by multiplying coordinates together and checking
signs, which is close to what a degree-2 model can express. Getting the
angle of a line requires an arctangent, and no polynomial matches that
over a wide range. On top of that, a yes/no answer only has to fall on
the right side of a boundary, while a predicted number has to be
correct. That is why the angle fails at every resolution: the limit
comes from the type of model, not from the image size.

**How big the gap really is.** An earlier estimate put the gap between
the CNN and the optical upper limit at about 6 percentage points. That
estimate came from data with duplicates and was wrong. On clean data the
gap is about 48 points for the whole-pixel dataset and about 18 points
for the improved generator. The main reason is position. A CNN looks for
the same pattern everywhere in the image, so it does not care where the
shape sits. The kernel model, and the optical network with its fixed
glass layers, have to learn every position separately from examples.
With 363 examples per class that is hopeless. With the better generator
and about 3000 per class it mostly works, and the limit was still rising
at the largest training set tested.

**Why the leakage mattered.** When only a limited number of different
images exist, a model that memorises all of them scores 100% on new
draws from the same generator. That says nothing about recognising
shapes it has never seen, which is the actual claim, so only the
duplicate-free test means anything.

## 6. Limitations

- The degree-2 kernel is an upper limit. What the optical network really
  reaches is unknown until it has been simulated.
- Some results come from a single seed (CNN) or from tests without
  duplicate removal (section 4.2).
- The improved generator is a quick test, not yet the project's dataset.
- There is no optical simulation and no hardware result yet.
- The references come from secondary reading and still need to be
  checked against the original papers.

## 7. Next steps

1. Rebuild the dataset with the improved rendering, balanced classes,
   stored generation parameters, seeds and metadata.
2. Find out where the upper limit stops rising, somewhere between 12000
   and 50000 training images. That value is the target for the optical
   network.
3. Write a simulation of light travelling between the layers, and check
   it against known cases before trusting it.
4. Train one to three optical layers in that simulation, first with
   freely chosen delays and then with only two allowed values, since
   only two can be made by hand. Compare against the controls from
   section 2.2.
5. Only then: test gratings, photoresist tests, and the optical bench.

## References

1. X. Lin et al., "All-optical machine learning using diffractive deep
   neural networks", Science 361, 1004 (2018).
2. H. Wei et al., "Comment on 'All-optical machine learning using
   diffractive deep neural networks'", arXiv (2018), and the authors'
   response.
3. J. Li et al., "Class-specific differential detection in diffractive
   optical neural networks improves inference accuracy", Advanced
   Photonics 1, 046001 (2019).
4. D. Pierangeli, G. Marcucci, C. Conti, "Photonic extreme learning
   machine by free-space optical propagation", Photonics Research 9,
   1446 (2021).
5. J. W. Goodman, "Introduction to Fourier Optics".

## Appendix: reproducing the numbers

All numbers in section 4 come from fixed-seed runs of the shape
generator in `dataset.py` (`min_size = image_size // 8`) together with
standard scikit-learn / TensorFlow models (ridge, degree-2 kernel SVM,
small fully connected network, CNN), following the deduplication and
class-balancing procedure described in section 3.3. The individual
benchmark scripts are being cleaned up and will be added to this
repository shortly.