# Chapter 5: Image Processing

> **Part**: `Part II: Image Processing and Analysis` | **Pages**: `69 - 109`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


5
Image Processing


This chapter contains information about lookup tables, convolution
kernels, spatial filters, and grayscale morphology.



## Lookup Tables


The lookup table (LUT) transformations are basic image-processing
functions that highlight details in areas containing significant information,
at the expense of other areas. These functions include histogram
equalization, gamma corrections, logarithmic corrections, and exponential
corrections.



### When to Use


Use LUT transformations to improve the contrast and brightness of an
image by modifying the dynamic intensity of regions with poor contrast.



### Concepts


A LUT transformation converts input gray-level values from the source
image into other gray-level values in the transformed image.


A LUT transformation applies the transform T(x) over a specified input
range [rangeMin, rangeMax] in the following manner:


T(x) = dynamicMin if x ≤ rangeMin
f(x) if rangeMin < x ≤ rangeMax
dynamicMax if x > rangeMax


where
x represents the input gray-level value
dynamicMin = 0 (8-bit images) or the smallest initial pixel
value (16-bit and floating point images)
dynamicMax = 255 (8-bit images) or the largest initial pixel
value (16-bit and floating point images)
dynamicRange = dynamicMax – dynamicMin
f(x) represents the new value.



## Chapter 5 Image Processing


The function scales f(x) so that f(rangeMin) = dynamicMin and
f(rangeMax) = dynamicMax. f(x) behaves on [rangeMin, rangeMax]
according to the method you select.


In the case of an 8-bit resolution, a LUT is a table of 256 elements. The
index element of the array represents an input gray-level value. The value
of each element indicates the output value.


The transfer function associated with a LUT has an intended effect on the
brightness and contrast of the image.



#### Example


The following example uses the following source image. In the linear
histogram of the source image, the gray-level intervals [0, 49] and
[191, 254] do not contain significant information.


Using the following LUT transformation, any pixel with a value less than
49 is set to 0, and any pixel with a value greater than 191 is set to 255.
The interval [50, 190] expands to [1, 254], increasing the intensity dynamic
of the regions with a concentration of pixels in the gray-level range
[50, 190].


If x ∈[0, 49 ], F(x) = 0


If x ∈[191, 254 ], F(x) = 255


else F(x) = 1.81 × x – 89.5


0
49
190
255


F(x)


0
x


The LUT transformation produces the following image. The linear
histogram of the new image contains only the two peaks of the
interval [50, 190].



#### Predefined Lookup Tables


Seven predefined LUTs are available in NI Vision: Linear, Logarithmic,
Power 1/Y, Square Root, Exponential, Power Y, and Square. Table 5-1
shows the transfer function for each LUT and describes its effect on an
image displayed in a palette that associates dark colors to low-intensity
values and bright colors to high-intensity values, such as the Gray palette.



#### Logarithmic and Inverse Gamma Correction


The logarithmic and inverse gamma corrections expand low gray-level
ranges while compressing high gray-level ranges. When using the Gray
palette, these transformations increase the overall brightness of an image



#### Table 5-1. LUT Transfer Functions


LUT
Transfer Function
Shading Correction


Linear
Increases the intensity dynamic by evenly
distributing a given gray-level interval [min, max]
over the full gray scale [0, 255]. Min and max
default values are 0 and 255 for an 8-bit image.


Logarithmic Power
1/Y Square Root


Increases the brightness and contrast in dark
regions. Decreases the contrast in bright regions.


Exponential Power
Y Square


Decreases the brightness and contrast in dark
regions. Increases the contrast in bright regions.


and increase the contrast in dark areas at the expense of the contrast in
bright areas.


The following graphs show how the transformations behave. The horizontal
axis represents the input gray-level range, and the vertical axis represents
the output gray-level range. Each input gray-level value is plotted
vertically, and its point of intersection with the look-up curve is plotted
horizontally to give an output value.


The Logarithmic, Square Root, and Power 1/Y functions expand intervals
containing low gray-level values while compressing intervals containing
high gray-level values.


The higher the gamma coefficient Y, the stronger the intensity correction.
The Logarithmic correction has a stronger effect than the Power 1/Y
function.


Logarithmic and Inverse Gamma Correction Examples


The following series of illustrations presents the linear and cumulative
histograms of an image after various LUT transformations. The more the
histogram is compressed on the right, the brighter the image.


Note
Graphics on the left represent the original image, graphics on the top right represent
the linear histogram, and graphics on the bottom right represent the cumulative histogram.


250


200


150


100


50


0


Log


Y = 4


Y = 3


Y = 2


The following graphic shows the original image and histograms.


A Power 1/Y transformation (where Y = 1.5) produces the following image
and histograms.


A Square Root or Power 1/Y transformation (where Y = 2) produces the
following image and histograms.


A Logarithm transformation produces the following image and histograms.



#### Exponential and Gamma Correction


