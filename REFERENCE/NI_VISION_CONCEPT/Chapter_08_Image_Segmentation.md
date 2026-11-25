# Chapter 8: Image Segmentation

> **Part**: `Part III: Particle Analysis` | **Pages**: `130 - 154`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


Part III


Particle Analysis


This section describes conceptual information about particle analysis,
including thresholding, morphology, and particle measurements.


Part III, Particle Analysis, contains the following chapters:


Chapter 8, Image Segmentation, contains information about segmenting
images using global grayscale thresholding, global color thresholding,
local thresholding, and morphological segmentation.


Chapter 9, Binary Morphology, contains information about structuring
elements, connectivity, and primary and advanced morphological
transformations.


Chapter 10, Particle Measurements, contains information about
characterizing digital particles.



## Introduction


You can use particle analysis to detect connected regions or groupings of
pixels in an image and then make selected measurements of those regions.
These regions are commonly referred to as particles. A particle is a
contiguous region of nonzero pixels. You can extract particles from a
grayscale image by thresholding the image into background and
foreground states. Zero valued pixels are in the background state, and all
nonzero valued pixels are in the foreground.


Particle analysis consists of a series of processing operations and analysis
functions that produce information about particles in an image. Using
particle analysis, you can detect and analyze any 2D shape in an image.



## Part III Particle Analysis



### When to Use


Use particle analysis when you are interested in finding particles whose
spatial characteristics satisfy certain criteria. In many applications where
computation is time-consuming, you can use particle filtering to eliminate
particles that are of no interest based on their spatial characteristics, and
keep only the relevant particles for further analysis.


You can use particle analysis to find statistical information—such as
the presence of particles, their number and size, and location.
This information allows you to perform many machine vision inspection
tasks—such as detecting flaws on silicon wafers, detecting soldering
defects on electronic boards, or web inspection applications such as finding
structural defects on wood planks or detecting cracks on plastics sheets.
You also can locate objects in motion control applications.


In applications where there is a significant variance in the shape or
orientation of an object, particle analysis is a powerful and flexible way
to search for the object. You can use a combination of the measurements
obtained through particle analysis to define a feature set that uniquely
defines the shape of the object.



### Concepts


A typical particle analysis process scans through an entire image, detects
all the particles in the image, and builds a detailed report on each particle.
You can use multiple parameters such as perimeter, angle, area, and center
of mass to identify and classify these particles. Using multiple parameters
can be faster and more effective than pattern matching in many
applications.


Also, by using different sets of parameters, you can uniquely identify a
feature in an image. For example, you could use the area of the template
particle as a criterion for removing all particles that do not match it within
some tolerance. You then can perform a more refined search on the
remaining particles using another list of parameter tolerances.


The following figure shows a sample list of parameters that you can obtain
in a particle analysis application. The binary image in this example was
obtained by thresholding the source image and removing particles that
touch the border of the image. You can use these parameters to identify and
classify particles. The following table shows the values obtained for the
particle enclosed in a rectangle, shown in the figure below.


Particle Measurement
Values


Area
2456


Number of Holes
1


Bounding Rect


Left


Top


Right


Bottom


127


8


200


86


Center of Mass


X


Y


167.51


37.61


Orientation
82.36º


Dimensions


Width


Height


73


78


To use particle analysis, first create a binary image using a thresholding
process. You then can improve the binary image using morphological
transformations and make measurements on the particles in the image.


8
Image Segmentation


This chapter contains information about segmenting images using global
grayscale thresholding, global color thresholding, local thresholding, and
morphological segmentation. Image segmentation is the process of
separating objects from the background and each other so that each object
can be identified and characterized. Refer to Chapter 10, Particle
Measurements, for information about characterizing objects after
segmentation.



## Thresholding


Thresholding segments an image into a particle region—which contains the
objects under inspection—and a background region based on the pixel
intensities within the image. The resulting image is a binary image.


Use thresholding to extract areas that correspond to significant structures in
an image and to focus analysis on these areas.


