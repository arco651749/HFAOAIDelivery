# Chapter 9: Binary Morphology

> **Part**: `Part III: Particle Analysis` | **Pages**: `155 - 185`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


9
Binary Morphology


This chapter contains information about element structuring, connectivity,
and primary and advanced binary morphology operations.



## Introduction


Binary morphological operations extract and alter the structure of particles
in a binary image. You can use these operations during your inspection
application to improve the information in a binary image before making
particle measurements, such as the area, perimeter, and orientation.


A binary image is an image containing particle regions with pixel values
of 1 and a background region with pixel values of 0. Binary images are the
result of the thresholding process. Because thresholding is a subjective
process, the resulting binary image may contain unwanted information,
such as noise particles, particles touching the border of images, particles
touching each other, and particles with uneven borders. By affecting the
shape of particles, morphological functions can remove this unwanted
information, thus improving the information in the binary image.



## Structuring Elements


Morphological operators that change the shape of particles process a pixel
based on its number of neighbors and the values of those neighbors. A
neighbor is a pixel whose value affects the values of nearby pixels during
certain image processing functions. Morphological transformations use a
2D binary mask called a structuring element to define the size and effect of
the neighborhood on each pixel, controlling the effect of the binary
morphological functions on the shape and the boundary of a particle.



### When to Use


Use a structuring element when you perform any primary binary
morphology operation or the advanced binary morphology operation
Separation. You can modify the size and the values of a structuring element
to alter the shape of particles in a specific way. However, study the basic
morphology operations before defining your own structuring element.



## Chapter 9 Binary Morphology



### Concepts


The size and contents of a structuring element specify which pixels a
morphological operation takes into account when determining the new
value of the pixel being processed. A structuring element must have an
odd-sized axis to accommodate a center pixel, which is the pixel being
processed. The contents of the structuring element are always binary,
composed of 1 and 0 values. The most common structuring element is
a 3 × 3 matrix containing values of 1. This matrix, shown below, is the
default structuring element for most binary and grayscale morphological
transformations.


Three factors influence how a structuring element defines which pixels to
process during a morphological transformation: the size of the structuring
element, the values of the structuring element sectors, and the shape of the
pixel frame.



#### Structuring Element Size


The size of a structuring element determines the size of the neighborhood
surrounding the pixel being processed. The coordinates of the pixel being
processed are determined as a function of the structuring element. In
Figure 9-1, the coordinates of the pixels being processed are (1, 1), (2, 2),
and (3, 3), respectively. The origin (0, 0) is always the top, left corner pixel.



#### Figure 9-1. Structuring Element Sizes


Using structuring elements requires an image border. A 3 × 3 structuring
element requires a minimum border size of 1. In the same way, structuring
elements of 5 × 5 and 7 × 7 require a minimum border size of 2 and 3,


1
1
1
1
1
1
1
1
1


3 × 3
5 × 5
7 × 7


respectively. Bigger structuring elements require corresponding increases
in the image border size. For more information about image borders, refer
to the Image Borders section of Chapter 1, Digital Images.


Note
NI Vision images have a default border size of 3. This border size enables you to use
structuring elements as large as 7 × 7 without any modification. If you plan to use
structuring elements larger than 7 × 7, specify a correspondingly larger border when
creating your image.


The size of the structuring element determines the speed of the
morphological transformation. The smaller the structuring element,
the faster the transformation.



#### Structuring Element Values


The binary values of a structuring element determine which neighborhood
pixels to consider during a transformation in the following manner:


•
If the value of a structuring element sector is 1, the value of the
corresponding source image pixel affects the central pixel’s value
during a transformation.


•
If the value of a structuring element sector is 0, the morphological
function disregards the value of the corresponding source image pixel.


Figure 9-2 illustrates the effect of structuring element values during a
morphological function. A morphological transformation using a
structuring element alters a pixel P0 so that it becomes a function of its
neighboring pixel values.



#### Figure 9-2. Effect of Structuring Element Values on a Morphological Function


Structuring Element
Source Image
Transform Image