The exponential and gamma corrections expand high gray-level ranges
while compressing low gray-level ranges. When using the Gray palette,
these transformations decrease the overall brightness of an image and
increase the contrast in bright areas at the expense of the contrast in
dark areas.


The following graphs show how the transformations behave. The horizontal
axis represents the input gray-level range, and the vertical axis represents
the output gray-level range. Each input gray-level value is plotted
vertically, and its point of intersection with the look-up curve is plotted
horizontally to give an output value.


The Exponential, Square, and Power Y functions expand intervals
containing high gray-level values while compressing intervals containing
low gray-level values.


The higher the gamma coefficient Y, the stronger the intensity correction.
The Exponential correction has a stronger effect than the Power Y function.


250


200


150


100


50


0


Exp


Y = 2


Y = 3


Y = 4


Exponential and Gamma Correction Examples


The following series of illustrations presents the linear and cumulative
histograms of an image after various LUT transformations. The more the
histogram is compressed, the darker the image.


Note
Graphics on the left represent the original image, graphics on the top right represent
the linear histogram, and graphics on the bottom right represent the cumulative histogram.


The following graphic shows the original image and histograms.


A Power Y transformation (where Y = 1.5) produces the following image
and histograms.


A Square or Power Y transformation (where Y = 2) produces the following
image and histograms.


An Exponential transformation produces the following image and
histograms.



#### Equalize


The Equalize function is a lookup table operation that does not work on a
predefined LUT. Instead, the LUT is computed based on the content of the
image where the function is applied.


The Equalize function alters the gray-level values of pixels so that they
become evenly distributed in the defined grayscale range, which is 0 to
255 for an 8-bit image. The function associates an equal amount of pixels
per constant gray-level interval and takes full advantage of the available
shades of gray. Use this transformation to increase the contrast in images
that do not use all gray levels.


The equalization can be limited to a gray-level interval, also called the
equalization range. In this case, the function evenly distributes the pixels
belonging to the equalization range over the full interval, which is 0 to
255 for an 8-bit image. The other pixels are set to 0. The image produced
reveals details in the regions that have an intensity in the equalization range;
other areas are cleared.


Equalization Example 1


This example shows how an equalization of the interval [0, 255] can spread
the information contained in the three original peaks over larger intervals.
The transformed image reveals more details about each component in the
original image. The following graphics show the original image and
histograms.


Note
In Examples 1 and 2, graphics on the left represent the original image, graphics on
the top right represent the linear histogram, and graphics on the bottom right represent the
cumulative histogram.


An equalization from [0, 255] to [0, 255] produces the following image and
histograms.


Note
The cumulative histogram of an image after a histogram equalization always has a
linear profile, as seen in the preceding example.


Equalization Example 2


This example shows how an equalization of the interval [166, 200] can
spread the information contained in the original third peak (ranging from
166 to 200) to the interval [0, 255]. The transformed image reveals details
about the component with the original intensity range [166, 200] while all
other components are set to black. An equalization from [166, 200] to
[0, 255] produces the following image and histograms.



## Convolution Kernels


A convolution kernel defines a 2D filter that you can apply to a grayscale
image. A convolution kernel is a 2D structure whose coefficients define the
characteristics of the convolution filter that it represents. In a typical
filtering operation, the coefficients of the convolution kernel determine the
filtered value of each pixel in the image. NI Vision provides a set of
convolution kernels that you can use to perform different types of filtering
operations on an image. You also can define your own convolution kernels,
thus creating custom filters.


Use a convolution kernel whenever you want to filter a grayscale image.
Filtering a grayscale image enhances the quality of the image to meet the
requirements of your application. Use filters to smooth an image, remove
noise from an image, enhance the edge information in an image, and so on.


A convolution kernel defines how a filter alters the pixel values in a
grayscale image. The convolution kernel is a 2D structure whose
coefficients define how the filtered value at each pixel is computed. The
filtered value of a pixel is a weighted combination of its original value and
the values of its neighboring pixels. The convolution kernel coefficients


define the contribution of each neighboring pixel to the pixel being
updated. The convolution kernel size determines the number of
neighboring pixels whose values are considered during the filtering
process.


In the case of a 3 × 3 kernel, illustrated in Figure 5-1a, the value of the
central pixel (shown in black) is derived from the values of its eight
surrounding neighbors (shown in gray). A 5 × 5 kernel, shown in
Figure 5-1b, specifies 24 neighbors, a 7 × 7 kernel specifies 48 neighbors,
and so forth.



#### Figure 5-1. Examples of Kernels


A filtering operation on an image involves moving the kernel from the
leftmost and topmost pixel in the image to the rightmost and bottommost
point in the image. At each pixel in the image, the new value is computed
using the values that lie under the kernel, as shown in Figure 5-2.



#### Figure 5-2. Mechanics of Filtering


1
Kernel
2
Image


2
1
2
1


a.
b.


Kernel


