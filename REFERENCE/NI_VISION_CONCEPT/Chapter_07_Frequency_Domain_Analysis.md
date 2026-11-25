# Chapter 7: Frequency Domain Analysis

> **Part**: `Part II: Image Processing and Analysis` | **Pages**: `117 - 129`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


7
Frequency Domain Analysis


This chapter contains information about converting images into the
frequency domain using the Fast Fourier transform, and information about
analyzing and processing images in the frequency domain.



## Introduction


Frequency filters alter pixel values with respect to the periodicity and
spatial distribution of the variations in light intensity in the image. Unlike
spatial filters, frequency filters do not apply directly to a spatial image,
but to its frequency representation. The frequency representation of an
image is obtained through the Fast Fourier Transform (FFT) function,
which reveals information about the periodicity and dispersion of the
patterns found in the source image.


You can filter the spatial frequencies seen in an FFT image. The
inverse FFT function then restores a spatial representation of the filtered
FFT image.


Frequency processing is another technique for extracting information from
an image. Instead of using the location and direction of light-intensity
variations, you can use frequency processing to manipulate the frequency
of the occurrence of these variations in the spatial domain. This new
component is called the spatial frequency, which is the frequency with
which the light intensity in an image varies as a function of spatial
coordinates.


Spatial frequencies of an image are computed with the FFT. The FFT is
calculated in two steps—a 1D Fast Fourier transform of the rows, followed
by a 1D Fast Fourier transform of the columns of the previous results.
The complex numbers that compose the FFT plane are encoded in a 64-bit
floating-point image called a complex image. The complex image is


f(x, y)
F(u, v)
H(u, v)
FFT
Filter


g(x, y)
Inverse FFT



## Chapter 7 Frequency Domain Analysis


formed by a 32-bit floating point number representing the real part and a
32-bit floating point number representing the imaginary part.


In an image, details and sharp edges are associated with moderate to high
spatial frequencies because they introduce significant gray-level variations
over short distances. Gradually varying patterns are associated with low
spatial frequencies. By filtering spatial frequencies, you can remove,
attenuate, or highlight the spatial components to which they relate.


Use a lowpass frequency filter to attenuate or remove, or truncate, high
frequencies present in the image. This filter suppresses information related
to rapid variations of light intensities in the spatial image. An inverse FFT,
used after a lowpass frequency filter, produces an image in which noise,
details, texture, and sharp edges are smoothed.


A highpass frequency filter attenuates or removes, or truncates, low
frequencies present in the complex image. This filter suppresses
information related to slow variations of light intensities in the spatial
image. In this case, an inverse FFT used after a highpass frequency filter
produces an image in which overall patterns are sharpened and details are
emphasized.


A mask frequency filter removes frequencies contained in a mask specified
by the user. Using a mask to alter the Fourier transform of an image offers
more possibilities than applying a lowpass or highpass filter. The image
mask is composed by the user and can describe very specific frequencies
and directions in the image. You can apply this technique, for example,
to filter dominant frequencies as well as their harmonics in the frequency
domain.



## When to Use


Because details and sharp edges introduce significant gray-level variations
over short distances, they are associated with moderate to high spatial
frequencies in an image. Gradually varying patterns are associated with
low spatial frequencies.


An image can have extraneous noise introduced during the digitization
process, such as periodic stripes. In the frequency domain, the periodic
pattern is reduced to a limited set of high spatial frequencies. Truncating
these particular frequencies and converting the filtered FFT image back to
the spatial domain produces a new image in which the grid pattern has
disappeared, while the overall features remain.



## Concepts


The FFT of an image is a 2D array of complex numbers, also represented
as a complex image. It represents the frequencies of occurrence of
light-intensity variations in the spatial domain. The low frequencies
correspond to smooth and gradual intensity variations found in the overall
patterns of the source image. The high frequencies correspond to abrupt
and short intensity variations found at the edges of objects, around noisy
pixels, and around details.



### FFT Representation


There are two possible representations of the Fast Fourier transform of an
image: the standard representation and the optical representation.



#### Standard Representation


