# Glossary

> **Part**: `Back Matter` | **Pages**: `357 - 380`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---



## Numbers


1D
One-dimensional.


2D
Two-dimensional.


3D
Three-dimensional.


3D view
Displays the light intensity of an image in a 3D coordinate system, where
the spatial coordinates of the image form two dimensions and the light
intensity forms the third dimension.



## A


acceptance level
In OCR, a value that indicates how closely an object must match a trained
character to be recognized. A high acceptance level value indicates that the
object and trained character must be closely matched for the object to be
recognized.


AIPD
The National Instruments internal image file format used for saving
complex images and calibration information associated with an image.
AIPD images have the file extension APD.


alignment
The process by which a machine vision application determines the location,
orientation, and scale of a part being inspected.


alpha channel
A channel used to code extra information, such as gamma correction, about
a color image. The alpha channel is stored as the first byte in the four-byte
representation of an RGB pixel.


area
A rectangular portion of an acquisition window or frame that is controlled
and defined by software.


area threshold
(1) A rectangular portion of an acquisition window or frame that is
controlled and defined by software; (2) The size of an object in pixels or
user-defined units.


arithmetic operators
The image operations multiply, divide, add, subtract, and remainder.


array
An ordered, indexed set of data elements of the same type.


artifact
In OCR, an extraneous pixel in the ROI during training.


aspect ratio
In OCR, the height/width ratio of a character.


auto-median function
A function that uses dual combinations of opening and closing operations
to smooth the boundaries of objects.


Auto-Split
In OCR, works in conjunction with the maximum character bounding
rectangle width, and uses an algorithm to analyze the right side of a
character bounding rectangle. AutoSplit then determines the rightmost
vertical line in the object that contains the fewest number of pixels and
moves the rightmost edge of the character bounding rectangle to that
location.



## B


b
Bit. One binary digit, either 0 or 1.


B
Byte. Eight related bits of data, an 8-bit binary number. Also denotes the
amount of memory required to store one byte of data.


barycenter
The grayscale value representing the centroid of the range of an image’s
grayscale values in the image histogram.


binary image
An image in which the objects usually have a pixel intensity of 1 (or 255)
and the background has a pixel intensity of 0.


binary morphology
Functions that perform morphological operations on a binary image.


binary threshold
The separation of an image into objects of interest (assigned pixel values
of 1) and background (assigned pixel values of 0) based on the intensities
of the image pixels.


bit depth
The number of bits (n) used to encode the value of a pixel. For a given n,
a pixel can take 2n different values. For example, if n equals eight bits,
a pixel can take 256 different values ranging from 0 to 255. If n equals
16 bits, a pixel can take 65,536 different values ranging from 0 to 65,535
or  –32,768 to 32,767.


black reference level
The level that represents the darkest value an image can have. See also
white reference level.


blurring
Reduces the amount of detail in an image. Blurring can occur when the
camera lens is out of focus or when an object moves rapidly in the field of
view. You can blur an image intentionally by applying a lowpass frequency
filter.


BMP
Bitmap. An image file format commonly used for 8-bit and color images.
BMP images have the file extension BMP.


border function
Removes objects (or particles) in a binary image that touch the image
border.


brightness
(1) A constant added to the red, green, and blue components of a color pixel
during the color decoding process; (2) The perception by which white
objects are distinguished from gray and light objects from dark objects.


buffer
Temporary storage in memory for acquired data.



## C


caliper
A measurement function that finds edge pairs along a specified path in the
image. This function performs an edge extraction and then finds edge pairs
based on specified criteria such as the distance between the leading and
trailing edges, edge contrasts, and so forth.


cell
A single module that encodes one bit of data in a 2D barcode.


center of mass
The point on an object where all the mass of the object could be
concentrated without changing the first moment of the object about
any axis.


character
A recognized group of foreground elements.


character bounding
rectangle
In OCR, the smallest rectangle that completely encloses a character.


character class
In OCR, a group of characters that have been trained with the same
character value.


character recognition
The ability of a machine to read human-readable text.


character segmentation
In OCR, the application of several parameters, such as thresholding,
character size, and element spacing, that isolates a character in an ROI.


