# Chapter 2: Display

> **Part**: `Part I: Vision Basics` | **Pages**: `32 - 42`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


2
Display


This chapter contains information about image display, palettes, regions of
interest, and nondestructive overlays.



## Image Display


Displaying images is an important component of a vision application
because it gives you the ability to visualize your data. Image processing
and image visualization are distinct and separate elements. Image
processing refers to the creation, acquisition, and analysis of images.
Image visualization refers to how image data is presented and how you
can interact with the visualized images. A typical imaging application
uses many images in memory that the application never displays.



### When to Use


Use display functions to visualize your image data, retrieve generated
events and the associated data from an image display environment, select
ROIs from an image interactively, and annotate the image with additional
information.



### Concepts


Depending on your application development environment, you can display
images in the following image display environments: an external window
(LabVIEW and LabWindows/CVI), the LabVIEW Image Display control
(LabVIEW 7.0 or later), and the CWIMAQViewer ActiveX control
(Visual Basic). Display functions display images, set attributes of the
image display environment, assign color palettes to image display
environments, close image display environments, and set up and use an
image browser in image display environments. Some ROI functions—a
subset of the display functions—interactively define ROIs in image display
environments. These ROI functions configure and display different
drawing tools, detect draw events, retrieve information about the region
drawn on the image display environment, and move and rotate ROIs.
Nondestructive overlays display important information on top of an image
without changing the values of the image pixels.



## Chapter 2 Display



### In-Depth Discussion


This section describes the display modes available in NI Vision and the
16-bit grayscale display mapping methods.



#### Display Modes


One of the key components of displaying images is the display mode that
the video adaptor operates. The display mode indicates how many bits
specify the color of a pixel on the display screen. Generally, the display
mode available from a video adaptor ranges from 8 bits to 32 bits per pixel,
depending the amount of video memory available on the video adaptor and
the screen resolution you choose.


If you have an 8-bit display mode, a pixel can be one of 256 different colors.
If you have a 16-bit display mode, a pixel can be one of 65,536 colors.
In 24-bit or 32-bit display mode, the color of a pixel on the screen is
encoded using 3 or 4 bytes, respectively. In these modes, information is
stored using 8 bits each for the red, green, and blue components of the pixel.
These modes offer the possibility to display about 16.7 million colors.


Understanding your display mode is important to understanding how
NI Vision displays the different image types on a screen. Image processing
functions often use grayscale images. Because display screen pixels are
made of red, green, and blue components, the pixels of a grayscale image
cannot be rendered directly.


In 24-bit or 32-bit display mode, the display adaptor uses 8 bits to encode
a grayscale value, offering 256 gray shades. This color resolution is
sufficient to display 8-bit grayscale images. However, higher bit depth
images, such as 16-bit grayscale images, are not accurately represented in
24-bit or 32-bit display mode. To display a 16-bit grayscale image, either
ignore the least significant bits or use a mapping function to convert
16 bits to 8 bits.



#### Mapping Methods for 16-Bit Image Display


The following techniques describe how NI Vision converts 16-bit images
to 8-bit images and displays them using mapping functions. Mapping
functions evenly distribute the dynamic range of the 16-bit image to an
8-bit image.


•
Full Dynamic—The minimum intensity value of the 16-bit image is
mapped to 0, and the maximum intensity value is mapped to 255.
All other values in the image are mapped between 0 and 255 using the
equation shown below. This mapping method is general purpose


because it insures the display of the complete dynamic range of the
image. Because the minimum and maximum pixel values in an image
are used to determine the full dynamic range of that image, the
presence of noisy or defective pixels (for non-Class A sensors) with
minimum or maximum values can affect the appearance of the
displayed image. NI Vision uses the following technique by default:


where
z is the 8-bit pixel value
x is the 16-bit value
y is the minimum intensity value
v is the maximum intensity value


