# Introduction
A toy project based on a global search framework I've concocted. Conceptually, the idea is to perform a low-resolution scan of an energy landscape to determine where the critical points are located. The scan starts with a stitch boundary, which is a set of vertices and edges (equivalently, vectors) with inwards orientation. The vectors (known as sutures) are then used to calculate the gradients of the landscape at the points and in the directions of the individual sutures. Based on the values of the initial boundary subsequent regions, internal to the first boundary, are chosen to narrow the search for critical points. This process is repeated until termination conditions are met. The collective gradients are used to create a low-resolution representation of the landscape. Once the low-resolution representation is created, further searching can occur with high-resolution algorithms (such as simulated annealing, genetic algorithms, SGD, etc...) to find an optimal result.

Presently, there are two main variants of a stitch boundary: The $+$ variant and the $\times$ variant.

<img src="assets/smallest_StitchBoundaries.png" alt="Smallest StitchBoundaries" width="300">

<br>

# Stitch Boundaries
In formaly writing, the two variants take on the notation from before. In code, the $+$ variant stitch boundary takes on the notation PStitchBoundary. Similarly, the $\times$ variant stitch boundary takes on the notation XStitchBoundary. Let every stitch boundary be divided into components categorized and named after the cardinal points and defined as follows:

Let:

$North(y_0, s_l, I) = \{((i, y_0),(i, y_0+s_l))|i\in I \}$

$South(y_0, \Delta{y}, s_l, I) = \{((i, y_0+\Delta{y}),(i, y_0 + \Delta{y} - s_l))|i\in I\}$

$West(x_0, s_l, J) = \{((x_0, j),(x_0 + s_l, j))|j\in J\}$

$East(x_0, \Delta{x}, s_l, J) = \{((x_0 + \Delta{x}, j),(x_0 + \Delta{x} - s_l, j))|j\in J\}$

Where $x_0$ and $y_0$ are the inital points for $x$ and $y$, respectively. $\Delta{x}$ and $\Delta{y}$ are the width and height of the boundary, respectively. For some sets $I$ and $J$, dependent on the type of stitch boundary.

<br>

## PStitchBoundary
A $+$ varient stitch boundary is the set:
$+(x_0, y_0, \Delta{x}, \Delta{y}, s_l) = North(y_0, s_l, I) \cup South(y_0, \Delta{y}, s_l, I) \cup West(x_0, s_l, J) \cup East(x_0, \Delta{x}, s_l, J)$

Where $I=[x_0 + 1, x_0 + \Delta{x})\subset\mathbb{Z}$ and $J=[y_0 + 1, y_0 + \Delta{y})\subset\mathbb{Z}$

Visually, a $+$ variant expands in the following way:
<img src="assets/PStitchBoundary_expansion.png" alt="PStitchBoundary Expansion" width="800">

The inital points and suture length are omitted for illustrative purposes. The tuples along side each stitch boundary indicate the width and height, respectively.

When superimposed over a grid, it may look like the following:

<img src="assets/PStitchBoundary.png" alt="PStitchBoundary" width="300">

<br>

## XStitchBoundary
In addition to the cardinal sets, a $\times$ variant stitch boundary also includes diagonal sutures:
Let $Diag(x_0, y_0, \Delta{x}, \Delta{y}, s_l) = \{ ((x_0, y_0), (x_0 + s_l, y_0 + s_l)),  ((x_0+\Delta{x}, y_0), (x_0+\Delta{x}-s_l, y_0+s_l)),  ((x_0, y_0 + \Delta{y}),(x_0 + s_l, y_0 + \Delta{y} - s_l)),  ((x_0 + \Delta{x}, y_0 + \Delta{y}), (x_0 + \Delta{x} - s_l, y_0 + \Delta{y} - s_l)) \}
$

Thus an $\times$ varient stitch boundary is the set:
$\times(x_0, y_0, \Delta{x}, \Delta{y}) = North(y_0, s_l, I) \cup South(y_0, \Delta{y}, s_l, I) \cup West(x_0, s_l, J) \cup East(x_0, \Delta{x}, s_l, J) \cup Diag(x_0, y_0, \Delta{x}, \Delta{y}, s_l)$

Where $I=[x_0 + 2, x_0 + \Delta{x} - 1)\subset\mathbb{Z}$ and $J=[y_0 + 2, y_0 + \Delta{y} - 1)\subset\mathbb{Z}$

Visually, an $\times$ variant expands in the following way:
<img src="assets/XStitchBoundary_expansion.png" alt="XStitchBoundary Expansion" width="800">

The inital points and suture length are omitted for illustrative purposes. The tuples along side each stitch boundary indicate the width and height, respectively.

When superimposed over a grid, it may look like the following:

<img src="assets/XStitchBoundary.png" alt="XStitchBoundary" width="300">

<br>

# Stitch Bands
I've devised derivatives of the stitch boundaries to evaluate properties like curl. These derived structures are called stitch bands. Stitch bands possess two closed simple curves, one along the outer vertices of the boundary and one along the inner vertices of the boundary. These properties may be of particular interest to systems in complex space.

## PStitchBand
<img src="assets/PStitchBand.png" alt="PStitchBand" width="300">

## XStitch Band
<img src="assets/XStitchBand.png" alt="XStitchBand" width="300">
