# Chapter 11: Edge Detection

> **Part**: `Part IV: Machine Vision` | **Pages**: `205 - 218`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


Part IV


Machine Vision


This section describes conceptual information about high-level operations
commonly used in machine vision applications such as edge detection,
pattern matching, dimensional measurements, color inspection, binary
particle classification, optical character recognition, and instrument
reading.


Part IV, Machine Vision, contains the following chapters:


Chapter 11, Edge Detection, contains information about edge detection
techniques and tools that locate edges, such as the rake, concentric rake,
spoke, and caliper.


Chapter 12, Pattern Matching, contains information about pattern
matching.


Chapter 13, Geometric Matching, contains information about geometric
matching and when to use it instead of pattern matching.


Chapter 14, Dimensional Measurements, contains information about
analytic tools, clamps, line fitting, and coordinate systems.


Chapter 15, Color Inspection, contains information about color spaces, the
color spectrum, color matching, color location, and color pattern matching.


Chapter 16, Binary Particle Classification, contains information about
training and classifying objects in an image.


Chapter 17, Golden Template Comparison, contains information about
inspection based on golden template comparison.


Chapter 18, Optical Character Recognition, contains information about
training and reading text and/or characters in an image.



## Part IV Machine Vision


Chapter 19, Instrument Readers, contains information about reading
meters, LCDs, and barcodes.


11
Edge Detection


This chapter describes edge detection techniques and tools that locate
edges, such as the rake, concentric rake, spoke, and caliper.



## Introduction


Edge detection finds edges along a line of pixels in the image.


Use the edge detection tools to identify and locate discontinuities in the
pixel intensities of an image. The discontinuities are typically associated
with abrupt changes in pixel intensity values that characterize the
boundaries of objects in a scene.


To detect edges in an image, specify a search region in which to
locate images. You can specify the search region interactively or
programmatically. When specified interactively, you can use one of the line
ROI tools to select the search path you want to analyze. You also can
programmatically fix the search regions based either on constant values or
the result of a previous processing step. For example, you may want to
locate edges along a specific portion of a part that has been previously
located using particle analysis or pattern matching algorithms. The edge
detection software analyzes the pixels along this region to detect edges. You
can configure the edge detection tool to find all edges, find the first edge,
or find the first and last edges in the region.



## When to Use


Edge detection is an effective tool for many machine vision applications.
It provides your application with information about the location of object
boundaries and the presence of discontinuities.


Use edge detection in the following three application areas: gauging,
detection, and alignment.



## Chapter 11 Edge Detection



### Gauging


Gauging applications make to make critical dimensional
measurements—such as length, distance, diameter, angle, and quantity—
to determine if the product under inspection is manufactured correctly.
Depending on whether the gauged parameters fall inside or outside of the
user-defined tolerance limits, the component or part is either classified or
rejected.


Gauging is often used both inline and offline in production. During inline
processes, each component is inspected as it is manufactured. Visual inline
gauging inspection is a widely used inspection technique in applications
such as mechanical assembly verification, electronic packaging inspection,
container inspection, glass vial inspection, and electronic connector
inspection.


Similarly, gauging applications often measure the quality of products
offline. First, a sample of products is extracted from the production line.
Next, measured distances between features on the object are studied to
determine if the sample falls within a tolerance range. You can measure the
distances separating the different edges located in an image, as well as
positions measured using particle analysis or pattern matching techniques.
Edges can also be combined in order to derive best fit lines, projections,
intersections, and angles. Use edge locations to compute estimations of
shape measurements such as circles, ellipses, polygons, and so on.


Figure 11-1 shows a gauging application using edge detection to measure
the length of the gap in a spark plug.



#### Figure 11-1. Gauging Application Using Edge Detection



### Detection


Part present/not present applications are typical in electronic connector
assembly and mechanical assembly applications. The objective of the
application is to determine if a part is present or not present using line
profiles and edge detection. An edge along the line profile is defined by the


level of contrast between background and foreground and the slope of the
transition. Using this technique, you can count the number of edges along
the line profile and compare the result to an expected number of edges. This
method offers a less numerically intensive alternative to other image
processing methods such as image correlation and pattern matching.


Figure 11-2 shows a simple detection application in which the number of
edges detected along the search line profile determines if a connector has
been assembled properly. Detection of eight edges indicates that there are
four wires. Any other edge count means that the part has been assembled
incorrectly.



#### Figure 11-2. Connector Inspection Using Edge Detection


Use edge detection to detect structural defects, such as cracks, or cosmetic
defects, such as scratches, on a part. If the part is of uniform intensity, these
defects show up as sharp changes in the intensity profile. Edge detection
identifies these changes.