•
90% Dynamic—The intensity corresponding to 5% of the cumulative
histogram is mapped to 0, the intensity corresponding to 95% of the
cumulated histogram is mapped to 255. Values in the 0 to 5% range are
mapped to 0, while values in the 95 to 100% range are mapped to 255.
This mapping method is more robust than the full dynamic method and
is not sensitive to small aberrations in the image. This method requires
the computation of the cumulative histogram or an estimate of the
histogram. Refer to Chapter 4, Image Analysis, for more information
on histograms.


•
Given Percent Range—This method is similar to the 90% Dynamic
method, except that the minimum and maximum percentages of the
cumulative histogram that the software maps to 8-bit are user defined.


•
Given Range—This technique is similar to the Full Dynamic method,
except that the minimum and maximum values to be mapped to
0 and 255 are user defined. You can use this method to enhance the
contrast of some regions of the image by finding the minimum and
maximum values of those regions and computing the histogram of
those regions. A histogram of this region shows the minimum and
maximum intensities of the pixels. Those values are used to stretch the
dynamic range of the entire image.


•
Downshifts—This technique is based on shifts of the pixel values. This
method applies a given number of right shifts to the 16-bit pixel value
and displays the least significant bit. This technique truncates some of
the lowest bits, which are not displayed. This method is very fast, but
it reduces the real dynamic of the sensor to 8-bit sensor capabilities.
It requires knowledge of the bit-depth of the imaging sensor that has
been used. For example, an image acquired with a 12-bit camera
should be visualized using four right shifts in order to display the


z
x
y
–
v
y
–
----------
255
×
=


eight most significant bits acquired with the camera. If you are using a
National Instruments image acquisition device, this technique is the
default used by Measurement & Automation Explorer (MAX).



## Palettes


At the time a grayscale image is displayed on the screen, NI Vision
converts the value of each pixel of the image into red, green, and blue
intensities for the corresponding pixel displayed on the screen. This process
uses a color table, called a palette, which associates a color to each possible
grayscale value of an image. NI Vision provides the capability to customize
the palette used to display an 8-bit grayscale image.


With palettes, you can produce different visual representations of an image
without altering the pixel data. Palettes can generate effects, such as
photonegative displays or color-coded displays. In the latter case, palettes
are useful for detailing particular image constituents in which the total
number of colors is limited.


Displaying images in different palettes helps emphasize regions with
particular intensities, identify smooth or abrupt gray-level variations, and
convey details that might be difficult to perceive in a grayscale image.
For example, the human eye is much more sensitive to small intensity
variations in a bright area than in a dark area. Using a color palette may help
you distinguish these slight changes.


A palette is a pre-defined or user-defined array of RGB values. It defines
for each possible gray-level value a corresponding color value to render the
pixel. The gray-level value of a pixel acts as an address that is indexed into
the table, returning three values corresponding to a red, green, and blue
(RGB) intensity. This set of RGB values defines a palette in which varying
amounts of red, green, and blue are mixed to produce a color representation
of the value range.


In the case of 8-bit grayscale images, pixels can take 28, or 256, values
ranging from 0 to 255. Color palettes are composed of 256 RGB elements.
A specific color is the result of applying a value between 0 and 255 for each
of the three color components: red, green, and blue. If the red, green, and
blue components have an identical value, the result is a gray level pixel
value.


A gray palette associates different shades of gray with each value so as to
produce a linear and continuous gradation of gray, from black to white.
You can set up the palette to assign the color black to the value 0 and white
to 255, or vice versa. Other palettes can reflect linear or nonlinear
gradations going from red to blue, light brown to dark brown, and so on.


NI Vision has five predefined color palettes. Each palette emphasizes
different shades of gray.


The following sections introduce the five predefined palettes available in
NI Vision. The graphs in each section represent the color tables used by
each palette. The horizontal axes of the graphs represent the input
gray-level range [0, 255], and the vertical axes represent the RGB
intensities assigned to a given gray-level value.



#### Gray Palette


