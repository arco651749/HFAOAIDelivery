# Chapter 15: Color Inspection

> **Part**: `Part IV: Machine Vision` | **Pages**: `263 - 297`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


15
Color Inspection


This chapter contains information about color spaces, the color spectrum,
color matching, color location, and color pattern matching.



## Color Spaces


Color spaces allow you to represent a color. A color space is a subspace
within a 3D coordinate system where each color is represented by a point.
You can use color spaces to facilitate the description of colors between
persons, machines, or software programs.


Various industries and applications use a number of different color spaces.
Humans perceive color according to parameters such as brightness, hue,
and intensity, while computers perceive color as a combination of red,
green, and blue. The printing industry uses cyan, magenta, and yellow
to specify color. The following is a list of common color spaces.


•
RGB—Based on red, green, and blue. Used by computers to display
images.


•
HSL—Based on hue, saturation, and luminance. Used in image
processing applications.


•
CIE—Based on brightness, hue, and colorfulness. Defined by the
Commission Internationale de l’Eclairage (International Commission
on Illumination) as the different sensations of color that the human
brain perceives.


•
CMY—Based on cyan, magenta, and yellow. Used by the printing
industry.


•
YIQ—Separates the luminance information (Y) from the color
information (I and Q). Used for TV broadcasting.



### When to Use


You must define a color space every time you process color images. With
NI Vision, you specify the color space associated with an image when you
create the image. NI Vision supports the RGB and HSL color spaces.



## Chapter 15 Color Inspection


If you expect the lighting conditions to vary considerably during your color
machine vision application, use the HSL color space. The HSL color space
provides more accurate color information than the RGB space when
running color processing functions, such as color matching, color location,
and color pattern matching. NI Vision’s advanced algorithms for
color processing—which perform under various lighting and noise
conditions—process images in the HSL color space.


If you do not expect the lighting conditions to vary considerably during
your application, and you can easily define the colors you are looking for
using red, green, and blue, use the RGB space. Also, use the RGB space if
you want only to display color images, but not process them, in your
application. The RGB space reproduces an image as you would expect to
see it. NI Vision always displays color images in the RGB space. If you
create an image in the HSL space, NI Vision automatically converts the
image to the RGB space before displaying it.



### Concepts


Because color is the brain’s reaction to a specific visual stimulus, color is
best described by the different sensations of color that the human brain
perceives. The color-sensitive cells in the eye’s retina sample color using
three bands that correspond to red, green, and blue light. The signals from
these cells travel to the brain where they combine to produce different
sensations of colors. The Commission Internationale de l’Eclairage has
defined the following sensations:


•
Brightness—The sensation of an area exhibiting more or less light


•
Hue—The sensation of an area appearing similar to a combination of
red, green, and blue


•
Colorfulness—The sensation of an area appearing to exhibit more or
less of its hue


•
Lightness—The sensation of an area’s brightness relative to a
reference white in the scene


•
Chroma—The colorfulness of an area with respect to a reference white
in the scene


•
Saturation—The colorfulness of an area relative to its brightness


The trichromatic theory describes how three separate lights—red, green,
and blue—can be combined to match any visible color. This theory is based
on the three color sensors that the eye uses. Printing and photography use


the trichromatic theory as the basis for combining three different colored
dyes to reproduce colors in a scene. Similarly, computer color spaces use
three parameters to define a color.


Most color spaces are geared toward displaying images with hardware,
such as color monitors and printers, or toward applications that manipulate
color information, such as computer graphics and image processing. Color
CRT monitors, the majority of color-video cameras, and most computer
graphics systems use the RGB color space. The HSL space, combined with
RGB and YIQ, is frequently used in applications that manipulate color,
such as image processing. The color picture publishing industry uses the
CMY color space, also known as CMYK. The YIQ space is the standard
for color TV broadcast.



#### RGB Color Space


The RGB color space is the most commonly used color space. The human
eye receives color information in separate red, green, and blue components
through cones—the color receptors present in the human eye. These three
colors are known as additive primary colors. In an additive color system,
the human brain processes the three primary light sources and combines
them to compose a single color “image.” The three primary color
components can combine to reproduce most possible colors.


You can visualize the RGB space as a 3D cube with red, green, and blue at
the corners of each axis, as shown in Figure 15-1. Black is at the cube
origin, while white is at the opposite corner of the cube. Each side of the
cube has a value between 0 and 1. Along each axis of the RGB cube, the
colors range from no contribution of that component to a fully saturated
color. Any point, or color, within the cube is specified by three numbers: an
R, G, B triple. The diagonal line of the cube from black (0, 0, 0) to white
(1, 1, 1) represents all the grayscale values or where all of the red, green,
and blue components are equal. Different computer hardware and software
combinations use different color ranges. Common combinations are 0–255
and 0–65,535 for each component. To map color values within these ranges
to values in the RGB cube, divide the color values by the maximum value
that the range can take.



#### Figure 15-1. RGB Cube