### Alignment


Alignment determines the position and orientation of a part. In many
machine vision applications, the object that you want to inspect may be at
different locations in the image. Edge detection finds the location of the
object in the image before you perform the inspection, so that you can
inspect only the regions of interest. The position and orientation of the part
can also be used to provide feedback information to a positioning device,
such as a stage.


Figure 11-3 shows the detection of the left boundary of a disk in the image.
You can use the location of the edges to determine the orientation of the
disk.


Figure 11-3.  Alignment Using Edge Detection
Concepts



### Definition of an Edge


An edge is a significant change in the grayscale values between
adjacent pixels in an image. In NI Vision, edge detection works on a 1D
profile of pixel values along a search region, as shown in Figure 11-4. The
1D search region can take the form of a line, the perimeter of a circle or
ellipse, the boundary of a rectangle or polygon, or a freehand region. The
software analyzes the pixel values along the profile to detect significant
intensity changes. You can specify characteristics of the intensity changes
to determine which changes constitute an edge.



#### Figure 11-4. Examples of Edges Located on a Bracket


1
Search Lines
2
Edges


1


2



### Characteristics of an Edge


Figure 11-5 illustrates a common model that is used to characterize
an edge.



#### Figure 11-5. Edge Model


The following list includes the main parameters of this model.


•
Edge strength—Defines the minimum difference in the grayscale
values between the background and the edge. The edge strength is also
called the edge contrast. Figure 11-6 shows an image that has different
edge strengths. The strength of an edge can vary for the following
reasons:


–
Lighting conditions—If the overall light in the scene is low,
the edges in image will have low strengths. Figure 11-6 illustrates
a change in the edge strength along the boundary of an object
relative to different lighting conditions.


–
Objects with different grayscale characteristics—The presence of
a very bright object causes other objects in the image with lower
overall intensities to have edges with smaller strengths.


1
Grayscale Profile
2
Edge Length


3
Edge Strength
4
Edge Location


2


3


1


4



#### Figure 11-6. Examples of Edges with Different Strengths


•
Edge length—Defines the maximum distance in which the desired
grayscale difference between the edge and the background must occur.
The length characterizes the slope of the edge. Use a longer length to
detect edges with a gradual transition between the background and the
edge.


•
Edge polarity—Defines whether an edge is rising or falling. A rising
edge is characterized by an increase in grayscale values as you cross
the edge. A falling edge is characterized by a decrease in grayscale
values as you cross the edge. The polarity of an edge is linked to the
search direction. Figure 11-7 shows examples of edge polarities.


•
Edge position—The x, y location of an edge in the image. Figure 11-5
shows the edge position for the edge model.



#### Figure 11-7. Edge Polarity



### Edge Detection Methods


NI Vision offers two ways to perform edge detection. Both methods
compute the edge strength at each pixel along the 1D profile. An edge
occurs when the edge strength is greater than a minimum strength.
Additional checks find the correct location of the edge. You can specify
the minimum strength by using the contrast parameter in the software.


a.
b.
c.


Rising Edge
Positive Polarity


Falling Edge
Negative Polarity


Rising Edge
Positive Polarity
Falling Edge
Negative Polarity



#### Simple Edge Detection


The software uses the pixel value at any point along the pixel profile to
define the edge strength at that point. To locate an edge point, the software
scans the pixel profile pixel by pixel from the beginning to the end. A rising
edge is detected at the first point at which the pixel value is greater than a
threshold value plus a hysteresis value. Set this threshold value to define
the minimum edge strength required for qualifying edges. Use the
hysteresis value to declare different edge strengths for the rising and falling
edges. When a rising edge is detected, the software looks for a falling edge.
A falling edge is detected when the pixel value falls below the specified
threshold value. This process is repeated until the end of the pixel profile.
The first edge along the profile can be either a rising or falling edge.
Figure 11-8 illustrates the simple edge model.


The simple edge detection method works well when there is little noise in
the image and when there is a distinct demarcation between the object and
the background.



#### Figure 11-8. Simple Edge Detection



#### Advanced Edge Detection


To compute the edge strength at a given point along the pixel profile, the
software averages pixels before and after the analyzed point. The pixels
that are averaged after the point can be a specific pixel distance from the


1
Grayscale Profile
2
Threshold Value
3
Hysteresis


4
Rising Edge Location
5
Falling Edge Location


2


4
5


1


3


