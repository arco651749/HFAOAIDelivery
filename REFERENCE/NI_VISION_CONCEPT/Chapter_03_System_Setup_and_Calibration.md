# Chapter 3: System Setup and Calibration

> **Part**: `Part I: Vision Basics` | **Pages**: `43 - 60`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


3
System Setup and Calibration


This chapter describes how to set up an imaging system and calibrate
the imaging setup so that you can convert pixel coordinates to real-world
coordinates. Converting pixel coordinates to real-world coordinates is
useful when you need to make accurate measurements from inspection
images using real-world units.



## Setting Up Your Imaging System


Before you acquire, analyze, and process images, you must set up your
imaging system. Five factors comprise a imaging system: field of view,
working distance, resolution, depth of field, and sensor size. Figure 3-1
illustrates these concepts.



## Chapter 3 System Setup and Calibration



### Figure 3-1. Fundamental Parameters of an Imaging System


1
Resolution
2
Field of View


3
Working Distance
4
Sensor Size


5
Depth of Field
6
Image


7
Pixel
8
Pixel Resolution


7


6


8


2


5


3


4


1


•
Resolution—The smallest feature size on your object that the imaging
system can distinguish


•
Pixel resolution—The minimum number of pixels needed to represent
the object under inspection


•
Field of view—The area of the object under inspection that the camera
can acquire


•
Working distance—The distance from the front of the camera lens to
the object under inspection


•
Sensor size—The size of a sensor’s active area, typically defined by the
sensor’s horizontal dimension


•
Depth of field—The maximum object depth that remains in focus


For additional information about the fundamental parameters of an imaging
system, refer to the Application Notes sections of the Edmund Industrial
Optics Optics and Optical Instruments Catalog, or visit Edmund Industrial
Optics at www.edmundoptics.com.



### Acquiring Quality Images


The manner in which you set up your system depends on the type of
analysis and processing you need to do. Your imaging system should
produce images with high enough quality so that you can extract the
information you need from the images. Five factors contribute to overall
image quality: resolution, contrast, depth of field, perspective, and
distortion.



#### Resolution


There are two kinds of resolution to consider when setting up your imaging
system: pixel resolution and resolution. Pixel resolution refers to the
minimum number of pixels you need to represent the object under
inspection. You can determine the pixel resolution you need by the smallest
feature you need to inspect. Try to have at least two pixels represent the
smallest feature. You can use the following equation to determine the
minimum pixel resolution required by your imaging system:


(length of object’s longest axis / size of object’s smallest feature) × 2


If the object does not occupy the entire field of view, the image size will be
greater than the pixel resolution.


Resolution indicates the amount of object detail that the imaging system
can reproduce. Images with low resolution lack detail and often appear


blurry. Three factors contribute to the resolution of your imaging system:
field of view, the camera sensor size, and number of pixels in the sensor.
When you know these three factors, you can determine the focal length of
your camera lens.


Field of View


The field of view is the area of the object under inspection that the camera
can acquire. Figure 3-2 describes the relationship between pixel resolution
and the field of view.



#### Figure 3-2. Relationship between Pixel Resolution and Field of View


Figure 3-2a shows an object that occupies the field of view. Figure 3-2b
shows an object that occupies less space than the field of view. If w is the
size of the smallest feature in the x direction and h is the size of the smallest
feature in the y direction, the minimum x pixel resolution is


and the minimum y pixel resolution is


Choose the larger pixel resolution of the two for your imaging application.


Note
In Figure 3-2b, the image size is larger than the pixel resolution.


a.
b.


h
h


w
w


wfov


hfov


wfov


hfov


wfov
w
---------
2
×


hfov
h
--------
2.
×


Sensor Size and Number of Pixels in the Sensor


The camera sensor size is important in determining your field of view,
which is a key element in determining your minimum resolution
requirement. The sensor’s diagonal length specifies the size of the sensor’s
active area. The number of pixels in your sensor should be greater than or
equal to the pixel resolution. Choose a camera with a sensor that satisfies
your minimum resolution requirement.


Lens Focal Length


When you determine the field of view and appropriate sensor size, you can
decide which type of camera lens meets your imaging needs. A lens is
defined primarily by its focal length. The relationship between the lens,
field of view, and sensor size is as follows:


focal length = (sensor size × working distance) / field of view


