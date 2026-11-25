# Chapter 1: Digital Images

> **Part**: `Part I: Vision Basics` | **Pages**: `19 - 31`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


Part I


Vision Basics


This section describes conceptual information about digital images, image
display, and system calibration.


Part I, Vision Basics, contains the following chapters:


Chapter 1, Digital Images, contains information about the properties of
digital images, image types, file formats, the internal representation of
images in NI Vision, image borders, and image masks.


Chapter 2, Display, contains information about image display, palettes,
regions of interest, and nondestructive overlays.


Chapter 3, System Setup and Calibration, describes how to set up an
imaging system and calibrate the imaging setup so that you can convert
pixel coordinates to real-world coordinates.


1
Digital Images


This chapter contains information about the properties of digital images,
image types, file formats, the internal representation of images in
NI Vision, image borders, and image masks.



## Definition of a Digital Image


An image is a 2D array of values representing light intensity. For the
purposes of image processing, the term image refers to a digital image.
An image is a function of the light intensity


f(x, y)


where f is the brightness of the point (x, y), and x and y represent the spatial
coordinates of a picture element, or pixel.


By convention, the spatial reference of the pixel with the coordinates (0, 0)
is located at the top, left corner of the image. Notice in Figure 1-1 that the
value of x increases moving from left to right, and the value of y increases
from top to bottom.



### Figure 1-1. Spatial Reference of the (0, 0) Pixel


In digital image processing, an imaging sensor converts an image into a
discrete number of pixels. The imaging sensor assigns to each pixel a
numeric location and a gray level or color value that specifies the brightness
or color of the pixel.


Y


X


f (x, y)


(0,0)



## Chapter 1 Digital Images



## Properties of a Digitized Image


A digitized image has three basic properties: resolution, definition,
and number of planes.



### Image Resolution


The spatial resolution of an image is determined by its number of rows
and columns of pixels. An image composed of m columns and n rows has
a resolution of m × n. This image has m pixels along its horizontal axis
and n pixels along its vertical axis.



### Image Definition


The definition of an image indicates the number of shades that you can see
in the image. The bit depth of an image is the number of bits used to encode
the value of a pixel. For a given bit depth of n, the image has an image
definition of 2n, meaning a pixel can have 2n different values. For example,
if n equals 8 bits, a pixel can have 256 different values ranging from
0 to 255. If n equals 16 bits, a pixel can have 65,536 different values
ranging from 0 to 65,535 or from –32,768 to 32,767. Currently, NI Vision
supports only a range of –32,768 to 32,767 for 16-bit images.


NI Vision can process images with 8-bit, 10-bit, 12-bit, 14-bit, 16-bit,
floating point, or color encoding. The manner in which you encode your
image depends on the nature of the image acquisition device, the type of
image processing you need to use, and the type of analysis you need to
perform. For example, 8-bit encoding is sufficient if you need to obtain the
shape information of objects in an image. However, if you need to precisely
measure the light intensity of an image or region in an image, you should
use 16-bit or floating-point encoding.


Use color encoded images when your machine vision or image processing
application depends on the color content of the objects you are inspecting
or analyzing.


NI Vision does not directly support other types of image encoding,
particularly images encoded as 1-bit, 2-bit, or 4-bit images. In these cases,
NI Vision automatically transforms the image into an 8-bit
image—the minimum bit depth for NI Vision—when opening the image
file.



### Number of Planes


The number of planes in an image corresponds to the number of arrays
of pixels that compose the image. A grayscale or pseudo-color image
is composed of one plane. A true-color image is composed of
three planes—one each for the red component, blue component, and
green component.


In true-color images, the color component intensities of a pixel are coded
into three different values. A color image is the combination of three arrays
of pixels corresponding to the red, green, and blue components in an RGB
image. HSL images are defined by their hue, saturation, and luminance
values.



## Image Types


The NI Vision libraries can manipulate three types of images: grayscale,
color, and complex images. Although NI Vision supports all three image
types, certain operations on specific image types are not possible. For
example, you cannot apply the logic operator AND to a complex image.


Table 1-1 shows how many bytes per pixel grayscale, color, and complex
images use. For an identical spatial resolution, a color image occupies
four times the memory space of an 8-bit grayscale image, and a complex
image occupies eight times the memory of an 8-bit grayscale image.



### Table 1-1. Bytes per Pixel


Image Type
Number of Bytes per Pixel Data


8-bit
(Unsigned)
Integer
Grayscale