Thresholding an image is often the first step in a variety of machine vision
applications that perform image analysis on binary images, such as particle
analysis, golden template comparison, and binary particle classification.



### Global Grayscale Thresholding


Global grayscale thresholding includes manual thresholding and automatic
thresholding techniques.


Global thresholding works best when the inspection images exhibit
uniform lighting both within each image and across multiple images.


Particles are characterized by an intensity range. They are composed
of pixels with gray-level values belonging to a given threshold interval



## Chapter 8 Image Segmentation


(overall luminosity or gray shade). All other pixels are considered to be
part of the background.


Thresholding sets all pixels that belong to a range of pixel values, called the
threshold interval, to 1 or a user-defined value, and it sets all other pixels
in the image to 0. Pixels inside the threshold interval are considered part of
a particle. Pixels outside the threshold interval are considered part of the
background.


Figure 8-1 shows the histogram of an image. All pixels in the image whose
values range from 166 to 255 are considered particle pixels.



#### Figure 8-1. Image Histogram and Threshold Interval



#### Manual Threshold


The threshold interval in a manual threshold has two user-defined
parameters: lower threshold and upper threshold. All pixels that have
gray-level vablues equal to or greater than the lower threshold and equal to
or smaller than the upper threshold are selected as pixels belonging to
particles in the image.


Manual Thresholding Example


This example uses the following source image.


0
166
255


Image Histogram


Threshold
Interval


Highlighting the pixels that belong to the threshold interval [166, 255]
(the brightest areas) produces the following image.



#### Automatic Threshold


NI Vision has five automatic thresholding techniques.


•
Clustering


•
Entropy


•
InterVariance


•
Metric


•
Moments


In contrast to manual thresholding, these techniques do not require that you
set the lower and upper threshold values. These techniques are well suited
for conditions in which the light intensity varies from image to image.


Clustering is the only multi-class thresholding method available. Clustering
operates on multiple classes so you can create tertiary or higher-level
images.


The other four methods—entropy, metric, moments, and interclass
variance—are reserved for strictly binary thresholding techniques.
The choice of which algorithm to apply depends on the type of image
to threshold.


Depending on your source image, it is sometimes useful to invert the
original grayscale image before applying an automatic threshold function,
such as entropy and moments. This is especially true for cases in which the
background is brighter than the foreground.


Clustering


Clustering is the most frequently used automatic thresholding method.
Use the clustering method when you need to threshold the image into more
than two classes.


Clustering sorts the histogram of the image within a discrete number of
classes corresponding to the number of phases perceived in an image. The
gray values are determined, and a barycenter is determined for each class.
This process repeats until it obtains a value that represents the center of
mass for each phase or class.


Example of Clustering


This example uses a clustering technique in two and three phases on an
image. Notice that the results from this function are generally independent
of the lighting conditions as well as the histogram values from the image.


This example uses the following original image.


Clustering in two phases produces the following image.


Clustering in three phases produces the following image.


Entropy


Based on a classical image analysis technique, entropy is best for detecting
particles that are present in minuscule proportions on the image. For
example, this function would be suitable for fault detection.


Interclass Variance


Interclass variance is based on discriminant analysis. An optimal threshold
is determined by maximizing the between-class variation with respect to
the threshold.


Metric


For each threshold, a value determined by the surfaces representing the
initial gray scale is calculated. The optimal threshold corresponds
to the smallest value.


Moments


This technique is suited for images that have poor contrast. The moments
method is based on the hypothesis that the observed image is a blurred
version of the theoretically binary original. The blurring that is produced
from the acquisition process, caused by electronic noise or slight
defocalization, is treated as if the statistical moments of average and
variance were the same for both the blurred image and the original image.
This function recalculates a theoretical binary image.



#### In-Depth Discussion


All automatic thresholding methods use the histogram of an image to
determine the threshold. Figure 8-2 explains the notations used to describe
the parameters of the histogram. These notations are used throughout this
section to show how each automatic thresholding method calculates the
threshold value for an image.