Filtering
Function


Neighbors


Central Pixel


When computing the filtered values of the pixels that lie along the border
of the image (the first row, last row, first column, or last column of pixels),
part of the kernel falls outside the image. For example, Figure 5-3 shows
that one row and one column of a 3 × 3 kernel fall outside the image when
computing the value of the topmost leftmost pixel.



#### Figure 5-3. Filtering Border Pixels


NI Vision automatically allocates a border region when you create an
image. The default border region is three pixels deep and contains pixel
values of 0. You also can define a custom border region and specify the
pixel values within the region. The size of the border region should be
greater than or equal to half the number of rows or columns in your kernel.
The filtering results from along the border of an image are unreliable
because the neighbors necessary to compute these values are missing,
therefore decreasing the efficiency of the filter, which works on a much
smaller number of pixels than specified for the rest of the image. For more
information about border regions, refer to Chapter 1, Digital Images.



## Spatial Filtering


Filters are divided into two types: linear (also called convolution) and
nonlinear.


A convolution is an algorithm that consists of recalculating the value of
a pixel based on its own pixel value and the pixel values of its neighbors
weighted by the coefficients of a convolution kernel. The sum of this
calculation is divided by the sum of the elements in the kernel to obtain


1
Border
2
Image
3
Kernel


1


2


1


3


a new pixel value. The size of the convolution kernel does not have a
theoretical limit and can be either square or rectangular (3 × 3, 5 × 5, 5 × 7,
9 × 3, 127 × 127, and so on). Convolutions are divided into four families:
gradient, Laplacian, smoothing, and Gaussian. This grouping is determined
by the convolution kernel contents or the weight assigned to each pixel,
which depends on the geographical position of that pixel in relation to the
central kernel pixel.


NI Vision features a set of standard convolution kernels for each family and
for the usual sizes (3 × 3, 5 × 5, and 7 × 7). You also can create your own
kernels and choose what to put into them. The size of the user-defined
kernel is virtually unlimited. With this capability, you can create filters with
specific characteristics.


Spatial filters serve a variety of purposes, such as detecting edges along a
specific direction, contouring patterns, reducing noise, and detail outlining
or smoothing. Filters smooth, sharpen, transform, and remove noise from
an image so that you can extract the information you need.


Nonlinear filters either extract the contours (edge detection) or remove the
isolated pixels. NI Vision has six different methods you can use for contour
extraction (Differentiation, Gradient, Prewitt, Roberts, Sigma, or Sobel).
The Canny Edge Detection filter is a specialized edge detection method
that locates edges accurately, even under low signal-to-noise conditions in
an image.


To harmonize pixel values, choose between two filters, each of which uses
a different method: NthOrder and LowPass. These functions require that
either a kernel size and order number or percentage is specified on input.


Spatial filters alter pixel values with respect to variations in light intensity
in their neighborhood. The neighborhood of a pixel is defined by the size
of a matrix, or mask, centered on the pixel itself. These filters can be
sensitive to the presence or absence of light-intensity variations.


Spatial filters fall into two categories:


•
Highpass filters emphasize significant variations of the light intensity
usually found at the boundary of objects. Highpass frequency filters
help isolate abruptly varying patterns that correspond to sharp edges,
details, and noise.


•
Lowpass filters attenuate variations of the light intensity. Lowpass
frequency filters help emphasize gradually varying patterns such as
objects and the background. They have the tendency to smooth images
by eliminating details and blurring edges.



#### Spatial Filter Types Summary


Table 5-2 describes the different types of spatial filters.



#### Linear Filters


A linear filter replaces each pixel by a weighted sum of its neighbors.
The matrix defining the neighborhood of the pixel also specifies the weight
assigned to each neighbor. This matrix is called the convolution kernel.


If the filter kernel contains both negative and positive coefficients, the
transfer function is equivalent to a weighted differentiation and produces a
sharpening or highpass filter. Typical highpass filters include gradient and
Laplacian filters.


If all coefficients in the kernel are positive, the transfer function is
equivalent to a weighted summation and produces a smoothing or lowpass
filter. Typical lowpass filters include smoothing and Gaussian filters.



#### Table 5-2. Spatial Filter Types


Filter Type
Filters


Linear


Highpass


Lowpass


Gradient, Laplacian


Smoothing, Gaussian


Nonlinear


Highpass


Lowpass


Gradient, Roberts, Sobel, Prewitt, Differentiation,
Sigma


Median, Nth Order, Lowpass


Gradient Filter


A gradient filter highlights the variations of light intensity along a specific
direction, which has the effect of outlining edges and revealing texture.


Given the following source image,


a gradient filter extracts horizontal edges to produce the following image.


A gradient filter highlights diagonal edges to produce the following image.


Kernel Definition


A gradient convolution filter is a first-order derivative. Its kernel uses the
following model:


a –b
c
b
x –d
c
d –a


where a, b, c, and d are integers and x = 0 or 1.