The RGB color space lies within the perceptual space of humans. In other
words, the RGB cube represents fewer colors than we can see.


The RGB space simplifies the design of computer monitors, but it is not
ideal for all applications. In the RGB color space, the red, green, and blue
color components are all necessary to describe a color. Therefore, RGB
is not as intuitive as other color spaces. The HSL color space describes
color using only the hue component, which makes HSL the best choice for
many image processing applications, such as color matching.


R


Red


(1, 0, 0)


Yellow


Green
G
(0, 1, 1)


Cyan


White


Grayscale


Black


Magenta


Blue
(0, 0, 1)


B



#### HSL Color Space


The HSL color space was developed to put color in terms that are easy for
humans to quantify. Hue, saturation, and brightness are characteristics that
distinguish one color from another in the HSL space. Hue corresponds to
the dominant wavelength of the color. The hue component is a color, such
as orange, green, or violet. You can visualize the range of hues as a
rainbow. Saturation refers to the amount of white added to the hue and
represents the relative purity of a color. A color without any white is fully
saturated. The degree of saturation is inversely proportional to the amount
of white light added. Colors such as pink, composed of red and white, and
lavender composed of purple and white, are less saturated than red and
purple. Brightness embodies the chromatic notion of luminance, or the
amplitude or power of light. Chromaticity is the combination of hue
and saturation. The relationship between chromaticity and brightness
characterizes a color. Systems that manipulate hue use the HSL color
space.


The coordinate system for the HSL color space is cylindrical. Colors are
defined inside a hexcone, as shown in Figure 15-4. The hue value runs from
0 to 360º. The saturation ranges from 0 to 1, where 1 represents the purest
color without any white. Luminance also ranges from 0 to 1, where 0 is
black and 1 is white.


Overall, two principal factors—the de-coupling of the intensity component
from the color information and the close relationship between chromaticity
and human perception of color—make the HSL space ideal for developing
machine vision applications.



#### CIE XYZ Color Space


The CIE color space system classifies colors according to the human vision
system. This system specifies colors in CIE coordinates and is a standard
for comparing one color in the CIE coordinates with another.


Visible light is electromagnetic energy that occupies approximately the
400 nm to 700 nm wavelength part of the spectrum. Humans perceive these
wavelengths as the colors violet through indigo, blue, green, yellow,
orange, and red. Figure 15-2 shows the amounts of red, green, and blue
light needed by an average observer to match a color of constant luminance
for all values of dominant wavelengths in the visible spectrum. The
dominant wavelength is the wavelength of the color humans see when
viewing the light. The negative values between 438.1 nm and 546.1 nm
indicate that all visible colors cannot be specified by adding together the
three positive primaries R, G, and B in the RGB color space.



#### Figure 15-2. Visible Light


Wavelength, 1 (nm)


Tristimulus Values


–0.2
400
500
600
700


0.4


0.2


0


438.1 nm


546.1 nm


700.0 nm


bλ


gλ


rλ


rλ


λ


In 1931, the CIE developed a system of three primary colors (XYZ) in
which all visible colors can be represented using a weighted sum of only
positive values of X, Y, and Z. Figure 15-3 shows the functions used to
define the weights of the X, Y, and Z components.



#### Figure 15-3. CIE Color-Matching Function



#### CIE L*a*b* Color Space


CIE 1976 L*a*b*, one of the CIE-based color spaces, is a way to linearize
the perceptibility of color differences. The nonlinear relations for L*, a*,
and b* mimic the logarithmic response of the eye.



#### CMY Color Space


CMY is another set of familiar primary colors: cyan, magenta, and yellow.
CMY is a subtractive color space in which these primary colors are
subtracted from white light to produce the desired color. The CMY color
space is the basis of most color printing and photography processes. CMY
is the complement of the RGB color space because cyan, magenta, and
yellow are the complements of red, green, and blue.



#### YIQ Color Space


The YIQ space is the primary color space adopted by the National
Television System Committee (NTSC) for color TV broadcasting. It is a
linear transformation of the RGB cube for transmission efficiency and for
maintaining compatibility with monochrome television standards. The
Y component of the YIQ system provides all the video information that a
monochrome television set requires. The main advantage of the YIQ space
for image processing is that the luminance information (Y) is de-coupled
from the color information (I and Q). Because luminance is proportional to
the amount of light perceived by the eye, modifications to the grayscale
appearance of the image do not affect the color information.



## Color Spectrum


The color spectrum represents the 3D color information associated with an
image or a region of an image in a concise 1D form that can be used by
many of the NI Vision color processing functions. Use the color spectrum
for color matching, color location, and color pattern matching applications
with NI Vision.


The color spectrum is a 1D representation of the 3D color information in an
image. The spectrum represents all the color information associated with
that image or a region of the image in the HSL space. The information is
packaged in a form that can be used by the color processing functions in NI
Vision.



### Color Space Used to Generate the Spectrum