Neighbors used
to calculate the
new P0 value


New P0 value


0
1
0


0
1
0


1
0
1



#### Pixel Frame Shape


A digital image is a 2D array of pixels arranged in a rectangular grid.
Morphological transformations that extract and alter the structure of
particles allow you to process pixels in either a square or hexagonal
configuration. These pixel configurations introduce the concept of a pixel
frame. Pixel frames can either be aligned (square) or shifted (hexagonal).
The pixel frame parameter is important for functions that alter the value of
pixels according to the intensity values of their neighbors. Your decision to
use a square or hexagonal frame affects how NI Vision analyzes the image
when you process it with functions that use this frame concept. NI Vision
uses the square frame by default.


Note
Pixels in the image do not physically shift in a horizontal pixel frame. Functions that
allow you to set the pixel frame shape merely process the pixel values differently when you
specify a hexagonal frame.


Figure 9-3 illustrates the difference between a square and hexagonal pixel
frame when a 3 × 3 and a 5 × 5 structuring element are applied.



#### Figure 9-3. Square and Hexagonal Pixel Frames


1
Square 3 × 3
2
Hexagonal 3 × 3


3
Square 5 × 5
4
Hexagonal 5 × 5


1
2


3
4


If a morphological function uses a 3 × 3 structuring element and a
hexagonal frame mode, the transformation does not consider the elements
[2, 0] and [2, 2] when calculating the effect of the neighbors on the pixel
being processed. If a morphological function uses a 5 × 5 structuring
element and a hexagonal frame mode, the transformation does not consider
the elements [0, 0], [4, 0], [4, 1], [4, 3], [0, 4], and [4, 4].


Figure 9-4 illustrates a morphological transformation using a 3 × 3
structuring element and a rectangular frame mode.


Figure 9-4.  Transformation Using a 3 × 3 Structuring Element and Rectangular Frame


Figure 9-5 illustrates a morphological transformation using a 3 × 3
structuring element and a hexagonal frame mode.


Figure 9-5.  Transformation Using a 3 × 3 Structuring Element and Hexagonal Frame


Table 9-1 illustrates the effect of the pixel frame shape on a neighborhood
given three structuring element sizes. The gray boxes indicate the
neighbors of each black center pixel.


p'0 = T(p0, p2, p4, p5, p7)
1
1
0
1
0
1


0
1
0


Structuring Element


p1
p4
p6


Image


p2
p0
p7


p3
p5
p8


p'0 = T(p0, p2, p3, p4, p6)


1
1
0
1
0
1


0
1
0


Structuring Element
Image


p2
p0


p1
p4
p5 p6


p3


Square Frame


In a square frame, pixels line up normally. Figure 9-6 shows a pixel in a
square frame surrounded by its eight neighbors. If d is the distance from the
vertical and horizontal neighbors to the central pixel, then the diagonal
neighbors are located at a distance of
from the central pixel.



#### Figure 9-6. Square Frame


Hexagonal Frame


In a hexagonal frame, the even lines of an image shift half a pixel to the
right. Therefore, the hexagonal frame places the pixels in a configuration
similar to a true circle. Figure 9-7 shows a pixel in a hexagonal frame
surrounded by its six neighbors. Each neighbor is an equal distance d from
the central pixel, which results in highly precise morphological
measurements.



#### Table 9-1. Pixel Neighborhoods Based on Pixel Frame Shapes


Structuring Element Size
Square Pixel Frame
Hexagonal Pixel Frame


3 × 3


5 × 5


7 × 7


2d


2d
d


d
d


2d


2d
d
2d



#### Figure 9-7. Hexagonal Frame



## Connectivity


After you identify the pixels belonging to a specified intensity threshold,
NI Vision groups them into particles. This grouping process introduces the
concept of connectivity. You can set the pixel connectivity in some
functions to specify how NI Vision determines whether two adjoining
pixels are included in the same particle.


Use connectivity-4 when you want NI Vision to consider pixels to be part
of the same particle only when the pixels touch along an adjacent edge. Use
connectivity-8 when you want NI Vision to consider pixels to be part of the
same particle even if the pixels touch only at a corner.