Filter Axis and Direction


This kernel has an axis of symmetry that runs between the positive and
negative coefficients of the kernel and through the central element. This
axis of symmetry gives the orientation of the edges to outline. For example,
if a = 0, b = –1, c = –1, d = –1, and x = 0, the kernel is the following:


0
1
1
–1
0
1
–1 –1
0


The axis of symmetry is located at 135°.


For a given direction, you can design a gradient filter to highlight or darken
the edges along that direction. The filter actually is sensitive to the
variations of intensity perpendicular to the axis of symmetry of its kernel.
Given the direction D going from the negative coefficients of the kernel
towards the positive coefficients, the filter highlights the pixels where the
light intensity increases along the direction D, and darkens the pixels where
the light intensity decreases.


The following two kernels emphasize edges oriented at 135°.


Note
Applying Prewitt #10 to an image returns the same results as applying Prewitt #2 to
its photometric negative because reversing the lookup table of an image converts bright
regions into dark regions and vice versa.


Edge Extraction and Edge Highlighting


The gradient filter has two effects, depending on whether the central
coefficient x is equal to 1 or 0.


•
If the central coefficient is null (x = 0), the gradient filter highlights
the pixels where variations of light intensity occur along a direction
specified by the configuration of the coefficients a, b, c, and d.
The transformed image contains black-white borders at the original
edges, and the shades of the overall patterns are darkened.


Prewitt #10
Prewitt #2


0 –1 –1
1
0 –1
1
1
0


Prewitt #10 highlights pixels where the light
intensity increases along the direction going
from northeast to southwest. It darkens pixels
where the light intensity decreases along that
same direction. This processing outlines the
northeast front edges of bright regions such as
the ones in the illustration.


0
1
1
–1
0
1
–1 –1
0


Prewitt #2 highlights pixels where the light
intensity increases along the direction going
from southwest to northeast. It darkens pixels
where the light intensity decreases along that
same direction. This processing outlines the
southwest front edges of bright regions such as
the ones in the illustration.


•
If the central coefficient is equal to 1 (x = 1), the gradient filter detects
the same variations as mentioned above, but superimposes them over
the source image. The transformed image looks like the source image
with edges highlighted. Use this type of kernel for grain extraction and
perception of texture.


Notice that Prewitt #15 can be decomposed as follows:


Note
The convolution filter using the second kernel on the right side of the equation
reproduces the source image. All neighboring pixels are multiplied by 0 and the central
pixel remains equal to itself: (P(i, j) = 1 × P(i, j)).


This equation indicates that Prewitt #15 adds the edges extracted by the
Kernel C to the source image.


Prewitt #15 = Prewitt #14 + Source Image


Source Image
Prewitt #14
Filtered Image


–1 –1
0
–1
0
1
0
1
1


Source Image
Prewitt #15
Filtered Image


–1 –1
0
–1
1
1
0
1
1


–1 –1
0
–1
1
1
0
1
1


=


–1 –1
0
–1
0
1
0
1
1


+


0
0
0
0
1
0
0
0
0


Edge Thickness


The larger the kernel, the thicker the edges. The following image illustrates
gradient west–east 3 × 3.


The following image illustrates gradient west–east 5 × 5.


Finally, the following image illustrates gradient west–east 7 × 7.


Laplacian Filters


A Laplacian filter highlights the variation of the light intensity surrounding
a pixel. The filter extracts the contour of objects and outlines details.
Unlike the gradient filter, it is omnidirectional.


Given the following source image,


a Laplacian filter extracts contours to produce the following image.


A Laplacian filter highlights contours to produce the following image.


Kernel Definition


The Laplacian convolution filter is a second–order derivative, and its
kernel uses the following model:


a
d
c
b
x
b
c
d
a


where a, b, c, and d are integers.


The Laplacian filter has two different effects, depending on whether the
central coefficient x is equal to or greater than the sum of the absolute
values of the outer coefficients.


Contour Extraction and Highlighting


If the central coefficient is equal to this sum
,
the Laplacian filter extracts the pixels where significant variations of light
intensity are found. The presence of sharp edges, boundaries between
objects, modification in the texture of a background, noise, or other effects
can cause these variations. The transformed image contains white contours
on a black background.


Notice the following source image, Laplacian kernel, and filtered image.


If the central coefficient is greater than the sum of the outer coefficients
(x > 2(a + b + c + d)), the Laplacian filter detects the same variations
as mentioned above, but superimposes them over the source image.
The transformed image looks like the source image, with all significant
variations of the light intensity highlighted.


Source Image
Laplacian #3
Filtered Image


–1 –1 –1
–1
8 –1
–1 –1 –1


Source Image
Laplacian #4
Filtered Image


–1 –1 –1
–1
9 –1
–1 –1 –1


x
2 a
b
c
d
+
+
+
(
)
=


Notice that the Laplacian #4 kernel can be decomposed as follows:


Note
The convolution filter, using the second kernel on the right side of the equation,
reproduces the source image. All neighboring pixels are multiplied by 0, and the central
pixel remains equal to itself: (P(i, j) = 1 × P(i, j)).


This equation indicates that the Laplacian #2 kernel adds the contours
extracted by the Laplacian #1 kernel to the source image.


Laplacian #4 = Laplacian #3 + Source Image


For example, if the central coefficient of Laplacian #4 kernel is 10, the
Laplacian filter adds the contours extracted by Laplacian #3 kernel to
the source image times 2, and so forth. A greater central coefficient
corresponds to less-prominent contours and details highlighted by the filter.


Contour Thickness


Larger kernels correspond to thicker contours. The following image is a
Laplacian 3 × 3.


The following image is a Laplacian 5 × 5.


–1 –1 –1
–1
9 –1
–1
1 –1


=


–1 –1 –1
–1 8 –1
–1 –1 –1


+


0
0
0
0
1
0
0
0
0


The following image is a Laplacian 7 × 7.


Smoothing Filter


A smoothing filter attenuates the variations of light intensity in the
neighborhood of a pixel. It smooths the overall shape of objects, blurs
edges, and removes details.


Given the following source image,


a smoothing filter produces the following image.


Kernel Definition


A smoothing convolution filter is an averaging filter whose kernel uses the
following model:


a
d
c
b
x
b
c
d
a


where a, b, c, and d are positive integers, and x = 0 or 1.


Because all the coefficients in a smoothing kernel are positive, each central
pixel becomes a weighted average of its neighbors. The stronger the weight
of a neighboring pixel, the more influence it has on the new value of the
central pixel.


For a given set of coefficients (a, b, c, d), a smoothing kernel with a central
coefficient equal to 0 (x = 0) has a stronger blurring effect than a smoothing
kernel with a central coefficient equal to 1 (x = 1).


Notice the following smoothing kernels and filtered images. A larger kernel
size corresponds to a stronger smoothing effect.


Kernel
Filtered Image


Kernel A


0
1
0
1
0
1
0
1
0


Filtered Image


Kernel B


2
2
2
2
1
2
2
2
2


Filtered Image


Gaussian Filters


A Gaussian filter attenuates the variations of light intensity in the
neighborhood of a pixel. It smooths the overall shape of objects and
attenuates details. It is similar to a smoothing filter, but its blurring effect
is more subdued.


Given the following source image,


a Gaussian filter produces the following image.


Kernel C


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


Filtered Image


Kernel D


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


Filtered Image


Kernel
Filtered Image


Kernel Definition


A Gaussian convolution filter is an averaging filter, and its kernel uses the
model


a
d
c
b
x
b
c
d
a


where a, b, c, and d are integers, and x > 1.


The coefficients of a Gaussian convolution kernel of a given size are the
best possible approximation using integer numbers of a Gaussian curve.
For example,


Because all the coefficients in a Gaussian kernel are positive, each pixel
becomes a weighted average of its neighbors. The stronger the weight of a
neighboring pixel, the more influence it has on the new value of the central
pixel.


Unlike a smoothing kernel, the central coefficient of a Gaussian filter is
greater than 1. Therefore the original value of a pixel is multiplied by a
weight greater than the weight of any of its neighbors. As a result, a greater
central coefficient corresponds to a more subtle smoothing effect. A larger
kernel size corresponds to a stronger smoothing effect.


3 × 3


1
2
1
2
4
2
1
2
1


5 × 5


1
2
4
2
1
2
4
8
4
2
4
8
16
8
4
2
4
8
4
2
1
2
4
2
1



#### Nonlinear Filters


A nonlinear filter replaces each pixel value with a nonlinear function of
its surrounding pixels. Like the linear filters, the nonlinear filters operate
on a neighborhood.



#### Nonlinear Prewitt Filter


The nonlinear Prewitt filter is a highpass filter that extracts the outer
contours of objects. It highlights significant variations of the light intensity
along the vertical and horizontal axes.


Each pixel is assigned the maximum value of its horizontal and vertical
gradient obtained with the following Prewitt convolution kernels:



#### Nonlinear Sobel Filter


The nonlinear Sobel filter is a highpass filter that extracts the outer
contours of objects. It highlights significant variations of the light intensity
along the vertical and horizontal axes.


Each pixel is assigned the maximum value of its horizontal and vertical
gradient obtained with the following Sobel convolution kernels:


As opposed to the Prewitt filter, the Sobel filter assigns a higher weight to
the horizontal and vertical neighbors of the central pixel.


Prewitt #0
Prewitt #12


–1
0
1
–1
0
1
–1
0
1


–1 –1 –1
0
0
0
1
1
1


Sobel #16
Sobel #28


–1
0
1
–2
0
2
–1
0
1


–1 –2 –1
0
0
0
1
2
1


Nonlinear Prewitt and Nonlinear Sobel Example


