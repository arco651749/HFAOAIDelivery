# Chapter 10: Particle Measurements

> **Part**: `Part III: Particle Analysis` | **Pages**: `186 - 204`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


10
Particle Measurements


This chapter contains information about characterizing particles in a binary
image.



## Introduction


A particle is a group of contiguous nonzero pixels in an image. Particles can
be characterized by measurements related to their attributes, such as
particle location, area, and shape.



### When to Use


Use particle measurements when you want to make shape measurements
on particles in a binary image.



### Pixel Measurements versus Real-World Measurements


In addition to making conventional pixel measurements, NI Vision particle
analysis functions can use calibration information attached to an image to
make measurements in calibrated real-world units. In applications that do
not require the display of corrected images, you can use the calibration
information attached to the image to make real-world measurements
directly without using time-consuming image correction.


In pixel measurements, a pixel is considered to have an area of one square
unit, located entirely at the center of the pixel. In calibrated measurements,
a pixel is a polygon with corners defined as plus or minus one half a unit
from the center of the pixel. Figure 10-1 illustrates this concept.



## Chapter 10 Particle Measurements



#### Figure 10-1. Pixel Coordinates to Real-World Coordinates


A pixel at (3, 8) is a square with corners at (2.5, 7.5), (3.5, 7.5), (3.5, 8.5),
and (2.5, 8.5). To make real-world measurements, the four corner
coordinates are transformed from pixel coordinates into real-world
coordinates. Using real-world coordinates, the area and moments of the
pixel can be integrated. Similarly, the area and moments of an entire
particle can be computed using the calibrated particle contour points.



## Particle Measurements


This section contains tables that list and describe the NI Vision particle
measurements. The tables include definitions, symbols, and equations for
particle measurements.


Note
Some equation symbols may be defined inside tables later in the chapter.


1
Point to Polygon
2
Pixel Coordinates to Real-World Coordinates


1
2


(2.5, 7.5)
(3.5, 7.5)


(2.5, 8.5)
(3, 8)
(3.5, 8.5)


(42, 27)


(46, 31)
(51, 30)


(52, 23)



### Particle Concepts


Table 10-1 contains concepts relating to particle measurements.



#### Table 10-1. Particle Concepts


Concept
Definition


Bounding Rect
Smallest rectangle with sides parallel to the x-axis and y-axis that
completely encloses the particle.


Perimeter
Length of a boundary of a region. Because the boundary of a binary
image is comprised of discrete pixels, NI Vision subsamples the
boundary points to approximate a smoother, more accurate perimeter.
Boundary points are the pixel corners that form the boundary of the
particle. Refer to Figure 10-1 for an illustration of pixel corners.


Particle hole
Contiguous region of zero-valued pixels completely surrounded by
pixels with nonzero values. Refer to the Particle Holes section for more
information.


Angle
Degrees of rotation measured counter-clockwise from the x-axis, such
that 0 ≤ θ < 180.


Equivalent Rect
Rectangle with the same perimeter and area as the particle.


Equivalent Ellipse
Ellipse with the same perimeter and area as the particle.


Width


Height


Bottom


Top


(0,0)
Left
Right


Max Feret Diameter
Line segment connecting the two perimeter points that are the furthest
apart.


Convex Hull
Smallest convex polygon containing all points in the particle. The
following figure illustrates two particles, shown in gray, and their
respective convex hulls, the areas enclosed by black lines.


Max Horiz. Segment
Length


Longest row of contiguous pixels in the particle. This measurement is
always given as a pixel measurement.


Sum
Moments of various orders relative to the x-axis and y-axis.


Table 10-1.  Particle Concepts (Continued)


Concept
Definition


2


1


5


3


4


1
Max Feret Diameter Start—Highest, leftmost of the two points defining
the Max Feret Diameter
2
Max Feret Diameter End—Lowest, rightmost of the two points defining
the Max Feret Diameter
3
Max Feret Diameter Orientation
4
Particle Perimeter
5
Max Feret Diameter



#### Particle Holes


A particle hole is a contiguous region of zero-valued pixels completely
surrounded by pixels with nonzero values. A particle located inside a hole
of a bigger particle is identified as a separate particle. The area of a hole
that contains a particle includes the area covered by that particle.