With connectivity-4, two pixels are considered part of the same particle if
they are horizontally or vertically adjacent. With connectivity-8, two pixels
are considered part of the same particle if they are horizontally, vertically,
or diagonally adjacent. Figure 9-8 illustrates the two types of connectivity.



#### Figure 9-8. Connectivity Types


d


d
d


d


d
d


Figure 9-9 illustrates how connectivity-4 and connectivity-8 affect the way
the number of particles in an image are determined. In Figure 9-9a, the
image has two particles with connectivity-4. In Figure 9-9b, the same
image has one particle with connectivity-8.



#### Figure 9-9. Example of Connectivity Processing



### In-Depth Discussion


In a rectangular pixel frame, each pixel P0 has eight neighbors, as shown in
the following graphic. From a mathematical point of view, the pixels P1, P3,
P5, and P7 are closer to P0 than the pixels P2, P4, P6, and P8.


If D is the distance from P0 to P1, then the distances between P0 and its eight
neighbors can range from D to
D, as shown in the following graphic.


a.
b.


P8 P1 P2
P7 P0 P3
P6 P5 P4


2


2D D
2D
D
0
D


2D D
2D


A pixel belongs to a particle if it is located a distance of D from another
pixel in the particle. In other words, two pixels are considered to be part of
the same particle if they are horizontally or vertically adjacent. They are
considered as part of two different particles if they are diagonally adjacent.
In Figure 9-10, the particle count equals 4.



#### Figure 9-10. Connectivity-4


A pixel belongs to a particle if it is located a distance of D or
D from
another pixel in the particle. In other words, two pixels are considered to be
part of the same particle if they are horizontally, vertically, or diagonally
adjacent. In Figure 9-11, the particle count equals 1.



#### Figure 9-11. Connectivity-8



## Primary Morphology Operations


Primary morphological operations work on binary images to process
each pixel based on its neighborhood. Each pixel is set either to 1 or 0,
depending on its neighborhood information and the operation used.
These operations always change the overall size and shape of particles in
the image.


2


Use the primary morphological operations for expanding or reducing
particles, smoothing the borders of objects, finding the external and internal
boundaries of particles, and locating particular configurations of pixels.


You can also use these transformations to prepare particles for quantitative
analysis, to observe the geometry of regions, and to extract the simplest
forms for modeling and identification purposes.


The primary morphology functions apply to binary images in which
particles have been set to 1 and the background is equal to 0. They
include three fundamental binary processing functions—erosion, dilation,
and hit-miss. The other transformations are combinations of these
three functions.


This section describes the following primary morphology transformations:


•
Erosion


•
Dilation


•
Opening


•
Closing


•
Inner gradient


•
Outer gradient


•
Hit-miss


•
Thinning


•
Thickening


•
Proper-opening


•
Proper-closing


•
Auto-median


Note
In the following descriptions, the term pixel denotes a pixel equal to 1, and the term
particle denotes a group of pixels equal to 1.



#### Erosion and Dilation Functions


An erosion eliminates pixels isolated in the background and erodes the
contour of particles according to the template defined by the structuring
element.


For a given pixel P0, the structuring element is centered on P0. The pixels
masked by a coefficient of the structuring element equal to 1 are then
referred as Pi.


•
If the value of one pixel Pi is equal to 0, then P0 is set to 0, else P0 is
set to 1.


•
If AND(Pi) = 1, then P0 = 1, else P0 = 0.


A dilation eliminates tiny holes isolated in particles and expands the
particle contours according to the template defined by the structuring
element. This function has the opposite effect of an erosion because the
dilation is equivalent to eroding the background.


For any given pixel P0, the structuring element is centered on P0. The pixels
masked by a coefficient of the structuring element equal to 1 then are
referred to as Pi.


•
If the value of one pixel Pi is equal to 1, then P0 is set to 1, else P0 is
set to 0.


•
If OR(Pi) = 1, then P0 = 1, else P0 = 0.


