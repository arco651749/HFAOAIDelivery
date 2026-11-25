# Chapter 13: Geometric Matching

> **Part**: `Part IV: Machine Vision` | **Pages**: `227 - 244`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


13
Geometric Matching


This chapter contains information about geometric matching.



## Introduction


Geometric matching locates regions in a grayscale image that match a
model, or template, of a reference pattern. Geometric matching is
specialized to locate templates that are characterized by distinct geometric
or shape information.


When using geometric matching, you create a template that represents the
object for which you are searching. Your machine vision application then
searches for instances of the template in each inspection image and
calculates a score for each match. The score relates how closely the
template resembles the located matches.


Geometric matching finds template matches regardless of lighting
variation, blur, noise, occlusion, and geometric transformations such as
shifting, rotation, or scaling of the template.



## When to Use


Geometric matching helps you quickly locate objects with good geometric
information in an inspection image. Figure 13-1 shows examples of objects
with good geometric or shape information.



### Figure 13-1. Examples of Objects on which Geometric Matching is Designed to Work



## Chapter 13 Geometric Matching


You can use geometric matching in the following application areas:


•
Gauging—Measures lengths, diameters, angles, and other critical
dimensions. If the measurements fall outside set tolerance levels, the
object is rejected. Use geometric matching to locate the object, or areas
of the object, you want to gauge. Use information about the size of the
object to preclude geometric matching from locating objects whose
sizes are too big or small.


•
Inspection—Detects simple flaws, such as scratches on objects,
missing objects, or unreadable print on objects. Use the occlusion
score returned by geometric matching to determine if an area of the
object under inspection is missing. Use the curve matching scores
returned by geometric matching to compare the boundary (or edges) of
a reference object to the object under inspection.


•
Alignment—Determines the position and orientation of a known
object by locating points of reference on the object or characteristic
features of the object.


•
Sorting—Sorts objects based on shape and/or size. Geometric
matching returns the location, orientation, and size of each object. You
can use the location of the object to pick up the object and place it into
the correct bin. Use geometric matching to locate different types of
objects, even when objects may partially occlude each other.


The objects that geometric matching locates in the inspection image may
be rotated, scaled, and occluded in the image. Geometric matching provides
your application with the number of object matches and their locations
within the inspection image. Geometric matching also provides
information about the percentage change in size (scale) of each match
and the amount by which each object in the match is occluded.


For example, you can search an image containing multiple automotive parts
for a particular type of part in a sorting application. Figure 13-2a shows an
image of the part that you need to locate. Figure 13-2b shows an inspection
image containing multiple parts and the located part that corresponds to the
template. Figure 13-3 shows the use of geometric matching in an alignment
application.



### Figure 13-2. Example of a Part Sorting Application that Uses Geometric Matching


a.
b.



### Figure 13-3. Example of an Alignment Application that Uses Geometric Matching



### When Not to Use Geometric Matching


The geometric matching algorithm is designed to find objects that have
distinct geometric information. The fundamental characteristics of some
objects may make other searching algorithms more optimal than geometric
matching. For example, the template image in some applications may be
defined primarily by the texture of an object, or the template image may
contain numerous edges and no distinct geometric information. In these
applications, the template image does not have a good set of features for the
geometric matching algorithm to model the template. Instead, the pattern
matching algorithm described in Chapter 12, Pattern Matching, would be
a better choice.


In some applications, the template image may contain sufficient geometric
information, but the inspection image may contain too many edges. The
presence of numerous edges in an inspection image can slow the
performance of the geometric matching algorithm because the algorithm
tries to extract features using all the edge information in the inspection
image. In such cases, if you do not expect template matches to be scaled or
occluded, use pattern matching to solve the application.


a.
b.



## What to Expect from a Geometric Matching Tool


Because geometric matching is an important tool for machine vision
applications, it must work reliably under various, sometimes harsh,
conditions. In automated machine vision applications—especially those
incorporated into manufacturing processes—the visual appearance of
materials or components under inspection can change because of factors
such as varying part orientation, scale, and lighting. The geometric
matching tool must maintain its ability to locate the template patterns
despite these changes. The following sections describe common situations
in which the geometric matching tool needs to return accurate results.



