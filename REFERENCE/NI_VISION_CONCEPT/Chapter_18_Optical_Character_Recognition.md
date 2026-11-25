# Chapter 18: Optical Character Recognition

> **Part**: `Part IV: Machine Vision` | **Pages**: `325 - 338`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


18
Optical Character Recognition


This chapter contains information about optical character recognition
(OCR).



## Introduction


OCR provides machine vision functions you can use in an application to
perform OCR. OCR is the process by which the machine vision software
reads text and/or characters in an image. OCR consists of the following
two parts:


•
An application for training characters


•
Tools such as the NI Vision Builder for Automated Inspection software
or libraries of LabVIEW VIs, LabWindows/CVI functions, and
Microsoft Visual Basic properties and methods. Use these tools to
create a machine vision application that analyzes an image and
compares objects in that image to the characters you trained to
determine if they match. The machine vision application returns the
matching characters that it read.


Training characters is the process by which you teach the machine vision
software the types of characters and/or patterns you want to read in the
image during the reading procedure. You can use OCR to train any number
of characters, creating a character set. The set of characters is later
compared with objects during the reading and verifying procedures. You
store the character set in a character set file. Training might be a one-time
process, or it might be a process you repeat several times, creating several
character sets to broaden the scope of characters you want to detect in an
image.


Reading characters is the process by which the machine vision application
you create analyzes an image to determine if the objects match the
characters you trained. The machine vision application reads characters
in an image using the character set that you created when you trained
characters.



## Chapter 18 Optical Character Recognition


Verifying characters is a process by which the machine vision application
you create inspects an image to verify the quality of the characters it read.
The application verifies characters in an image using the reference
characters of the character set you created during the training process.



## When to Use


Typically, machine vision OCR is used in automated inspection
applications to identify or classify components. For example, you can use
OCR to detect and analyze the serial number on an automobile engine that
is moving along a production line. Using OCR in this instance helps you
identify the part quickly, which in turn helps you quickly select the
appropriate inspection process for the part.


You can use OCR in a wide variety of other machine vision applications,
such as the following:


•
Inspecting pill bottle labels and lot codes in pharmaceutical
applications


•
Verifying wafers and IC package codes in semiconductor applications


•
Controlling the quality of stamped machine parts


•
Sorting and tracking mail packages and parcels


•
Reading alphanumeric characters on automotive parts



## Training Characters


Training involves teaching OCR the characters and/or patterns you want to
detect during the reading procedure.


All the characters that have been trained with the same character value form
a character class. You can designate the trained character that best
represents the character value as the reference character for the character
class.


Figure 18-1 illustrates the steps involved in the training procedure.



### Figure 18-1. Steps of an OCR Training Procedure


Note
The diagram item enclosed in dashed lines is an optional step.


The process of locating characters in an image is often referred to as
character segmentation. Before you can train characters, you must set up
OCR to determine the criteria that segment the characters you want to train.
When you finish segmenting the characters, use OCR to train the
characters, storing information that enables OCR to recognize the same
characters in other images. You train the OCR software by providing a
character value for each of the segmented characters, creating a unique
representation of each segmented character. You then save the character set
to a character set file to use later in an OCR reading procedure.


Specify ROI


Acquire
Image


OCR Extracts
Feature Information
for Each Character


Assign a Character
Value to Each
Segmented Character


Save Character Set to
Character Set File


OCR Separates
Each Character from
Image Background


Assign a Reference
Character to Each
Character Class


Refer to the NI OCR Training Interface Help that ships with the NI OCR
Training Interface for information about setting up and training characters
using OCR.



## Reading Characters


When you perform the reading procedure, the machine vision application
you create with OCR functions segments each object in the image and
compares it to characters in the character set you created during the training
procedure. OCR extracts unique features from each segmented object in the
image and compares each object to each character stored in the character
set. OCR returns the character value of the character in the character set that
best matches the object and returns a nonzero classification score. If no
character in the character set matches the object, OCR returns the
substitution character as the character value and returns a classification
score of zero. After reading, you can perform an optional verifying
procedure to verify the quality of printed characters.


Refer to Chapter 5, Performing Machine Vision Tasks, of the NI Vision
user manual for your ADE to get information about using OCR to read and
analyze images for trained characters.


