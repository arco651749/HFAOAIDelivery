# Chapter 19: Instrument Readers

> **Part**: `Part IV: Machine Vision` | **Pages**: `339 - 348`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


19
Instrument Readers


This chapter contains information about instrument readers that read
meters, liquid crystal displays (LCDs), and barcodes.



## Introduction


Instrument readers are functions you can use to accelerate the development
of applications that require reading meters, seven segment displays, and
barcodes.



### When to Use


Use instrument readers when you need to obtain information from images
of simple meters, LCD displays, and barcodes.



## Meter Functions


Meter functions simplify and accelerate the development of applications
that require reading values from meters or gauges. These functions provide
high-level vision processes to extract the position of a meter or gauge
needle.


You can use this information to build different applications such as the
calibration of a gauge. Use the functions to compute the base of the needle
and its extremities from an area of interest indicating the initial and the
full-scale position of the needle. You then can use these VIs to read the
position of the needle using parameters computed earlier.


The recognition process consists of the following two phases:


•
A learning phase during which the user must specify the extremities of
the needle


•
An analysis phase during which the current position of the needle is
determined


The meter functions are designed to work with meters or gauges that have
either a dark needle on a light background or a light needle on a dark
background.



## Chapter 19 Instrument Readers



### Meter Algorithm Limits


This section explains the limit conditions of the algorithm used for the
meter functions. The algorithm is fairly insensitive to light variations.


The position of the base of the needle is very important in the detection
process. Carefully draw the lines that indicate the initial and the full-scale
position of the needle. The coordinates of the base and of the points of the
arc curved by the tip of the needle are computed during the setup phase.
These coordinates are used to read the meter during inspection.



## LCD Functions


LCD functions simplify and accelerate the development of applications
that require reading values from seven-segment displays.


Use these functions to extract seven-segment digit information from an
image.


The reading process consists of two phases.


•
A learning phase during which the user specifies an area of interest in
the image to locate the seven-segment display


•
A reading phase during which the area specified by the user is analyzed
to read the seven-segment digit


The NI Vision LCD functions provide the high-level vision processes
required for recognizing and reading seven-segment digit indicators. The
LCD functions are designed for seven-segment displays that use either
LCDs or LEDs composed of electroluminescent indicators or
light-emitting diodes, respectively.


The LCD functions can perform the following tasks:


•
Detect the area around each seven-segment digit from a rectangular
area that contains multiple digits


•
Read the value of a single digit


•
Read the value, sign, and decimal separator of the displayed number



### LCD Algorithm Limits


The following factors can cause a bad detection.


•
Very high horizontal or vertical light drift


•
Very low contrast between the background and the segments


•
Very high level of noise


•
Very low resolution of the image


Each of these factors is quantified to indicate when the algorithm might not
give accurate results.


Light drift is quantified by the difference between the average pixel values
at the top left and the bottom right of the background of the LCD screen.
Detection results might be inaccurate when light drift is greater than 90 in
8-bit images.


Contrast is measured as the difference between the average pixel values
in a rectangular region in the background and a rectangular region in a
segment. This difference must be greater than 30 in 8-bit images, which
have 256 gray levels, to obtain accurate results.


Noise is defined as the standard deviation of the pixel values contained in a
rectangular region in the background. This value must be less than 15 for
8-bit images, which have 256 gray levels, to obtain accurate results.


Each digit must be larger than 18 × 12 pixels to obtain accurate results.



## Barcode Functions


NI Vision currently supports the following barcodes: Code 25, Code 39,
Code 93, Code 128, EAN 8, EAN 13, Codabar, MSI, and UPC A.


The process used to recognize barcodes consists of two phases.


•
A learning phase in which the user specifies an area of interest in the
image which helps to localize the region occupied by the barcode


•
The recognition phase during which the region specified by the user is
analyzed to decode the barcode



### Barcode Algorithm Limits


The following factors can cause errors in the decoding process.


•
Very low resolution of the image


•
Very high horizontal or vertical light drift


•
Contrast along the bars of the image


•
High level of noise


The limit conditions are different for barcodes that have two different
widths of bars and spaces—such as Code 39, Codabar, Code 25, and
MSI code—and for 1D barcodes that have four different widths of bars and
spaces—such as Code 93, Code 128, EAN 13, EAN 8, and UPC A.


The resolution of an image is determined by the width of the smallest bar
and space. These widths must be at least 3 pixels for all barcodes.


Light drift is quantified by the difference between the average of the gray
level of the left, or upper, line and the right, or bottom, line of the
background of the barcode. Decoding inaccuracies can occur if the light
drift is greater than 120 for barcodes with two different widths of bars and
spaces and greater than 100 for barcodes with four different widths of bars
and spaces.