(1 byte or
8-bit)


8-bit for the grayscale intensity


16-bit
(Signed)
Integer
Grayscale


(2 bytes or
16-bit)


16-bit for the grayscale intensity



### Grayscale Images


A grayscale image is composed of a single plane of pixels. Each pixel is
encoded using one of the following single numbers:


•
An 8-bit unsigned integer representing grayscale values between
0 and 255


•
A 16-bit signed integer representing grayscale values between
–32,768 and +32,767


•
A single-precision floating point number, encoded using four bytes,
representing grayscale values ranging from –∞ to ∞


32-bit
Floating-
Point
Grayscale


(4 bytes or
32-bit)


32-bit for the grayscale intensity


RGB Color


(4 bytes or
32-bit)


8-bit for the
alpha value
(not used)


8-bit for the
red intensity


8-bit for the
green intensity


8-bit for the
blue intensity


HSL Color


(4 bytes or
32-bit)


8-bit not used
8-bit for the hue
8-bit for the
saturation


8-bit for the
luminance


Complex


(8 bytes or
64-bit)


32-bit floating for the real part
32-bit for the imaginary part


Table 1-1.  Bytes per Pixel (Continued)


Image Type
Number of Bytes per Pixel Data



### Color Images


A color image is encoded in memory as either a red, green, and blue (RGB)
image or a hue, saturation, and luminance (HSL) image. Color image pixels
are a composite of four values. RGB images store color information using
8 bits each for the red, green, and blue planes. HSL images store color
information using 8 bits each for hue, saturation, and luminance. RGB
U64 images store color information using 16 bits each for the red, green,
and blue planes. In the RGB and HSL color models, an additional 8-bit
value goes unused. This representation is known as 4 × 8-bit or 32-bit
encoding. In the RGB U64 color model, an additional 16-bit value goes
unused. This representation is known as 4 × 16-bit or 64-bit encoding.



### Complex Images


A complex image contains the frequency information of a grayscale image.
You can create a complex image by applying a Fast Fourier transform
(FFT) to a grayscale image. After you transform a grayscale image into a
complex image, you can perform frequency domain operations on the
image.


Each pixel in a complex image is encoded as two single-precision
floating-point values, which represent the real and imaginary components
of the complex pixel. You can extract the following four components from
a complex image: the real part, imaginary part, magnitude, and phase.


Alpha plane (not used)


Red or hue plane


Green or saturation plane


Blue or luminance plane



## Image Files


An image file is composed of a header followed by pixel values. Depending
on the file format, the header contains image information about the
horizontal and vertical resolution, pixel definition, and the original palette.
Image files may also store information about calibration, pattern matching
templates, and overlays. The following are common image file formats:


•
Bitmap (BMP)


•
Tagged image file format (TIFF)


•
Portable network graphics (PNG)—Offers the capability of storing
image information about spatial calibration, pattern matching
templates, and overlays


•
Joint Photographic Experts Group format (JPEG)


•
National Instruments internal image file format (AIPD)—Used for
saving floating-point, complex, and HSL images


Standard formats for 8-bit grayscale and RGB color images are BMP,
TIFF, PNG, JPEG, and AIPD. Standard formats for 16-bit grayscale, 64-bit
RGB, and complex images are PNG and AIPD.



## Internal Representation of an NI Vision Image


Figure 1-2 illustrates how an NI Vision image is represented in system
memory. In addition to the image pixels, the stored image includes
additional rows and columns of pixels called the image border and the left
and right alignments. Specific processing functions involving pixel
neighborhood operations use image borders. The alignment regions ensure
that the first pixel of the image is 32-byte aligned in memory. The size of
the alignment blocks depend on the image width and border size. Aligning
the image increases processing speed by as much as 30%.


The line width is the total number of pixels in a horizontal line of an image,
which includes the sum of the horizontal resolution, the image borders, and
the left and right alignments. The horizontal resolution and line width may
be the same length if the horizontal resolution is a multiple of 32 bytes and
the border size is 0.



### Figure 1-2. Internal Image Representation


1
Image
2
Image Border


3
Vertical Resolution
4
Left Alignment


5
Horizontal Resolution
6
Right Alignment


7
Line Width


2


2


2
2


3


4
5
6


7


1



## Image Borders


Many image processing functions process a pixel by using the values of its
neighbors. A neighbor is a pixel whose value affects the value of a nearby
pixel when an image is processed. Pixels along the edge of an image do not
have neighbors on all four sides. If you need to use a function that processes
pixels based on the value of their neighboring pixels, specify an image
border that surrounds the image to account for these outlying pixels.
You define the image border by specifying a border size and the values of
the border pixels.