Figure 18-2 illustrates the steps involved in the reading procedure.



### Figure 18-2. Steps of an OCR Reading Procedure


Note
The diagram item enclosed in dashed lines is an optional step.


Specify ROI


Acquire
Image
Load Character
Set File


OCR Extracts
Feature Information
For Each Character


OCR Returns
Recognized
Characters


OCR Compares
Characters To
Character Set


OCR Separates
Each Character From
Image Background


Open OCR
Session


OCR Verifies
Recognized
Characters



## OCR Session


An OCR session applies to both the training and reading procedures. An
OCR session prepares the software to identify a set of characters during
either the training procedure or the reading procedure. A session consists
of the properties you set and the character set that you train or read from a
file. OCR uses session information to compare objects with trained
characters to determine if they match. If you want to process an image
containing characters that you stored in multiple character sets, use
multiple OCR sessions simultaneously to read all the characters
simultaneously.


You also can merge several character sets in one session. If you choose to
merge multiple character sets, train each of the character sets with the same
segmentation parameters.



## Concepts and Terminology


The following sections describe OCR concepts and terminology.



### Region of Interest (ROI)


The ROI applies to both the training and reading procedures. During
training, the ROI is the region that contains the objects you want to train.
During reading, the ROI is the region that contains the objects you want to
read by comparing the objects to the character set. You can use the ROI to
effectively increase the accuracy and efficiency of OCR. During training,
you can use the ROI to carefully specify the region in the image that
contains the objects you want to train while excluding artifacts. During
reading, you can use the ROI to enclose only the objects you want to read,
which reduces processing time by limiting the area OCR must analyze.


Note
An ROI must contain only one line of text to train or read.



### Particles, Elements, Objects, and Characters


Particles, elements, objects, and characters apply to both the training and
reading procedures. Particles are groups of connected pixels. Elements are
particles that are part of an object. For example, the dots in a dot-matrix
object are elements. A group of one or more elements forms an object based
on the element spacing criteria. A character is a trained object.


Refer to the Element Spacing section of this chapter for information about
element spacing.



### Patterns


Patterns are characters for which the character value is a string of more
than one character. For example, a logo is a pattern because it requires a
string of more than one character to describe it. Non-ASCII characters are
also patterns.



### Character Segmentation


Character segmentation applies to both the training and reading procedures.
Character segmentation refers to the process of locating and separating
each character in the image from the background.


Figure 18-3 illustrates the concepts included in the character segmentation
process.



#### Figure 18-3. Concepts Involved in Character Segmentation



#### Thresholding


Thresholding is one of the most important concepts in the segmentation
process. Thresholding is separating image pixels into foreground and
background pixels based on their intensity values. Foreground pixels are
those whose intensity values are within the lower and upper threshold


1
Acquired Image
2
ROI
3
Character Bounding Rectangle
4
Character
5
Artifact


6
Element
7
Vertical Element Spacing
8
Horizontal Element Spacing
9
Character Spacing


1


2


3


4


6
5


7
8
9


values of the threshold range. Background pixels are pixels whose intensity
values lie outside the lower and upper threshold values of the threshold
range.


OCR includes one manual method and three automatic methods of
calculating the thresholding range:


•
Fixed Range is a method by which you manually set the threshold
value. This method processes grayscale images quickly, but requires
that lighting remain uniform across the ROI and constant from image
to image.


The following three automatic thresholding methods are affected by
the pixel intensity of the objects in the ROI. If the objects are dark on
a light background, the automatic methods calculate the high threshold
value and set the low threshold value to the lower value of the
threshold limits. If the objects are light on a dark background, the
automatic methods calculate the low threshold value and set the high
threshold value to the upper value of the threshold limits.


•
Uniform is a method by which OCR calculates a single threshold
value and uses that value to extract pixels from items across the entire
ROI. This method is fast and is the best option when lighting remains
uniform across the ROI.


•
Linear is a method that divides the ROI into blocks, calculates
different threshold values for the blocks on the left and right side of an
ROI, and linearly interpolates values for the blocks in between. This
method is useful when one side of the ROI is brighter than the other
and the light intensity changes uniformly across the ROI.


•
Non linear is a method that divides the ROI into blocks, calculates a
threshold value for each block, and uses the resulting value to extract
pixel data.