Moment of Inertia
Moments about the particle center of mass. Provides a representation of
the pixel distribution in a particle with respect to the particle center of
mass. Moments of inertia are shift invariant.


Norm. Moment of
Inertia


Moment of Inertia normalized with regard to the particle area.
Normalized moments of inertia are shift and scale invariant.


Hu Moment
Moments derived from the Norm. Moment of Inertia measurements.
Hu Moments are shift, scale, and rotation invariant.


Particle #
Area
Holes’ Area


Particle &
Holes’ Area


Particle 1
A
B + C
A + B + C


Particle 2
D
0
D


Particle 3
E
F + G
E + F + G


Particle 4
G
0
G


Table 10-1.  Particle Concepts (Continued)


Concept
Definition


A


B
C
D
E
F
G


Particle 1
Particle 2
Particle 3


Particle 4


Holes’ measurements are valuable when analyzing particles similar to the
one in Figure 10-2a. For example, if you threshold a cell with a dark
nucleus (Figure 10-2a) so that the nucleus appears as a hole in the cell
(Figure 10-2b), you can make the following cell measurements:


•
Holes’ Area—Returns the size of the nucleus.


•
Particle & Holes’ Area—Returns the size of the entire cell.


•
Holes’ Area/Particle & Holes’ Area—Returns the percentage of the
cell that the nucleus occupies.



#### Figure 10-2. Holes’ Measurements


a.
b.



### Coordinates


Table 10-2 lists the NI Vision particle measurements relating to
coordinates.



#### Table 10-2. Coordinates


Measurement
Definition
Symbol
Equation


Center of Mass
Point representing the average
position of the total particle mass,
assuming every point in the
particle has a constant density.
The center of mass can be located
outside the particle if the particle
is not convex.


—
—


First Pixel
Highest, leftmost particle pixel.
The first pixel is always given as
a pixel measurement.The black
squares in the following figure
represent the first pixel of each
particle.


—
—


Center of Mass x
X-coordinate of the particle
Center of Mass.


x


Center of Mass y
Y-coordinate of the particle
Center of Mass.


y


First Pixel x
X-coordinate of the first particle
pixel.


—
—


First Pixel y
Y-coordinate of the first particle
pixel.


—
—


Σx
A-----


Σy
A-----


Bounding Rect
Left


X-coordinate of the leftmost
particle point.


BL
—


Bounding Rect
Top


Y-coordinate of highest particle
point.


BT
—


Bounding Rect
Right


X-coordinate of the rightmost
particle point.


BR
—


Bounding Rect
Bottom


Y-coordinate of the lowest
particle point.


BB
—


Max Feret
Diameter Start x


X-coordinate of the Max Feret
Diameter Start.


Fx1
—


Max Feret
Diameter Start y


Y-coordinate of the Max Feret
Diameter Start.


Fy1
—


Max Feret
Diameter End x


X-coordinate of the Max Feret
Diameter End.


Fx2
—


Max Feret
Diameter End y


Y-coordinate of the Max Feret
Diameter End.


Fy2
—


Max Horiz.
Segment Length
Left


X-coordinate of the leftmost pixel
in the Max Horiz. Segment. Max
Horiz. Segment Length Left is
always given as a pixel
measurement.


—
—


Max Horiz.
Segment Length
Right


X-coordinate of the rightmost
pixel in the Max Horiz. Segment.
Max Horiz. Segment Length
Right is always given as a pixel
measurement.


—
—


Max Horiz.
Segment Length
Row


Y-coordinate for all of the pixels
in the Max Horiz. Segment. Max
Horiz. Segment Length Row is
always given as a pixel
measurement.


—
—


Table 10-2.  Coordinates (Continued)


Measurement
Definition
Symbol
Equation



### Lengths


Table 10-3 lists the NI Vision particle relating to length.



#### Table 10-3. Lengths


Measurement
Definition
Symbol
Equation


Bounding Rect
Width


Distance between Bounding Rect
Left and Bounding Rect Right.


W


Bounding Rect
Height


Distance between Bounding Rect
Top and Bounding Rect Bottom.


H


Bounding Rect
Diagonal


Distance between opposite
corners of the Bounding Rect.


—