character set
In OCR, a set of trained characters and/or patterns.


character set file
In OCR, a file that contains a character set.


character size
In OCR, the number of pixels that make up a character.


character spacing
In OCR, the horizontal distance between the right edge of one character
bounding rectangle and the left edge of the next character bounding
rectangle.


character value
In OCR, a string that describes a character. For example, you might assign
the character value “A” to a group of elements that resembles the letter A.


chroma
The color information in a video signal.


chromaticity
The combination of hue and saturation. The relationship between
chromaticity and brightness characterizes a color.


chrominance
See chroma.


circle function
Detects circular objects in a binary image.


class
A category representing a collection of similar samples.


classification
An operation that assigns samples to classes based on predefined features.


classification accuracy
The probability that a sample is classified into the class to which it belongs.


classification confidence
The degree of certainty that a sample or character is assigned to one class
instead of other classes. See also class and sample.


classification predictive
value
The probability that a sample classified into a given class belongs to that
class.


classification score
See classification confidence.


classifier
A function or VI that assigns a sample to a class.


closing
A dilation followed by an erosion. A closing fills small holes in objects and
smooths the boundaries of objects.


clustering
A technique in which an image is sorted within a discrete number of classes
corresponding to the number of phases perceived in the image. The gray
values and a barycenter are determined for each class. This process is
repeated until a value is obtained that represents the center of mass for each
phase or class.


CLUT
Color lookup table. A table for converting the value of a pixel in an image
into a red, green, and blue (RGB) intensity.


code word
Character value of the printed bar/space pattern in a barcode or 2D
symbology.


color image
An image containing color information, usually encoded in the RGB form.


color space
The mathematical representation for a color. For example, color can be
described in terms of red, green, and blue; hue, saturation, and luminance;
or hue, saturation, and intensity.


complex image
Stores information obtained from the FFT of an image. The complex
numbers that compose the FFT plane are encoded in 64-bit floating-point
values: 32 bits for the real part and 32 bits for the imaginary part.


connectivity
Defines which of the surrounding pixels of a given pixel constitute its
neighborhood.


Only pixels adjacent in the horizontal and vertical directions are considered
neighbors.


All adjacent pixels are considered neighbors.


contrast
A constant multiplication factor applied to the luma and chroma
components of a color pixel in the color decoding process.


convex hull
The smallest convex polygon that can encapsulate a particle.


convex hull function
Computes the convex hull of objects in a binary image.


convolution
See linear filter.


convolution kernel
2D matrices, or templates, used to represent the filter in the filtering
process. The contents of these kernels are a discrete 2D representation of
the impulse response of the filter that they represent.


cross correlation
The most common way to perform pattern matching.


curve extraction
The process of finding curves, or connected edge points, in a grayscale
image. Curves usually represent the boundaries of objects in the image.



## D


Danielsson function
Similar to the distance functions, but with more accurate results.


dB
Decibel. A unit for expressing a logarithmic measure of the ratio of
two signal levels: dB = 20log10 V1/V2, for signals in volts.


default setting
A default parameter value recorded in the driver. In many cases, the default
input of a control is a certain value (often 0).


defect image
An image that shows all the defects found during golden template
comparison.


definition
The number of values a pixel can take on, equivalent to the number of
colors or shades that you can see in the image.


dendrite
The branches of the skeleton of an object.


densitometry
The determination of optical or photographic density.


density function
For each gray level in a linear histogram, the function gives the number of
pixels in the image that have the same gray level.


determinism
A characteristic of a system that describes how consistently it can respond
to external events or perform operations within a given time limit.


differentiation filter
Extracts the contours (edge detection) in gray level.


digital image
An image f (x, y) that has been converted into a discrete number of pixels.
Both spatial coordinates and brightness are specified.


dilation
Increases the size of an object along its boundary and removes tiny holes in
the object.


distance calibration
Determines the physical dimensions of a pixel by defining the physical
dimensions of a line in the image.


distance function
Assigns to each pixel in an object a gray-level value equal to its shortest
Euclidean distance from the border of the object.


distance metric
A metric that computes the distance between features in a classification
application.


distribution function
For each gray level in a linear histogram, the function gives the number of
pixels in the image that are less than or equal to that gray level.