OCR includes a method by which you can improve performance during
automatic thresholding, which includes the Uniform, Linear, and
Non linear methods:


•
Optimize for Speed allows you to determine if accuracy or speed
takes precedence in the threshold calculation algorithm. If speed takes
precedence, enable Optimize for Speed to perform the thresholding
calculation more quickly, but less accurately. If accuracy takes
precedence, disable Optimize for Speed to perform the thresholding
calculation more slowly, but more accurately.


If you enable Optimize for Speed, you also can enable Bi modal
calculation to configure OCR to calculate both the lower and upper
threshold levels for images that are dominated by two pixel intensity
levels.



#### Threshold Limits


Threshold limits are bounds on the value of the threshold calculated by the
automatic threshold calculation algorithms. For example, if the threshold
limits are 10 and 240, OCR uses only intensities between 10 and 240 as the
threshold value. Use the threshold limits to prevent the OCR automatic
threshold algorithms from returning too low or too high values for the
threshold in a noisy image or an image that contains a low population of
dark or light pixels. The default range is 0 to 255.



#### Character Spacing


Character spacing is the horizontal distance, in pixels, between the right
edge of one character bounding rectangle and the left edge of the next
character bounding rectangle.


If an image consists of segmented or dot-matrix characters and the spacing
between two characters is less than the spacing between the elements of a
character, you must use individual ROIs around each character. Refer to
Figure 18-3 for more information about character spacing.



#### Element Spacing


Element spacing consists of horizontal element spacing and vertical
element spacing. Horizontal element spacing is the space between two
horizontally adjacent elements. Set this value to 1 or 2 for stroke characters
and 4 or 5 for dot-matrix or segmented characters. Dot-matrix or segmented
characters are characters comprised of a series of small elements. Stroke
characters are continuous characters in which breaks are due only to
imperfections in the image. If you set the horizontal element spacing too
low, you might accidentally eliminate elements of an object. If you set the
horizontal element spacing too high, you might include extraneous
elements in the object, resulting in a trained object that does not represent
a matchable character.


Vertical element spacing is the space between two vertically adjacent
elements. Use the default value, 0, to consider all elements within the
vertical direction of the ROI to be part of an object. If you set vertical
element spacing too high, you might include artifacts as part of an object.


If you set vertical element spacing too low, you might eliminate elements
that are part of a valid object. Refer to Figure 18-3 for more information
about horizontal and vertical element spacing.


Figure 18-4 demonstrates how character spacing and element spacing
affect OCR.



#### Figure 18-4. Concepts Involved in Character Segmentation


Item 2 represents an image for which the horizontal element spacing was
set incorrectly. The letters O and R are divided vertically because horizontal
element spacing was set too low and the OCR segmentation process did not
detect that the elements represent a single character. The letter C is trained
correctly because the horizontal element spacing value falls within the
range that applies to this character. Item 3 represents an image for which
the character spacing value was set too high, and thus OCR segments all
three letters into one character.


1
Correct Image
2
Incorrect Element Spacing


3
Incorrect Character Spacing


1


3


2



#### Character Bounding Rectangle


The character bounding rectangle is the smallest rectangle that completely
encloses a character. Refer to Figure 18-3 for more information about
character bounding rectangles.



#### AutoSplit


AutoSplit applies to both the training and reading procedures. Use
AutoSplit when an image contains characters that are slanted. AutoSplit,
which works in conjunction with the maximum character bounding
rectangle width, uses an algorithm to analyze the right side of a character
bounding rectangle and determine the rightmost vertical line in the object
that contains the fewest number of pixels. AutoSplit moves the rightmost
edge of the character bounding rectangle to that location. The default value
is False.



#### Character Size


Character size is the total number of pixels in a character. Generally,
character size should be between 25 and 40 pixels. If characters are too
small, training becomes difficult because of the limited data. The additional
data included with large characters is not helpful in the OCR process, and
the large characters can cause the reading process to become very slow.


Tip
You can adjust the character size to filter small particles.



### Substitution Character


Substitution character applies to the reading procedure only. OCR uses the
substitution character for unrecognized characters. The substitution
character is a question mark (?) by default.



### Acceptance Level