This example uses the following source image.


A nonlinear Prewitt filter produces the following image.


A nonlinear Sobel filter produces the following image.


Both filters outline the contours of the objects. Because of the different
convolution kernels they combine, the nonlinear Prewitt has the tendency
to outline curved contours while the nonlinear Sobel extracts square
contours. This difference is noticeable when observing the outlines of
isolated pixels.



#### Nonlinear Gradient Filter


The nonlinear gradient filter outlines contours where an intensity variation
occurs along the vertical axis.



#### Roberts Filter


The Roberts filter outlines the contours that highlight pixels where an
intensity variation occurs along the diagonal axes.



#### Differentiation Filter


The differentiation filter produces continuous contours by highlighting
each pixel where an intensity variation occurs between itself and its three
upper-left neighbors.



#### Sigma Filter


The Sigma filter is a highpass filter. It outlines contours and details by
setting pixels to the mean value found in their neighborhood, if their
deviation from this value is not significant. The example on the left shows
an image before filtering. The example on the right shows the image after
filtering.



#### Lowpass Filter


The lowpass filter reduces details and blurs edges by setting pixels to the
mean value found in their neighborhood, if their deviation from this value
is large. The example on the left shows an image before filtering.
The example on the right shows the image after filtering.



#### Median Filter


The median filter is a lowpass filter. It assigns to each pixel the median
value of its neighborhood, effectively removing isolated pixels and
reducing detail. However, the median filter does not blur the contour
of objects.


You can implement the median filter by performing an Nth order filter and
setting the order to (f 2 – 1) / 2 for a given filter size of f × f.



#### Nth Order Filter


The Nth order filter is an extension of the median filter. It assigns to each
pixel the Nth value of its neighborhood when they are sorted in increasing
order. The value N specifies the order of the filter, which you can use to
moderate the effect of the filter on the overall light intensity of the image.
A lower order corresponds to a darker transformed image; a higher order
corresponds to a brighter transformed image.


To see the effect of the Nth order filter, notice the example of an image with
bright objects and a dark background. When viewing this image with the
Gray palette, the objects have higher gray-level values than the background.


For a Given Filter Size f × f
Example of a Filter Size 3 × 3


•
If N < (f 2 – 1) / 2, the Nth order filter has the
tendency to erode bright regions (or dilate
dark regions).


•
If N = 0, each pixel is replaced by its local
minimum.


Order 0


(smooths image,
erodes bright
objects)



### In-Depth Discussion


If P(i, j) represents the intensity of the pixel P with the coordinates (i, j),
the pixels surrounding P(i, j) can be indexed as follows (in the case of a
3 × 3 matrix):


A linear filter assigns to P(i, j) a value that is a linear combination of its
surrounding values. For example,


P(i, j) = P(i, j – 1) + P(i – 1, j) + 2P(i, j) + P(i + 1, j) + P(i, j + 1)


A nonlinear filter assigns to P(i, j) a value that is not a linear combination of
the surrounding values. For example,


P(i, j) = max(P(i – 1, j – 1), P(i + 1, j – 1), P(i – 1, j + 1), P(i + 1, j + 1))


For a Given Filter Size f × f
Example of a Filter Size 3 × 3


•
If N = (f 2 – 1) / 2, each pixel is replaced by
its local median value. Dark pixels isolated in
objects are removed, as well as bright pixels
isolated in the background. The overall area
of the background and object regions does
not change.


Order 4


(equivalent to a
median filter)


•
If N > (f 2 – 1) / 2, the Nth order filter has the
tendency to dilate bright regions and erode
dark regions.


•
If N = f 2 – 1, each pixel is replaced by its
local maximum.


Order 8


(smooths image,
dilates bright
objects)


P(i – 1, j – 1)
P(i, j – 1)
P(i + 1, j – 1)


P(i – 1, j)
P(i, j)
P(i + 1, j)


P(i – 1, j + 1)
P(i, j + 1)
P(i + 1, j + 1)


In the case of a 5 × 5 neighborhood, the i and j indexes vary from –2 to 2.
The series of pixels that includes P(i, j) and its surrounding pixels is
annotated as P(n, m).


For each pixel P(i, j) in an image where i and j represent the coordinates of
the pixel, the convolution kernel is centered on P(i, j). Each pixel masked by
the kernel is multiplied by the coefficient placed on top of it. P(i, j) becomes
either the sum of these products divided by the sum of the coefficient or 1,
depending on which is greater.


In the case of a 3 × 3 neighborhood, the pixels surrounding P(i, j) and the
coefficients of the kernel, K, can be indexed as follows:


The pixel P(i, j) is given the value (1 / N)Σ K(a, b)P(a, b), with a ranging from
(i – 1) to (i + 1), and b ranging from ( j – 1) to ( j + 1). N is the normalization
factor, equal to Σ K(a, b) or 1, whichever is greater.