### Part Quantity, Orientation, and Size


The geometric matching algorithm can detect the following items in an
inspection image:


•
One or more template matches


•
Position of the template match


•
Orientation of the template match


•
Change in size of the template match compared to the template image


You can use the geometric matching algorithm to locate template matches
that are rotated or scaled by certain amounts. Figure 13-4a shows a
template image. Figure 13-4b shows the template match rotated and scaled
in the image.



#### Figure 13-4. Examples of a Rotated and Scaled Template Match


a.
b.



### Non-Linear or Non-Uniform Lighting Conditions


The geometric matching algorithm can find a template match in an
inspection image under conditions of non-linear and non-uniform lighting
changes across the image. These lighting changes include light drifts,
glares, and shadows. Figure 13-5a shows a template image. Figure 13-5b
shows the typical conditions under which geometric matching correctly
finds template matches.



#### Figure 13-5. Examples of Lighting Conditions



### Contrast Reversal


The geometric matching algorithm can find a template match in an
inspection image even if the contrast of the match is reversed from the
original template image. Figure 13-6 illustrates a typical contrast reversal.
Figure 13-6a shows the original template image. Figure 13-6b shows an
inspection image with the contrast reversed. The geometric matching
algorithm can locate the part in Figure 13-6b with the same accuracy as the
part in Figure 13-6a.


a.
b.



#### Figure 13-6. Example of Contrast Reversal



### Partial Occlusion


The geometric matching algorithm can find a template match in an
inspection image even when the match is partially occluded because of
overlapping parts or the part under inspection not fully being within the
boundary of the image. In addition to locating occluded matches, the
algorithm returns the percentage of occlusion for each match.


In many machine vision applications, the part under inspection may be
partially occluded by other parts that touch or overlap it. Also, the part may
seem partially occluded because of degradations in the manufacturing
process. Figure 13-7 illustrates different scenarios of occlusion under
which geometric matching can find a template match. Figure 13-5a
represents the template image for this example.



#### Figure 13-7. Examples of Matching Under Occlusion


a.
b.



### Different Image Backgrounds


The geometric matching algorithm can find a template match even if the
inspection image has a background that is different from the background in
the template image. Figure 13-8 shows examples of geometric matching
locating a template match in inspection images with different backgrounds.
Figure 13-5a represents the template image for this example.



#### Figure 13-8. Example of Matching with Different Backgrounds



## Geometric Matching Technique


Searching and matching algorithms, such as pattern matching or geometric
matching, find regions in the inspection image that contain information
similar to the information in the template. This information, after being
synthesized, becomes the set of features that describes the image. Pattern
matching and geometric matching algorithms use these sets of features to
find matches in inspection images.


Pattern matching algorithms, such as the one described in Chapter 12,
Pattern Matching, use the pixel intensity information present in the
template image as the primary feature for matching. The geometric
matching algorithm uses geometric information present in the template
image as the primary features for matching. Geometric features can range
from low-level features, such as edges or curves, to higher-level features,
such as the geometric shapes made by the curves in the image.


Figure 13-9 shows the information from the template image in
Figure 13-5a that the geometric matching algorithm may use as matching
features. Figure 13-9a shows the curves that correspond to edges in the
template image. These curves form the basic geometric features.
Figure 13-9b shows higher-level shape features that the algorithm also
uses for matching.



### Figure 13-9. Geometric Information Used for Matching


The geometric matching process consists of two stages: learning and
matching. During the learning stage, the geometric matching algorithm
extracts geometric features from the template image. The algorithm
organizes and stores these features and the spatial relationships between
these features in a manner that facilitates faster searching in the inspection
image. In NI Vision, the information learned during this stage is stored as
part of the template image.