The color spectrum represents the color distribution of an image in the HSL
space, as shown in Figure 15-4. If the input image is in RGB format, the
image is first converted to HSL format and the color spectrum is computed
from the HSL space. Using HSL images directly—those acquired with an
NI PCI/PXI-1411 image acquisition device with an onboard RGB to HSL
conversion for color matching—improves the operation speed.



#### Figure 15-4. HSL Color Space


Colors represented in the HSL model space are easy for humans to quantify.
The luminance—or intensity—component in the HSL space is separated
from the color information. This feature leads to a more robust color
representation independent of light intensity variation. However, the
chromaticity—or hue and saturation—plane cannot be used to represent the
black and white colors that often comprise the background colors in many
machine vision applications. Refer to the In-Depth Discussion section for
more information about color spaces.


180˚


Green
120˚


Blue
240˚


60˚


300˚


Red
0˚


White


Saturation


Black


H


u


e


Luminance



### Generating the Color Spectrum


Each element in the color spectrum array corresponds to a bin of colors
in the HSL space. The last two elements of the array represent black and
white colors, respectively. Figure 15-5 illustrates how the HSL color space
is divided into bins. The hue space is divided into a number of equal
sectors, and each sector is further divided into two parts: one part
representing high saturation values and another part representing low
saturation values. Each of these parts corresponds to a color bin—an
element in the color spectrum array.



#### Figure 15-5. The HSL Space Divided into Bins and Sectors


The color sensitivity parameter determines the number of sectors the
hue space is divided into. Figure 15-5a shows the hue color space when
luminance is equal to 128. Figure 15-5b shows the hue space divided
into a number of sectors, depending on the desired color sensitivity.
Figure 15-5c shows each sector divided further into a high saturation
bin and a low saturation bin. The saturation threshold determines the
radius of the inner circle that separates each sector into bins.


Figure 15-6 illustrates the correspondence between the color spectrum
elements and the bins in the color space. The first element in the color
spectrum array represents the high saturation part in the first sector; the
second element represents the low saturation part; the third element
represents the high saturation part of the second sector and so on. If
there are n bins in the color space, the color spectrum array contains
n + 2 elements. The last two components in the color spectrum represent
the black and white color, respectively.


1
Sector
2
Saturation Threshold
3
Color Bins


a.
b.
c.


2


3


1



#### Figure 15-6. Hue Color Space and the Color Spectrum Array Relationship


A color spectrum with a larger number of bins, or elements, represents the
color information in an image with more detail, such as a higher color
resolution, than a spectrum with fewer bins. In NI Vision, you can choose
between three color sensitivity settings—low, medium, and high. Low
divides the hue color space into seven sectors, giving a total of
2 × 7 + 2 = 16 bins. Medium divides the hue color space into 14 sectors,
giving a total of 2 × 14 + 2 = 30 bins. High divides the hue color space
into 28 sectors, giving a total of 2 × 28 + 2 = 58 bins.


The value of each element in the color spectrum indicates the percentage
of image pixels in each color bin. When the number of bins is set according
to the color sensitivity parameter, the machine vision software scans the
image, counts the number of pixels that fall into each bin, and stores the
ratio of the count and total number of pixels in the image in the appropriate
element within the color spectrum array.


Black


White


Element #1


Element #2


Element #3


Element #(n+1)


Element #(n+2)


#4


#3


#1


#2
#(n-1)


#n


a.
b.


The software also applies a special adaptive learning algorithm to
determine if pixels are either black or white before assigning it to a
color bin. Figure 15-7b represents the low sensitivity color spectrum
of Figure 15-7a. The height of each bar corresponds to the percentage
of pixels in the image that fall into the corresponding bin.


The color spectrum contains useful information about the color distribution
in the image. You can analyze the color spectrum to get information such
as the most dominant color in the image, which is the element with the
highest value in the color spectrum. You also can use the array of the color
spectrum to directly analyze the color distribution and for color matching
applications.



#### Figure 15-7. Color Spectrum Associated with an Image



## Color Matching


Color matching quantifies which colors and how much of each color exist
in a region of an image and uses this information to check if another image
contains the same colors in the same ratio.


Use color matching to compare the color content of an image or regions
within an image to a reference color information. With color matching,
you create an image or select regions in an image that contain the color
information you want to use as a reference. The color information in the
image may consist of one or more colors. The machine vision software
then learns the 3D color information in the image and represents this
information as a 1D color spectrum. Your machine vision application
compares the color information in the entire image or regions in the image
to the learned color spectrum, calculating a score for each region. The score
relates how closely the color information in the image region matches the
information represented by the color spectrum.


a.
b.


Color matching can be used for applications such as color identification,
color inspection, color object location and other applications that require
the comparison of color information to make decisions.



#### Color Identification


Color identification identifies an object by comparing the color information
in the image of the object to a database of reference colors that correspond
to pre-defined object types. The object is assigned a label corresponding to
the object type with closest reference color in the database. Use color
matching to first learn the color information of all the pre-defined object
types. The color spectrums associated with each of the pre-defined object
types become the reference colors. Your machine vision application then
uses color matching to compare the color information in the image of the
object to the reference color spectrums. The object receives the label of the
color spectrum with the highest match score.