#### Figure 8-2. Parameters of a Histogram


•
i represents the gray level value


•
k represents the gray level value chosen as the threshold


Gray Level Value


Histogram Value


h(i)


i


Class 0
Class 1


k


•
h(i) represents the number of pixels in the image at each gray level
value


•
N represents the total number of gray levels in the image (256 for an
8-bit image)


•
n represents the total number of pixels in the image


Use the automatic thresholding techniques to determine the threshold pixel
value k such that all gray-level values less than or equal to k belong to
one class 0 and the other gray level values belong to another class 1, as
shown in Figure 8-2.


Clustering


The threshold value is the pixel value k for which the following condition
is true:


where µ1 is the mean of all pixel values that lie between 0 and k, and µ2 is
the mean of all the pixel values that lie between k + 1 and 255.


Entropy


In this method, the threshold value is obtained by applying information
theory to the histogram data. In information theory, the entropy of the
histogram signifies the amount of information associated with the
histogram. Let


represent the probability of occurrence of the gray level i. The entropy of a
histogram of an image with gray levels in the range [0, N – 1] is given by


µ1
µ2
+
2
-----------------
k
=


p i( )
h i( )


h i( )


i
0
=


N
1
–
∑


-----------------
=


H
p i( )
2
log p i( )


i
0
=


N
1
–
∑
–
=


If k is the value of the threshold, then the two entropies


represent the measures of the entropy (information) associated with the
black and white pixels in the image after thresholding. Pb(i) is the
probability of the background, and Pb(w) is the probability of the object.


The optimal threshold value is gray-level value that maximizes the entropy
in the thresholded image given by


Simplified, the threshold value is the pixel value k at which the following
expression is maximized:


InterVariance


The threshold value is the pixel value k at which the following expression
is maximized:


Hb
Pb i( )
2
log Pb i( ),


i
0
=


k
∑
–
=


Hw
Pw i( )
2
log Pw i( )


i
k
1
+
=


N
1
–
∑
–
=


Hb
Hw
+


1


h i( )


i
0
=


k
∑


-----------------
2 h i( )
1
+
(
)h i( )
log


i
0
=


k
∑
–
1


h i( )


i
k
1
+
=


N
1
–
∑


------------------------
2 h i( )
1
+
(
)h i( )
log


i
k
1
+
=


N
1
–
∑
2
log
h i( )


i
0
=


k
∑
h i( )


i
k
1
+
=


N
1
–
∑








+
–


σB
2 k
( )
µT ω k
( )
µ k
( )
–
[
]2


ω k
( ) 1
ω k
( )
–
[
]
------------------------------------------
=


where


Metric


The threshold value is the pixel value k at which the following expression
is minimized:


where
µ1 is the mean of all pixel values in the image that lie between
0, and k, and
µ2 is the mean of all the pixel values in the image that lie
between k + 1 and 255.


Moments


In this method the threshold value is computed in such a way that the
moments of the image to be thresholded are preserved in the binary output
image.


The kth moment m of an image is calculated as


,


where n is the total number of pixels in the image.


µ k
( )
ip i( )


i
0
=


k
∑
=


µT
ip i( )


i
0
=


N
1
–
∑
=


ω k
( )
p i( )


i
0
=


k
∑
=


h i( )


i
0
=


i
k
=
∑
i
µ1
–
(
)
h i( )


i
k
1
+
=


i
N
1
–
=
∑
i
µ2
–
(
)
+


mk
1
n--
ikh i( )


i
0
=


i
N
1
–
=
∑
=



### Global Color Thresholding


Color thresholding converts a color image into a binary image.


Threshold a color image when you need to isolate features for analysis and
processing or to remove unnecessary features.


Note
Before performing a color threshold, you may need to enhance your image with
lookup tables or the equalize function.


To threshold a color image, specify a threshold interval for each of the three
color components. A pixel in the output image is set to 1 if and only if its
color components fall within the specified ranges. Otherwise, the pixel
value is set to 0.