During the matching stage, the geometric matching algorithm extracts
geometric features from the inspection image that correspond to the
features in the template image. Then, the algorithm finds matches by
locating regions in the inspection image where features align themselves in
spatial patterns similar to the spatial patterns of the features in the template.



### Learning


The learning stage consists of the following three main steps: curve
extraction, feature extraction, and representation of the spatial relationships
between the features.



#### Curve Extraction


A curve is a set of edge points that are connected to form a continuous
contour. Curves typically represent the boundary of the part in the image.
Figure 13-9a shows the six curves extracted from the template image
shown in Figure 13-5a.


1
Curves
2
Circular Features


3
Rectangular Features
4
Linear Features


5
Corners


1


2


3


3


4
4


1


5


5


5


5


The curve extraction process consists of three steps: finding curve seed
points, tracing the curve, and refining the curves.


Finding Curve Seed Points


A seed point is a point on a curve from which tracing begins. To qualify as
a seed point, a pixel cannot be part of an already existing curve. Also, the
pixel must have an edge contrast greater than the user-defined
Edge Threshold. The edge contrast at a pixel is computed as a function of
the intensity value at that pixel and the intensities of its neighboring pixels.
If P(i, j) represents the intensity of the pixel P with the coordinates (i, j), the
edge contrast at (i, j) is defined as


For an 8-bit image, the edge contrast may vary from 0 to 360.


To increase the speed of the curve extraction process, the algorithm visits
only a limited number of pixels in the image to determine if the pixel is a
valid seed point. The number of pixels to visit is based on the values that
the user provides for the Row Step and Column Step parameters. The
higher these values are, the faster the algorithm searches for seed points.
However, to make sure that the algorithm finds a seed point on all of the
curves, Row Step must be smaller than the smallest curve in the y direction,
and Column Step must be smaller than the smallest curve in the
x direction.


The algorithm starts by scanning the image rows from the top left corner.
Starting at the first pixel, the edge contrast of the pixel is computed. If the
edge contrast is greater than the given threshold, the curve is traced from
this point. If the contrast is lower than the threshold, or if this pixel is
already a member of an existing curve previously computed, the algorithm
analyzes the next pixel in the row to determine if it qualifies as a seed point.
This process is repeated until the end of the current row is reached. The
algorithm then skips Row Step rows and repeats the process.


After scanning all of the rows, the algorithm scans the image columns to
locate seed points. The algorithm starts at the top left corner and analyzes
each column that is Column Step apart.


P i
1
–
j,
(
)
P i
1
+
j,
(
)
–
(
)2
P i j
1
–
,
(
)
P i j
1
+
,
(
)
–
(
)2
+


Tracing the Curve


When it finds a seed point, the curve extraction algorithm traces the rest of
the curve. Tracing is the process by which a pixel that neighbors the last
pixel on the curve is added to the curve if it has the strongest edge contrast
in the neighborhood and the edge contrast is greater than acceptable edge
threshold for a curve point. This process is repeated until no more pixels
can be added to the curve in the current direction. The algorithm then
returns to the seed point and tries to trace the curve in the opposite
direction. Figure 13-10 illustrates this process.



#### Figure 13-10. Curve Extraction


Note
For the purpose of simplifying Figure 13-10, Row Step and Column Step are not
smaller than the smallest feature.


1
Scan Lines
2
Row Step


3
Column Step
4
Curve Seeds


5
Curves


5


1


4


2


3


Refining the Curve


During the final stage of curve extraction, the algorithm performs the
following tasks to refine the extracted curves:


•
Combines curves into one large curve if their end points are close
together


•
Closes a curve if the end points of the curve are within a user-defined
distance of each other


•
Removes curves that fall below a certain size threshold defined by
the user



#### Feature Extraction


Feature extraction is the process of extracting high-level geometric features
from the curves obtained from curve extraction. These features can be
lines, rectangles, corners, or circles.


First, the algorithm approximates each curve using polygons. Then, the
algorithm uses the line segments forming these polygons to create linear
and corner features. These linear features are used to compose higher-level
rectangular features. The curves or segments of curves that cannot be
approximated well with polygons or lines are used to create circular
features. Typical features that the algorithm extracts are shown in
Figure 13-9.