Figure 15-8 shows an example of a tile identification application.
Figure 15-8a shows the image of a tile that needs to be identified.
Figure 15-8b shows the scores obtained using color matching with a set of
the reference tiles.



#### Figure 15-8. Color Matching


Use color matching to verify the presence of correct components in
automotive assemblies. An example of a color identification task is to
ensure that the color of the fabric in the interior of a car adheres to
specifications.



#### Color Inspection


Color inspection detects simple flaws such as missing or misplaced color
components, defects on the surfaces of color objects, or printing errors on
color labels. You can use color matching for these applications if known
regions of interest predefine the object or areas to be inspected in the image.
You can define these regions, or they can be the output of some other
machine vision tool, such as pattern matching.


The layout of the fuses in junction boxes in automotive assemblies is easily
defined by regions of interest. Color matching determines if all of the fuses
are present and in the correct locations. Figure 15-9 shows an example of a
fuse box inspection application in which the exact location of the fuses in


1
Score = 592
2
Score = 6


3
Score = 31
4
Score = 338


5
Score = 1000
6
Score = 405


a.
b.


1
2
3


4
5
6


the image can be specified by regions of interest. Color matching compares
the color of the fuse in each region to the color that is expected to be in that
region.



#### Figure 15-9. Fuse Box Inspection Using Color Matching


Color matching can be used to inspect printed circuit boards containing a
variety of components including diodes, resistors, integrated circuits, and
capacitors. In a manufacturing environment, color matching can find flaws
in a manufactured product when the flaws are accompanied by a color
change.


Color matching is performed in two steps. In the first step, the machine
vision software learns a reference color distribution. In the second step,
the software compares color information from other images to the
reference image and returns a score as an indicator of similarity.


1
Score = 51
2
Score = 382
3
Score = 23


4
Score = 649
5
Score = 29
6
Score = 70


7
Score = 1000
8
Score = 667
9
Score = 990


10 Score = 8
11 Inspection Regions


a.
b.


6
7
8
9


1
2
3
4
5


10


11



#### Learning Color Distribution


The machine vision software learns a color distribution by generating a
color spectrum. You provide the software with an image or regions in the
image containing the color information that you want to use as a reference
in your application. The machine vision software then generates a color
spectrum based on the information you provide. The color spectrum
becomes the basis of comparison during the matching phase.



#### Comparing Color Distributions


During the matching phase, the color spectrum obtained from the target
image or region in the target image is compared to the reference color
spectrum taken during the learning step. A match score is computed based
on the similarity between these two color spectrums using the Manhattan
distance between two vectors. A fuzzy membership weighting function is
applied to both the color spectrums before computing the distance between
them. The weighting function compensates for some errors that may occur
during the binning process in the color space. The fuzzy color comparison
approach provides a robust and accurate quantitative match score. The
match score, ranging from 0 to 1000, defines the similarity between the
color spectrums. A score of zero represents no similarity between the color
spectrums, whereas a score of 1000 represents a perfect match.
Figure 15-10 illustrates the comparison process.



#### Figure 15-10. Comparing Two Spectrums for Similarity


Image or
Inspection
Area


Template
Color
Spectrum


Match Score
(0–1000)
Absolute
Difference


Fuzzy Weighting
Function


Fuzzy Weighting
Function
Color
Spectrum



## Color Location


Use color location to quickly locate known color regions in an image. With
color location, you create a model or template that represents the colors that
you are searching. Your machine vision application then searches for the
model in each acquired image, and calculates a score for each match. The
score indicates how closely the color information in the model matches the
color information in the found regions.


Color can simplify a monochrome visual inspection problem by improving
contrast or separating the object from the background. Color location
algorithms provide a quick way to locate regions in an image with specific
colors.


Use color location when your application has the following characteristics:


•
Requires the location and the number of regions in an image with their
specific color information


•
Relies on the cumulative color information in the region, instead of
how the colors are arranged in the region


•
Does not require the orientation of the region


•
Does not require the location with subpixel accuracy


The color location tools in NI Vision measure the similarity between an
idealized representation of a feature, called a model, and a feature that may
be present in an image. A feature for color location is defined as a region in
an image with specific colors.


Color location is useful in many applications. Color location provides your
application with information about the number of instances and locations
of the template within an image. Use color location in the following general
applications—inspection, identification, and sorting.



#### Inspection


Inspection detects flaws such as missing components, incorrect printing,
and incorrect fibers on textiles. A common pharmaceutical inspection
application is inspecting a blister pack for the correct pills. Blister pack
inspection involves checking that all the pills are of the correct type, which
is easily performed by checking that all the pills have the same color
information. Because your task is to determine if there are a fixed number
of the correct pills in the pack, color location is a very effective tool.