dot-matrix character
In OCR, a character comprised of a series of small elements. See also
segmented character.


driver
Software that controls a specific hardware device, such as an image
acquisition device or DAQ device.


dynamic range
The ratio of the largest signal level a circuit can handle to the smallest
signal level it can handle (usually taken to be the noise level), normally
expressed in decibels.



## E


ECC
Error Checking and Correcting—Type of algorithm used for error
correction with Data Matrix codes.


edge
Defined by a sharp transition in the pixel intensities in an image or along an
array of pixels.


edge contrast
The difference between the average pixel intensity before the edge and the
average pixel intensity after the edge.


edge detection
Any of several techniques that identify the edges of objects in an image.


edge hysteresis
The difference in threshold level between a rising and a falling edge.


edge steepness
The number of pixels that corresponds to the slope or transition area of
an edge.


element
In OCR, a connected group of foreground pixels. Adjacent elements form
a character. See also object.


element spacing
In OCR, the amount of space, in pixels, between elements. See also
horizontal element spacing and vertical element spacing.


energy center
The center of mass of a grayscale image. See also center of mass.


entropy
A measure of the randomness in an image. An image with high entropy
contains more pixel value variation than an image with low entropy.


equalize function
See histogram equalization.


erasure
A missing or undecodable code word at a known position in a 2D barcode.


erosion
Reduces the size of an object along its boundary and eliminates isolated
points in the image.


Euclidean distance
The shortest distance between two points in a Cartesian system.


exponential and
gamma corrections
Expand the high gray-level information in an image while suppressing low
gray-level information.


exponential function
Decreases brightness and increases contrast in bright regions of an image,
and decreases contrast in dark regions of an image.



## F


feature
A measurement from or attribute of a sample.


feature extraction
An operation that computes features of a sample.


feature vector
A 1D array in which each element represents a different feature of a sample.


FFT
Fast Fourier Transform. A method used to compute the Fourier transform
of an image.


fiducial
A reference pattern on a part that helps a machine vision application find
the part location and orientation in an image. An alignment mark.


finder pattern
The perimeter of a Data Matrix barcode. The left and bottom sides of the
the finder pattern form a solid L shape. The right and bottom sides of the
finder pattern are made of alternating light and dark cells.


form
A window or area on the screen on which you place controls and indicators
to create the user interface for your program.


Fourier spectrum
The magnitude information of the Fourier transform of an image.


Fourier transform
Transforms an image from the spatial domain to the frequency domain.


frequency filters
The counterparts of spatial filters in the frequency domain. For images,
frequency information is in the form of spatial frequency.


function
A set of software instructions executed by a single line of code that may
have input and/or output parameters and returns a value when executed.



## G


gamma
The nonlinear change in the difference between the video signal’s
brightness level and the voltage level needed to produce that brightness.


gauging
Measurement of an object or distances between objects.


Gaussian filter
A filter similar to the smoothing filter, but using a Gaussian kernel in the
filter operation. The blurring in a Gaussian filter is more gentle than a
smoothing filter.


geometric features
Information extracted from a grayscale template that are used to locate the
template in the target image. Geometric features in an image range from
low-level features such as edges or curves detected in the image to
higher-level features such as the geometric shapes made by the curves in the
image.


geometric matching
A technique used to locate quickly a grayscale template that is
characterized by distinct geometric or shape information within a grayscale
image.


golden template
An image containing an ideal representation of an object under inspection.


gradient convolution
filter
See gradient filter.


gradient filter
An edge detection algorithm that extracts the contours in gray-level values.
Gradient filters include the Prewitt and Sobel filters.


gray level
The brightness of a pixel in an image.


gray-level dilation
Increases the brightness of pixels in an image that are surrounded by other
pixels with a higher intensity.


gray-level erosion
Reduces the brightness of pixels in an image that are surrounded by other
pixels with a lower intensity.


grayscale image
An image with monochrome information.


grayscale morphology
Functions that perform morphological operations on a gray-level image.



## H


h
Hour.


highpass attenuation
The inverse of lowpass attenuation.


highpass FFT filter
Removes or attenuates low frequencies present in the FFT domain of an
image.