Perimeter
Length of the outer boundary
of the particle. Because the
boundary is comprised of discrete
pixels, NI Vision subsamples the
boundary points to approximate a
smoother, more accurate
perimeter.


P
—


Convex Hull
Perimeter


Perimeter of the Convex Hull.
PCH
—


Holes’ Perimeter
Sum of the perimeters of each
hole in the particle.


—
—


Max Feret
Diameter


Distance between the Max Feret
Diameter Start and the Max Feret
Diameter End.


F


Equivalent
Ellipse Major
Axis


Length of the major axis of the
Equivalent Ellipse.


E2a


Equivalent
Ellipse Minor
Axis


Length of the minor axis of the
Equivalent Ellipse.


E2b


Equivalent
Ellipse Minor
Axis (Feret)


Length of the minor axis of the
ellipse with the same area as the
particle, and Major Axis equal in
length to the Max Feret Diameter.


EF2b


BR
BL
–


BB
BT
–


W2
H2
+


Fy2
Fy1
–
(
)2
Fx2
Fx1
–
(
)2
+


P2


2π2
--------
2A
π
------
+
P2


2π2
--------
2A
π
------
–
+


P2


2π2
--------
2A
π
------
+
P2


2π2
--------
2A
π
------
–
–


4ACH
π F
⋅
------------


Equivalent Rect
Long Side


Longest side of the Equivalent
Rect.


Ra


Equivalent Rect
Short Side


Shortest side of the Equivalent
Rect.


Rb


Equivalent Rect
Diagonal


Distance between opposite
corners of the Equivalent Rect.


Rd


Equivalent Rect
Short Side
(Feret)


Shortest side of the rectangle with
the same area as the particle, and
longest side equal in length to the
Max Feret Diameter.


RFb


Average Horiz.
Segment Length


Average length of a horizontal
segment in the particle. Sum of
the horizontal segments that do
not superimpose any other
horizontal segment. Average
Horiz. Segment Length is always
given as a pixel measurement.


—


Average Vert.
Segment Length


Average length of a vertical
segment in the particle. Sum of
the vertical segments that do not
superimpose any other vertical
segment. Average Vert. Segment
Length is always given as a pixel
measurement.


—


Hydraulic
Radius


Particle area divided by the
particle perimeter.


—


Waddel Disk
Diameter


Diameter of a disk with the same
area as the particle.


—


Table 10-3.  Lengths (Continued)


Measurement
Definition
Symbol
Equation


1
4-- P
P2
16A
–
+
(
)


1
4-- P
P2
16A
–
–
(
)


Ra
2
Rb
2
+


ACH
F
---------


A
SH
-----


A
SV
-----


A
P---


2 A
π---


Ellipses


•
Equivalent Ellipse Major Axis—Total length of the major axis of the
ellipse that has the same area and same perimeter as a particle. This
length is equal to 2a.


This definition gives the following set of equations:


where
a = 1/2 E2a
b = 1/2 E2b


For a given area and perimeter, only one solution (a, b) exists.


•
Equivalent Ellipse Minor Axis—Total length of the minor axis of the
ellipse that has the same area and same perimeter as a particle. This
length is equal to 2b.


•
Ellipse Ratio—Ratio of the major axis of the equivalent ellipse to its
minor axis, which is defined as


The more elongated the equivalent ellipse, the higher the ellipse ratio.
The closer the equivalent ellipse is to a circle, the closer the ellipse
ratio is to 1.


Area
πab
=


Perimeter
π 2 a2
b2
+
(
)
≈


E2a


E2b


ellipse major axis
ellipse minor axis
------------------------------------------
a
b--
=


Rectangles


•
Equivalent Rect Long Side—Length of the long side (Ra) of the
rectangle that has the same area and same perimeter as a particle


This definition gives the following set of equations:


This set of equations can be expressed so that the sum Ra + Rb and the
product RaRb become functions of the parameters Particle Area and
Particle Perimeter. Ra and Rb then become the two solutions of the
following polynomial equation:


2x2 – Px + 2A = 0


Notice that for a given area and perimeter, only one solution (Ra, Rb)
exists.


•
Equivalent Rect Short Side—Length of the short side of the
rectangle that has the same area and same perimeter as a particle.
This length is equal to Rb.


•
Equivalent Rect Diagonal—Distance between opposite corners of
the Equivalent Rect.