In overexposed images, the gray levels of the wide and narrow bars in the
barcode tend to differ. Decoding results may not be accurate when the
difference in gray levels is less than 80 for barcodes with two different
widths of bars and spaces, and less than 100 for barcodes with four different
widths of bars and spaces.


Consider the difference in gray levels between the narrow bars and the wide
bars. The narrow bars are scarcely visible. If this difference of gray level
exceeds 115 on 8-bit images (256 gray levels) for barcodes with
two different widths of bars and spaces and 100 for barcodes with
four different widths of bars and spaces, the results may be inaccurate.


Noise is defined as the standard deviation of a rectangular region of interest
drawn in the background. It must be less than 57 for barcodes with
two different widths of bars and spaces and less than 27 for barcodes with
four different widths of bars and spaces.


Reflections on the barcode can introduce errors in the value read from the
barcode. Similarly, bars and spaces that are masked by the reflection
produce errors.



## 2D Barcode Functions


The term 2D barcode refers to both matrix barcodes and multi-row
barcodes. Matrix barcodes encode data based on the position of square,
hexagonal, or round cells within a matrix. Multi-row barcodes are barcodes
that consist of multiple stacked rows of barcode data. NI Vision currently
supports Data Matrix and PDF417 2D barcodes.


The process used to recognize 2D barcodes consists of two phases:


•
A coarse locating phase during which the user specifies an ROI in the
image, which helps localize the region occupied by the 2D barcode.
This phase is optional, but it can increase the performance of the
second phase by reducing the size of the search region.


•
A locating and decoding phase during which the software searches the
ROI for one or more 2D barcodes and decodes each located 2D
barcode.



### Data Matrix


A Data Matrix barcode is a matrix built on a square or rectangular grid with
a finder pattern around the perimeter of the matrix. Each cell of the matrix
contains a single data cell. The cells can be either square or circular.
Locating and decoding Data Matrix barcodes requires a minimum cell size
of 2.5 pixels. Each symbol character value is encoded in a unit called a code
word.


Data Matrix barcodes use one of two error checking and correction (ECC)
schemes. Data Matrix barcodes that use the ECC schemes 000 to 140 are
based on the original specification. These barcodes use a convolution error
correction scheme and use a less efficient data packing mechanism that
often requires only encoding characters from a particular portion of the
ASCII character set. Data Matrix barcodes that use the ECC 200 scheme
use a Reed-Solomon error correction algorithm and a more efficient data
packing mechanism. The ECC 200 scheme also allows for the generation
of multiple connected matrices, which enables the encoding of larger data
sets.



#### Quality Grading


NI Vision can assess the quality of a Data Matrix barcode based on how
well the barcode meets certain parameters. For each parameter, NI Vision
returns one of the following letter grades: A, B, C, D, or F. An A indicates
that the barcode meets the highest standard for a particular parameter. An
F indicates that the barcode is of the lowest quality for that parameter.


Data Matrix barcodes are graded on the following parameters:


•
Decode—Tests whether the Data Matrix features are correct enough to
be readable when the barcode is optimally imaged. The barcode is
assigned an A or F, based on whether the decoding is successful or not.
The decode process also locates and defines the area covered by the
barcode in the image, adaptively creates a grid mapping of the data cell
centers, and performs error correction.


•
Symbol Contrast—Tests whether the light and dark pixels in the image
are sufficiently and consistently distinct throughout the barcode. All
pixels are sorted by their reflectance values to determine the darkest
10% and lightest 10%. The mean reflectance of the darkest 10% and
the mean reflectance of the lightest 10% are calculated. The difference
of the two means is the symbol contrast. The following list shows how
the symbol contrast is graded.


–
A (4.0) if symbol contrast ≥ 70%


–
B (3.0) if symbol contrast ≥ 55%


–
C (2.0) if symbol contrast ≥ 40%


–
D (1.0) if symbol contrast ≥ 20%


–
F (0.0) if symbol contrast < 20%


Figure 19-1 shows a Data Matrix barcode with a symbol contrast value
of 8.87%, which returns a grade of F.



#### Figure 19-1. Data Matrix with Poor Contrast