Figure 8-3 shows the histograms of each plane of a color image stored in
RGB format. The gray shaded region indicates the threshold range for each
of the color planes. For a pixel in the color image to be set to 1 in the binary
image, its red value should lie between 130 and 200, its green value should
lie between 100 and 150, and its blue value should lie between 55 and 115.



#### Figure 8-3. Threshold Ranges for an RGB Image


0
130
200
255


Red Plane
Histogram


0
100
150
255


Green Plane
Histogram


0
55
115
255


Blue Plane
Histogram


To threshold an RGB image, first determine the red, green, and blue
values of the pixels that constitute the objects you want to analyze after
thresholding. Then, specify a threshold range for each color plane that
encompasses the color values of interest. You must choose correct ranges
for all three color planes to isolate a color of interest.


Figure 8-4 shows the histograms of each plane of a color image stored in
HSL format. The gray shaded region indicates the threshold range for each
of the color planes. For a pixel in the color image to be set to 1 in the binary
image, its hue value should lie between 165 and 215, its saturation value
should lie between 0 and 30, and its luminance value should lie between
25 and 210.



#### Figure 8-4. Threshold Ranges for an HSL Image


The hue plane contains the main color information in an image. To
threshold an HSL image, first determine the hue values of the pixels that
you want to analyze after thresholding. In some applications, you may need
to select colors with the same hue value but various saturation values.
Because the luminance plane contains only information about the intensity
levels in the image, you can set the luminance threshold range to include all
the luminance values, thus making the thresholding process independent
from intensity information.


0
165
215 255


Hue Plane
Histogram


0
30
255


Saturation
Plane
Histogram


0
25
210
255


Luminance
Plane
Histogram



### Local Thresholding


Local thresholding, also known as locally adaptive thresholding, is like
global grayscale thresholding in that both create a binary image by
segmenting a grayscale image into a particle region and a background
region. Unlike global grayscale thresholding, which categorizes a pixel as
part of a particle or the background based on a single threshold value
derived from the intensity statistics of the entire image, local thresholding
categorizes a pixel based on the intensity statistics of its neighboring pixels.


Use local thresholding to isolate objects of interest from the background in
images that exhibit nonuniform lighting changes. Nonuniform lighting
changes, such as those resulting from a strong illumination gradient or
shadows, often make global thresholding ineffective.


Figure 8-5 show the effect of global thresholding and local thresholding on
an image with nonuniform lighting changes. Figure 8-5a show the original
inspection image of LCD digits. Figure 8-5b shows how a global threshold
segments the inspection image. Notice that many of the nondigit pixels in
the bottom, right corner are erroneously selected as particles. Figure 8-5c
shows how a local threshold segments the inspection image. Only pixels
belonging to LCD digits are selected as particles.



#### Figure 8-5. Global Thresholding Compared to Local Thresholding


The local threshoding algorithm calculates local pixel intensity
statistics—such as range, variance, surface fitting parameters, or their
logical combinations—for each pixel in an inspection image. The result of
this calculation is the local threshold value for the pixel under
consideration. The algorithm compares the original intensity value of the


a.
b.
c.


pixel under consideration to its local threshold value and determines
whether the pixel belongs to a particle or the background.


A user-defined window specifies which neighboring pixels are considered
in the statistical calculation. The default window size is 32 × 32. However,
the window size should be approximately the size of the smallest object you
want to separate from the background. Figure 8-6 shows a simplified local
thresholding window.



#### Figure 8-6. Window Used to calculate Local Threshold Values


Note
The pixel intensities of all of the pixels in the window, including the pixel under
consideration, are used to calculate the local threshold value.


A typical local thresholding function requires a large amount of
computation time. Also, the time a typical local thresholding function takes
to complete often varies depending on the window size. This lack of
determinism prevents local thresholding from being used in real-time
applications. The NI Vision local thresholding function uses a fully
optimized, efficient algorithm implementation whose computation speed is
independent of the window size. This significantly reduces the computation
cost and makes using the function in a real-time segmentation applications
possible.