•
Rectangle Ratio—Ratio of the long side of the equivalent rectangle to
its short side, which is defined as


The more elongated the equivalent rectangle, the higher the rectangle
ratio.


The closer the equivalent rectangle is to a square, the closer to 1 the
rectangle ratio.


A
Area
RaRb
=
=


P
Perimeter
2 Ra
Rb
+
(
)
=
=


Ra


Rb
Rd


Ra
2
Rb
2
+


rectangle long side
rectangle short side
----------------------------------------------
Ra
Rb
-----
=


Hydraulic radius


A disk with radius R has a hydraulic radius equal to



### Areas


Table 10-4 lists the NI Vision particle area measurements.


Image Area


Figure 10-3a shows an image of a calibration grid. The image exhibits
nonlinear distortion. Figure 10-3b shows an image of coins taken with the
same camera setup used in Figure 10-3a. The dashed line around
Figure 10-3b defines the image area in pixels. Figure 10-3c illustrates the
image of coins after image correction. The dashed line around Figure 10-3c
defines the image area in calibrated units.



#### Table 10-4. Areas


Measurement
Definition
Symbol
Equation


Area
Area of the particle.
A
—


Holes’ Area
Sum of the areas of each
hole in the particle.


AH
—


Particle & Holes’
Area


Area of a particle that
completely covers the
image.


AT


Convex Hull Area
Area of the particle
Convex Hull.


ACH
—


Image Area
Area of the image.
AI
—


disk area
disk perimeter
---------------------------------
πR2


2πR
----------
R
2---
=
=


A
AH
+



#### Figure 10-3. Image Area in Pixels and Calibrated Units



### Quantities


Table 10-5 lists the NI Vision particle measurements relating to quantity.



### Angles


Table 10-6 lists the NI Vision particle angle measurements. The equations
are given in radians. The results are given in degrees that are mapped into
the range 0 to 180, such that 0 ≤ θ < 180.



#### Table 10-5. Quantities


Measurement
Definition
Symbol


Number of Holes
Number of holes in the particle.
—


Number of Horiz.
Segments


Number of horizontal segments in the
particle. Number of Horiz. Segments is
always given as a pixel measurement.


SH


Number of Vert.
Segments


Number of vertical segments in the
particle. Number of Vert. Segments is
always given as a pixel measurement.


SV


a.
b.
c.


The Orientation angle is measured counterclockwise from the horizontal
axis, as shown in Figure 10-4. The value can range from 0° to 180°. Angles
outside this range are mapped into the range. For example, a 190° angle is
considered to be a 10° angle.



#### Figure 10-4. Orientation


Note
Refer to the Max Feret Diameter entry in Table 10-1 for an illustration of Max Feret
Diameter Orientation.



#### Table 10-6. Angles


Measurement
Definition
Equation


Orientation
The angle of the line that passes
through the particle Center of Mass
about which the particle has the lowest
moment of inertia.


Max Feret Diameter
Orientation


The angle of the Max Feret Diameter.


1
Line with Lowest Moment of Inertia
2
Orientation in Degrees


3
Horizontal Axis


1
2--
2Σxy
Σyy
Σxx
–
---------------------




atan


Fy1
Fy2
–
Fx2
Fx1
–
---------------------




atan


1


2


3



### Ratios


Table 10-7 lists the NI Vision particle ratio measurements.



### Factors


Table 10-8 lists the NI Vision particle factor measurements.



#### Table 10-7. Ratios


Measurement
Definition
Equation


% Area/Image Area
Percentage of the particle Area covering
the Image Area.


% Area/(Particle & Holes’
Area)


Percentage of the particle Area in relation
to its Particle & Holes’ Area.


Ratio of Equivalent Ellipse
Axes


Equivalent Ellipse Major Axis divided by
Equivalent Ellipse Minor Axis.


Ratio of Equivalent Rect
Sides


Equivalent Rect Long Side divided by
Equivalent Rect Short Side.



#### Table 10-8. Factors


Measurement
Definition
Equation


Elongation Factor
Max Feret Diameter divided by
Equivalent Rect Short Side (Feret).
The more elongated the shape of a
particle, the higher its elongation
factor.


Compactness Factor
Area divided by the product of
Bounding Rect Width and Bounding
Rect Height. The compactness factor
belongs to the interval [0, 1].