Figure 15-11a shows the template image of the part of the pill that contains
the color information that you want to locate. Figure 15-11b shows the pills
located in a good blister pack. Figure 15-11c shows the pills located when
a blister pack contains the wrong type of pills or missing pills. Because the
exact locations of the pills is not necessary for the inspection, the number
of matches returned by color location indicates whether a blister pack
passes inspection.



#### Figure 15-11. Blister Pack Inspection Using Color Matching



#### Identification


Identification assigns a label to an object based on its features. In many
applications, the color-coded identification marks are placed on the objects.
In these applications, color matching locates the color code and identifies
the object. In a spring identification application, different types of
springs are identified by a collection of color marks painted on the coil.
If you know the different types of color patches that are used to mark the
springs, color location can find which color marks appear in the image.
You then can use this information to identify the type of spring.


Sorting


Sorting separates objects based on attributes such as color, size, and shape.
In many applications, especially in the pharmaceutical and plastic
industries, objects are sorted according to color, such as pills and plastic
pellets. Figure 15-12 shows an example of how to sort different colored
candies. Using color templates of the different candies in the image,
color location quickly locates the positions of the different candies.


a.
b.
c.



#### Figure 15-12. Sorting Candy by Color Information



### What to Expect from a Color Location Tool


In automated machine vision applications, the visual appearance of
inspected materials or components changes because of factors such as
orientation of the part, scale changes, and lighting changes. The color
location tool maintains its ability to locate the reference patterns despite
these changes. The color location tool provides accurate results during the
following common situations: pattern orientation and multiple instances,
ambient lighting conditions, and blur and noise conditions.


a.
b.


c.
d.



#### Pattern Orientation and Multiple Instances


A color location tool locates the reference pattern in an image even if the
pattern in the image is rotated or scaled. When a pattern is rotated or
slightly scaled in the image, the color location tool can detect the following:


•
The pattern in the image


•
The position of the pattern in the image


•
Multiple instances of the pattern in the image, if applicable


Because color location only works on the color information of a region and
does not use any kind of shape information from the template, it does not
find the angle of the rotation of the match. It only locates the position of a
region in the image whose size matches a template containing similar color
information.


Refer to Figure 15-11 for an example of pattern orientation and multiple
instances. Figure 15-11a shows a template image. Figures 15-11b
and 15-11c show multiple shifted and rotated occurrences of the template.



#### Ambient Lighting Conditions


The color location tool finds the reference pattern in an image under
conditions of uniform changes in the lighting across the image. Color
location also finds patterns under conditions of non-uniform light changes,
such as shadows.


Figure 15-13 shows typical conditions under which the color location tool
works correctly. Figure 15-13a shows the original template image.
Figure 15-13b shows the same pattern under bright light. Figure 15-13c
shows the pattern under poor lighting.



#### Figure 15-13. Examples of Lighting Conditions



#### Blur and Noise Conditions


Color location finds patterns that have undergone some transformation
because of blurring or noise. Blurring usually occurs because of incorrect
focus or depth of field changes.


Color location is built upon the color matching functions to quickly locate
regions with specific color information in an image. Refer to the Color
Matching section for more information.


The color location functions extend the capabilities of color matching to
applications in which the location of the objects in the image is unknown.
Color location uses the color information in a template image to look for
occurrences of the template in the search image. The basic operation moves
the template across the image pixel by pixel and comparing the color
information at the current location in the image to the color information in
the template using the color matching algorithm.


The color location process consists of two main steps—learning template
information and searching for the template in an image. Figure 15-14
illustrates the general flow of the color location process. During the
learning phase, the software extracts the color spectrum from the template
image. This color spectrum is used to compare the color information of the
template with the color information in the image.


a.
b.
c.


During the search step, a region the size of the template is moved across the
image pixel by pixel from the top of the image to the bottom. At each pixel,
the function computes the color spectrum of the region under consideration.
This color spectrum is then compared with the template’s color spectrum to
compute a match score.


The search step is divided into two phases. First, the software performs a
coarse-to-fine search phase that identifies all possible locations, even those
with very low match scores. The objective of this phase is to quickly find
possible locations in the image that may be potential matches to the
template information. Because stepping through the image pixel by pixel
and computing match scores is time consuming, the following techniques
are used to speed up the search process.


•
Subsampling—When stepping through the image, the color
information is taken from only a few sample points in the image to use
for comparison with the template. This reduces the amount of data
used to compute the color spectrum in the image, which speeds up the
search process.


•
Step size—Instead of moving the template across the image pixel by
pixel, the search process skips a few pixels between the each color
comparison, thus speeding up the search process. The step size
indicates the number of pixels to skip. For color location, the initial
step size can be as large as half the size of the template.


The initial search phase generates a list of possible match locations in the
image. In the second step, that list is searched for the location of the best
match using a hill-climbing algorithm.



#### Figure 15-14. Overview of the Color Location Process



## Color Pattern Matching