After the algorithm extracts high-level geometric features from the
template image, the features are ordered based on the following criteria:


•
Type—Lines, rectangles, corners, or circles


•
Strength—How accurately the features portray a given geometric
structure


•
Saliency—How well the features describe the template


After the features have been ordered, the best are chosen to describe the
template.



#### Representation of Spatial Relationships


Given two features, the algorithm learns the spatial relationship between
the features, which consists of the vector from the first feature to the second
feature. These spatial relationships describe how the features are arranged
spatially in the template in relationship to one another. The algorithm uses
these relationships to create a model of features that describes the template.
The algorithm uses this template model during the matching stage to create
match candidates and to verify that matches are properly found.



### Matching


The matching stage consists of five main steps. The first two steps
performed on the inspection image are curve extraction and feature
extraction, which are similar to the curve extraction and feature extraction
that occur during the learning stage. The final three steps are feature
correspondence matching, template model matching, and match
refinement.



#### Feature Correspondence Matching


Feature correspondence matching is the process of matching a given
template feature to a similar type of feature in the inspection image, called
a target feature. The algorithm uses feature correspondence matching to do
the following:


•
Create an initial set of potential matches in the inspection image.


•
Update potential matches with additional information or refined
parameters, such as position, angle, and scale.



#### Template Model Matching


Template model matching is the process of superimposing the template
model from the learning step onto a potential match in the inspection image
to confirm that the potential match exists or to improve the match. After
superimposing the template model onto a potential match, the presence of
additional target features found in accordance with the template model and
its spatial relationships to existing features confirms the existence of the
potential match and yields additional information that the algorithm uses to
update and improve the accuracy of the match.



#### Match Refinement


Match refinement is the final step in the matching stage. Match refinement
carefully refines known matches for increased positional, scalar, and
angular accuracy. Match refinement uses curves extracted from both the
template image and inspection image to ensure that the matches are
accurately and precisely found.



## Geometric Matching Using Calibrated Images


During matching, the geometric matching algorithm uses calibration
information attached to the inspection image to return the position, angle,
and bounding rectangle of a match in both pixel and real-world units.
In addition, if the image is calibrated for perspective or nonlinear distortion
errors, geometric matching uses the attached calibration information
directly to find matches in the inspection image without using
time-consuming image correction.



### Simple Calibration or Previously Corrected Images


If an inspection image contains simple calibration information, or if the
inspection image has been corrected prior to being used by geometric
matching, the matching stage performs the same way that it does with
uncalibrated images. However, each match result is returned in both pixel
and real-world units. The pixel-unit results are identical to the results that
would have been returned from matching the same, uncalibrated image.
Geometric matching converts the pixel units to real-world units using the
simple calibration information attached to the inspection image.



### Perspective or Nonlinear Distortion Calibration


If an inspection image contains calibration information for perspective or
nonlinear distortions, the first step in the matching process is different than
it would be with uncalibrated images. In the first step, curves extracted
from the inspection image are corrected for distortion errors using
calibration information. The remaining four steps in the matching process
are performed on the corrected curves. Each match result is returned in
pixel and real-world units.


Match results in pixel units are returned to be consistent with the inspection
image. As a result, the bounding rectangle of a match in pixel units may not
be rectangular, as shown in Figure 13-11. Figure 13-11a shows the
template image of a metallic part. Figure 13-11b shows an image of a
calibration grid. The image exhibits nonlinear distortion. Figure 13-11c


shows an image of metallic parts taken with the same camera setup used in
Figure 13-11b. The gray lines depict the bounding rectangle of each match
found by geometric matching.



#### Figure 13-11. Geometric Matching Using Calibration Information



## In-Depth Discussion


This section provides additional information you may need for building
successful geometric matching applications.



### Geometric Matching Report