The size of the border should accommodate the largest pixel neighborhood
required by the function you are using. The size of the neighborhood is
specified by the size of a 2D array. For example, if a function uses the
eight adjoining neighbors of a pixel for processing, the size of the
neighborhood is 3 × 3, indicating an array with three columns and
three rows. Set the border size to be greater than or equal to half the number
of rows or columns of the 2D array rounded down to the nearest integer
value. For example, if a function uses a 3 × 3 neighborhood, the image
should have a border size of at least 1; if a function uses a 5 × 5
neighborhood, the image should have a border size of at least 2. In NI
Vision, an image is created with a default border size of 3, which can
support any function using up to a 7 × 7 neighborhood without any
modification.


NI Vision provides three ways to specify the pixel values of the image
border. Figure 1-3 illustrates these options. Figure 1-3a shows the pixel
values of an image. By default, all image border pixels have a value of 0, as
shown in Figure 1-3b. You can copy the values of the pixels along the edge
of the image into the border pixels, as shown in Figure 1-3c, or you can
mirror the pixel values along the edge of the image into the border pixels,
as shown in Figure 1-3d.



### Figure 1-3. Setting the Pixel Values of an Image Border


The method you use to fill the border pixels depends on the processing
function you require for your application. Review how the function works
before choosing a border-filling method because your choice can
drastically affect the processing results. For example, if you are using a
function that detects edges in an image based on the difference between a
pixel and its neighbors, do not set the border pixel values to zero. As shown
in Figure 1-3b, an image border containing zero values introduces
significant differences between the pixel values in the border and the image
pixels along the border, which causes the function to detect erroneous edges
along the border of the image. If you are using an edge detection function,
copy or mirror the pixel values along the border into the border region to
obtain more accurate results.


8 10 10 8 11 13 15 17 13 14 12 10 10 12


10 9
9 10 12 11 8 15 14 12 11 7
7 11


10 9
9 10 12 11 8 15 14 12 11 7
7 11


8 10 10 8 11 13 15 17 13 14 12 10 10 12


12 10 10 12 13 14 12 16 12 15 10 9
9 10


15 14 14 15 12 33 34 36 32 12 14 11 11 14


12 13 13 12 14 29 40 41 33 13 12 13 13 12


11 15 15 11 10 30 42 45 31 15 12 10 10 12


9 10 10 9 13 31 30 32 33 12 13 11 11 13


8 12 12 8 12 14 12 13 12 14 11 13 13 11


13 11 11 13 11 12 9 16 17 11 13 14 14 13


9 10 10 9 15 11 12 20 16 12 11 8
8 11


13 11 11 13 11 12 9 16 17 11 13 14 14 13


9 10 10 9 15 11 12 20 16 12 11 8
8 11


9
9
9 10 12 11 8 15 14 12 11 7
7
7


9
9
9 10 12 11 8 15 14 12 11 7
7
7


9
9
9 10 12 11 8 15 14 12 11 7
7
7


10 10 10 8 11 13 15 17 13 14 12 10 10 10


10 10 10 12 13 14 12 16 12 15 10 9
9
9


14 14 14 15 12 33 34 36 32 12 14 11 11 11


13 13 13 12 14 29 40 41 33 13 12 13 13 13


15 15 15 11 10 30 42 45 31 15 12 10 10 10


10 10 10 9 13 31 30 32 33 12 13 11 11 11


12 12 12 8 12 14 12 13 12 14 11 13 13 13


11 11 11 13 11 12 9 16 17 11 13 14 14 14


10 10 10 9 15 11 12 20 16 12 11 8
8
8


10 10 10 9 15 11 12 20 16 22 11 8
8
8


10 10 10 9 15 11 12 20 16 22 11 8
8
8


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
0
0
0
0


0
0
9 10 12 11 8 15 14 12 11 7
0
0


0
0 10 8 11 13 15 17 13 14 12 10 0
0


0
0 10 12 13 14 12 16 12 15 10 9
0
0


0
0 14 15 12 33 34 36 32 12 14 11 0
0


0
0 13 12 14 29 40 41 33 13 12 13 0
0


0
0 15 11 10 30 42 45 31 15 12 10 0
0


0
0 10 9 13 31 30 32 33 12 13 11 0
0


0
0 12 8 12 14 12 13 12 14 11 13 0
0