•
Print Growth—Tests the extent to which dark or light markings
appropriately fill their cell boundaries. This parameter is an important
indication of process quality, which affects the reading performance of
the function. The dimensions (D) of the markings are determined by
counting pixels in the image. Horizontal and vertical dimensions are
checked separately. The print growth grade is based on the dimension
with the largest print growth (D'). For each dimension, the following
values are specified:


–
nominal value (Dnom) = 0.50


–
maximum value (Dmax) = 0.65


–
minimum value (Dmin) = 0.35


Normalize each measured D to its corresponding nominal and limit
values:


D' = (D – Dnom) / (Dmax – Dnom) if D > Dnom


= (D – Dnom) / (Dnom – Dmin) otherwise.


The following list shows how print growth is graded.


–
A (4.0) if –0.50 ≤ D' ≤ 0.50


–
B (3.0) if –0.70 ≤ D' ≤ 0.70


–
C (2.0) if –0.85 ≤ D' ≤ 0.85


–
D (1.0) if –1.00 ≤ D' ≤ 1.00


–
F (0.0) if D’ < –1.00 or D’ > 1.00


Figure 19-2 shows a Data Matrix barcode with a print growth value of 0.79,
which returns a grade of C.



#### Figure 19-2. Data Matrix with Print Growth


•
Axial Nonuniformity—Measures and grades the spacing of the cell
centers. Axial nonuniformity tests for uneven scaling of the barcode,
which would inhibit readability at some atypical viewing angles. The
spacings between adjacent sampling points are independently sorted
for each polygonal axis. Then the average spacing (Xavg) along each
axis is computed. Axial nonuniformity is a measure of how much the
sampling point spacing differs from one axis to another.


Axial Nonuniformity = abs(Xavg – Yavg) / ((Xavg + Yavg) / 2)


where abs() yields the absolute value.


The following list shows how axial nonuniformity is graded.


–
A (4.0) if axial nonuniformity ≤ 0.06


–
B (3.0) if axial nonuniformity ≤ 0.08


–
C (2.0) if axial nonuniformity ≤ 0.10


–
D (1.0) if axial nonuniformity ≤ 0.12


–
F (0.0) if axial nonuniformity > 0.12


Figure 19-3 shows a Data Matrix barcode with an axial nonuniformity
value of 0.2714, which returns a grade of F.



#### Figure 19-3. Data Matrix with Axial Nonuniformity


•
Unused Error Correction—Tests the extent to which regional or spot
damage in the symbol has eroded the reading safety margin that the
error correction provides.


The convolutional error encoding for Data Matrix barcodes
ECC 000–ECC 140 can correct for the following maximum
percentages of bit errors (Emax):


–
ECC 000: Emax = 0.0%


–
ECC 050: Emax = 2.8%


–
ECC 080: Emax = 5.5%


–
ECC 100: Emax = 12.6%


–
ECC 140: Emax = 25.0%


The actual percentage of bit errors (Eact) is the number of bits that were
corrected divided by the total number of bits in the symbol’s data
fields. The unused error correction for Data Matrix barcodes
ECC 000–ECC 140 is expressed as


Unused Error Correction = 1.0 – (Eact / Emax)


For ECC 200 barcodes, the correction capacity of the Reed-Solomon
decoding is expressed as


e + 2t ≤ d – p


where
e is the number of erasures
t is the number of errors
d is the number of error correction code words
p is the number of code words reserved for error detection.


Values for d and p are defined by the specification for the given
symbol. Values e and t are determined during a successful decode
process. The amount of unused error correction is computed as


Unused Error Correction = 1.0 – (e + 2t) / (d –p).


In barcodes with more than one Reed-Solomon block, the unused error
correction is calculated for each block independently, and the lowest
value is used to calculate the unused error correction grade.


The following list shows how unused error correction is graded.


–
A (4.0) if unused error correction ≥ 0.62


–
B (3.0) if unused error correction ≥ 0.50


–
C (2.0) if unused error correction ≥ 0.37


–
D (1.0) if unused error correction ≥ 0.25


–
F (0.0) if unused error correction < 0.25


Figure 19-4 shows a Data Matrix barcode with an unused error
correction value of 0.00, which returns a grade of F.



#### Figure 19-4. Data Matrix with Little Unused Error Correction


•
Overall Grade Symbol—The lowest of the grades from the other
symbol parameters.



### PDF417


A PDF417 barcode is a multi-row barcode in which each data element is
encoded in a code word. Each row consists of a start pattern, a left row
indicator code word, one to 30 data code words, a right row indicator code
word, and a stop pattern. Each code word consists of 17 cells and encodes
four bars and four spaces. Each bar and each space has a maximum width
of six cells.


Locating and decoding PDF417 barcodes requires a minimum cell size of
1.5 pixels and a minimum row height of 4.5 pixels.


Locating and decoding PDF417 barcodes also requires a quiet zone of at
least one cell width around the perimeter of the barcode. However, a larger
quiet zone increases the likelihood of successful location.



### 2D Barcode Algorithm Limits


The following factors can cause errors in the search and decoding phase:


•
Very low resolution of the image.


•
Very high horizontal or vertical light drift.


•
Contrast along the bars of the image.


•
High level of noise or blurring.


•
Inconsistent printing or stamping techniques—such as misaligned
barcode elements—inconsistent element size, or elements with
inconsistent borders.


•
In PDF417 barcodes, a quiet zone that is too small or contains too
much noise.