highpass filter
Emphasizes the intensity variations in an image, detects edges or object
boundaries, and enhances fine details in an image.


highpass frequency
filter
Removes or attenuates low frequencies present in the frequency domain of
the image. A highpass frequency filter suppresses information related to
slow variations of light intensities in the spatial image.


highpass truncation
The inverse of lowpass truncation.


histogram
Indicates the quantitative distribution of the pixels of an image per
gray-level value.


histogram equalization
Transforms the gray-level values of the pixels of an image to occupy the
entire range (0 to 255 in an 8-bit image) of the histogram, increasing the
contrast of the image.


histogram inversion
Finds the photometric negative of an image. The histogram of a reversed
image is equal to the original histogram flipped horizontally around the
center of the histogram.


histograph
In LabVIEW, a histogram that can be wired directly into a graph.


hit-miss function
Locates objects in the image similar to the pattern defined in the structuring
element.


hole filling function
Fills all holes in objects that are present in a binary image.


horizontal element
spacing
In OCR, the space, in pixels, between horizontally adjacent elements.


HSI
A color encoding scheme in hue, saturation, and intensity.


HSL
A color encoding scheme using hue, saturation, and luminance information
where each image in the pixel is encoded using 32 bits: 8 bits for hue, 8 bits
for saturation, 8 bits for luminance, and 8 unused bits.


HSV
A color encoding scheme in hue, saturation, and value.


hue
Represents the dominant color of a pixel. The hue function is a continuous
function that covers all the possible colors generated using the R, G, and
B primaries. See also RGB.



## I


I/O
Input/output. The transfer of data to/from a computer system involving
communications channels, operator interface devices, and/or data
acquisition and control interfaces.


identification
confidence
The degree of similarity between a sample and members of the class to
which the sample is assigned. See also class and sample.


image
A 2D light intensity function f (x, y) where x and y denote spatial
coordinates and the value f at any point (x, y) is proportional to the
brightness at that point.


image border
A user-defined region of pixels surrounding an image. Functions that
process pixels based on the value of the pixel neighbors require image
borders.


Image Browser
An image that contains thumbnails of images to analyze or process in a
vision application.


image buffer
A memory location used to store images.


image definition
See pixel depth.


image display
environment
A window or control that displays an image.


image enhancement
The process of improving the quality of an image that you acquire from a
sensor in terms of signal-to-noise ratio, image contrast, edge definition, and
so on.


image file
A file containing pixel data and additional information about the image.


image format
Defines how an image is stored in a file. Usually composed of a header
followed by the pixel data.


image mask
A binary image that isolates parts of a source image for further processing.
A pixel in the source image is processed if its corresponding mask pixel has
a nonzero value. A source pixel whose corresponding mask pixel has a
value of 0 is left unchanged.


image palette
The gradation of colors used to display an image on screen, usually defined
by a CLUT.


image processing
Encompasses various processes and analysis functions that you can apply
to an image.


image segmentation
The process of separating objects from the background and each other so
that each object can be identified and characterized.


image source
The original input image.


image understanding
A technique that interprets the content of the image at a symbolic level
rather than a pixel level.


image visualization
The presentation (display) of an image (image data) to the user.


imaging
Any process of acquiring and displaying images and analyzing image data.


IMAQ
Image Acquisition.


INL
Integral nonlinearity. A measure in LSB of the worst-case deviation from
the ideal A/D or D/A transfer characteristic of the analog I/O circuitry.


inner gradient
Finds the inner boundary of objects.


inspection
The process by which parts are tested for simple defects, such as missing
parts or cracks on part surfaces.


inspection function
Analyzes groups of pixels within an image and returns information about
the size, shape, position, and pixel connectivity. Typical applications
include testing the quality of parts, analyzing defects, locating objects,
and sorting objects.


instrument driver
A set of high-level software functions, such as NI-IMAQ, that control
specific plug-in computer boards. Instrument drivers are available in
several forms, ranging from a function callable in a programming language
to a VI in LabVIEW.


intensity
The sum of the red, green, and blue primary colors divided by
three—(Red + Green + Blue) / 3.