This palette has a gradual gray-level variation from black to white.
Each value is assigned to an equal amount of red, green, and blue in order
to produce a gray-level.


Red


Green


Blue


0
255



#### Temperature Palette


This palette has a gradation from light brown to dark brown. 0 is black
and 255 is white.



#### Rainbow Palette


This palette has a gradation from blue to red with a prominent range
of greens in the middle value range. 0 is blue and 255 is red.


Red


Green


Blue


0
128
255


Red


Green


Blue


0
128
64
192
255



#### Gradient Palette


This palette has a gradation from red to white with a prominent range of
light blue in the upper value range. 0 is black and 255 is white.



#### Binary Palette


This palette has 17 cycles of 15 different colors. Table 2-1 illustrates these
colors, where g is the gray-level value.



#### Table 2-1. Gray-Level Values in the Binary Palette


g =
R
G
B
Resulting Color


1
255
0
0
Red


2
0
255
0
Green


3
0
0
255
Blue


4
255
255
0
Yellow


5
255
0
255
Purple


6
0
255
255
Aqua


7
255
127
0
Orange


8
255
0
127
Magenta


9
127
255
0
Bright green


10
127
0
255
Violet


11
0
127
255
Sky blue


12
0
255
127
Sea green


Red


Green


Blue


0
128
192
255


The values 0 and 255 are special cases. A value of 0 results in black, and a
value of 255 results in white.


This periodic palette is appropriate for the display of binary and labeled
images.



## Regions of Interest


A region of interest (ROI) is an area of an image in which you want to
perform your image analysis.


Use ROIs to focus your processing and analysis on part of an image. You
can define an ROI using standard contours, such as an oval or rectangle,
or freehand contours. You also can perform any of the following options:


•
Construct an ROI in an image display environment


•
Associate an ROI with an image display environment


•
Extract an ROI associated with an image display environment


•
Erase the current ROI from an image display environment


13
255
127
127
Rose


14
127
255
127
Spring green


15
127
127
255
Periwinkle


Table 2-1.  Gray-Level Values in the Binary Palette (Continued)


g =
R
G
B
Resulting Color


Red


Green


Blue


0
16


•
Transform an ROI into an image mask


•
Transform an image mask into an ROI


An ROI describes a region or multiple regions of an image in which you
want to focus your processing and analysis. These regions are defined by
specific contours. NI Vision supports the following contour types.



#### Table 2-2. Types of Contours an ROI May Contain


Icon
Contour Name


Point


Line


Rectangle


Oval


Polygon


Freehand Region


Annulus


Broken Line


Freehand Line


Rotated Rectangle


You can define an ROI interactively, programmatically, or with an image
mask. Define an ROI interactively by using the tools from the tools palette
to draw an ROI on a displayed image. For more information about defining
ROIs programmatically or with an image mask, refer to your NI Vision user
manual.



## Nondestructive Overlay


A nondestructive overlay enables you to annotate the display of an image
with useful information without actually modifying the image. You can
overlay text, lines, points, complex geometric shapes, and bitmaps on top
of your image without changing the underlying pixel values in your image;
only the display of the image is affected. Figure 2-1 shows how you can use
the overlay to depict the orientation of each particle in the image.



### Figure 2-1. Nondestructive Overlay


You can use nondestructive overlays for many purposes, such as the
following:


•
Highlighting the location in an image where objects have been
detected


•
Adding quantitative or qualitative information to the displayed
image—like the match score from a pattern matching function


•
Displaying ruler grids or alignment marks


Angle = 150˚


Angle = 47˚


Angle = 124˚


Angle = 90˚


Angle = 3˚


Angle = 76˚


Angle = 65˚


Overlays do not affect the results of any analysis or processing
functions—they affect only the display. The overlay is associated with
an image, so there are no special overlay data types. You need only to add
the overlay to your image. NI Vision clears the overlay anytime you change
the size or orientation of the image because the overlay ceases to have
meaning. You can save overlays with images using the PNG file format.