If you cannot change the working distance, you are limited in choosing a
focal length for your lens. If you have a fixed working distance and your
focal length is short, your images may appear distorted. However, if you
have the flexibility to change your working distance, modify the distance
so that you can select a lens with the appropriate focal length and minimize
distortion.



#### Contrast


Resolution and contrast are closely related factors contributing to image
quality. Contrast defines the differences in intensity values between the
object under inspection and the background. Your imaging system should
have enough contrast to distinguish objects from the background. Proper
lighting techniques can enhance the contrast of your system.



#### Depth of Field


The depth of field of a lens is its ability to keep objects of varying heights
in focus. If you need to inspect objects with various heights, chose a lens
that can maintain the image quality you need as the objects move closer to
and further from the lens.



#### Perspective


Perspective errors often occur when the camera axis is not perpendicular to
the object you are inspecting. Figure 3-3a shows an ideal camera position.
Figure 3-3b shows a camera imaging an object from an angle.



#### Figure 3-3. Camera Angle Relative to the Object under Inspection


Perspective errors appear as changes in the object’s magnification
depending on the object’s distance from the lens. Figure 3-4a shows a grid
of dots. Figure 3-4b illustrates perspective errors caused by a camera
imaging the grid from an angle.



#### Figure 3-4. Perspective and Distortion Errors


Try to position your camera perpendicular to the object you are trying
to inspect to reduce perspective errors. If you need to take precise
measurements from your image, correct perspective error by applying
calibration techniques to your image.


1
Lens Distortion
2
Perspective Error
3
Known Orientation Offset


3


2


1


a.
b.


a.
c.
b.



#### Distortion


Nonlinear distortion is a geometric aberration caused by optical errors in
the camera lens. A typical camera lens introduces radial distortion. This
causes points that are away from the lens’s optical center to appear further
away from the center than they really are. Figure 3-4c illustrates the effect
of distortion on a grid of dots. When distortion occurs, information in the
image is misplaced relative to the center of the field of view, but the
information is not necessarily lost. Therefore, you can undistort your image
through spatial calibration.



## Spatial Calibration


Spatial calibration is the process of computing pixel to real-world unit
transformations while accounting for many errors inherent to the imaging
setup. Calibrating your imaging setup is important when you need to make
accurate measurements in real-world units.


An image contains information in the form of pixels. Spatial calibration
allows you to translate a measurement from pixel units into another unit,
such as inches or centimeters. This conversion is easy if you know a
conversion ratio between pixels and real-world units. For example, if
one pixel equals one inch, a length measurement of 10 pixels equals
10 inches.


This conversion may not be straightforward because perspective projection
and lens distortion affect the measurement in pixels. Calibration accounts
for possible errors by constructing mappings that you can use to convert
between pixel and real world units. You also can use the calibration
information to correct perspective or nonlinear distortion errors for image
display and shape measurements.



### When to Use


Calibrate your imaging system when you need to make accurate and
reliable measurements. Use the NI Vision calibration tools to do the
following:


•
Calibrate your imaging setup automatically by imaging a standard
pattern, such as a calibration template, or by providing reference points


•
Convert measurements—such as lengths, areas, widths—from
real-world units to pixel units and back


•
Apply a learned calibration mapping to correct an image acquired
through a calibrated setup


•
Assign an arbitrary coordinate system to measure positions in
real-world units


•
Make real-world measurements on binary images



### Concepts


To calibrate an imaging setup, the calibration software uses a set of known
mappings between points in the image and their corresponding locations in
the real world. The calibration software uses these known mappings to
compute the pixel to real-world mapping for the entire image. The resulting
calibration information is valid only for the imaging setup that you used to
create the mapping. Any change in the imaging setup that violates the
mapping information compromises the accuracy of the calibration
information.



#### Calibration Process


The calibration software requires a list of known pixel to real-world
mappings to compute calibration information for the entire image.
You can specify the list in two ways.


•
Image a grid of dots similar to the one shown in Figure 3-5a. Input the
dx and dy spacing between the dots in real-world units. The calibration
software uses the image of the grid, shown in Figure 3-5b, and the
spacing between the dots in the grid to generate the list of pixel to
real-world mappings required for the calibration process.


•
Input a list of real world points and the corresponding pixel
coordinates directly to the calibration software.



#### Figure 3-5. Calibration Setup


a.


dy


dx


b.


