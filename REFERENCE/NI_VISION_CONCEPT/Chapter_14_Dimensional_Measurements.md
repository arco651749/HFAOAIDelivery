# Chapter 14: Dimensional Measurements

> **Part**: `Part IV: Machine Vision` | **Pages**: `245 - 262`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


14
Dimensional Measurements


This chapter contains information about coordinate systems, analytic tools,
and clamps.



## Introduction


You can use dimensional measurements or gauging tools in NI Vision to
obtain quantifiable, critical distance measurements—such as distances,
angles, areas, line fits, circular fits, and quantities. These measurements can
help you to determine if a product was manufactured correctly.


Components such as connectors, switches, and relays are small and
manufactured in high quantity. Human inspection of these components is
tedious, time consuming, and inconsistent. NI Vision can quickly and
consistently measure certain features on these components and generate a
report of the results. If the gauged distance or count does not fall within
user-specified tolerance limits, the component or part fails to meet
production specifications and should be rejected.



### When to Use


Use gauging for applications in which inspection decisions are made
on critical dimensional information obtained from image of the part.
Gauging is often used in both inline and offline production. During
inline processes, each component is inspected as it is manufactured. Inline
gauging inspection is often used in mechanical assembly verification,
electronic packaging inspection, container inspection, glass vile
inspection, and electronic connector inspection.


You also can use gauging to measure the quality of products off-line.
First, a sample of products is extracted from the production line. Then,
using measured distances between features on the object, NI Vision
determines if the sample falls within a tolerance range. Gauging techniques
also allow you to measure the distance between particles and edges in
binary images and easily quantify image measurements.



## Chapter 14 Dimensional Measurements



### Concepts


The gauging process consists of the following four steps:


1.
Locate the component or part in the image.


2.
Locate features in different areas of the part.


3.
Make measurements using these features.


4.
Compare the measurements to specifications to determine if the part
passes inspection.



### Locating the Part in the Image


A typical gauging application extracts measurements from ROIs rather
than from an entire image. To use this technique, the necessary parts of the
object must always appear inside the ROIs you define.


Usually, the object under inspection appears shifted or rotated within
the images you want to process. When this occurs, the ROIs need to shift
and rotate in the same way as the object. In order for the ROIs to move in
relation to the object, you must locate the object in every image. Locating
the object in the image involves determining the x, y position and the
orientation of the object in the image using the reference coordinate system
functions. You can build a coordinate reference using edge detection or
pattern matching.



### Locating Features


To gauge an object, you need to find landmarks or object features on which
you can base your measurements. In most applications, you can make
measurements based on points detected in the image or geometric fits to the
detected points. Object features that are useful for measurements fall into
two categories:


•
Edge points along the boundary of an object located by the edge
detection method


•
Shapes or patterns within the object located by pattern matching



### Making Measurements


You can make different types of measurements from the features found
in the image. Typical measurements include the distance between points;
the angle between two lines represented by three or four points; the best
linear, circular, or elliptical fits; and the areas of geometric shapes—such


as circles, ellipses, and polygons—that fit detected points. For more
information about the types of measurements you can make, refer to your
NI Vision user manual.



### Qualifying Measurements


The last step of a gauging application involves determining the quality
of the part based on the measurements obtained from the image. You can
determine the quality of the part using either relative comparisons or
absolute comparisons.


In many applications, the measurements obtained from the inspection
image can be compared to the same measurements obtained from a
standard specification or a reference image. Because all the measurements
are made on images of the part, you can compare them directly.


In other applications, the dimensional measurements obtained from the
image must be compared with values that are specified in real units. In this
case, convert the measurements from the image into real-world units using
the calibration tools described in Chapter 3, System Setup and Calibration.



## Coordinate System


In a typical machine vision application, measurements are extracted from
an ROI rather than from the entire image. The object under inspection must
always appear in the defined ROI in order to extract measurements from
that ROI.


When the location and orientation of the object under inspection is always
the same in the inspection images, you can make measurements directly
without locating the object in every inspection image.


In most cases, the object under inspection is not positioned in the camera
field of view consistently enough to use fixed search areas. If the object is
shifted or rotated within an image, the search areas should shift and rotate
with the object. The search areas are defined relative to a coordinate
system. A coordinate system is defined by a reference point (origin) and
a reference angle in the image or by the lines that make up its two axes.


Use coordinate systems in a gauging application when the object does not
appear in the same position in every inspection image. You also can use a
coordinate system to define search areas on the object relative to the
location of the object in the image.


