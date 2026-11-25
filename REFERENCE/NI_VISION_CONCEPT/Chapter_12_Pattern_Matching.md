# Chapter 12: Pattern Matching

> **Part**: `Part IV: Machine Vision` | **Pages**: `219 - 226`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


12
Pattern Matching


This chapter contains information about pattern matching.



## Introduction


Pattern matching quickly locates regions of a grayscale image that match
a known reference pattern, also referred to as a model or template.


Note
A template is an idealized representation of a feature in the image. Refer to the
Pattern Matching Techniques section for the definition of an image feature.


When using pattern matching, you create a template that represents the
object for which you are searching. Your machine vision application then
searches for instances of the template in each acquired image, calculating a
score for each match. This score relates how closely the template resembles
the located matches.


Pattern matching finds template matches regardless of lighting variation,
blur, noise, and geometric transformations such as shifting, rotation, or
scaling of the template.



## When to Use


Pattern matching algorithms are some of the most important functions in
machine vision because of their use in varying applications. You can use
pattern matching in the following three general applications:


•
Alignment—Determines the position and orientation of a known
object by locating fiducials. Use the fiducials as points of reference on
the object.


•
Gauging—Measures lengths, diameters, angles, and other critical
dimensions. If the measurements fall outside set tolerance levels, the
component is rejected. Use pattern matching to locate the object you
want to gauge.


•
Inspection—Detects simple flaws, such as missing parts or unreadable
print.



## Chapter 12 Pattern Matching


Pattern matching provides your application with the number of instances
and the locations of template matches within an inspection image. For
example, you can search an image containing a printed circuit board (PCB)
for one or more fiducials. The machine vision application uses the fiducials
to align the board for chip placement from a chip mounting device.
Figure 12-1a shows part of a PCB. Figure 12-1b shows a common fiducial
used in PCB inspections or chip pick-and-place applications.



### Figure 12-1. Example of a Common Fiducial


Gauging applications first locate and then measure, or gauge, the
dimensions of an object in an image. If the measurement falls within a
tolerance range, the object passes inspection. If it falls outside the tolerance
range, the object is rejected.


Searching for and finding image features is the key processing task that
determines the success of many gauging applications, such as inspecting
the leads on a quad pack or inspecting an antilock-brake sensor. In real-time
applications, search speed is critical.



## What to Expect from a Pattern Matching Tool


Because pattern matching is the first step in many machine vision
applications, it must work reliably under various conditions. In automated
machine vision applications, the visual appearance of materials or


a.
b.


components under inspection can change because of varying factors such
as part orientation, scale changes, and lighting changes. The pattern
matching tool must maintain its ability to locate the reference patterns
despite these changes. The following sections describe common situations
in which the pattern matching tool needs to return accurate results.



### Pattern Orientation and Multiple Instances


A pattern matching algorithm needs to locate the reference pattern in an
image even if the pattern in the image is rotated or scaled. When a pattern
is rotated or scaled in the image, the pattern matching tool can detect the
following items in the image:


•
The pattern in the image


•
The position of the pattern in the image


•
The orientation of the pattern


•
Multiple instances of the pattern in the image, if applicable


Figure 12-2a shows a template image. Figure 12-2b shows a template
match shifted in the image. Figure 12-2c shows a template match rotated
in the image. Figure 12-2d shows a template match scaled in the image.
Figures 12-2b to 12-2d also illustrate multiple instances of the template.



#### Figure 12-2. Pattern Orientation and Multiple Instances



### Ambient Lighting Conditions


A pattern matching algorithm needs the ability to find the reference pattern
in an image under conditions of uniform lighting changes in the lighting
across the image. Figure 12-3 illustrates the typical conditions under which
pattern matching works correctly. Figure 12-3a shows the original template


a.
b.
c.
d.


image. Figure 12-3b shows a template match under bright light.
Figure 12-3c shows a template match under poor lighting.



#### Figure 12-3. Examples of Lighting Conditions



### Blur and Noise Conditions


A pattern matching algorithm needs the ability to find patterns that have
undergone some transformation because of blurring or noise. Blurring
usually occurs because of incorrect focus or depth of field changes. Refer
to Chapter 3, System Setup and Calibration, for more information about
depth of field.


Figure 12-4 illustrates typical blurring and noise conditions under which
pattern matching works correctly. Figure 12-4a shows the original template
image. Figure 12-4b shows the changes on the image caused by blurring.
Figure 12-4c shows the changes on the image caused by noise.



#### Figure 12-4. Examples of Blur and Noise



## Pattern Matching Techniques


Pattern matching techniques include normalized cross-correlation,
pyramidal matching, scale- and rotation-invariant matching, and image
understanding.



### Normalized Cross-Correlation


Normalized cross-correlation is the most common method for finding a
template in an image. Because the underlying mechanism for correlation is
based on a series of multiplication operations, the correlation process is
time consuming. Technologies such as MMX allow for parallel