Use color pattern matching to quickly locate known reference patterns, or
fiducials, in a color image. With color pattern matching, you create a model
or template that represents the object you are searching for. Then your
machine vision application searches for the model in each acquired image,
calculating a score for each match. The score indicates how closely the
model matches the color pattern found. Use color pattern matching to
locate reference patterns that are fully described by the color and spatial
information in the pattern.


Grayscale, or monochrome, pattern matching is a well-established tool for
alignment, gauging, and inspection applications. Refer to Chapter 12,
Pattern Matching, for more information about pattern matching. In all of
these application areas, color simplifies a monochrome problem by


Template


Image


Refine each match location
using a hill climbing process
and update scores.


Initial Match List


Template Descriptor


Learning Phase


Matching Phase


Learn color information
in the template.


Uses a coarse to fine
search strategy to find
a list of possible
matches with scores.


improving contrast or separation of the object from the background. Color
pattern matching algorithms provide a quick way to locate objects when
color is present.


Use color pattern matching when the object under inspection has the
following qualities:


•
The object contains color information that is very different from the
background, and you want to find the location of the object in the
image very precisely. For these applications, color pattern matching
provides a more accurate solution than color location—because color
location does not use shape information during the search phase,
finding the locations of the matches with pixel accuracy is difficult.


•
The object has grayscale properties that are difficult to characterize or
that are very similar to other objects in the search image. In such cases,
grayscale pattern matching may not give accurate results. If the object
has some color information that differentiates it from the other objects
in the scene, color provides the machine vision software with the
additional information to locate the object.


Figure 15-15 illustrates the advantage of using color pattern matching over
color location to locate the resistors in an image. Although color location
finds the resistors in the image, the matches are not very accurate because
they are limited to color information. Color pattern matching uses color
matching first to locate the objects, and then pattern matching to refine the
locations, providing more accurate results.



#### Figure 15-15. Comparison between Color Location and Color Pattern Matching


Figure 15-16 shows the advantage of using color information when
locating color-coded fuses on a fuse box. Figure 15-16a shows a grayscale
image of the fuse box. In the image of the fuse box in Figure 15-16a, the


a.
b.
c.


grayscale pattern matching tool has difficulty clearly differentiating
between fuse 20 and fuse 25 and will return close match scores because of
similar grayscale intensities and the translucent nature of the fuses. In the
color image, Figure 15-16b, the addition of color helps to improve the
accuracy and reliability of the pattern matching tool.



#### Figure 15-16. Benefit of Adding Color to Fuse Box Inspection


The color pattern matching tools in NI Vision measure the similarity
between an idealized representation of a feature, called a model, and the
feature that may be present in an image. A feature is defined as a specific
pattern of color pixels in an image.


Color pattern matching is the key to many applications. Color pattern
matching provides your application with information about the number of
instances and location of the template within an image. Use color pattern
matching in the following three general applications: gauging, inspection,
and alignment.


Gauging


Many gauging applications locate and then measure or gauge the distance
between objects. Searching and finding a feature is the key processing
task that determines the success of many gauging applications. If the
components you want to gauge are uniquely identified by their color,
color pattern matching provides a fast way to locate the components.


Inspection detects simple flaws, such as missing parts or unreadable
printing. A common application is inspecting the labels on consumer
product bottles for printing defects. Because most of the labels are in color,
color pattern matching is used to locate the labels in the image before a


a.
b.


detailed inspection of the label is performed. The score returned by the
color pattern matching tool can also be used to decide whether a label is
acceptable.


Alignment


Alignment determines the position and orientation of a known object by
locating fiducials. Use the fiducials as points of reference on the object.
Grayscale pattern matching is sufficient for most applications, but some
alignment applications require color pattern matching for more reliable
results.



### What to Expect from a Color Pattern Matching Tool


In automated machine vision applications, the visual appearance of
materials or components under inspection can change due to factors such
as orientation of the part, scale changes, and lighting changes. The color
pattern matching tool maintains its ability to locate the reference patterns
and gives accurate results despite these changes.


A color pattern matching tool locates the reference pattern in an image even
when the pattern in the image is rotated and slightly scaled. When a pattern
is rotated or scaled in the image, the color pattern matching tool detects the
following features of an image:


•
The pattern in the image


•
The position of the pattern in the image


•
The orientation of the pattern


•
Multiple instances of the pattern in the image, if applicable


Figure 15-17a shows a template image, or pattern. Figures 15-17b
and 15-17c illustrate multiple occurrences of the template. Figure 15-17b
shows the template shifted in the image. Figure 15-17c shows the template
rotated in the image.



#### Figure 15-17. Pattern Orientation


The color pattern matching tool finds the reference pattern in an image
under conditions of uniform changes in the lighting across the image.
Because color analysis is more robust when dealing with variations in
lighting than grayscale processing, color pattern matching performs better
under conditions of non-uniform light changes, such as in the presence of
shadows, than grayscale pattern matching.