All measurements are defined with respect to a coordinate system.
A coordinate system is based on a characteristic feature of the object under
inspection, which is used as a reference for the measurements. When you
inspect an object, first locate the reference feature in the inspection image.
Choose a feature on the object that the software can reliably detect in every
image. Do not choose a feature that may be affected by manufacturing
errors that would make the feature impossible to locate in images of
defective parts.


You can restrict the region of the image in which the software searches
for the feature by specifying an ROI that encloses the feature. Defining an
ROI in which you expect to find the feature can prevent mismatches if the
feature appears in multiple regions of the image. A small ROI may also
improve the locating speed.


Complete the following general steps to define a coordinate system and
make measurements based on the new coordinate system.


1.
Define a reference coordinate system.


a.
Define a search area that encompasses the reference feature or
features on which you base your coordinate system. Make sure
that the search area encompasses the features in all your
inspection images.


b.
Locate an easy-to-find reference feature of the object under
inspection. That feature serves as the base for a reference
coordinate system in a reference image. You can use two primary
techniques to locate the feature: edge detection or pattern
matching.


The software builds a coordinate system to keep track of the location
and orientation of the object in the image.


2.
Set up measurement areas within the reference image in which you
want to make measurements.


3.
Acquire an image of the object to inspect or measure.


4.
Update the coordinate system. During this step, NI Vision locates the
features in the search area and builds a new coordinate system based
on the new location of the features.


5.
Make measurements within the updated measurement area.


NI Vision computes the difference between the reference coordinate
system and the new coordinate system. Based on this difference, the
software moves the new measurement areas with respect to the new
coordinate system.


Figure 14-1a illustrates a reference image with a defined reference
coordinate system. Figure 14-1b illustrates an inspection image with an
updated coordinate system.



#### Figure 14-1. Coordinate Systems of a Reference Image and Inspection Image



### In-Depth Discussion


You can use four different strategies to build a coordinate system.
Two strategies are based on detecting the reference edges of the object
under inspection. The other two strategies involve locating a specific
pattern using a pattern matching algorithm.



#### Edge-Based Coordinate System Functions


These functions determine the axis of the coordinate system by locating
edges of the part under inspection. Use an edge-based method if you can
identify two straight, distinct, non-parallel edges on the object you want to


1
Search Area for the Coordinate System
2
Object Edges


3
Origin of the Coordinate System
4
Measurement Area


1


4


1


4


a.
b.


2


3


3


2


locate. Because the software uses these edges as references for creating the
coordinate system, choose edges that are unambiguous and always present
in the object under inspection.


Single Search Area


This method involves locating the two axes of the coordinate
system—the main axis and secondary axis—in a single search area based
on an edge detection algorithm. First, the function determines the main axis
of the coordinate system, as illustrated in Figure 14-2a. A rake function
finds the intersection pixels between multiple search lines and the edge of
the object. You can specify the search direction along these search lines.
The intersection points are determined by their contrast, width, and
steepness. For more information about detecting edges, refer to Chapter 11,
Edge Detection. A line fitted through the intersection points defines the
main axis. The function then searches for a secondary axis within the same
search area, as shown in Figure 14-2b. The software uses multiple parallel
lines that are parallel to the main axis to scan for edges, and then fits a line
through the edge of the object closest to the search area and perpendicular
to the main axis. This line defines the secondary axis of the coordinate
system. The secondary axis must not be parallel to the main axis. The
intersection between the main axis and secondary axis defines the origin
of the reference coordinate system.



#### Figure 14-2. Locating a Coordinate System with One Search Area


1
Search Area for the Coordinate System
2
Search Lines


3
Main Axis
4
Secondary Axis


5
Origin of the Reference
Coordinate System


3


1


2


3


1


2


4


a.
b.


5


Two Search Areas


This method uses the same operating mode as the single search area
method. However, the two edges used to define the coordinate system axes
are located in two distinct search areas.


The function first determines the position of the main axis of the coordinate
system. It locates the intersection points between a set of parallel search
lines in the primary search area and a distinct straight edge of the object.
The intersection points are determined based on their contrast, width, and
steepness. For more information about detecting edges, refer to Chapter 11,
Edge Detection. A line fitted through the intersection points defines the
primary axis. The process is repeated perpendicularly in the secondary
search area to locate the secondary axis. The intersection between the
primary axis and secondary axis is the origin of the coordinate system.


Figure 14-3a illustrates a reference image with a defined reference
coordinate system. Figure 14-3b illustrates an inspection image with an
updated coordinate system.



#### Figure 14-3. Locating a Coordinate System with Two Search Areas


1
Primary Search Area
2
Secondary Search Area