a.
b.
c.


a.
b.
c.


multiplications and reduce overall computation time. To increase the speed
of the matching process, reduce the size of the image and restrict the region
of the image in which the matching occurs. Pyramidal matching and image
understanding are two ways to increase the speed of the matching process.



### Scale- and Rotation-Invariant Matching


Normalized cross-correlation is a good technique for finding patterns
in an image when the patterns in the image are not scaled or rotated.
Typically, cross-correlation can detect patterns of the same size up to
a rotation of 5° to 10°. Extending correlation to detect patterns that are
invariant to scale changes and rotation is difficult.


For scale-invariant matching, you must repeat the process of scaling
or resizing the template and then perform the correlation operation.
This adds a significant amount of computation to your matching process.
Normalizing for rotation is even more difficult. If a clue regarding rotation
can be extracted from the image, you can simply rotate the template and
perform the correlation. However, if the nature of rotation is unknown,
looking for the best match requires exhaustive rotations of the template.


You also can carry out correlation in the frequency domain using the
Fast Fourier Transform (FFT). If the image and the template are the same
size, this approach is more efficient than performing correlation in the
spatial domain. In the frequency domain, correlation is obtained by
multiplying the FFT of the image by the complex conjugate of the FFT of
the template. Normalized cross-correlation is considerably more difficult to
implement in the frequency domain.



### Pyramidal Matching


You can improve the computation time of pattern matching by reducing the
size of the image and the template. In pyramidal matching, both the image
and the template are sampled to smaller spatial resolutions. For instance, by
sampling every other pixel, the image and the template can be reduced
to one-fourth of their original sizes. Matching is performed first on the
reduced images. Because the images are smaller, matching is faster.
When matching is complete, only areas with high match scores need to
be considered as matching areas in the original image.



### Image Understanding


A pattern matching feature is a salient pattern of pixels that describe a
template. Because most images contain redundant information, using all
the information in the image to match patterns is time-insensitive and
inaccurate.


NI Vision uses a non-uniform sampling technique that incorporates image
understanding to thoroughly and efficiently describe the template. This
intelligent sampling technique specifically includes a combination of edge
pixels and region pixels as shown in Figure 12-5b. NI Vision uses a similar
technique when the user indicates that the pattern might be rotated in the
image. This technique uses specially chosen template pixels whose
values—or relative changes in values—reflect the rotation of the pattern.


Intelligent sampling of the template both reduces the redundant
information and emphasizes the feature to allow for an efficient, yet robust,
cross-correlation implementation. NI Vision pattern matching is able to
accurately locate objects that vary in size (±5%) and orientation (between
0° and 360°) and that have a degraded appearance.



#### Figure 12-5. Good Pattern Matching Sampling Techniques


a.
b.



## In-Depth Discussion


This section provides additional information you may need for building
successful searching applications.


The following is the basic concept of correlation: Consider a subimage
w(x, y) of size K × L within an image f(x, y) of size M × N, where K ≤M
and L ≤N. The correlation between w(x, y) and f(x, y) at a point (i, j) is
given by


where
i = 0,1,…M – 1,
j = 0,1… N – 1, and the summation is taken over the region in
the image where w and f overlap.


Figure 12-6 illustrates the correlation procedure. Assume that the origin of
the image f is at the top left corner. Correlation is the process of moving the
template or subimage w around the image area and computing the value C
in that area. This involves multiplying each pixel in the template by the
image pixel that it overlaps and then summing the results over all the pixels
of the template. The maximum value of C indicates the position where
w best matches f. Correlation values are not accurate at the borders of the
image.


C i j
( , )
w x y
( , )f x
i
+
y
j
+
(
,
)


y
0
=


K
1
–
∑
x
0
=


L
1
–
∑
=



#### Figure 12-6. Correlation Procedure


Basic correlation is very sensitive to amplitude changes in the image, such
as intensity, and in the template. For example, if the intensity of the image
f is doubled, so are the values of c. You can overcome sensitivity by
computing the normalized correlation coefficient, which is defined as


where w (calculated only once) is the average intensity value of the pixels
in the template w. The variable f is the average value of f in the region
coincident with the current location of w. The value of R lies in the range
–1 to 1 and is independent of scale changes in the intensity values of f and w.


M


N


L


K


x


y


(0, 0)


f(x, y)


w(x, y)


(i, j)
i


j


R i j
( , )


w x y
( , )
w
–
(
) f x
i
+
y
j
+
(
,
)
f i j
( , )
–
(
)


y
0
=


K
1
–
∑
x
0
=


L
1
–
∑


w x y
( , )
w
–
(
)2


y
0
=


K
1
–
∑
x
0
=


L
1
–
∑


1
2--


f x
i
+
y
j
+
(
,
)
f i j
( , )
–
(
)2


y
0
=


K
1
–
∑
x
0
=


L
1
–
∑


1
2--
----------------------------------------------------------------------------------------------------------------------------------------------
=