A
AI
----
100%
⋅


A
AT
-----
100%
⋅


E2a
E2b
-------


Ra
Rb
-----


F
RFb
---------


A
W H
⋅
-------------



### Sums


Table 10-9 lists the NI Vision particle sum measurements.


Heywood Circularity Factor
Perimeter divided by the
circumference of a circle with the
same area. The closer the shape of a
particle is to a disk, the closer the
Heywood circularity factor is to 1.


Type Factor
Factor relating area to moment of
inertia.



#### Table 10-9. Sums


Measurement
Symbol


Sum x
Σx


Sum y
Σy


Sum xx
Σxx


Sum xy
Σxy


Sum yy
Σyy


Sum xxx
Σxxx


Sum xxy
Σxxy


Sum xyy
Σxyy


Sum yyy
Σyyy


Table 10-8.  Factors (Continued)


Measurement
Definition
Equation


P
2 πA
--------------


A2


4π Ixx Iyy
⋅
---------------------------



### Moments


Table 10-10 lists the NI Vision particle moment measurements.



#### Table 10-10. Moments


Measurement
Symbol
Equation


Moment of Inertia xx
Ixx


Moment of Inertia xy
Ixy


Moment of Inertia yy
Iyy


Moment of Inertia xxx
Ixxx


Moment of Inertia xxy
Ixxy


Moment of Inertia xyy
Ixyy


Moment of Inertia yyy
Iyyy


Norm. Moment of
Inertia xx


Nxx


Norm. Moment of
Inertia xy


Nxy


Norm. Moment of
Inertia yy


Nyy


Norm. Moment of
Inertia xxx


Nxxx


Σxx
Σx
2


A-----
–


Σxy
Σx Σy
⋅
A
---------------
–


Σyy
Σy
2


A-----
–


Σxxx
3xΣxx
–
2x
2Σx
+


Σxxy
2xΣxy
–
yΣxx
–
2x
2Σy
+


Σxyy
2yΣxy
–
xΣyy
–
2y
2Σx
+


Σyyy
3yΣyy
–
2y
2Σy
+


Ixx
A2
-----


Ixy
A2
-----


Iyy
A2
-----


Ixxx
A5 2
⁄
----------


Norm. Moment of
Inertia xxy


Nxxy


Norm. Moment of
Inertia xyy


Nxyy


Norm. Moment of
Inertia yyy


Nyyy


Hu Moment 1
H1


Hu Moment 2
H2


Hu Moment 3
H3


Hu Moment 4
H4


Hu Moment 5
H5


Hu Moment 6
H6


Hu Moment 7
H7


Table 10-10.  Moments (Continued)


Measurement
Symbol
Equation


Ixxy
A5 2
⁄
----------


Ixyy
A5 2
⁄
----------


Iyyy
A5 2
⁄
----------


Nxx
Nyy
+


Nxx
Nyy
–
(
)2
4Nxy
2
+


Nxxx
3Nxyy
–
(
)2
3Nxxy
Nyyy
–
(
)2
+


Nxxx
Nxyy
+
(
)2
Nxxy
Nyyy
+
(
)2
+


Nxxx
3Nxyy
–
(
) Nxxx
Nxyy
+
(
)
Nxxx
Nxyy
+
(
)2


3 Nxxy
Nyyy
+
(
)2
–


[


]
3Nxxy
Nyyy
–
(
) Nxxy
Nyyy
+
(
)


3 Nxxx
Nxyy
+
(
)2
Nxxy
Nyyy
+
(
)2
–
[
]


+


Nxx
Nyy
–
(
)
Nxxx
Nxyy
+
(
)2
Nxxy
Nyyy
+
(
)2
–
[
]


4Nxy Nxxx
Nxyy
+
(
) Nxxy
Nyyy
+
(
)
+


3Nxxy
Nyyy
–
(
) Nxxx
Nxyy
+
(
)
Nyyy
Nxyy
+
(
)2


3 Nxxy
Nyyy
+
(
)2
–


[


]
3Nxyy
Nyyy
–
(
) Nxxy
Nyyy
+
(
)


3 Nxxx
Nxyy
+
(
)2
Nxxy
Nyyy
+
(
)2
–
[
]


+