The calibration process uses the list of pixel to real-world mappings and
a user-defined algorithm to create a mapping for the entire image. The
calibration software also generates an error map. An error map returns an
estimate of the worst case error when a pixel coordinate is transformed into
a real-world coordinate.


Use the calibration information obtained from the calibration process to
convert any pixel coordinate to its real-world coordinate and back.



#### Coordinate System


To express measurements in real-world units, you must define a coordinate
system. Define a coordinate system by its origin, angle, and axis direction.
Figure 3-6a shows the coordinate system of a calibration grid in the real
world. Figure 3-6b shows the coordinate system of an image of the
corresponding calibration grid. The origin, expressed in pixels, defines the
center of your coordinate system. The origins of the coordinate systems
depicted in Figure 3-6 lie at the center of the circled dots. The angle
specifies the orientation of your coordinate system with respect to the
horizontal axis in the real world. Notice in Figure 3-6b that the horizontal
axis automatically aligns to the top row of dots in the image of the grid.
The calibration procedure determines the direction of the horizontal axis
in the real world, which is along the topmost row of dots in the image of
the grid.



#### Figure 3-6. Origin and Angle of a Coordinate System


1
Origin in the Real World Grid
2
Origin in the Grid Image


y


x


a.


y


x


b.


1
2


The second axis direction can be either indirect, as shown in Figure 3-7a,
or direct, as shown in Figure 3-7b. The indirect axis orientation
corresponds to the way a coordinate system is present in digital images.
The direct axis orientation corresponds to the way a coordinate system is
present in the real world.



#### Figure 3-7. Axis Direction of a Coordinate System


If you do not specify a coordinate system, the calibration process defines a
default coordinate system, as follows:


1.
The origin is placed at the center of the left, topmost dot in the
calibration grid.


2.
The angle is set to zero. This aligns the x-axis with the topmost row
of dots in the grid.


3.
The axis direction is set to indirect. This aligns the y-axis to the
leftmost column of the dots in the grid.


If you specify a list of points instead of a grid for the calibration process,
the software defines a default coordinate system, as follows:


1.
The origin is placed at the point in the list with the lowest x-coordinate
value and then the lowest y-coordinate value.


2.
The angle is set to zero.


3.
The axis direction is set to indirect.


If you define a coordinate system yourself, remember the following:


•
Express the origin in pixels. Always choose an origin location that lies
within the calibration grid so that you can convert the location to
real-world units.


•
Specify the angle as the angle between the new coordinate system and
the horizontal direction in the real world. If your imaging system has
perspective errors but no lens distortion, this angle can be visualized as
shown in Figure 3-11. However, if your images exhibit nonlinear
distortion, visualizing the coordinate system in the image is not trivial.


X


Y
X


Y


a. Indirect
b. Direct



#### Calibration Algorithms


NI Vision has two algorithms for calibration: perspective and nonlinear.
Perspective calibration corrects for perspective errors, and nonlinear
calibration corrects for perspective errors and nonlinear lens distortion.
Learning for perspective is faster than learning for nonlinear distortion.


The perspective algorithm computes one pixel to real-world mapping for
the entire image. You can use this mapping to convert the coordinates of
any pixel in the image to real-world units.


The nonlinear algorithm computes pixel to real-world mappings in a
rectangular region centered around each dot in the calibration grid, as
shown in Figure 3-8. NI Vision estimates the mapping information around
each dot based on its neighboring dots. You can convert pixel units to
real-world units within the area covered by the grid dots. Because NI Vision
computes the mappings around each dot, only the area in the image covered
by the grid dots is calibrated accurately.


The calibration ROI output of the calibration function defines the region of
the image in which the calibration information is accurate. The calibration
ROI in the perspective method encompasses the entire image. The
calibration ROI in the nonlinear method encompasses the bounding
rectangle that encloses all the rectangular regions around the grid dots.
Figure 3-8 illustrates the calibration ROI concept.



#### Figure 3-8. Calibrating ROIs


1
Calibration ROI Using the Perspective Algorithm
2
Calibration ROI Using the Nonlinear Algorithm
3
Rectangular Region Surrounding Each Dot


1


2


3


Note
You can convert pixels that lie outside the calibration ROI to real-world units, but
these conversions may be inaccurate.



#### Calibration Quality Information


The quality score and error map outputs of the calibration function indicate
how well your system is calibrated.