In the standard representation, high frequencies are grouped at the center of
the image while low frequencies are located at the edges. The constant
term, or null frequency, is in the upper-left corner of the image. The
frequency range is


where M is the horizontal resolution of the image, and N is the vertical
resolution of the image.


0 N
,
[
]
0 M
,
[
]
×


A
B


C
D
Low
Frequencies


Low
Frequencies


Low


High


High


Low
High


Low


High


Low


High
Frequencies


Note
NI Vision uses the standard representation to represent complex images in memory.
Use this representation when building an image mask.


Figure 7-1a shows an image. Figure 7-1b shows the FFT of the same image
using standard representation.



#### Figure 7-1. FFT of an Image in Standard Representation



#### Optical Representation


In the optical representation, low frequencies are grouped at the center of
the image while high frequencies are located at the edges. The constant
term, or null frequency, is at the center of the image. The frequency range
is as follows:


a. Original Image
b. FFT in Standard Representation


N
2---
–
N
2---
,
M
2----
–
M
2----
,
×


.


Figure 7-2a shows the same original image as shown in Figure 7-1a.
Figure 7-2b shows the FFT of the image in optical representation.



#### Figure 7-2. FFT of an Image in Optical Representation


Note
NI Vision uses optical representation when displaying a complex image.


You can switch from standard representation to optical representation by
permuting the A, B, C, and D quarters.


D
C


B
A
High
Frequencies


High
Frequencies


High


Low


Low


High
Low


High


Low


High


Low
Frequencies


a. Original Image
b. FFT in Optical Representation


Intensities in the FFT image are proportional to the amplitude of the
displayed component.



### Lowpass FFT Filters


A lowpass frequency filter attenuates, or removes, high frequencies
present in the FFT plane. This filter suppresses information related to
rapid variations of light intensities in the spatial image. In this case, an
inverse FFT produces an image in which noise, details, texture, and sharp
edges are smoothed.


A lowpass frequency filter attenuates, or removes, spatial frequencies
located outside a frequency range centered on the fundamental (or null)
frequency.



#### Lowpass Attenuation


Lowpass attenuation applies a linear attenuation to the full frequency
range, increasing from the null frequency f0 to the maximum frequency fmax.
This is done by multiplying each frequency by a coefficient C, which is a
function of its deviation from the fundamental and maximum frequencies.


where
C( f0) = 1
C( fmax) = 0


H(u, v)


v
u


C f( )
fmax
f
–
fmax
f0
–
-------------------
=


1


0
f0
fmax


C(f)



#### Lowpass Truncation


Lowpass truncation removes a frequency f if it is higher than the cutoff or
truncation frequency, fc. This is done by multiplying each frequency f by a
coefficient C equal to 0 or 1, depending on whether the frequency f is
greater than the truncation frequency fc.


If
f > fc


then
C( f) = 0


else
C( f) = 1


The following series of graphics illustrates the behavior of both types of
lowpass filters. They represent the 3D-view profile of the magnitude of
the FFT.


This example uses the following original FFT.


After lowpass attenuation, the magnitude of the central peak is the same,
and variations at the edges almost have disappeared.


1


0
f0
fc
fmax


C(f)


After lowpass truncation with fc = f0 + 20%( fmax – f0), spatial frequencies
outside the truncation range [ f0, fc] are removed. The part of the central
peak that remains is identical to the one in the original FFT plane.



### Highpass FFT Filters


A highpass FFT filter attenuates, or removes, low frequencies present in
the FFT plane. It has the effect of suppressing information related to
slow variations of light intensities in the spatial image. In this case, the
Inverse FFT command produces an image in which overall patterns are
attenuated and details are emphasized.


H(u, v)


v
u



#### Highpass Attenuation


Highpass attenuation applies a linear attenuation to the full frequency
range, increasing from the maximum frequency fmax to the null frequency f0.
This is done by multiplying each frequency by a coefficient C, which is a
function of its deviation from the fundamental and maximum frequencies.


where
C( f0) = 0
C( fmax) = 1



#### Highpass Truncation