Acceptance level applies to the reading procedure. Acceptance level is a
value that indicates how closely a read character must match a trained
character to be recognized. Refer to the Classification Score section of this
chapter for more information about how the acceptance level affects
character recognition. The valid range for this value is 0 to 1000. The
default value is 700. Experiment with different values to determine which
value works best for your application.



### Read Strategy


Read strategy applies only to the reading procedure. Read strategy refers
to the criteria OCR uses to determine if a character matches a trained
character in the character set. The possible modes are Aggressive and
Conservative. In Aggressive mode, the reading procedure uses fewer
criteria than Conservative mode to determine if an object matches a
trained character. Aggressive mode works well for most applications.
In Conservative mode, the reading procedure uses extensive criteria to
determine if an object matches a trained character.


Note
Conservative mode might result in OCR not recognizing characters. Test your
application with Conservative mode before deciding to use it.



### Read Resolution


Read resolution applies to the reading procedure. When you save a
character set, OCR saves a variety of information about each character in
the character set. Read resolution is the level of character detail OCR uses
to determine if an object matches a trained character. By default, OCR uses
a low read resolution, using few details to determine if there is a match
between an object and a trained character. The low read resolution enables
OCR to perform the reading procedure more quickly. You can configure
OCR to use a medium or high read resolution, and therefore use more
details to determine if an object matches a trained character. Using a high
read resolution reduces the speed at which OCR processes.


The low resolution works well with most applications, but some
applications might require the higher level of detail available in medium or
high resolutions.


Note
Using medium or high resolution might result in OCR not recognizing characters. If
you choose to use medium or high resolution, test your application thoroughly.



### Valid Characters


Valid characters applies only to the reading procedure. Valid characters
refers to the practice of limiting the characters that the reading procedure
uses when analyzing an image. For example, if you know that the first
character in an ROI should be a number, you can limit the reading
procedure to comparing the first character in the ROI only to numbers in
the character set. Limiting the characters that the reading procedure uses
when analyzing an image increases the speed and accuracy of OCR.



### Aspect Ratio Independence


Aspect ratio independence applies only to the reading procedure. Aspect
ratio independence is the ability to read characters at a different size and
height/width ratio than the training size and height/width ratio. To maintain
performance in the OCR process, National Instruments recommends you
limit the difference to ±50%. Avoid creating character sets whose
characters differ only in height and width. Consider separating the
characters into different character sets, using valid characters to restrict
trained characters, and enforcing the aspect ratio.



### OCR Scores


The following sections describe the scores returned by the reading
procedure.



#### Classification Score


The classification score indicates the degree to which the assigned
character class represents the input object better than other character
classes in the character set. It is defined as follows:


Classification Score = (1– d1 / d2) × 1000


where d1 is the distance of the object to the best match in the closest class,
and d2 is the distance of the object to the best match in the second closest
class. Distance is defined as a measure of the differences between the object
and a trained character. The smaller the distance, the closer the object is to
the trained character. Because d1 ≤d2, the classification score is between
0 and 1000. A trained character is considered a match only if the distance
between the object and the trained character is smaller than a value
controlled by the acceptance level. The larger the acceptance level, the
smaller the distance between the object and the trained character has to be
for OCR to match the object.



#### Verification Score


If an input object belongs to a character class for which a reference
character has been designated, OCR compares the object to the reference
character and outputs a score the indicates how closely the input object
matches the reference character. The score ranges from 0 to 1000, where
0 represents no similarity and 1000 represents a perfect match. You can use
this score to verify the quality of printed characters.



### Removing Small Particles


Removing small particles applies to both the training and reading
procedures. The process of removing small particles involves applying a
user-specified number of 3 × 3 erosions to the thresholded image. OCR
fully restores any objects that remain after applying the erosions. For
example, in Figure 18-5, if any portion of the letters X and G remains after
removing small particles, OCR fully restores the X and G.



#### Figure 18-5. Unwanted Particles



### Removing Particles That Touch the ROI


Removing particles that touch the ROI applies to both the training and
reading procedures. You can configure OCR to remove small particles that
touch an ROI you specified. Refer to Figure 18-6 for examples of particles
that touch the ROI.



#### Figure 18-6. Particles that Touch the ROI


1
Particle


1
Particle to Remove
2
Artifact to Remove
3
ROI


1


2
3


1
1