The quality score, which ranges from 0 to 1,000, reflects how well the
calibration function learned the grid or set of points you provided. The
quality score does not reflect the accuracy of the calibration, but rather
describes how well the calibration mapping adapts to the learned grid or
feature points.


Use the quality score to determine whether the calibration algorithm you
chose is adequate. NI Vision returns a low quality score if you calibrate an
image with high nonlinear distortion using the perspective method or if you
use a sparse grid to calibrate an image with high nonlinear distortion.


You also can use this score to gauge whether the setup is behaving as
expected. For example, if you are using a lens with very little lens
distortion, perspective calibration should produce accurate results.
However, system setup problems, such as a physically distorted calibration
template, may cause a low quality score regardless of your lens quality.


The error map is an estimate of the positional error that you can expect
when you convert a pixel coordinate into a real-world coordinate. The error
map is a 2D array that contains the expected positional error for each pixel
in the image. The error value of the pixel coordinate (i, j) indicates the
largest possible location error for the estimated real-world coordinate (x, y)
as compared to the true real-world location. The following equation shows
how to calculate the error value.


The error value indicates the radical distance from the true real world
position in which the estimated real world coordinates can live. The error
value has a confidence interval of 95%, which implies that the positional
error of the estimated real-world coordinate is equal to or smaller than the
error value 95% of the time. A pixel coordinate with a small error value
indicates that its estimated real-world coordinate is computed very
accurately. A large error value indicates that the estimated real-world
coordinate for a pixel may not be accurate.


e i j,
(
)
x
xtrue
–
(
)2
y
ytrue
–
(
)2
+
=


Use the error map to determine whether your imaging setup and calibration
information satisfy the accuracy requirements of your inspection
application. If the error values are greater than the positional errors that
your application can tolerate, you need to improve your imaging setup.
An imaging system with high lens distortion usually results in an error map
with high values. If you are using a lens with considerable distortion, you
can use the error map to determine the position of the pixels that satisfy
your application’s accuracy requirements. Because the effect of lens
distortion increases toward the image borders, pixels close to the center
of the image have lower error values than the pixels at the image borders.



#### Image Correction


Image correction involves transforming a distorted image acquired
in a calibrated setup into an image where perspective errors and lens
distortion are corrected. NI Vision corrects an image by applying
the transformation from pixel to real-world coordinates for each pixel
in the input image. Then NI Vision applies simple shift and scaling
transformations to position the real-world coordinates into a new image.
NI Vision uses interpolation during the scaling process to generate the new
image.


When you learn for correction, you have the option of constructing a
correction table. The correction table is a lookup table, stored in memory,
that contains the real-world location information of all the pixels in the
image. The lookup table greatly increases the speed of image correction but
requires more memory and increases your learning time. Use this option
when you want to correct several images at a time in your vision
application.


Tip
Correcting images is a time-intensive operation. You may be able to get the
measurements you need without image correction. For example, you can use NI Vision
particle analysis functions to compute calibrated measurements directly from an image that
contains calibration information but has not been corrected. Also, you can convert pixel
coordinates returned by edge detection tools into real-world coordinates. Refer to
Chapter 5, Performing Machine Vision Tasks, of your NI Vision user manual for more
information.



#### Scaling Mode


The scaling mode defines how to scale a corrected image. Two scaling
mode options are available: scale to fit and scale to preserve area.
Figure 3-9 illustrates the scaling modes. Figure 3-9a shows the original
image. With the scale to fit option, the corrected image is scaled to fit in an
image the same size as the original image, as shown in Figure 3-9b. With
the scale to preserve area option, the corrected image is scaled such that
features in the image retain the same area as they did in the original image,
as shown in Figure 3-9c. Images that are scaled to preserve area are usually
larger than the original image. Because scaling to preserve the area
increases the size of the image, the processing time for the function may
increase.



#### Figure 3-9. Scaling Modes


The scaling mode you choose depends on your application. Scale to
preserve the area when your vision application requires the true area of
objects in the image. Use scale to fit for all other vision applications.



#### Correction Region


You can correct an entire image or regions in the image based on
user-defined ROIs or the calibration ROI defined by the calibration
software. Figure 3-10 illustrates the different image areas you can specify
for correction. NI Vision learns calibration information for only the regions
you specify.


a.
b.
c.



#### Figure 3-10. ROI Modes