Figure 9-12 illustrates the effects of erosion and dilation. Figure 9-12a is
the binary source image. Figure 9-12b represents the source image after
erosion, and Figure 9-12c shows the source image after dilation.



#### Figure 9-12. Erosion and Dilation Functions


Figure 9-13 is the source image for the examples in Tables 9-2 and 9-3,
in which gray cells indicate pixels equal to 1.


a
b
c



#### Figure 9-13. Source Image before Erosion and Dilation


Tables 9-2 and 9-3 show how the structuring element can control the effects
of erosion or dilation, respectively. The larger the structuring element, the
more templates can be edited and the more selective the effect.



#### Table 9-2. How the Structure Element Affects Erosion


Structuring Element
After Erosion
Description


A pixel is cleared if it is equal to 1 and if its three
upper-left neighbors do not equal 1. The erosion
truncates the upper-left particle borders.


A pixel is cleared if it is equal to 1 and if its lower
and right neighbors do not equal 1. The erosion
truncates the bottom and right particle borders but
retains the corners.



#### Table 9-3. How the Structure Element Affects Dilation


Structuring Element
After Dilation
Description


A pixel is set to 1 if it is equal to 1 or if one of
its three upper-left neighbors equals 1. The
dilation expands the lower-right particle
borders.


A pixel is set to 1 if it is equal to 1 or if it its
lower or right neighbor equals 1. The dilation
expands the upper and left particle borders.



#### Opening and Closing Functions


The opening function is an erosion followed by a dilation. This function
removes small particles and smooths boundaries. This operation does not
significantly alter the area and shape of particles because erosion and
dilation are dual transformations, in which borders removed by the erosion
function are restored during dilation. However, small particles eliminated
during the erosion are not restored by the dilation. If I is an image,


opening(I) = dilation(erosion(I))


The closing function is a dilation followed by an erosion. This function fills
tiny holes and smooths boundaries. This operation does not significantly
alter the area and shape of particles because dilation and erosion are
morphological complements, where borders expanded by the dilation
function are then reduced by the erosion function. However, erosion does
not restore any tiny holes filled during dilation. If I is an image,


closing(I) = erosion(dilation(I))


The following figures illustrate examples of the opening and closing
function.



#### Figure 9-14. Opening and Closing Functions


1
1
1
1
1
1
1
1
1


Original Image
Structuring Element
After Opening
After Closing


1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1


0
0
1
0
0
0
1
1
1
0
1
1
1
1
1
0
1
1
1
0
0
0
1
0
0


Structuring Element
After Opening
Structuring Element
After Closing



#### Inner Gradient Function


The internal edge subtracts the eroded image from its source image.
The remaining pixels correspond to the pixels eliminated by the erosion
process. If I is an image,


internal edge(I) = I – erosion(I) = XOR(I, erosion(I))



#### Outer Gradient Function


The external edge subtracts the source image from the dilated image of the
source image. The remaining pixels correspond to the pixels added by the
dilation process. If I is an image,


external edge(I) = dilation(I) – I = XOR(I, dilation(I))


Figure 9-15a shows the binary source image. Figure 9-15b shows the
image produced from an extraction using a 5 × 5 structuring element.
The superimposition of the internal edge is shown in white, and the external
edge is shown in gray. The thickness of the extended contours depends on
the size of the structuring element.



#### Figure 9-15. External Edges



#### Hit-Miss Function


The hit-miss function locates particular configurations of pixels. This
function extracts each pixel located in a neighborhood exactly matching
the template defined by the structuring element. Depending on the
configuration of the structuring element, the hit-miss function can locate
single isolated pixels, cross-shape or longitudinal patterns, right angles
along the edges of particles, and other user-specified shapes. The larger the
size of the structuring element, the more specific the researched template
can be. Refer to Table 9-4 for strategies on using the hit-miss function.


a.
b.


In a structuring element with a central coefficient equal to 0, a hit-miss
function changes all pixels set to 1 in the source image to the value 0.


For a given pixel P0, the structuring element is centered on P0. The pixels
masked by the structuring element are then referred to as Pi.