0
0 11 13 11 12 9 16 17 11 13 14 0
0


0
0 10 9 15 11 12 20 16 12 11 8
0
0


20 20 20 20 20 20 20 20 20 20


20 20 20 20 20 20 20 20 20 20


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
0
0
0
0


20 20 20 20 20 20 20 20 20 20 20 20 20 20


20 20 20 20 20 20 20 20 20 20 20 20 20 20


20 20 9 10 12 11 8 15 14 12 11 7 20 20


20 20 10 8 11 13 15 17 13 14 12 10 20 20


20 20 10 12 13 14 12 16 12 15 10 9 20 20


20 20 14 15 12 33 34 36 32 12 14 11 20 20


20 20 13 12 14 29 40 41 33 13 12 13 20 20


20 20 15 11 10 30 42 45 31 15 12 10 20 20


20 20 10 9 13 31 30 32 33 12 13 11 20 20


20 20 12 8 12 14 12 13 12 14 11 13 20 20


20 20 11 13 11 12 9 16 17 11 13 14 20 20


20 20 10 9 15 11 12 20 16 12 11 8 20 20


20 20 20 20 20 20 20 20 20 20 20 20 20 20


20 20 20 20 20 20 20 20 20 20 20 20 20 20


a.
b.


c.
d.


In NI Vision, most image processing functions that use neighbors
automatically set pixel values in the image border using neighborhoods.
The grayscale filtering operations low pass, Nth order, and edge detection
use the mirroring method to set pixels in the image border. The binary
morphology, grayscale morphology, and segmentation functions copy the
pixel values along the border into the border region. The correlate, circles,
reject border, remove particles, skeleton, and label functions set the pixel
values in the border to zero.


Note
The border of an image is taken into account only for processing. The border is never
displayed or stored in a file.



## Image Masks


An image mask isolates parts of an image for processing. If a function has
an image mask parameter, the function process or analysis depends on both
the source image and the image mask.


An image mask is an 8-bit binary image that is the same size as or smaller
than the inspection image. Pixels in the image mask determine whether
corresponding pixels in the inspection image are processed. If a pixel in the
image mask has a nonzero value, the corresponding pixel in the inspection
image is processed. If a pixel in the image mask has a value of 0, the
corresponding pixel in the inspection image is not processed.



### When to Use


Use image masks when you want to focus your processing or inspection on
particular regions in the image.



### Concepts


Pixels in the source image are processed if corresponding pixels in the
image mask have values other than zero. Figure 1-4 shows how a mask
affects the output of the function that inverts the pixel values in an image.
Figure 1-4a shows the inspection image. Figure 1-4b shows the image
mask. Pixels in the mask with zero values are represented in black, and
pixels with nonzero values are represented in white. Figure 1-4c shows the
inverse of the inspection image using the image mask. Figure 1-4d shows
the inverse of the inspection image without the image mask.



#### Figure 1-4. The Effect of an Image Mask


You can limit the area in which your function applies an image mask to
the bounding rectangle of the region you want to process. This technique
saves memory by limiting the image mask to only the part of the image
containing significant information. To keep track of the location of this
region of interest (ROI) in regard to the original image, NI Vision sets an
offset. An offset defines the coordinate position in the original image where
you want to place the origin of the image mask.


Figure 1-5 illustrates the different methods of applying image masks.
Figure 1-5a shows the ROI in which you want to apply an image mask.
Figure 1-5b shows an image mask with the same size as the inspection
image. In this case, the offset is set to [0, 0]. A mask image also can be the
size of the bounding rectangle of the ROI, as shown in Figure 1-5c, where
the offset specifies the location of the mask image in the reference image.
You can define this offset to apply the mask image to different regions in
the inspection image.



#### Figure 1-5. Using an Offset to Limit an Image Mask


Figure 1-6 illustrates the use of a mask with two different offsets.
Figure 1-6a shows the inspection image, and Figure 1-6b shows the image
mask. Figure 1-6c and Figure 1-6d show the results of a function using the
image mask given the offsets of [0, 0] and [3, 1], respectively.


1
Region of Interest
2
Image Mask


a.
b.
c.
d.


a.
b.
c.


1


2


1
1


2



#### Figure 1-6. Effect of Applying a Mask with Different Offsets


For more information about ROIs, refer to the Regions of Interest section
of Chapter 2, Display.


a.


c.


b.


d.


Border pixels


Pixels not affected by the mask


Pixels affected by the mask
