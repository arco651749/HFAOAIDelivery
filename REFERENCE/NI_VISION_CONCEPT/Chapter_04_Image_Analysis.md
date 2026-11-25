# Chapter 4: Image Analysis

> **Part**: `Part II: Image Processing and Analysis` | **Pages**: `61 - 68`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


Part II


Image Processing and Analysis


This section describes conceptual information about image analysis and
processing, operators, and frequency domain analysis.


Part II, Image Processing and Analysis, contains the following chapters:


Chapter 4, Image Analysis, contains information about histograms, line
profiles, and intensity measurements.


Chapter 5, Image Processing, contains information about lookup tables,
kernels, spatial filtering, and grayscale morphology.


Chapter 6, Operators, contains information about arithmetic and logic
operators that mask, combine, and compare images.


Chapter 7, Frequency Domain Analysis, contains information about
frequency domain analysis, the Fast Fourier transform, and analyzing and
processing images in the frequency domain.


4
Image Analysis


This chapter contains information about histograms, line profiles,
and intensity measurements.


Image analysis combines techniques that compute statistics and
measurements based on the gray-level intensities of the image pixels.
You can use the image analysis functions to understand the content of the
image and to decide which type of inspection tools to use to solve your
application. Image analysis functions also provide measurements that you
can use to perform basic inspection tasks such as presence or absence
verification.



## Histogram


A histogram counts and graphs the total number of pixels at each grayscale
level. From the graph, you can tell whether the image contains distinct
regions of a certain gray-level value.


A histogram provides a general description of the appearance of an image
and helps identify various components such as the background, objects,
and noise.



### When to Use


The histogram is a fundamental image analysis tool that describes the
distribution of the pixel intensities in an image. Use the histogram to
determine if the overall intensity in the image is high enough for your
inspection task. You can use the histogram to determine whether an image
contains distinct regions of certain grayscale values. You also can use a
histogram to adjust the image acquisition conditions.


You can detect two important criteria by looking at the histogram.


•
Saturation—Too little light in the imaging environment leads to
underexposure of the imaging sensor, while too much light causes
overexposure, or saturation, of the imaging sensor. Images acquired
under underexposed or saturated conditions will not contain all the
information that you want to inspect from the scene being observed.
It is important to detect these imaging conditions and correct for them



## Chapter 4 Image Analysis


during setup of your imaging system. You can detect whether a sensor
is underexposed or saturated by looking at the histogram. An
underexposed image contains a large number of pixels with low
gray-level values. This appears as a peak at the lower end of the
histogram. An overexposed or saturated image contains a large number
of pixels with very high gray-level values. This condition is
represented by a peak at the upper end of the histogram, as shown in
Figure 4-1.


•
Lack of contrast—A widely-used type of imaging application involves
inspecting and counting parts of interest in a scene. A strategy to
separate the objects from the background relies on a difference in the
intensities of both, for example, a bright part and a darker background.
In this case, the analysis of the histogram of the image reveals two or
more well-separated intensity populations, as shown in Figure 4-2.
Tune your imaging setup until the histogram of your acquired images
has the contrast required by your application.



### Concepts


The histogram is the function H defined on the grayscale range
[0, …, k, …, 255] such that the number of pixels equal to the gray-level
value k is


H(k) = nk


where
k is the gray-level value,
nk is the number of pixels in an image with a gray-level value
equal to k, and
Σ nk from k = 0 to 255 is the total number of pixels in an
image.


The histogram plot in Figure 4-1 reveals which gray levels occur frequently
and which occur rarely.



#### Figure 4-1. Histogram Plot


0
k


nk


255


Grayscale Range


Two types of histograms can be calculated: the linear and cumulative
histograms.


In both cases, the horizontal axis represents the gray-level value that ranges
from 0 to 255. For a gray-level value k, the vertical axis of the linear
histogram indicates the number of pixels nk set to the value k, and the
vertical axis of the cumulative histogram indicates the percentage of pixels
set to a value less than or equal to k.



### Linear Histogram


The density function is


HLinear(k) = nk


where
HLinear(k) is the number of pixels equal to k.


The probability function is


PLinear(k) = nk /n


where
PLinear(k) is the probability that a pixel is equal to k.



#### Figure 4-2. Sample of a Linear Histogram



### Cumulative Histogram


The distribution function is


HCumul(k)=


where
HCumul(k) is the number of pixels that are less than or equal
to k.


nk


k


ni


i
0
=


k
∑


The probability function is


PCumul(k) =


where
PCumul(k) is the probability that a pixel is less than or equal
to k.



#### Figure 4-3. Sample of a Cumulative Histogram



### Interpretation


The gray-level intervals featuring a concentrated set of pixels reveal the
presence of significant components in the image and their respective
intensity ranges.


In Figure 4-2, the linear histogram reveals that the image is composed of
three major elements. The cumulative histogram of the same image in
Figure 4-3 shows that the two left-most peaks compose approximately 80%
of the image, while the remaining 20% corresponds to the third peak.



### Histogram Scale


The vertical axis of a histogram plot can be shown in a linear or logarithmic
scale. A logarithmic scale lets you visualize gray-level values used by small
numbers of pixels. These values might appear unused when the histogram
is displayed in a linear scale.


In a logarithmic scale, the vertical axis of the histogram gives the logarithm
of the number of pixels per gray-level value. The use of minor gray-level
values becomes more prominent at the expense of the dominant gray-level
values. The logarithmic scale emphasizes small histogram values that are
not typically noticeable in a linear scale. Figure 4-4 illustrates the
difference between the display of the histogram of the same image in a
linear and logarithmic scale. In this particular image, three pixels are
equal to 0.


ni
n---


i
0
=


k
∑


Hcumul(k)


k



#### Figure 4-4. Histogram of the Same Image Using Linear and Logarithmic Vertical Scales



### Histogram of Color Images


The histogram of a color image is expressed as a series of three tables, each
corresponding to the histograms of the three primary components in the
color model in Table 4-1.



## Line Profile


A line profile plots the variations of intensity along a line. It returns the
grayscale values of the pixels along a line and graphs it.


The line profile utility is helpful for examining boundaries between
components, quantifying the magnitude of intensity variations, and
detecting the presence of repetitive patterns.



#### Table 4-1. Color Models and Primary Components


Color Model
Components


RGB
Red, Green, Blue


HSL
Hue, Saturation, Luminance


nk


k


nk


a. Linear Vertical Scale


b. Logarithmic Vertical Scale


Figure 4-5 illustrates a typical line profile.



#### Figure 4-5. Line Profile


The peaks and valleys represent increases and decreases of the light
intensity along the line selected in the image. Their width and magnitude
are proportional to the size and intensity of their related regions.


For example, a bright object with uniform intensity appears in the plot as
a plateau. The higher the contrast between an object and its surrounding
background, the steeper the slopes of the plateau. Noisy pixels, on the other
hand, produce a series of narrow peaks.



## Intensity Measurements


Intensity measurements measure the grayscale image statistics in an image
or regions in an image.


You can use intensity measurements to measure the average intensity value
in a region of the image to determine, for example, the presence or absence
of a part or a defect in a part.


Intensity Max
(Brighter)


Intensity Min
(Darker) Starting Point
Ending Point


NI Vision contains the following densitometry parameters:


•
Minimum Gray Value—Minimum intensity value in gray-level units


•
Maximum Gray Value—Maximum intensity value in gray-level units


•
Mean Gray Value—Mean intensity value in the particle expressed in
gray-level units


•
Standard Deviation—Standard deviation of the intensity values