intensity calibration
Assigning user-defined quantities, such as optical densities or
concentrations, to the gray-level values in an image.


intensity profile
The gray-level distribution of the pixels along an ROI in an image.


intensity range
Defines the range of gray-level values in an object of an image.


intensity threshold
Characterizes an object based on the range of gray-level values in the
object. If the intensity range of the object falls within the user-specified
range, it is considered an object. Otherwise it is considered part of the
background.


interpolation
The technique used to find values in between known values when
resampling an image or an array of pixels.


invariant feature
A feature vector that is invariant to changes in the scale, rotation, and mirror
symmetry of samples.


IRE
A relative unit of measure (named for the Institute of Radio Engineers).
0 IRE corresponds to the blanking level of a video signal, 100 IRE to the
white level. Notice that for CCIR/PAL video, the black level is equal to the
blanking level or 0 IRE, while for RS-170/NTSC video, the black level is
at 7.5 IRE.


J


JPEG
Joint Photographic Experts Group. An image file format for storing 8-bit
and color images with lossy compression. JPEG images have the file
extension JPG.


JPEG 2000
An Image file format for storing 8-bit, 16-bit, or color images with either
lossy or lossless compression. JPEG2000 images have the file extension
JP2.


K


kernel
A structure that represents a pixel and its relationship to its neighbors.
The relationship is specified by the weighted coefficients of each neighbor.



## L


labeling
A morphology operation that identifies each object in a binary image and
assigns a unique pixel value to all the pixels in an object. This process is
useful for identifying the number of objects in the image and giving each
object a unique pixel intensity.


LabVIEW
Laboratory Virtual Instrument Engineering Workbench. A program
development environment application based on the programming language
G used commonly for test and measurement applications.


Laplacian filter
Extracts the contours of objects in the image by highlighting the variation
of light intensity surrounding a pixel.


line gauge
Measures the distance between selected edges with high-precision subpixel
accuracy along a line in an image. For example, this function can be used
to measure distances between points and edges. This function also can step
and repeat its measurements across the image.


line profile
Represents the gray-level distribution along a line of pixels in an image.


linear filter
A special algorithm that calculates the value of a pixel based on its own
pixel value as well as the pixel values of its neighbors. The sum of this
calculation is divided by the sum of the elements in the matrix to obtain
a new pixel value.


local threshold
A method of image segmentation that categorizes a pixel as part of a
particle or the background based on the intensity statistics of the particle’s
neighboring pixels.


logarithmic and inverse
gamma corrections
Expand low gray-level information in an image while compressing
information from the high gray-level ranges.


logarithmic function
Increases the brightness and contrast in dark regions of an image and
decreases the contrast in bright regions of the image.


logic operators
The image operations AND, NAND, OR, XOR, NOR, XNOR, difference,
mask, mean, max, and min.


lossless compression
Compression in which the decompressed image is identical to the original
image.


lossy compression
Compression in which the decompressed image is visually similar but not
identical to the original image.


lowpass attenuation
Applies a linear attenuation to the frequencies in an image, with no
attenuation at the lowest frequency and full attenuation at the highest
frequency.


lowpass FFT filter
Removes or attenuates high frequencies present in the FFT domain of an
image.


lowpass filter
Attenuates intensity variations in an image. You can use these filters to
smooth an image by eliminating fine details and blurring edges.


lowpass frequency
filter
Attenuates high frequencies present in the frequency domain of the image.
A lowpass frequency filter suppresses information related to fast variations
of light intensities in the spatial image.


lowpass truncation
Removes all frequency information above a certain frequency.


LSB
Least significant bit.


L-skeleton function
Uses an L-shaped structuring element in the skeleton function.


luma
The brightness information in the video picture. The luma signal amplitude
varies in proportion to the brightness of the video signal and corresponds
exactly to the monochrome picture.


luminance
See luma.


LUT
Lookup table. A table containing values used to transform the gray-level
values of an image. For each gray-level value in the image, the
corresponding new value is obtained from the lookup table.



## M


machine vision
An automated application that performs a set of visual inspection tasks.


mask FFT filter
Removes frequencies contained in a mask (range) specified by the user.