If the new value P(i, j) is negative, it is set to 0. If the new value P(i, j) is greater
than 255, it is set to 255 (in the case of 8-bit resolution).


The greater the absolute value of a coefficient K(a, b), the more the pixel P(a, b)
contributes to the new value of P(i, j). If a coefficient K(a, b) is 0, the neighbor
P(a, b) does not contribute to the new value of P(i, j) (notice that P(a, b) might
be P(i, j) itself).


If the convolution kernel is


0
0
0
–2
1
2
0
0
0


then
P(i, j) = (–2P(i – 1, j) + P(i, j) + 2P(i + 1, j))


P(i – 1, j – 1)
P(i, j – 1)
P(i + 1, j – 1)
K(i – 1, j – 1)
K(i, j – 1)
K(i + 1, j – 1)


P(i – 1, j)
P(i, j)
P(i + 1, j)
K(i – 1, j)
K(i, j)
K(i + 1, j)


P(i – 1, j + 1)
P(i, j + 1)
P(i + 1, j + 1)
K(i – 1, j + 1)
K(i, j + 1)
K(i + 1, j + 1)


If the convolution kernel is


0
1
0
1
0
1
0
1
0


then
P(i, j) = (P(i, j – 1) + P(i – 1, j) + P(i + 1, j) + P(i, j + 1))


P(i, j) = max[|P(i + 1, j – 1) – P(i – 1, j – 1) + P(i + 1, j) – P(i – 1, j) + P(i + 1, j + 1) – P(i – 1, j + 1)|,


|P(i – 1, j + 1) – P(i – 1, j – 1) + P(i, j + 1) – P(i, j – 1) + P(i + 1, j + 1) – P(i + 1, j – 1)|]


P(i, j) = max[|P(i + 1, j – 1) – P(i – 1, j – 1) + 2P(i + 1, j) – 2P(i – 1, j) + P(i + 1, j + 1) – P(i – 1, j + 1)|,


|P(i – 1, j + 1) – P(i – 1, j – 1) + 2P(i, j + 1) – 2P(i, j – 1) + P(i + 1, j + 1) – P(i + 1, j – 1)|]


The new value of a pixel becomes the maximum absolute value between its
deviation from the upper neighbor and the deviation of its two left
neighbors.


P(i, j) = max[|P(i, j – 1) – P(i, j)|, |P(i – 1, j – 1) – P(i – 1, j)|]


The new value of a pixel becomes the maximum absolute value between
the deviation of its upper-left neighbor and the deviation of its two other
neighbors.


P(i, j) = max[|P(i – 1, j – 1) – P(i, j)|, |P(i, j – 1) – P(i – 1, j)|]


Pi-1,j-1


Pi-1,j


Pi,j-1


Pi,j


Pi-1,j-1


Pi-1,j


Pi,j-1


Pi,j


The new value of a pixel becomes the absolute value of its maximum
deviation from its upper-left neighbors.


P(i, j) = max[|P(i – 1, j) – P(i, j)|, |P(i – 1, j – 1) – P(i, j)|, |P(i, j – 1) – P(i, j)|]


If
P(i, j) – M > S


Then
P(i, j) = P(i, j)


Else
P(i, j) = M


Given M, the mean value of P(i, j) and its neighbors, and S, their standard
deviation, each pixel P(i, j) is set to the mean value M if it falls inside the
range [M – S, M + S].


If
P(i, j) – M < S


Then
P(i, j) = P(i, j)


Else
P(i, j) = M


Given M, the mean value of P(i, j) and its neighbors, and S, their standard
deviation, each pixel P(i, j) is set to the mean value M if it falls outside the
range [M – S, M + S].


P(i, j) = median value of the series [P(n, m)]


P(i, j) = Nth value in the series [P(n, m)]


where
the P(n, m) are sorted in increasing order.


Pi-1,j-1


Pi-1,j


Pi,j-1


Pi,j


The following example uses a 3 × 3 neighborhood.


The following table shows the new output value of the central pixel for each
Nth order value.


Notice that for a given filter size f, the Nth order can rank from 0 to f 2 – 1.
For example, in the case of a filter size 3, the Nth order ranges from 0 to
8 (32 – 1).



## Grayscale Morphology


Morphological transformations extract and alter the structure of particles
in an image. They fall into two categories:


•
Binary Morphology functions, which apply to binary images


•
Grayscale morphology functions, which apply to gray-level images


In grayscale morphology, a pixel is compared to those pixels surrounding
it in order to keep the pixels whose values are the smallest (in the case of
an erosion) or the largest (in the case of a dilation).


Use grayscale morphology functions to filter or smooth the pixel intensities
of an image. Applications include noise filtering, uneven background
correction, and gray-level feature extraction.


13
10
9


12
4
8


5
5
6


Nth Order
0
1
2
3
4
5
6
7
8


New Pixel Value
4
5
5
6
8
9
10
12
13