3
Origin of the Coordinate System
4
Measurement Area


1


3


2


4


1


3


2


4


a.
b.



#### Pattern Matching-Based Coordinate System Functions


Using pattern matching techniques to locate a reference feature is a good
alternative to edge detection when you cannot find straight, distinct edges
in the image. The reference feature, or template, is the basis for the
coordinate system.


The software searches for a template image in a rectangular search area of
the reference image. The location and orientation of the located template is
used to create the reference position of a coordinate system or to update the
current location and orientation of an existing coordinate system.


The same constraints on feature stability and robustness that apply to
the edge-detection techniques also apply to pattern matching. Pattern
matching uses one of two strategies: shift-invariant pattern matching
and rotation-invariant pattern matching. Shift-invariant pattern matching
locates a template in an ROI or in the entire image with a maximum
tolerance in rotation of ±5°. The rotation-invariant strategy locates a
template in the image even when the template varies in orientation between
0° and 360°. For recommendations about the type of patterns to use for a
template, refer to Chapter 12, Pattern Matching.


Figure 14-4 illustrates how to locate a coordinate system using a
shift-invariant pattern matching strategy. Figure 14-4a shows a reference
image with a defined reference coordinate system. Figure 14-4b shows an
inspection image with an updated coordinate system.



#### Figure 14-4. Locating a Coordinate System with Shift-Invariant Pattern Matching


1
Located Feature
2
Coordinate System
3
Measurement Area


2


1


2


1


3


3


a.
b.


Figure 14-5 illustrates how to locate a coordinate system using a
rotation-invariant pattern matching strategy. Figure 14-5a shows a
reference image with a defined reference coordinate system. Figure 14-5b
shows an inspection image with an updated coordinate system.



#### Figure 14-5. Locating a Coordinate System with Rotation-Invariant Pattern Matching



## Finding Features or Measurement Points


Before making measurements, you must locate features that you can use to
make the measurements. There are many ways to find these features on an
image. The most common features used to make measurements are points
along the boundary of the part you want to gauge.



### Edge-Based Features


Use the edge detection techniques described in Chapter 11, Edge
Detection, to find edge points along a single search contour or along
multiple search contours defined inside a 2D search area.


1
Located Feature
2
Coordinate System


3
Origin of the Coordinate System
4
Measurement Areas


2


3


1


4
2


3


4


1


a.
b.



### Line and Circular Features


Use the line detection functions in NI Vision to find vertically or
horizontally oriented lines. These functions use the rake and concentric
rake functions to find a set of points along the edge of an object and then fit
a line through the edge.


Refer to Chapter 11, Edge Detection, for more information on the rake and
concentric rake functions. The line fitting method is described later in this
chapter. Figure 14-6 illustrates how a rake finds a straight edge.



#### Figure 14-6. Finding a Straight Feature


Use the circle detection function to locate circular edges. This function uses
a spoke to find points on a circular edge, and then fits a circle on the
detected points. Figure 14-7 illustrates how a spoke finds circular edges.


1
Search Region
2
Search Lines


3
Detected Edge Points
4
Line Fit to Edge Points


2


1


4


3



#### Figure 14-7. Circle Detection



### Shape-Based Features


Use pattern matching or color pattern matching to find features that are
better described by the shape and grayscale or color content than the
boundaries of the part.



#### Figure 14-8. Finding Shape Features


1
Annular Search Region
2
Search Lines


3
Detected Edge Points
4
Circle Fit to Edge Points


2
3


4


1



## Making Measurements on the Image


After you have located points in the image, you can make distance or
geometrical measurements based on those points.



### Distance Measurements


Make distance measurements using one of the following methods:


•
Measure the distance between points found by one of the feature
detection methods.


•
Measure the distance between two edges of an object using the clamp
functions available in NI Vision. Clamp functions measure the
separation between two edges in a rectangular region using the rake
function. First, the clamp functions detect points along the two edges
using the rake function. They then compute the distance between the
detected points and return the largest or smallest distance. Use the
clamp functions to perform the following functions:


–
Find the smallest or largest horizontal separation between
two vertically oriented edges.


–
Find the smallest or largest vertical separation between
two horizontally oriented edges.


Figure 14-9 illustrates how a clamp function finds the minimum distance
between edges of an object.



#### Figure 14-9. Clamp Function



### Analytic Geometry


You can make the following geometrical measurements from the feature
points detected in the image.


•
The area of a polygon specified by its vertex points


•
The line that fits to a set of points and the equation of that line


•
The circle that fits to a set of points and its area, perimeter, and radius