match score
A number ranging from 0 to 1,000 that indicates how closely an acquired
image matches the template image. A match score of 1,000 indicates a
perfect match. A match score of 0 indicates no match.


median filter
A lowpass filter that assigns to each pixel the median value of its neighbors.
This filter effectively removes isolated pixels without blurring the contours
of objects.


memory buffer
See buffer.


method
In Visual Basic, a set of software instructions executed by a single line of
code that may have input and/or output parameters and returns a value
when executed.


MMX
Multimedia Extensions. Intel chip-based technology that allows parallel
operations on integers, which results in accelerated processing of 8-bit
images.


morphological
transformations
Extract and alter the structure of objects in an image. You can use these
transformations for expanding (dilating) or reducing (eroding) objects,
filling holes, closing inclusions, or smoothing borders. They are used
primarily to delineate objects and prepare them for quantitative inspection
analysis.


MSB
Most significant bit.


M-skeleton function
Uses an M-shaped structuring element in the skeleton function.


multiple template
matching
The technique used to simultaneously locate multiple grayscale templates
within a grayscale image.



## N


neighbor
A pixel whose value affects the value of a nearby pixel when an image is
processed. The neighbors of a pixel are usually defined by a kernel or a
structuring element.


neighborhood
operations
Operations on a point in an image that take into consideration the values of
the pixels neighboring that point.


NI-IMAQ
The driver software for National Instruments image acquisition devices.


nonlinear filter
Replaces each pixel value with a nonlinear function of its surrounding
pixels.


nonlinear gradient filter
A highpass edge-extraction filter that favors vertical edges.


nonlinear Prewitt filter
A highpass, edge-extraction filter based on 2D gradient information.


nonlinear Sobel filter
A highpass, edge-extraction filter based on 2D gradient information. The
filter has a smoothing effect that reduces noise enhancements caused by
gradient operators.


Nth order filter
Filters an image using a nonlinear filter. This filter orders (or classifies) the
pixel values surrounding the pixel being processed. The pixel being
processed is set to the Nth pixel value, where N is the order of the filter.


number of planes
(in an image)
The number of arrays of pixels that compose the image. A gray-level or
pseudo-color image is composed of one plane. An RGB image is composed
of three planes: one for the red component, one for the blue component, and
one for the green component.



## O


object
In OCR, a group of elements that satisfy element spacing requirements.
An object is an unrecognized character. See also particle.


occlusion invariant
matching
A geometric matching technique in which the reference pattern can be
partially obscured in the target image.


OCR
Optical character recognition. The process of analyzing an image to detect
and recognize characters/text in the image.


OCR Session
The character set and parameter settings that define an instance of OCR.


OCV
Optical character verification. A machine vision application that inspects
the quality of printed characters.


offset
The coordinate position in an image where you want to place the origin of
another image. Setting an offset is useful when performing mask
operations.


opening
An erosion followed by a dilation. An opening removes small objects and
smooths boundaries of objects in the image.


operators
Allow masking, combination, and comparison of images. You can use
arithmetic and logic operators in NI Vision.


optical representation
Contains the low-frequency information at the center and the
high-frequency information at the corners of an FFT-transformed image.


outer gradient
Finds the outer boundary of objects.



## P


palette
The gradation of colors used to display an image on screen, usually defined
by a CLUT.


particle
A connected region or grouping of pixels in an image in which all pixels
have the same intensity level.


particle analysis
A series of processing operations and analysis functions that produce
information about the particles in an image.


particle classifier
Classifies particles. See also classifier and particle.


pattern
In OCR, a character for which the character value requires more than
one byte.


pattern matching
The technique used to quickly locate quickly a grayscale template within a
grayscale image.


picture aspect ratio
The ratio of the active pixel region to the active line region. For standard
video signals like RS-170 or CCIR, the full-size picture aspect ratio
normally is 4/3 (1.33).


picture element
An element of a digital image. Also called pixel.


pixel
Picture element. The smallest division that makes up the video scan line.
For display on a computer monitor, a pixel’s optimum dimension is square
(aspect ratio of 1:1, or the width equal to the height).


pixel aspect ratio
The ratio between the physical horizontal and vertical sizes of the region
covered by the pixel. An acquired pixel should optimally be square, thus the
optimal value is 1.0, but typically it falls between 0.95 and 1.05, depending
on camera quality.