Highpass truncation removes a frequency f if it is lower than the cutoff or
truncation frequency, fc. This is done by multiplying each frequency f by a
coefficient C equal to 1 or 0, depending on whether the frequency f is
greater than the truncation frequency fc.


If
f < fc


then
C( f) = 0


else
C( f) = 1


The following series of graphics illustrates the behavior of both types of
highpass filters. They represent the 3D-view profile of the magnitude of the
FFT. This example uses the following original FFT image.


C f( )
f
f0
–
fmax
f0
–
-------------------
=


1


0
f0
fmax


C(f)


1


0
f0
fc
fmax


C(f)


After highpass attenuation, the central peak has been removed,
and variations present at the edges remain.


After highpass truncation with fc = f0 + 20%( fmax – f0), spatial frequencies
inside the truncation range [ f0, fc] are set to 0. The remaining frequencies
are identical to the ones in the original FFT plane.



### Mask FFT Filters


A mask FFT filter removes frequencies contained in a mask specified by
the user. Depending on the mask definition, this filter can act as a lowpass,
bandpass, highpass, or any type of selective filter.



## In-Depth Discussion



### Fourier Transform


The spatial frequencies of an image are calculated by a function called the
Fourier Transform. It is defined in the continuous domain as


where
f(x, y) is the light intensity of the point (x, y), and
(u, v) are the horizontal and vertical spatial frequencies.


The Fourier Transform assigns a complex number to each set (u, v).


Inversely, a Fast Fourier Transform F(u, v) can be transformed into a spatial
image f(x, y) of resolution NM using the following formula:


where N × M is the resolution of the spatial image f(x, y).


H(u, v)


v
u


F u v
,
(
)
f x y
,
(
)e j2π xu
yv
+
(
)
–
x y
d
d


∞
–


∞
∫
∞
–


∞
∫
=


f x y
,
(
)
1
NM
--------
F u v
,
(
)e


j2π ux
N
-----
vy
M
-----
+






v
0
=


M
1
–
∑
u
0
=


N
1
–
∑
=


In the discrete domain, the Fourier Transform is calculated with an efficient
algorithm called the Fast Fourier Transform (FFT).


Because
, F(u, v) is composed of an
infinite sum of sine and cosine terms. Each pair (u, v) determines the
frequency of its corresponding sine and cosine pair. For a given set (u, v),
notice that all values f (x, y) contribute to F(u, v). Because of this
complexity, the FFT calculation is time consuming.


Given an image with a resolution N × M and given ∆x and ∆y the spatial
step increments, the FFT of the source image has the same resolution NM
and its frequency step increments ∆u and ∆v, which are defined in the
following equations:



### FFT Display


An FFT image can be visualized using any of its four complex components:
real part, imaginary part, magnitude, and phase. The relation between these
components is expressed by


F(u, v) = R(u, v) + jI(u, v)


where
R(u, v) is the real part and
I(u, v) is the imaginary part, and


F(u, v) =


where
is the magnitude and
ϕ(u, v) is the phase.


The magnitude of F(u, v) is also called the Fourier spectrum and is equal to


The Fourier spectrum to the power of two is known as the power spectrum
or spectral density.


F u v
,
(
)
f x y
,
(
)e


j2π
–
ux
N
-----
vy
M
-----
+






y
0
=


M
1
–
∑
x
0
=


N
1
–
∑
=


e j2πux
–
2πux
cos
j
2πux
sin
–
=


∆u
1
N
∆x
×
----------------
=
∆v
1
M
∆y
×
-----------------
=


F u v
,
(
)
ejϕ u v
,
〈
〉
×


F u v
,
(
)


F u v
,
(
)
R u v
,
(
)2
I
+
u v
,
(
)2
=


The phase ϕ(u, v) is also called the phase angle and is equal to


By default, when you display a complex image, the magnitude plane of the
complex image is displayed using the optical representation. To visualize
the magnitude values properly, the magnitude values are scaled by the
factor m before they are displayed. The factor m is calculated as


where
w is the width of the image and
h is the height of the image.


ϕ u v
,
(
)
I u v
,
(
)
R u v
,
(
)
----------------
atan
=


128
w
h
×
------------