•
The ellipse that fits to a set of points and its area, perimeter, and the
lengths of its major and minor axis


•
The intersection point of two lines specified by their start and end
points


•
The line bisecting the angle formed by two lines


•
The line midway between a point and a line that is parallel to the line


•
The perpendicular line from a point to a line, which computes the
perpendicular distance between the point and the line


1
Rectangular Search Region
2
Search Lines for Edge Detection
3
Detected Edge Points


4
Line Fit to Edge Points
5
Measured Distance


1


3


5


4
2



#### Line Fitting


The line fitting function in NI Vision uses a robust algorithm to find a line
that best fits a set of points. The line fitting function works specifically with
the feature points obtained during gauging applications.


In a typical gauging application, a rake or a concentric rake function finds
a set of points that lie along a straight edge of the object. In an ideal case,
all the detected points would make a straight line. However, points usually
do not appear in a straight line for one of the following reasons:


•
The edge of the object does not occupy the entire search region used
by the rake.


•
The edge of the object is not a continuous straight line.


•
Noise in the image causes points along the edge to shift from their true
positions.


Figure 14-10 illustrates an example of a set of points located by the rake
function. As shown in the figure, a typical line fitting algorithm that uses
all of the points to fit a line returns inaccurate results. The line fitting
function in NI Vision compensates for outlying points in the dataset and
returns a more accurate result.


NI Vision uses the following process to fit a line. NI Vision assumes that a
point is part of a line if the point lies within a user-defined distance—or
pixel radius—from the fitted line. Then the line fitting algorithm fits a line
to a subset of points that fall along an almost straight line. NI Vision
determines the quality of the line fit by measuring its mean square distance
(MSD), which is the average of the squared distances between each point
and the estimated line. Figure 14-11 illustrates how the MSD is calculated.
Next, the line fitting function removes the subset of points from the original
set. NI Vision repeats these steps until all points have been fit. Then, the
line fitting algorithm finds the line with the lowest MSD, which
corresponds to the line with the best quality. The function then improves the
quality of the line by successively removing the furthest points from the
line until a user-defined minimum score is obtained or a user-specified
maximum number of iterations is exceeded.


The result of the line fitting function is a line that is fit to the strongest
subset of the points after ignoring the outlying points, as shown in
Figure 14-12.



#### Figure 14-10. Data Set and Fitted Line Using Two Methods



#### Figure 14-11. Calculation of the Mean Square Distance (MSD)


1
Edge Points
2
Standard Line Fit
3
NI Vision Fit Line


1
Perpendicular Distance from an
Edge Point to the Line


2
Line Fit
3
Points Used to Fit the Line


3


2


1


d0
d2


d1


1


2


3


Σ dk


N–1


k=0


N
MSD =


2


The pixel radius, minimum score, and maximum iteration parameters
control the behavior of the line fit function.


The pixel radius defines the maximum distance allowed, in pixels, between
a valid point and the estimated line. The algorithm estimates a line where
at least half the points in the set are within the pixel radius. If a set of points
does not have such a line, the function attempts to return the line that has
the most number of valid points.



#### Figure 14-12. Strongest Line Fit


Increasing the pixel radius increases the distance allowed between a
point and the estimated line. Typically, you can use the imaging system
resolution and the amount of noise in your system to gauge this parameter.
If the resolution of the imaging system is very high, use a small pixel radius
to minimize the use of outlying points in the line fit. Use a higher pixel
radius if your image is noisy.


1
Strongest Line Returned by the Line Fit Function
2
Alternate Line Discarded by the Line Fit Function


2


1


The minimum score allows you to improve the quality of the estimated line.
The line fitting function removes the point furthest from the fit line, and
then refits a line to the remaining points and computes the MSD of the line.
Next, the function computes a line fit score (LFS) for the new fit using the
following equation


where PR is the pixel radius.


NI Vision repeats the entire process until the score is greater than or equal
to the minimum score or until the number of iterations exceeds the
user-defined maximum number of iterations.


Use a high minimum score to obtain the most accurate line fit. For example,
combining a large pixel radius and a high minimum score produces an
accurate fit within a very noisy data set. A small pixel radius and a small
minimum score produces a robust fit in a standard data set.


The maximum number of iterations defines a limit in the search for a line
that satisfies the minimum score. If you reach the maximum number of
iterations before the algorithm finds a line matching the desired minimum
score, the algorithm stops and returns the current line. If you do not need to
improve the quality of the line in order to obtain the desired results, set the
maximum iterations value to 0 in the line fit function.


LFS
1
MSD
–
PR2
---------------------




1000
×
=