pixel calibration
Directly calibrates the physical dimensions of a pixel in an image.


pixel depth
The number of bits used to represent the gray level of a pixel.


PNG
Portable Network Graphic. An image file format for storing 8-bit, 16-bit,
and color images with lossless compression. PNG images have the file
extension PNG.


power 1/Y function
Similar to a logarithmic function but with a weaker effect.


power Y function
See exponential function.


Prewitt filter
An edge detection algorithm that extracts the contours in gray-level values
using a 3 × 3 filter kernel.


probability function
Defines the probability that a pixel in an image has a certain gray-level
value.


proper-closing
A finite combination of successive closing and opening operations that you
can use to fill small holes and smooth the boundaries of objects.


proper-opening
A finite combination of successive opening and closing operations that you
can use to remove small particles and smooth the boundaries of objects.


property
Attribute that controls the appearance or behavior of an object. The
property can be a specific value or another object with its own properties
and methods. See also method.


pyramidal matching
A technique used to increase the speed of a pattern matching algorithm by
matching subsampled versions of the image and the reference pattern.


Q


quantitative analysis
Obtaining various measurements of objects in an image.


quiet zone
An area containing no data that is required to surround a 2D barcode. This
area is measured in cell widths.


R


read resolution
The level of character detail OCR uses to determine if an object matches a
trained character.


read strategy
The method by which you determine how stringently OCR analyzes objects
to determine if they match trained characters.


reading
In OCR, the process of segmenting each object in an image and comparing
it to trained characters to determine if there is a match. See also training and
verifying.


real time
A property of an event or system in which data is processed as it is acquired
instead of being accumulated and processed at a later time.


reference character
In OCR, the character in a character class that is designated as the best
representative of the character value for which all the characters in the class
were trained.


reflectance value
A value used to determine the symbol contrast of a Data Matrix barcode in
an image. The reflectance value of a pixel equals the pixel intensity divided
by the maximum possible value for the given image type. (For example,
255 is the maximum possible pixel value for an 8-bit image.)


region of interest
Region of interest. (1) An area of the image that is graphically selected
from a window displaying the image. This area can be used to focus further
processing. (2) A hardware-programmable rectangular portion of the
acquisition window. See also ROI.


relative accuracy
A measure in LSB of the accuracy of an ADC; it includes all nonlinearity
and quantization errors but does not include offset and gain errors of the
circuitry feeding the ADC.


resolution
The number of rows and columns of pixels. An image composed of m rows
and n columns has a resolution of m × n.


reverse function
Inverts the pixel values in an image, producing a photometric negative of
the image.


RGB
A color encoding scheme using red, green, and blue (RGB) color
information where each pixel in the color image is encoded using 32 bits:
8 bits for red, 8 bits for green, 8 bits for blue, and 8 bits for the alpha value
(unused).


RGB U64
A color encoding scheme using red, green, and blue (RGB) color
information where each pixel in the color image is encoded using
64 bits:16  bits for red, 16 bits for green, 16 bits for blue, and 16 bits for
the alpha value (unused).


Roberts filter
An edge detection algorithm that extracts the contours in gray level,
favoring diagonal edges.


ROI
See region of interest.


ROI tools
A collection of tools that enable you to select a region of interest from an
image. These tools let you select points, lines, annuli, polygons, rectangles,
rotated rectangles, ovals, and freehand open and closed contours.


rotational shift
The amount by which one image is rotated with respect to a reference
image. This rotation is computed with respect to the center of the image.


rotation-invariant
matching
A pattern matching technique in which the reference pattern can be located
at any orientation in the test image as well as rotated at any degree.



## S


s
Seconds.


sample
An object in an image that you want to classify.


saturation
The amount of white added to a pure color. Saturation relates to the richness
of a color. A saturation of zero corresponds to a pure color with no white
added. Pink is a red with low saturation.


scale-invariant
matching
A pattern matching technique in which the reference pattern can be any size
in the test image.


segmentation function
Fully partitions a labeled binary image into non-overlapping segments,
with each segment containing a unique particle.