The geometric matching algorithm returns a report about the matches found
in the inspection image. This report contains the location, angle, scale,
occlusion percentage, and accuracy scores of the matches. The following
sections explain the accuracy scores in greater detail.



#### Score


The general score ranks the match results on a scale of 0 to 1000, where
0 indicates no match and 1000 indicates a perfect match. The general score
takes the following factors into consideration:


•
The number of geometric features in the template image that matched
the target


•
The individual scores obtained from matching template features to
their corresponding features in the inspection image


a.
b.
c.


•
The score obtained by comparing the edge strengths of the curves in
the template image to the edge strengths of the corresponding curves
in the inspection image


When geometric matching is used to find objects, the score is computed
using only the curves and features in the template that were matched in the
inspection image. Therefore, a partially occluded match could have a very
high score if the features in the non-occluded regions of the part matched
perfectly with the template features.


Figure 13-12a shows the learned template curves of a part. Figure 13-12b
shows the template match curves of a non-occluded part. Figure 13-12c
shows the template match curves of an occluded part.



#### Figure 13-12. Score and Occlusion Percent Reported by Geometric Matching


Note
The general score is the score that the algorithm uses during matching to remove
matches that fall below a user-defined Minimum Match Score value.



#### Template Target Curve Score


The template target curve score specifies how closely the curves in the
template image match the curves in the match region of the inspection, or
target, image. Score values can range from 0 to 1000, where a score of
1000 indicates that all template curves have a corresponding curve in the
match region of the inspection image.


The template target curve score is computed by combining the match scores
obtained by comparing each curve in the template to its corresponding
curve in the target match region. Unlike the general score, the template
target curve score is computed using all of the template curves.


Score = 1000; Occlusion % = 0


b.
a.
c.


Score = 1000; Occlusion % = 65


A low score implies one or both of the following:


•
Some curves, or parts of curves, that are present in the template were
not found in the inspection image, perhaps because of occlusion.


•
The curves found in the inspection image were deformed and did not
perfectly match the template curves.


You can use the template target curve score in inspection tasks to determine
if the located part has flaws caused by anomalies such as process variations
or printing errors. These flaws appear as deformed or missing curves in the
inspection image. Figure 13-13 shows template target curve scores
obtained for different scenarios.



#### Target Template Curve Score


The target template curve score specifies how closely the curves in the
match region of the inspection, or target, image match the curves in the
template. Score values can range from 0 to 1000, where a score of
1000 indicates that all curves in the match region of the inspection image
have a corresponding curve in the template image.


The target template curve score is computed by combining the match scores
obtained by comparing each curve in the match region to the curves in the
template image.


A low score implies one or both of the following:


•
Some curves, or parts of curves, that are present in the match region of
the inspection image were not found in the template image.


•
The curves found in the inspection image were deformed and did not
perfectly match the template curves.


You can use the target template curve score in inspection tasks to determine
if there were additional curves in the inspection image because of flaws,
such as scratches, or because of spurious objects in the match region that
were not present in the template image. Figure 13-13 shows target template
curve scores obtained for different scenarios.



#### Figure 13-13. Curve Match Scores Returned by Geometric Matching



#### Correlation Score


The correlation score is obtained by computing the correlation value
between the pixel intensities of the template image to the pixel intensities
of the target match. The correlation score is similar to the score returned by
the pattern matching algorithm described in Chapter 12, Pattern Matching.


The correlation score ranges from 0 to 1000. A score of 1000 indicates a
perfect match. The value of the correlation score is always positive. The
algorithm returns the same correlation score for a match whose contrast is
similar to that of the template and for a match whose contrast is a reversed
version of the template.


Note
The Contrast Reversed or inverse outputs of geometric matching indicate whether
the contrast in the match region is the inverse of the contrast in the template.


You can specify regions in the template image that you do not want to use
when computing the correlation score. Use the NI Vision Template Editor
to specify regions in the template that you want to exclude from the
computation of the correlation score.


Template-Target Score = 700
Target-Template Score = 1000


b.
a.
c.


Template-Target Score = 1000
Target-Template Score = 800