1
Image
2
Local Thresholding Window


3
Pixel under Consideration


1


2
3


The following sections describe the algorithms available in the NI Vision
local thresholding function.


Note
You must specify whether you are looking for dark objects on a light background or
light objects on a dark background regardless of which algorithm you use.


Niblack Algorithm


This algorithm has been experimentally shown to be the best among eleven
locally adaptive thresholding algorithms, based on a goal-directed
evaluation from OCR and map image segmentation applications. The
algorithm is effective for many image thresholding applications, such as
display inspection and OCR.


The Niblack algorithm is sensitive to the window size and produces noisy
segmentation results in areas of the image with a large, uniform
background. To solve this problem, the NI Vision local thresholding
function computes a deviation factor that the algorithm uses to correctly
categorize pixels.


Background Correction Algorithm


This algorithm combines the local and global threshoding concepts for
image segmentation. Figure 8-7 illustrates the background correction
algorithm.



#### Figure 8-7. Background Correction Algorithm


Inspection Image


Binary Image


Background-corrected Image


No


Yes


Perform Global Threshold


Subtract Pixel Value from
Average Intensity of Window


Subtract Average Intensity
of Window from Pixel Value


Looking
for Bright
Objects?


The background-corrected image is thresholded using the interclass
variance automatic thresholding method described in the Automatic
Threshold section of this chapter.


In the Niblack algorithm, the local threshold value T(i, j) at pixel (i, j) is
calculated as


T(i, j) = m(i, j) + k.σ(i, j)


where m(i, j) is the local sample mean, k is the deviation factor, and σ(i, j)
is the variance.


Each image pixel I(i, j) is categorized as a particle or background pixel
based on the following:


if I(i, j) > T(i, j), I(i, j) = particle


else I(i, j) = background


Tip
Setting k to 0 to increases the computation speed of the Niblack algorithm.


In the background correction algorithm, the background-corrected image
B(i, j) is calculated as


B(i, j) = I(i, j) – m(i, j)


where m(i, j) is the local mean at pixel (i, j).



### Thresholding Considerations


A critical and frequent problem in segmenting an image into particle and
background regions occurs when the boundaries are not sharply
demarcated. In such a case, the determination of a correct threshold interval
becomes subjective. Therefore, you may want to enhance your images
before thresholding to outline where the correct borders lie. You can use
lookup tables, filters, FFTs, or equalize functions to enhance your images.
Observing the intensity profile of a line crossing a boundary area is also
helpful in selecting a correct threshold value. Finally, keep in mind that
morphological transformations can help you retouch the shape of binary
particles and, therefore, correct unsatisfactory selections that occurred
during thresholding.



## Morphological Segmentation


In some image analysis and machine vision applications—such as
industrial defect inspection or biomedical imaging—segmentation based
on thresholding or edge detection is not sufficient because the image
quality is insufficient or the objects under inspection touch or overlap.
In such applications, morphological segmentation is an effective method of
image segmentation. Morphological segmentation partitions an image
based on the topographic surface of the image. The image is separated into
non-overlapping regions with each region containing a unique particle.


Thresholding can segment objects from the background only if the objects
are well separated from each other and have intensity values that differ
significantly from the background. Binary morphology operators, such as
close or open, often return inaccurate results when segmenting overlapping
particles.


Use morphological segmentation to segment touching or overlapping
objects from each other and from the background. Also, use morphological
segmentation when the objects have intensity values similar to the
background.


Note
The morphological segmentation process described in the following section works
best when the objects under inspection are convex.


Morphological segmentation is a multiple-step process involving several
NI Vision functions. The following list describes each morphological
segmentation step and where to find more information about each step.


1.
Use a global or local threshold to create a binary image. Refer to the
Global Grayscale Thresholding, Global Color Thresholding, or Local
Thresholding sections of this chapter for more information about
thresholding.