•
If the value of each pixel Pi is equal to the coefficient of the structuring
element placed on top of it, then the pixel P0 is set to 1, else the pixel
P0 is set to 0.


•
In other words, if the pixels Pi define the exact same template as the
structuring element, then P0 = 1, else P0 = 0.


Figures 9-16b, 9-16c, 9-16d, and 9-16e show the result of three hit-miss
functions applied to the same source image, represented in Figure 9-16a.
Each hit-miss function uses a different structuring element, which is
specified above each transformed image. Gray cells indicate pixels
equal to 1.



#### Figure 9-16. Hit-Miss Function


A second example of the hit-miss function shows how, when given the
binary image shown in Figure 9-17, the function can locate various patterns
specified in the structuring element. The results are displayed in Table 9-4.



#### Figure 9-17. Binary Image before Application of Hit-Miss Function


b.
c.
d.
e.
a.



#### Thinning Function


The thinning function eliminates pixels that are located in a neighborhood
matching a template specified by the structuring element. Depending on the
configuration of the structuring element, you can also use thinning to
remove single pixels isolated in the background and right angles along the
edges of particles. A larger structuring element allows for a more specific
template.


The thinning function extracts the intersection between a source image
and its transformed image after a hit-miss function. In binary terms, the
operation subtracts its hit-miss transformation from a source image.



#### Table 9-4. Using the Hit-Miss Function


Strategy
Structuring Element
Resulting Image


Use the hit-miss function to locate
pixels isolated in a background.


The structuring element on the right
extracts all pixels equal to 1 that are
surrounded by at least two layers of
pixels that are equal to 0.


0
0
0
0
0
0
0
0
0
0
0
0
1
0
0
0
0
0
0
0
0
0
0
0
0


Use the hit-miss function to locate
single pixel holes in particles.


The structuring element on the right
extracts all pixels equal to 0 that are
surrounded by at least one layer of
pixels that are equal to 1.


1
1
1
1
0
1
1
1
1


Use the hit-miss function to locate
pixels along a vertical left edge.


The structuring element on the right
extracts pixels surrounded by at least
one layer of pixels equal to 1 to the
left and pixels that are equal to 0 to
the right.


1
1
0
1
1
0
1
1
0


Do not use this function when the central coefficient of the structuring
element is equal to 0. In such cases, the hit-miss function can change only
the value of certain pixels in the background from 0 to 1. However, the
subtraction of the thinning function then resets these pixels back to 0.


If I is an image,


thinning(I) = I – hit-miss(I) = XOR (I, hit-miss(I))


Figure 9-18a shows the binary source image used in the following example
of thinning. Figure 9-18b illustrates the resulting image, in which single
pixels in the background are removed from the image. This example uses
the following structuring element:


0
0
0
0
1
0
0
0
0



#### Figure 9-18. Thinning Function


Another thinning example uses the source image shown in Figure 9-19a.
Figures 9-19b through 9-19d show the results of three thinnings applied to
the source image. Each thinning uses a different structuring element, which
is specified above each transformed image. Gray cells indicate pixels
equal to 1.


a.
b.



#### Figure 9-19. Thinning Function with Structuring Elements



#### Thickening Function


The thickening function adds to an image those pixels located in a
neighborhood that matches a template specified by the structuring element.
Depending on the configuration of the structuring element, you can use
thickening to fill holes and smooth right angles along the edges of particles.
A larger structuring element allows for a more specific template.


The thickening function extracts the union between a source image and
its transformed image, which was created by a hit-miss function using a
structuring element specified for thickening. In binary terms, the operation
adds a hit-miss transformation to a source image.


Do not use this function when the central coefficient of the structuring
element is equal to 1. In such cases, the hit-miss function can turn only
certain particle pixels from 1 to 0. However, the addition of the thickening
function resets these pixels to 1.


If I is an image,


thickening(I) = I + hit-miss(I) = OR (I, hit-miss(I))


Figure 9-20a represents the binary source file used in the following
thickening example. Figure 9-20b shows the result of the thickening
function applied to the source image, which filled single pixel holes
using the following structuring element:


1
1
1
1
0
1
1
1
1


a.
b.
c.
d.



#### Figure 9-20. Thickening Function


Figure 9-21a represents the source image for another thickening example.
Figures 9-21b through 9-21d show the results of three thickenings as
applied to the source image. Each thickening uses a different structuring
element, which is specified on top of each transformed image. Gray cells
indicate pixels equal to 1.



#### Figure 9-21. Thickening Function with Different Structuring Elements



#### Proper-Opening Function


The proper-opening function is a finite and dual combination of openings
and closings. It removes small particles and smooths the contour of
particles according to the template defined by the structuring element.


If I is the source image, the proper-opening function extracts the
intersection between the source image I and its transformed image obtained
after an opening, followed by a closing, and then followed by another
opening.


a.
b.


a.
b.
c.
d.


proper-opening(I) = AND(I, OCO(I))


or


proper-opening(I) = AND(I, DEEDDE(I))


where
I is the source image,
E is an erosion,
D is a dilation,
O is an opening,
C is a closing,
F(I) is the image obtained after applying the function F to the
image I, and
GF(I) is the image obtained after applying the function F to
the image I followed by the function G to the image I.



#### Proper-Closing Function


The proper-closing function is a finite and dual combination of closings
and openings. It fills tiny holes and smooths the inner contour of particles
according to the template defined by the structuring element.


If I is the source image, the proper-closing function extracts the union of
the source image I and its transformed image obtained after a closing,
followed by an opening, and then followed by another closing.


proper-closing(I ) = OR(I, COC(I))


or


proper-closing(I) = OR(I, EDDEED(I))


where
I is the source image,
E is an erosion,
D is a dilation,
O is an opening,
C is a closing,
F(I) is the image obtained after applying the function F to the
image I, and
GF(I) is the image obtained after applying the function F to
the image I followed by the function G to the image I.



#### Auto-Median Function


The auto-median function is a dual combination of openings and closings.
It generates simpler particles that contain fewer details.


If I is the source image, the auto-median function extracts the intersection
between the proper-opening and proper-closing of the source image I.


auto-median(I) = AND(OCO(I), COC(I))


or


auto-median(I) = AND(DEEDDE(I), EDDEED(I))


where
I is the source image,
E is an erosion,
D is a dilation,
O is an opening,
C is a closing,
F(I) is the image obtained after applying the function F to
the image I, and
GF(I) is the image obtained after applying the function F
to the image I followed by the function G to the image I.



## Advanced Morphology Operations


The advanced morphology operations are built upon the primary
morphological operators and work on particles as opposed to pixels. Each
of the operations have been developed to perform specific operations on the
particles in a binary image.


Use the advanced morphological operations to fill holes in particles,
remove particles that touch the border of the image, remove unwanted
small and large particles, separate touching particles, find the convex hull
of particles, and more.


You can use these transformations to prepare particles for quantitative
analysis, observe the geometry of regions, extract the simplest forms for
modeling and identification purposes, and so forth.


The advanced morphology functions are conditional combinations of
fundamental transformations, such as binary erosion and dilation. The
functions apply to binary images in which a threshold of 1 has been applied
to particles and where the background is equal to 0. This section describes
the following advanced binary morphology functions:


•
Border


•
Hole filling


•
Labeling


•
Lowpass filters


•
Highpass filters


•
Separation


•
Skeleton


•
Segmentation


•
Distance


•
Danielsson


•
Circle


•
Convex Hull


Note
In this section of the manual, the term pixel denotes a pixel equal to 1, and the term
particle denotes a group of pixels equal to 1.



#### Border Function


The border function removes particles that touch the border of the image.
These particles may have been truncated during the digitization of the
image, and their elimination them helps to avoid erroneous particle
measurements and statistics.



#### Hole Filling Function


The hole filling function fills the holes within particles.



#### Labeling Function


The labeling function assigns a different gray-level value to each particle.
The image produced is not a binary image, but a labeled image using a
number of gray-level values equal to the number of particles in the image
plus the gray level 0 used in the background area.