point, which you define by setting the steepness parameter. This number
corresponds to the expected transition region in the edge profile. Define the
number of pixels averaged on each side by setting the width parameter.
After computing the average, the software computes the difference
between these averages to determine the contrast. Filtering reduces the
effects of noise along the profile. If you expect the image to contain a lot
of noise, use a large filter width. Figure 11-9 illustrates the relationship
between the parameters and the edge profile.


To find the edge, the software scans across the 1D grayscale profile pixel
by pixel. At each point, the edge strength, or contrast, is computed. If the
contrast at the current point is greater than the user-set value for the
minimum contrast for an edge, the point is stored for further analysis.
Starting from this point, successive points are analyzed until the contrast
reaches a maximum value and then falls below that value. The point where
the contrast reaches the maximum value is tagged as the start edge location.
The value of the steepness parameter is added to the start edge location to
obtain the end edge location. The first point between the start edge location
and end edge location—where the difference between the point intensity
value and the start edge value is greater than or equal to 90% of the
difference between the start edge value and end edge value—is returned as
the edge location.



#### Figure 11-9. Advanced Edge Detection


1
Pixels
2
Grayscale Values


3
Width
4
Steepness


5
Contrast
6
Edge Location


5


1


3
4
3


2


6



#### Subpixel Accuracy


When the resolution of the image is high enough, most measurement
applications make accurate measurements using pixel accuracy only.
However, it is sometimes difficult to obtain the minimum image resolution
needed by a machine vision application because of the limits on the size of
the sensors available or the price. In these cases, you need to find edge
positions with subpixel accuracy.


Subpixel analysis is a software method that estimates the pixel values that
a higher resolution imaging system would have provided. To compute the
location of an edge with subpixel precision, the edge detection software
first fits a higher-order interpolating function, such as a quadratic or cubic
function, to the pixel intensity data.


The interpolating function provides the edge detection algorithm with pixel
intensity values between the original pixel values. The software then uses
the intensity information to find the location of the edge with subpixel
accuracy.


Figure 11-10 illustrates how a cubic spline function fits to a set of pixel
values. Using this fit, values at locations in between pixels are estimated.
The edge detection algorithms use these values to estimate the location of
an edge with subpixel accuracy.



#### Figure 11-10. Obtaining Subpixel Information Using Interpolation


1
Known Pixel Value
2
Interpolating Function


3
Interpolated Value
4
Subpixel Location


3


4


2


1


With the imaging system components and software tools available today,
you can reliably estimate one-fourth subpixel accuracy. However, the
results of the estimation depend heavily on the imaging setup, such as
lighting conditions and the camera lens. Before resorting to subpixel
information, try to improve the image resolution. For more information
on improving your images, see your NI Vision user manual.



### Extending Edge Detection to 2D Search Regions


The edge detection tool in NI Vision works on a 1D profile. The Rake,
Spoke, and Concentric Rake tools extend the use of edge detection to
two dimensions. In these edge detection variations, the 2D search area is
covered by a number of search lines over which the edge detection is
performed. You can control the number of the search lines used in the
search region by defining the separation between the lines.



#### Rake


Rake works on a rectangular search region, along search lines that are
drawn parallel to the orientation of the rectangle. Control the number of
lines in the area by specifying the search direction as left to right or right to
left for a horizontally oriented rectangle. Specify the search direction as top
to bottom or bottom to top for a vertically oriented rectangle. Figure 11-11
illustrates the basics of the Rake function.



#### Figure 11-11. Rake Function


1
Search Area
2
Search Line
3
Search Direction
4
Edge Points


2
4


1


2
4


1


a.
b.


3
3



#### Spoke


Spoke works on an annular search region, along search lines that are drawn
from the center of the region to the outer boundary and that fall within the
search area. Control the number of lines in the region by specifying the
angle between each line. Specify the search direction as either from the
center outward or from the outer boundary to the center. Figure 11-12
illustrates the basics of the Spoke function.



#### Figure 11-12. Spoke Function


1
Search Area
2
Search Line
3
Search Direction
4
Edge Points


4


4


2
2
1


a.
b.


1


3
3



#### Concentric Rake


Concentric Rake works on an annular search region. It is an adaptation of
the Rake to an annular region. Figure 11-13 illustrates the basics of the
concentric rake. Edge detection is performed along search lines that occur
in the search region and that are concentric to the outer circular boundary.
Control the number of concentric search lines that are used for the edge
detection by specifying the radial distance between the concentric lines in
pixels. Specify the direction of the search as either clockwise or
anti-clockwise.



#### Figure 11-13. Concentric Rake Function


1
Search Area
2
Search Line
3
Search Direction
4
Edge Points


1


2


1


2


3


3
4
4
