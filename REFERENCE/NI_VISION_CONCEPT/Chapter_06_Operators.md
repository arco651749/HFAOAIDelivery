# Chapter 6: Operators

> **Part**: `Part II: Image Processing and Analysis` | **Pages**: `110 - 116`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


6
Operators


This chapter contains information about arithmetic and logic operators,
which mask, combine, and compare images.



## Introduction


Operators perform basic arithmetic and logical operations on images.
Use operators to add, subtract, multiply, and divide an image with other
images or constants. You also can perform logical operations, such as
AND/NAND, OR/NOR, and XOR/XNOR, and make pixel comparisons
between an image and other images or a constant.



## When to Use


Common applications of these operators include time-delayed
comparisons, identification of the union or intersection between images,
correction of image backgrounds to eliminate light drifts, and comparisons
between several images and a model. You also can use operators to
threshold or mask images and to alter contrast and brightness.



## Concepts


An arithmetic or logical operation between images is a pixel-by-pixel
transformation. It produces an image in which each pixel derives its value
from the values of pixels with the same coordinates in other images.


If A is an image with a resolution XY, B is an image with a resolution XY,
and Op is the operator, then the image N resulting from the combination of
A and B through the operator Op is such that each pixel P of the resulting
image N is assigned the value


pn = (pa)(Op)(pb)


where
pa is the value of pixel P in image a, and
pb is the value of pixel P in image b.



## Chapter 6 Operators



### Arithmetic Operators


The equations in Table 6-1 describe the usage of arithmetic operators with
8-bit resolution images a and b.


If the resulting pixel value pn is negative, it is set to 0. If it is greater than
255, it is set to 255.



### Logic and Comparison Operators


Logic operators are bitwise operators. They manipulate gray-level values
coded on one byte at the bit level. The equations in Table 6-2 describe the
usage of logical operators. The truth tables for logic operators are presented
in the Truth Tables section.



#### Table 6-1. Arithmetic Operators


Operator
Equation


Multiply
pn = min(pa × pb, 255)


Divide
pn = max(pa/pb, 0)


Add
pn = min(pa + pb, 255)


Subtract
pn = max(pa – pb, 0)


Modulo
pn = pamodpb


Absolute Difference
pn =  pa – pb


Pa


Pb


Pn


(Op)


In the case of images with 8-bit resolution, logic operators are mainly
designed to do the following:


•
Combine gray-level images with binary mask images, which are
composed of pixels equal to 0 or 255.


•
Combine or compare images with binary or labeled contents.


Table 6-3 illustrates how logic operators can be used to extract or remove
information in an image.



#### Table 6-2. Logical and Comparison Operators


Operator
Equation


Logical Operators


AND
pn = pa AND pb


NAND
pn = pa NAND pb


OR
pn = pa OR pb


NOR
pn = pa NOR pb


XOR
pn = pa XOR pb


Logic Difference
pn = pa AND (NOT pb)


Comparison Operators


Mask
if pb = 0,
then pn = 0,
else pn = pa


Mean
pn = mean[pa, pb]


Max
pn = max[pa, pb]


Min
pn = min[pa, pb]



#### Table 6-3. Using Logical Operators with Binary Image Masks


For a given pa
If pb = 255, then
If pb = 0, then


AND
pa AND 255 = pa
pa AND 0 = 0


NAND
pa NAND 255 = NOT pa
pa NAND 0 = 255


OR
pa OR 255 = 255
pa OR 0 = pa


NOR
pa NOR 255 = 0
pa NOR 0 = NOT pa



#### Truth Tables


The following truth tables describe the rules used by the logic operators.
The top row and left column give the values of input bits. The cells in the
table give the output value for a given set of two input bits.


XOR
pa XOR 255 = NOT pa
pa XOR 0 = pa


Logic Difference
pa – NOT 255 = pa
pa – NOT 0 = 0


AND
NAND


b
b
b
b


a = 0


a = 1


0
0
a = 0


a = 1


1
1


0
1
1
0


OR
NOR


b
b
b
b


a = 0
0
1
a = 0
1
0


a = 1
1
1
a = 1
0
0


Table 6-3.  Using Logical Operators with Binary Image Masks (Continued)


For a given pa
If pb = 255, then
If pb = 0, then



### Example 1


The following figure shows the source grayscale image used in this
example.


Regions of interest have been isolated in a binary format, retouched with
morphological manipulations, and finally multiplied by 255 to obtain the
following image mask.


XOR
XNOR


b
b
b = 0


a = 0
0
1
a = 0
1
0


a = 1
1
0
a = 1
0
1


NOT


NOT a


a = 0
1


a = 1
0


The source image AND mask image operation restores the original
intensity of the object regions in the mask.


The source image OR mask image operation restores the original intensity
of the background region in the mask.



### Example 2


This example demonstrates the use of the OR operation to produce an
image containing the union of two binary images. The following image
represents the first image, with a background value of 0 and objects with a
gray-level value of 128.


The following figure shows the second image, featuring a background
value of 0 and objects with gray-level values of 255.


Image #1 OR Image #2 produces a union, as shown in the following image.