The labeling function identifies particles using either connectivity-4 or
connectivity-8 criteria. For more information on connectivity, refer to the
Connectivity section.



#### Lowpass and Highpass Filters


The lowpass filter removes small particles according to their widths as
specified by a parameter called filter size. For a given filter size N, the
lowpass filter eliminates particles whose widths are less than or equal to
(N – 1) pixels. These particles disappear after (N – 1) / 2 erosions.


The highpass filter removes large particles according to their widths as
specified by a parameter called filter size. For a given filter size N, the
highpass filter eliminates particles with widths greater than or equal to
N pixels. These particles do not disappear after (N / 2 + 1) erosions.


Both the highpass and lowpass morphological filters use erosions to select
particles for removal. Since erosions or filters cannot discriminate particles
with widths of 2k pixels from particles with widths of 2k – 1 pixels, a single
erosion eliminates both particles that are 2 pixels wide and 1 pixel wide.


Table 9-5 shows the effect of lowpass and highpass filtering.



#### Table 9-5. Effect of Lowpass and Highpass Filtering


Filter Size (N)
Highpass Filter
Lowpass Filter


N is an even number
(N = 2k)


• Removes particles with a width
greater than or equal to 2k


• Uses k – 1 erosions


• Removes particles with a width
less than or equal to 2k – 2


• Uses k – 1 erosions


N is an odd number
(N = 2k + 1)


• Removes particles with a width
greater than or equal to 2k + 1


•  Uses k erosions


• Removes particles with a width
less than or equal to 2k


• Uses k erosions


Figure 9-22a represents the binary source image used in this example.
Figure 9-22b shows how, for a given filter size, a highpass filter produces
the following image. Gray particles and white particles are filtered out by a
lowpass and highpass filter, respectively.



#### Figure 9-22. Lowpass and Highpass Filter Functions



#### Separation Function


The separation function breaks narrow isthmuses and separates touching
particles with respect to a user-specified filter size. This operation uses
erosions, labeling, and conditional dilations.


For example, after thresholding an image, two gray-level particles
overlapping one another might appear as a single binary particle. You can
observe narrowing where the original particles have intersected. If the
narrowing has a width of M pixels, a separation using a filter size of
(M + 1) breaks it and restores the two original particles. This applies to all
particles that contain a narrowing shorter than N pixels.


For a given filter size N, the separation function segments particles with
a narrowing shorter than or equal to (N – 1) pixels. These particles are
divided into two parts after (N – 1) / 2 erosions.


The above definition is true when N is an odd number, but should be
modified slightly when N is an even number, due to the use of erosions in
determining whether a narrowing should be broken or kept. The function
cannot discriminate a narrowing with a width of 2k pixels from a narrowing
with a width of (2k – 1) pixels, therefore, one erosion breaks both a
narrowing that is two pixels wide as well as a narrowing that is
one pixel wide.


a.
b.


The precision of the separation is limited to the elimination of constrictions
that have a width smaller than an even number of pixels:


•
If N is an even number (2k), the separation breaks a narrowing with a
width smaller than or equal to (2k – 2) pixels. It uses (k – 1) erosions.


•
If N is an odd number (2k + 1), the separation breaks a narrowing with
a width smaller than or equal to 2k. It uses k erosions.



#### Skeleton Functions


A skeleton function applies a succession of thinnings until the width of each
particle becomes equal to one pixel. The skeleton functions are both time-
and memory-consuming. They are based on conditional applications of
thinnings and openings that use various configurations of structuring
elements.


L-Skeleton uses the following type of structuring element:


0
?
1
0
1
1
0
?
1


M-Skeleton uses the following type of structuring element:


?
?
1
0
1
1
?
?
17


Skiz is an L-Skeleton performed on an inverse of the image.


L-Skeleton Function


The L-skeleton function indicates the L-shaped structuring element
skeleton function. Using the source image in Figure 9-23a, the L-skeleton
function produces the image in Figure 9-23b.



#### Figure 9-23. L-Skeleton Function


a.
b.


M-Skeleton Function