Figure 15-18a shows the original template image. Figure 15-18b shows the
same pattern under bright light. Figure 15-18c shows the pattern under poor
lighting.



#### Figure 15-18. Examples of Lighting Conditions


a.
b.
c.


a.
b.
c.


Color pattern matching finds patterns that have undergone some
transformation because of blurring or noise. Blurring usually occurs
because of incorrect focus or depth of field changes.


Color pattern matching is a unique approach that combines color and
spatial information to quickly find color patterns in an image. It uses the
technologies behind color matching and grayscale pattern matching in a
synergistic way to locate color patterns in color images.



#### Color Matching and Color Location


Color matching compares the color content of an image or regions in an
image to existing color information. The color information in the image
may consist of one or more colors. To use color matching, define regions
in an image that contain the color information you want to use as a
reference. The machine vision functions then learn the 3D color
information in the image and represents it as a 1D color spectrum. Your
machine vision application compares the color information in the entire
image or regions in the image to the learned color spectrum, calculating a
score for each region. This score relates how closely the color information
in the image region matches the information represented by the color
spectrum. To use color matching, you need to know the location of the
objects in the image before performing the match.


Color location functions extend the capabilities of color matching to
applications where you do not know the location of the objects in the image.
Color location uses the color information from a template image to look for
occurrences of the template in the search image. The basic operation moves
the template across the image pixel by pixel and compares the color
information at the current location in the image to the color information
in the template, using the color matching algorithm. Because searching an
entire image for color matches is time consuming, the color location
software uses some techniques to speed up the location process. A
coarse-to-fine search strategy finds the rough locations of the matches in
the image. A more refined search, using a hill climbing algorithm, is then
performed around each match to get the accurate location of the match.
Color location is an efficient way to look for occurrences of regions in an
image with specific color attributes.


Refer to the Color Matching and Color Location sections for more
information.



#### Grayscale Pattern Matching


NI Vision grayscale pattern matching methods incorporate image
understanding techniques to interpret the template information and use that
information to find the template in the image. Image understanding refers
to image processing techniques that generate information about the features
of a template image. These methods include the following:


•
Geometric modeling of images


•
Efficient non-uniform sampling of images


•
Extraction of rotation-independent template information


NI Vision uses a combination of the edge information in the image and an
intelligent image sampling technique to match patterns. The image edge
content provides information about the structure of the image in a compact
form. The intelligent sampling technique extracts points from the template
that represent the overall content of the image. The edge information and
the smart sampling method reduce the inherently redundant information in
an image and improve the speed and accuracy of the pattern matching tool.
In cases where the pattern can be rotated in the image, a similar technique
is used, but with specially chosen template pixels whose values, or relative
change in values, reflect the rotation of the pattern. The result is fast and
accurate grayscale pattern matching.


NI Vision pattern matching accurately locates objects in conditions where
they vary in size (±5%) and orientation (between 0° and 360°) and when
their appearance is degraded.


Refer to Chapter 12, Pattern Matching, for more information on grayscale
pattern matching.



#### Combining Color Location and Grayscale Pattern Matching


Color pattern matching uses a combination of color location and grayscale
pattern matching to search for the template. When you use color pattern
matching to search for a template, the software uses the color information
in the template to look for occurrences of the template in the image. The
software then applies grayscale pattern matching in a region around each of
these occurrences to find the exact position of the template in the image.
Figure 15-19 illustrates the general flow of the color pattern matching
algorithm. The size of the searchable region is determined by the software,
based on the inputs you provide, such as search strategy and color
sensitivity.



#### Figure 15-19. Overview of the Color Pattern Matching Process



### In-Depth Discussion


There are standard ways to convert RGB to grayscale and to convert one
color space to another. The transformation from RGB to grayscale is linear.
However, some transformations from one color space to another are
nonlinear because some color spaces represent colors that cannot be
represented in other spaces.


Template


Image


Match locations
based on color


Template Descriptor


Learning Phase


Matching Phase


Learn color information
and information for
grayscale pattern
matching.


Use the first part of the
color location algorithm
to find instances of the
template in the image.


Search a region around
each color match using
grayscale pattern matching
to obtain final locations.


Score each match according to
color and grayscale information.



#### RGB to Grayscale


The following equations convert an RGB image into a grayscale image on
a pixel-by-pixel basis.


grayscale value = 0.299R + 0.587G + 0.114B


This equation is part of the NTSC standard for luminance. An alternative
conversion from RGB to grayscale is a simple average:


grayscale value = (R + G + B) / 3



#### RGB and HSL


There is no matrix operation that allows you to convert from the RGB
color space to the HSL color space. The following equations describe the
nonlinear transformation that maps the RGB color space to the HSL color
space.


V2 =
(G – B)
V1 = 2R – G – B
L = 0.299R + 0.587G + 0.114B
H = 256tan–1 (V2 / V1) / (2π)
S = 255(1 – 3min(R, G, B) / (R + G + B))


The following equations map the HSL color space to the RGB color space.


3


h
H 2π
256
--------
=