The gray-level morphology functions apply to gray-level images. You can
use these functions to alter the shape of regions by expanding bright areas
at the expense of dark areas and vice versa. These functions smooth
gradually varying patterns and increase the contrast in boundary areas.
This section describes the following gray-level morphology functions:


•
Erosion


•
Dilation


•
Opening


•
Closing


•
Proper-opening


•
Proper-closing


•
Auto-median


These functions are derived from the combination of gray-level erosions
and dilations that use a structuring element.



#### Erosion Function


A gray-level erosion reduces the brightness of pixels that are surrounded
by neighbors with a lower intensity. The neighborhood is defined by a
structuring element.



#### Dilation Function


A gray-level dilation increases the brightness of each pixel that is
surrounded by neighbors with a higher intensity. The neighborhood is
defined by a structuring element. The gray-level dilation has the opposite
effect of the gray-level erosion because dilating bright regions also erodes
dark regions.



#### Erosion and Dilation Examples


This example uses the following source image.


Table 5-3 provides example structuring elements and the corresponding
eroded and dilated images.



#### Opening Function


The gray-level opening function consists of a gray-level erosion followed
by a gray-level dilation. It removes bright spots isolated in dark regions and
smooths boundaries. The effects of the function are moderated by the
configuration of the structuring element.


opening(I) = dilation(erosion (I))


This operation does not significantly alter the area and shape of particles
because erosion and dilation are morphological opposites. Bright borders
reduced by the erosion are restored by the dilation. However, small bright
particles that vanish during the erosion do not reappear after the dilation.



#### Table 5-3. Erosion and Dilation Examples


Structuring Element
Erosion
Dilation


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
1
0
1
1
1
0
1
0



#### Closing Function


The gray-level closing function consists of a gray-level dilation followed
by a gray-level erosion. It removes dark spots isolated in bright regions and
smooths boundaries. The effects of the function are moderated by the
configuration of the structuring element.


closing(I) = erosion(dilation (I))


This operation does not significantly alter the area and shape of particles
because dilation and erosion are morphological opposites. Bright borders
expanded by the dilation are reduced by the erosion. However, small dark
particles that vanish during the dilation do not reappear after the erosion.



#### Opening and Closing Examples


This example uses the following source image.


The opening function produces the following image.


A closing function produces the following image.


Note
Consecutive applications of an opening or closing function always give the same
results.



#### Proper-Opening Function


The gray-level proper-opening function is a finite and dual combination of
openings and closings. It removes bright pixels isolated in dark regions and
smooths the boundaries of bright regions. The effects of the function are
moderated by the configuration of the structuring element.



#### Proper-Closing Function


The proper-closing function is a finite and dual combination of closings
and openings. It removes dark pixels isolated in bright regions and smooths
the boundaries of dark regions. The effects of the function are moderated
by the configuration of the structuring element.



#### Auto-Median Function


The auto-median function uses dual combinations of openings and
closings. It generates simpler particles that have fewer details.



#### Erosion Concept and Mathematics


Each pixel in an image becomes equal to the minimum value of its
neighbors.


For a given pixel P0, the structuring element is centered on P0. The pixels
masked by a coefficient of the structuring element equal to 1 are then
referred as Pi.


P0 = min(Pi)


Note
A gray-level erosion using a structuring element f × f with all its coefficients set
to 1 is equivalent to an Nth order filter with a filter size f × f and the value N equal to 0.
Refer to the Nonlinear Filters section for more information.



#### Dilation Concept and Mathematics


Each pixel in an image becomes equal to the maximum value of its
neighbors.


For a given pixel P0, the structuring element is centered on P0. The pixels
masked by a coefficient of the structuring element equal to 1 are then
referred as Pi.


P0 = max(Pi)


Note
A gray-level dilation using a structuring element f × f with all its coefficients set
to 1 is equivalent to an Nth order filter with a filter size f × f and the value N equal
to f 2 – 1. Refer to the Nonlinear Filters section for more information.



#### Proper-Opening Concept and Mathematics


If I is the source image, the proper-opening function extracts the minimum
value of each pixel between the source image I and its transformed image
obtained after an opening, followed by a closing, and followed by another
opening.


proper-opening(I) = min(I, OCO (I))


or


proper-opening(I) = min(I, DEEDDE(I))


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



#### Proper-Closing Concept and Mathematics


If I is the source image, the proper-closing function extracts the maximum
value of each pixel between the source image I and its transformed image
obtained after a closing, followed by an opening, and followed by another
closing.


proper-closing(I) = max(I, COC(I))


or


proper-closing(I) = max(I, EDDEED(I))


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



#### Auto-Median Concept and Mathematics


If I is the source image, the auto-median function extracts the minimum
value of each pixel between the two images obtained by applying a
proper-opening and a proper-closing of the source image I.


auto-median(I) = min(OCO(I), COC(I))


or


auto-median(I) = min(DEEDDE(I), EDDEED(I))


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