The M-skeleton function extracts a skeleton with more dendrites or
branches. Using the source image in Figure 9-23a, the M-skeleton function
produces the image shown in Figure 9-24.



#### Figure 9-24. M-Skeleton Function


Skiz Function


The skiz (skeleton of influence zones) function behaves like an L-skeleton
function applied to the background regions instead of the particle regions.
It produces median lines that are at an equal distance from the particles.


Using the source image in Figure 9-23a, the skiz function produces the
image in Figure 9-25, which is shown superimposed on the source image.



#### Figure 9-25. Skiz Function



#### Segmentation Function


The segmentation function is applied only to labeled images. It partitions
an image into segments that are centered around a particle such that they do
not overlap or leave empty zones. Empty zones are caused by dilating
particles until they touch one another.


Note
The segmentation function is time-consuming. Reduce the image to its minimum
significant size before selecting this function.


In Figure 9-26, binary particles, which are shown in black, are
superimposed on top of the segments, which are shown in gray shades.



#### Figure 9-26. Segmentation Function


When applied to an image with binary particles, the transformed image
turns red because it is entirely composed of pixels set to 1.


Comparisons Between Segmentation and Skiz Functions


The segmentation function extracts segments that contain only one particle.
A segment represents the area in which this particle can be moved without
intercepting another particle, assuming that all particles move at the same
speed.


The edges of these segments give a representation of the external skeletons
of the particles. Unlike the skiz function, segmentation does not involve
median distances.


You can obtain segments using successive dilations of particles until they
touch each other and cover the entire image. The final image contains as
many segments as there were particles in the original image. However, if
you consider the inside of closed skiz lines as segments, you may produce
more segments than particles originally present in the image. Consider the
upper-right region in Figure 9-27. This image shows the following features:


•
Original particles in black


•
Segments in shades of gray


•
Skiz lines



#### Figure 9-27. Segmentation with Skiz Lines



#### Distance Function


The distance function assigns a gray-level value to each pixel equal to the
shortest distance to the particle border. This distance may be equal to the
distance to the outer particle border or to a hole within the particle.


Tip
Use the Danielsson function instead of the distance function when possible.



#### Danielsson Function


The Danielsson function also creates a distance map but is a more accurate
algorithm than the classical distance function. Because the destination
image is 8-bit, its pixels cannot have a value greater than 255. Any pixels
with a distance to the edge greater than 255 are set to 255.


For example, a circle with a radius of 300 yields 255 concentric rings whose
pixel values range from 1 to 255 from the perimeter of the circle inward.
The rest of the circle is filled with a solid circle whose pixel value is 255
and radius is 45.


Figure 9-28a shows the source threshold image used in the following
example. The image is sequentially processed with a lowpass filter, hole
filling, and the Danielsson function. The Danielsson function produces the
distance map image shown in Figure 9-28b.



#### Figure 9-28. Danielsson Function


View the resulting image with a binary palette. In this palette, each level
corresponds to a different color. Thus, you easily can determine the relation
of a set of pixels to the border of a particle. The first layer, which forms the
border, is red. The second layer, closest to the border, is green, the third
layer is blue, and so forth.


a.
b.



#### Circle Function


The circle function separates overlapping circular particles using the
Danielsson coefficient to reconstitute the form of an particle, provided that
the particles are essentially circular. The particles are treated as a set of
overlapping discs that are then separated into separate discs. This allows
you to trace circles corresponding to each particle.


Figure 9-29a shows the source image for the following example.
Figure 9-29b shows the image after the circle function is applied to the
image.



#### Figure 9-29. Circle Function


a.
b.



#### Convex Hull Function


The convex hull function is useful for closing particles so that
measurements can be made on the particle, even when the particle contour
is discontinuous.


The convex hull function calculates a convex envelope around each
particle, effectively closing the particle. The image to which you apply a
convex hull function must be binary.


Figure 9-30a shows the original labeled image used in this example.
Figure 9-30b shows the results after the convex hull function is applied to
the image.



#### Figure 9-30. Convex Hull Function


a.
b.