segmented character
A character that OCR isolates according to specific parameters, such as
thresholding, character size, and so on.


separation function
Separates particles that touch each other by narrow isthmuses.


shape descriptor
A feature vector that describes the shape of a sample. See also feature
vector and particle analysis.


shape detection
Detects rectangles, lines, ellipses, and circles within images.


shape matching
Finds objects in an image whose shape matches the shape of the object
specified by a shape template. The matching process is invariant to rotation
and can be set to be invariant to the scale of the objects.


shift-invariant
matching
A pattern matching technique in which the reference pattern can be located
anywhere in the test image but cannot be rotated or scaled.


Sigma filter
A highpass filter that outlines edges.


skeleton function
Applies a succession of thinning operations to an object until its width
becomes one pixel.


skiz function
Obtains lines in an image that separate each object from the others and are
equidistant from the objects that they separate.


smoothing filter
Blurs an image by attenuating variations of light intensity in the
neighborhood of a pixel.


Sobel filter
An edge detection algorithm that extracts the contours in gray-level values
using a 3 × 3 filter kernel.


spatial calibration
Assigns physical dimensions to the area of a pixel in an image.


spatial filters
Alter the intensity of a pixel relative to variations in intensities of its
neighboring pixels. You can use these filters for edge detection, image
enhancement, noise reduction, smoothing, and so forth.


spatial resolution
The number of pixels in an image in terms of the number of rows and
columns in the image.


square function
See exponential function.


square root function
See logarithmic function.


standard representation
Contains the low-frequency information at the corners and high-frequency
information at the center of an FFT-transformed image.


stroke character
In OCR, a character that consists of continuous elements in which breaks
are caused only by imperfections in the image.


structuring element
A binary mask used in most morphological operations. A structuring
element is used to determine which neighboring pixels contribute in the
operation.


subpixel analysis
Finds the location of the edge coordinates in terms of fractions of a pixel.


substitution character
In OCR, a character that represents unrecognized characters. Typically,
the substitution character is a question mark (?).


substitution error
An erroneously decoded code word at an unknown position in a
2D barcode. See also code word.



## T


template
A color, shape, or pattern that you are trying to match in an image using the
color matching or pattern matching functions. A template can be a region
selected from an image or it can be an entire image.


thickening
Alters the shape of objects by adding parts to the object that match the
pattern specified in the structuring element.


thinning
Alters the shape of objects by eliminating parts of the object that match the
pattern specified in the structuring element.


threshold
A method of image segmentation that separates particles from the
background by assigning all pixels with intensities within a specified range
to the particle and the rest of the pixels to the background. In the resulting
binary image, particles are represented with a pixel intensity of 255 and the
background is set to 0.


threshold interval
Two parameters: the lower threshold gray-level value and the upper
threshold gray-level value.


TIFF
Tagged Image File Format. An image format commonly used for encoding
8-bit, 16-bit, and color images. TIFF images have the file extension TIF.


tools palette
A collection of tools that enable you to select regions of interest, zoom in
and out, and change the image palette.


training
In OCR, the process of teaching the software the characters and/or patterns
you want to detect during the reading procedure. See also reading and
verifying.


truth table
A table associated with a logic operator that describes the rules used for that
operation.



## V


V
Volts.


value
The grayscale intensity of a color pixel computed as the average of the
maximum and minimum red, green, and blue values of that pixel.


verifying
In OCR, the process of comparing an input character to a reference
character and returning a score that indicates how closely the input
character matches the reference character. See also reading and training.


vertical element
spacing
In OCR, the space, in pixels, between vertically adjacent elements.


VI
Virtual Instrument. (1) A combination of hardware and/or software
elements, typically used with a PC, that has the functionality of a classic
stand-alone instrument; (2) A LabVIEW software module (VI), which
consists of a front panel user interface and a block diagram program.


W


watershed transform
A method of image segmentation that partitions an image based on the
topographic surface of the image. The image is separated into
non-overlapping segments with each segment containing a unique particle.


white reference level
The level that defines what is white for a particular video system. See also
black reference level.


Z


zones
Areas in a displayed image that respond to user clicks. You can use these
zones to control events which can then be interpreted within LabVIEW.