•
Full Image—Corrects the entire image regardless of the calibration
ROI and the user-defined ROI.


•
User or Calibration ROI—Corrects pixels in both the user-defined ROI
and the calibration ROI.


•
User ROI—Corrects only the pixels inside the user-defined ROI
specified during the learn calibration phase.


•
User and Calibration ROI—Corrects only the pixels that lie in the
intersection of the user-defined ROI and the calibration ROI.


•
Calibration ROI—Corrects only the pixels inside the calibration ROI.
The calibration ROI is computed by the calibration algorithm.


The valid coordinate indicates whether the pixel coordinate you are trying
to map to a real-world coordinate lies within the image region you
corrected. For example, if you corrected only the pixels within the
calibration ROI but you try to map a pixel outside the calibration ROI to
real-world coordinates, the Corrected Image Learn ROI parameter
indicates an error.


1
Full Image
2
User or Calibration ROI
3
User ROI


4
User and Calibration ROI
5
Calibration ROI


4


3


1


2


5



#### Simple Calibration


When your camera axis is perpendicular to the image plane and lens
distortion is negligible, you can use simple calibration to calibrate your
imaging setup. In simple calibration, a pixel coordinate is transformed to
a real-world coordinate through scaling in the x (horizontal) and y (vertical)
directions.


Simple calibration maps pixel coordinates to real-world coordinates
directly without a calibration grid. The software rotates and scales a pixel
coordinate according to predefined coordinate reference and scaling
factors.


To perform a simple calibration, define a coordinate system and scaling
mode. Figure 3-11 illustrates how to define a coordinate system. To set a
coordinate reference, define the angle between the x-axis and the horizontal
axis of the image in degrees. Express the center as the position, in pixels,
where you want the coordinate reference origin. Set the axis direction to
direct or indirect. Set the scaling mode option to scale to fit or scale to
preserve area. Simple calibration also offers a correction table option.


Note
If you use simple calibration with the angle set to 0, you do not need to learn for
correction because you do not need to correct your image.



#### Figure 3-11. Defining a New Coordinate System


1
Default Origin
2
New Origin


x


y


y'


x'


y


x


2


1



#### Redefining a Coordinate System


You can use simple calibration to change the coordinate system assigned to
a calibrated image. When you define a new coordinate system, remember
the following:


•
Express the origin in pixels. Always choose an origin location that lies
within the calibration grid so that you can convert the location to
real-world units.


•
Specify the angle as the angle between the new coordinate system and
the horizontal direction in the real world.


In some vision applications, you may need to image several regions of
an object to inspect it completely. You can image these different regions
by moving the object until the desired region lies under the camera or by
moving the camera so that it lies above the desired region. In either case,
each image maps to different regions in the real world. You can specify a
new position for the origin and orientation of the coordinate system so that
the origin lies on a point on the object under inspection.


Figure 3-12 shows an inspection application whose objective is to
determine the location of the hole in the board with respect to the corner of
the board. The board is on a stage that can translate in the x and y directions
and can rotate about its center. The corner of the board is located at the
center of the stage.


In the initial setup, shown in Figure 3-12a, you define a coordinate system
that aligns with the corner of the board using simple calibration. Specify the
origin of the coordinate system as the location in pixels of the corner of the
board, set the angle of the axis to 180°, and set the axis direction to indirect.
Use pattern matching to find the location in pixels of the hole, which is
indicated by the crosshair mark in Figure 3-12a. Convert the location of the
hole in pixels to a real world location. This conversion returns the real
world location of the hole with respect to the defined coordinate system.


During the inspection process, the stage may translate and rotate by a
known amount. This causes the board to occupy a new location in the
camera’s field of view, which makes the board appear translated and rotated
in subsequent images, as shown in Figure 3-12b. Because the board has
moved, the original coordinate system no longer aligns with the corner of
the board. Therefore, measurements made using this coordinate system will
be inaccurate.


Use the information about how much the stage has moved to determine
the new location of the corner of the board in the image and update the


coordinate system using simple calibration to reflect this change. The
origin of the updated coordinate reference system becomes the new pixel
location of the corner of the board, and the angle of the coordinate system
is the angle by which the stage has rotated.


The updated coordinate system is shown in Figure 3-12c. Measurements
made with the new coordinate system are accurate.



#### Figure 3-12. Moving Coordinate System


X


Y


a.


X


Y


b.


X


Y


c.