2.
If necessary, use binary morphology operations to improve the quality
of the image by filling holes in particles or remove extraneous noise
from the image. Refer to Chapter 9, Binary Morphology, for more
information about binary morphology.


3.
Use the Danielsson function to transform the binary image into a
grayscale distance map in which each particle pixel is assigned a
gray-level value equal to its shortest Euclidean distance from the


particle border. Refer to Danielsson Function section of Chapter 9,
Binary Morphology, for more information about the Danielsson
function.


4.
Perform a watershed transform on the distance map to find the
watershed separation lines. Refer to the Watershed Transform section
of this chapter for more information about watershed transforms.


5.
Superimpose the watershed lines on the original image using an image
mask. Refer to the Image Masks section of Chapter 1, Digital Images,
for more information about image masks.


Figure 8-8 summarizes the morphological segmentation process and shows
an example of each step.



#### Figure 8-8. Morphological Segmentation Process


Use Global or Local
Thresholding to Create
Binary Image


Use Binary Morphology
to Improve
Image Quality


Use the Danielsson
Function to Create a
Distance Map


Perform a Watershed
Transform


Superimpose Watershed
Lines on Original Image
Using an Image Mask


Inspection
Image


Binary Morphology Unnecessary
Because Binary Image Quality
Meets Application Needs



### Watershed Transform


In geography, a watershed is an area of land from which all rain that falls
on the land flows into a specific body of water. In imaging, the watershed
transform algorithm considers the objects under inspection to be the bodies
of water. Figure 8-9 illustrates this concept.



#### Figure 8-9. 3D View of a Distance Map


Figure 8-9a shows an inspection image after it has been thresholded.
Figure 8-9b shows the distance map of objects in the image using the
gradient palette. Figure 8-9c shows the topographic surface of the distance
map. Each object from the inspection image forms a deep, conical lake
called a catchment basin. The pixels to which the distance map function
assigned the highest value represent the deepest parts of each catchment
basin. The image background represents the land surrounding the
catchment basins.


To understand how a watershed transform works, imagine that the
catchment basins are dry. If rain were to fall evenly across the image, the
basins would fill up at the same rate. Eventually, the water in the basins
represented by the circle and square would merge, forming one lake. To
prevent the two lakes from becoming one, the watershed transform
algorithm builds a dam, or watershed line, where the waters would begin to
mix.


Figure 8-10a shows the same distance map as Figure 8-9b with a line
through the bottom two objects. Figure 8-10b shows the intensities of the
pixels along the line in Figure 8-10a. Notice the watershed line preventing
the waters from the two catchment basins from mixing.


a.
b.
c.



#### Figure 8-10. Watershed Line


As the rainfall continues, the rising water in all three lakes would begin to
flood the land. The watershed transform algorithm builds dams on the land
to prevent the flood waters from each lake from merging. Figure 8-11
shows the watershed transform image after segmentation is complete. The
water from each catchment basin is represented by a different pixel value.
The black lines represent the watershed lines.



#### Figure 8-11. Inspection Image Segmented with Watershed Lines


Vincent and Soille’s Algorithm


The Vincent and Soille’s algorithm fills catchment basins from the bottom
up. Imagine that a hole is located in each local minimum. When the
topographic surface is immersed in water, water starts filling all the
catchment basins, minima of which are under the water level. If two
catchment basins are about to merge as a result of further immersion, the


a.
b.


270


260


250


240


230


220


210


200
0
20
40
60
80
100
120
140
160
187


Pixel Position
End Point
Start Point


Pixel Value


Catchment
Basin


Catchment
Basin


Watershed Line


algorithm builds a vertical dam up to the highest surface altitude. The dam
represents the watershed line. The core algorithm of the NI Vision
watershed transform function is based on Vincent and Soille’s algorithm.
The concept behind the NI Vision implementation of Vincent and Soille’s
algorithm is to sort the pixels in decreasing order of their grayscale values,
followed by a flooding step consisting of a fast breadth-first scanning of all
pixels in the order of their grayscale values.
