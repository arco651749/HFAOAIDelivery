# Chapter 17: Golden Template Comparison

> **Part**: `Part IV: Machine Vision` | **Pages**: `319 - 324`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


17
Golden Template Comparison


This chapter contains information about inspection based on golden
template comparison.



## Introduction


Golden template comparison compares the pixel intensities of an image
under inspection to a golden template. A golden template is an image
containing an ideal representation of an object under inspection. A pixel in
an inspection image is returned as a defect if it does not match the
corresponding pixel in the golden template within a specified tolerance.



## When to Use


Inspection based on golden template comparison is a common vision
application. Use golden template comparison when you want to inspect for
defects, and other methods of defect detection are not feasible. To use
golden template comparison, you must be able to acquire an image that
represents the ideal inspection image for your application.


Example applications in which golden template comparison would be
effective include validating a printed label or a logo stamped on a part.



## Concepts


Conceptually, inspection based on golden template comparison is simple:
Subtract an image of an ideal part and another image of a part under
inspection. Any visible defects on the inspected part show up as differences
in intensity in the resulting defect image. Figure 17-1 illustrates this
concept.



## Chapter 17 Golden Template Comparison



### Figure 17-1. Golden Template Comparison Defects Overlaid on Image


Figure 17-1a shows the golden template in a label inspection application.
Figure 17-1b shows the inspection image. Figure 17-1c show the resulting
defect image. Defect areas in which the inspection image was brighter than
the template are overlaid in green. Defect areas in which the inspection
image was darker than the template are overlaid in red.


Using simple subtraction to detect flaws does not take into account several
factors about the application that may affect the comparison result. The
following sections discuss these factors and explain how NI Vision
compensates for them during golden template comparison.



### Alignment


In most applications, the location of the part in the golden template and the
location of the part in the inspection image differ. Figure 17-2 illustrates
this concept and shows how differing part locations affect inspection.



#### Figure 17-2. Misalignment of the Template and Inspection Image


a.
b.
c.


a.
b.
c.


Figure 17-2a shows the golden template. Figure 17-2b shows the
inspection image. The label in the inspection image is identical to the label
in the golden template. However, the part in the inspection image is located
slightly higher and to the right compared to the part in the golden template.


Figure 17-2c shows the resulting defect image. The top and right areas of
the label are detected as dark defects compared to their corresponding
pixels in the template, which are white background pixels. Similarly, the
left and bottom appear as bright defects. The text and logo inside the label
also appear as defects because of the part misalignment.


Aligning the part in the template with the part in the inspection image is
necessary for an effective golden template comparison. To align the parts,
you must specify a location, angle, and scale at which to superimpose the
golden template on the inspection image. You can use the position, angle,
and scale defined by other NI Vision functions, such as pattern matching,
or geometric matching, or edge detection.



### Perspective Correction


The part under inspection may appear at a different perspective in the
inspection image than the perspective of the part in the golden template.
Figure 17-3 illustrates this concept and shows how differing image
perspectives affect inspection.



#### Figure 17-3. Perspective Differences between the Template and Inspection Image


Figure 17-3a shows the golden template. Figure 17-3b shows the
inspection image. The label in the inspection image is identical to the label
in the golden template. However, the left side of the part in the inspection
image is closer to the camera than the right side of the part, giving the part
a warped perspective appearance.


a.
b.
c.


Figure 17-3c shows the resulting defect image. Although the angles and
scales of the labels are the same, the template is still misaligned because of
the perspective difference.


Golden template comparison corrects for perspective differences by
correlating the template and inspection image at several points. Not only
does this correlation compute a more accurate alignment, but it can also
correct for errors of up to two pixels in the input alignment.



### Histogram Matching


The inspection images may be acquired under different lighting conditions
than the golden template. As a result the intensities between a pixel in the
golden template and its corresponding pixel in an inspection image may
vary significantly. Figure 17-4 illustrates this concept and shows how
differing pixel intensities affect inspection.



#### Figure 17-4. Lighting Differences between the Template and Inspection Image


Figure 17-4a shows the golden template. Figure 17-4b shows the
inspection image. The label in the inspection image is identical to the label
in the golden template. However, the inspection image was acquired under
dimmer lighting. Although the images are aligned and corrected for
perspective differences, the defect image, shown in Figure 17-4c, displays
a single, large, dark defect because of the shift in lighting intensity.


Golden template comparison normalizes the pixel intensities in the
inspection image using histogram matching. Figure 17-5a shows the
histogram of the golden template, which peaks in intensity near 110 and
then stays low until it saturates at 255. Figure 17-5b shows the histogram
of the inspection image, which peaks in intensity near 50 and peaks again
near 200.


a.
b.
c.


Using a histogram matching algorithm, golden template comparison
computes a lookup table to apply to the inspection image. After the lookup
table is applied, the histogram of the resulting defect image, shown in
Figure 17-5c, exhibits the same general characteristics as the template
histogram. Notice the peak near 110 and the saturation at 255.



#### Figure 17-5. Histogram Matching in Golden Template Comparison



### Ignoring Edges


Even after alignment, perspective correction, and histogram matching, the
defect image may return small defects even when the part under inspection
seems identical to the golden template. These small defects are usually
confined to edges, or sharp transitions in pixel intensities.


Figure 17-6a shows the golden template. Figure 17-6b shows the
inspection image. The label in the inspection image is almost identical to
the label in the golden template. Figure 17-6c shows insignificant defects
resulting from of a small, residual misalignment or quantization errors
from the image acquisition. Although these minor variations do not affect
the quality of the inspected product, a similarly sized scratch or smudge not
on an edge would be a significant defect.


a.
b.


c.


Number of Pixels


Number of Pixels


Number of Pixels


0
50
100
150
200
255


0
50
100
150
200
255


0
50
100
150
200
255



#### Figure 17-6. Small Edge Differences between the Template and Inspection Image


To distinguish minor edge defects from significant defects, you can define
edge areas for golden template comparison to ignore using the NI Vision
Template Editor. Differences in areas you want to ignore are not returned
as defects. You can preview different edge thicknesses in the training
interface, and optionally change edge thickness during runtime.



### Using Defect Information for Inspection


Golden template comparison isolates areas in the inspection image that
differ from the golden template. To use the defect information in a machine
vision application, you need to analyze and process the information using
other NI Vision functions. Examples of functions you can use to analyze
and process the defect information include particle filters, binary
morphology, particle analysis, and binary particle classification.


a.
b.
c.