s
S 255
⁄
=


s'
1
s
–
(
) 3
⁄
=


f h
( )
1
s
h
( )
cos
⋅
–
π 3
⁄
h
–
(
)
cos
⁄
(
) 3
⁄
=


b
s'
=


r
f h
( )
=


g
1
r
–
b
–
=







0
h
2π 3
⁄
≤
<
[
]


h'
h
2π 3
⁄
–
=


r
s'
=


g
f h'
(
)
=


b
1
r
–
g
–
=









2π 3
⁄
h
4π 3
⁄
≤
<
[
]



#### RGB and CIE XYZ


The following 3 × 3 matrix converts RGB to CIE XYZ.


By projecting the tristimulus values on to the unit plane X + Y + Z = 1,
color can be expressed in a 2D plane. The chromaticity coordinates are
defined as follows:


x = X / (X + Y + Z)


y = Y / (X + Y + Z)


z = Z / (X + Y + Z)


You can obtain z from x and y by z = 1 – x + y. Hence, chromaticity
coordinates are usually given as (x, y) only. The chromaticity values depend
on the hue or dominant wavelength and the saturation. Chromaticity values
are independent of luminance.


h'
h
4π 3
⁄
–
=


g
s'
=


b
f h'
(
)
=


r
1
g
–
b
–
=









4π 3
⁄
h
2π
≤
<
[
]


l
0.299r
0.587g
0.114b
+
+
=


l'
L l⁄
=


R
rl'
=


G
gl'
=


B
bl'
=


X
Y
Z


0.412453 0.357580 0.180423
0.212671 0.715160 0.072169
0.019334 0.119193 0.950227


R
G
B


=


The diagram from (x, y) is referred to as the CIE 1931 chromaticity
diagram, or the CIE (x, y) chromaticity diagram, as illustrated in the
bell curve of Figure 15-20.



#### Figure 15-20. CIE Chromaticity Diagram


The three color components R, G, and B define a triangle inside the
CIE diagram of Figure 15-20. Any color within the triangle can be formed
by mixing R, G, and B. The triangle is called a gamut. Because the gamut
is only a subset of the CIE color space, combinations of R, G, and B cannot
generate all visible colors.


To transform values back to the RGB space from the CIE XYZ space, use
the following matrix operation:


Notice that the transform matrix has negative coefficients. Therefore, some
XYZ color may transform into R, G, B values that are negative or greater
than one. This means that not all visible colors can be produced using the
RGB color space.



#### RGB and CIE L*a*b*


To transform RGB to CIE L*a*b*, you first must transform the
RGB values into the CIE XYZ space. Use the following equations to
convert the CIE XYZ values into the CIE L*a*b* values.


L* = 116 × (Y/Yn)1/3 – 16 for Y/Yn > 0.008856


L* = 903.3 × Y / Yn otherwise
a* = 500(f(X / Xn) – f(Y / Yn))
b* = 200(f(Y / Yn) – f(Z / Zn))


where
f(t) = t1/3 for t > 0.008856
f(t) = 7.787t + 16/116 otherwise


Here Xn, Yn, and Zn are the tri-stimulus values of the reference white.


L* represent the light intensity. NI Vision normalizes the result of the L*
transformation to range from 0 to 255. The hue and chroma can be
calculated as follows:


Hue = tan–1(b*/a*)


Based on the fact that the color space is now approximately uniform, a color
difference formula can be given as the Euclidean distance between the
coordinates of two colors in the CIE L*a*b*.


R
G
B


3.240479
1.537150
–
0.498535
–
0.969256
–
1.875992
0.041556
0.055648
0.204043
–
1.057311


X
Y
Z


=


Chroma
a*
(
)
2
b*
(
)
2
+
=


∆Eab
*
∆L*
(
)2
∆a*
(
)2
∆b*
(
)2
+
+
=


To transform CIE L*a*b* values to RGB, first convert the CIE L*a*b*
values to CIE XYZ using the following equations:


X = Xn(P + a* / 500)3


Y = YnP3


Z = Zn(P – b* / 200)3


where
P = (L* + 16) / 116


Then, use the conversion matrix given in the RGB and CIE XYZ section to
convert CIE XYZ to RGB.



#### RGB and CMY


The following matrix operation converts the RGB color space to the CMY
color space.


Normalize all color values to lie between 0 and 1 before using this
conversion equation. To obtain RGB values from a set of CMY values,
subtract the individual CMY values from 1.



#### RGB and YIQ


The following matrix operation converts the RGB color space to the YIQ
color space.


The following matrix operation converts the YIQ color space to the RGB
color space.


C
M
Y


1
1
1


R
G
B


–
=


Y
I
Q


0.299
0.587
0.114
0.596
0.275
–
0.321
–
0.212
0.523
–
0.311


R
G
B


=


R
G
B


1.0
0.956
0.621
1.0
0.272
–
0.647
–
1.0
1.105
–
1.702


Y
I
Q


=
