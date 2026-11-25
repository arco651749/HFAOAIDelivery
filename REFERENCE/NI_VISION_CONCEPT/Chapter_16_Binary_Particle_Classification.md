# Chapter 16: Binary Particle Classification

> **Part**: `Part IV: Machine Vision` | **Pages**: `298 - 318`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


16
Binary Particle Classification


This chapter contains information about binary particle classification.



## Introduction


Binary particle classification identifies an unknown binary sample
by comparing a set of its significant features to a set of features that
conceptually represent classes of known samples. Classification involves
two phases: training and classifying.


•
Training is a phase during which you teach the machine vision
software the types of samples you want to classify during the
classifying phase. You can train any number of samples to create a set
of classes, which you later compare to unknown samples during the
classifying phase. You store the classes in a classifier file. Training
might be a one-time process, or it might be an incremental process you
repeat to add new samples to existing classes or to create several
classes, thus broadening the scope of samples you want to classify.


•
Classifying is a phase during which your custom machine vision
application classifies an unknown sample in an inspection image
into one of the classes you trained. The classifying phase classifies a
sample according to how similar the sample features are to the same
features of the trained samples.



### When to Use


The need to classify is common in many machine vision applications.
Typical applications involving particle classification include the following:


•
Sorting—Sorts samples of varied shapes. For example, a particle
classifier can sort different mechanical parts on a conveyor belt into
different bins. Example outputs of a sorting or identification
application could be user-defined labels of certain classes.


•
Inspection—Inspects samples by assigning each sample an
identification score and then rejecting samples that do not closely
match members of the training set. Example outputs of a sample
inspection application could be Pass or Fail.



## Chapter 16 Binary Particle Classification



### Ideal Images for Classification


Images of samples acquired in a backlit environment are ideal for particle
classification. Figures 16-1 and 16-2 show examples images of backlit
samples.



#### Figure 16-1. Sample Images of Mechanical Parts



#### Figure 16-2. Sample Images of Animal Cracker Shapes


Figures 16-3 and 16-4 show samples that are not ideal for particle
classification because they contain several unconnected parts or are
grayscale and have an internal pattern.



#### Figure 16-3. Binary Shapes Composed of Several Unconnected Parts



#### Figure 16-4. Grayscale Shapes with Internal Patterns



### General Classification Procedure


Consider an example application whose purpose is to sort nuts and bolts.
The classes in this example are Nut and Bolt.


Before you can train a classification application, you must determine a set
of features, known as a feature vector, on which to base the comparison of
the unknown sample to the classes of known samples. Features in the
feature vector must uniquely describe the classes of known samples. An
appropriate feature vector for the example application would be {Heywood
Circularity, Elongation Factor}.


The following table shows good feature values for the nuts and bolts shown
in Figure 16-5. The closer the shape of a sample is to a circle, the closer its
Heywood circularity factor is to 1. The more elongated the shape of a
sample, the higher its elongation factor.


The class Nut is characterized by a strong circularity feature and a weak
elongation feature. The class Bolt is characterized by a weak circularity
feature and a strong elongation feature.


After you determine a feature vector, gather examples of the samples you
want to classify. A robust classification system contains many example
samples for each class. All the samples belonging to a class should have
similar feature vector values to prevent mismatches.


After you have gathered the samples, train the classifier by computing the
feature vector values for all of the samples. Then you can begin to classify
samples by calculating the same feature vector for the unknown sample and
comparing those values to the feature vector values of the known samples.
The classifier assigns the unknown sample a class name based on how
similar its feature values are to the values of a known sample.


Figure 16-5a shows a binary image of nuts and bolts. Figure 16-5b shows
these samples classified by circularity and elongation.


Class


Average Heywood
Circularity


Average Elongation
Factor


Nut
1.109
1.505


Bolt
1.914
3.380



#### Figure 16-5. Classification of Nuts and Bolts


1
Circularity
2
Elongation
3
Bolts
4
Nuts


1


2


4


3


a.
b.



## Training the Particle Classifier


Figure 16-6 illustrates the process of training and testing a classifier.



### Figure 16-6. Classification Training and Testing


Collect Training and
Testing Images


Set Classifier
Parameters


Add or Remove
Training Samples


Train
Classifier


Test
Classifier


Save
Classifier


Pass
Testing?


Yes


No


Based on your specific application, predefine and label a set of training
samples that represent the properties of the entire population of samples
you want to classify. Configure the classifier by selecting the proper
classification method and distance metric for your application. For
example, you can configure the NI Particle Classifier to distinguish the
following:


•
Small differences between sample shapes independent of scale,
rotation, and mirror symmetry


•
Shapes that differ only by scale


•
Shapes that differ only by mirror symmetry


•
Any combination of the above points


If testing indicates that the classifier is not performing as expected, you can
restart the training process by collecting better representative samples or
trying different training settings. In some machine vision applications, new
parts need to be added to an existing classification system. This can be done
by incrementally adding samples of the new parts to the existing classifier.



## Classifying Samples


After you train the classifier, you can classify images of samples into their
corresponding classes for sorting or defect inspection. Figure 16-7
illustrates a general functional diagram of the classifying phase.



### Figure 16-7. General Steps of the Classifying Phase


Image
Acquisition
Preprocessing
Feature
Extraction
Classification


Decision



### Preprocessing


Preprocessing operations prepare images for better feature extraction.
Preprocessing includes noise filtering; thresholding; rejecting particles that
touch the image border; and removing small, insignificant particles.


For best results, acquire the inspection images under the same lighting
conditions in which you acquired the training images. Also, apply the same
preprocessing options to the inspection images that you used to preprocess
the training images.



### Feature Extraction


Feature extraction computes the feature vector in the feature space from an
input image. Feature extraction reduces the input image data by measuring
certain features or properties that distinguish images of different classes.
Which features to use depends on the goal of the classification system. The
features could be raw pixel values or some abstract representation of the
image data. For identification applications, select features that most
efficiently preserve class separability—feature values for one class should
be significantly different from the values for another class. For inspection
applications, select features that distinguish the acceptable from the
defective.


The NI Particle Classifier classifies samples using different types of shape
descriptors. A shape descriptor is a feature vector based on particle
analysis measurements. Each type of shape descriptor contains one or more
shape measurements made from a sample.


The default NI Particle Classifier shape descriptor is based on shape
characteristics that are invariant to scale changes, rotation, and mirror
symmetry. Another type of shape descriptor is based on the size of the
sample and is used along with the default shape descriptor to distinguish
samples with the same shape but different scale, such as different sized
coins. The NI Particle Classifier also uses a reflection-dependent shape
descriptor to distinguish samples that are the same shape but exhibit mirror
symmetry, such as a lowercase letter p and a lowercase letter q. The
NI Particle Classifier uses these different types of shape descriptors in
a multi-classifier system to achieve scale-dependent classification,
reflection-dependent classification, or scale and reflection-dependent
classification.



#### Invariant Features


The NI Particle Classifier uses the following features for scale-, rotation-,
and reflection-invariant shape descriptors:


•
Feature 1 describes the circularity of the sample.


•
Feature 2 describes the degree of elongation of the sample.


•
Feature 3 represents the convexity of the sample shape.


•
Feature 4 is a more detailed description of the convexity of a sample
shape.


•
Feature 5 is used for the discrimination of samples with holes.


•
Feature 6 is used for more detailed discrimination of samples with
holes.


•
Feature 7 represents the spread of the sample.


•
Feature 8 represents the slenderness of the sample.



### Classification


The NI Particle Classifier can apply the following classification
algorithms: Minimum Mean Distance, Nearest Neighbor, and K-Nearest
Neighbor. Each of these methods may employ different distance metrics:
Maximum distance (L∞), Sum distance (L1), and Euclidean distance (L2).
Refer to the Instance-Based Learning section for definitions of these
distance metrics.



## Classification Methods



### Instance-Based Learning


Typical instance-based learning includes Nearest Neighbor, K-Nearest
Neighbor, and Minimum Mean Distance algorithms. The most intuitive
way of determining the class of a feature vector is to find its proximity to a
class or features of a class using a distance function. Based on the definition
of the proximity, there are several different algorithms, as follows.


The NI Particle Classifier provides three distance metrics: Euclidean
distance, Sum distance, and Maximum distance.


Let X = [x1, x2, ... xn] and Y = [y1, y2, ... yn] be the feature vectors.



#### Nearest Neighbor Classifier


In Nearest Neighbor classification, the distance of an input feature vector
X of unknown class to a class Cj is defined as the distance to the closest
sample that is used to represent the class.


d(X,Cj) =
d(X,Xi j)


where d(X,Xi j) is the distance between X and Xi j.


The classification rule assigns a pattern X of unknown classification to the
class of its nearest neighbor.


X ∈Class Cj, if d(X,Cj) =
d(X,Ci)


Nearest neighbor classification is the most intuitive approach for
classification. If representative feature vectors for each class are available,
Nearest Neighbor classification works well in most classification
applications.


In some classification applications, a class may be represented by multiple
samples that are not in the same cluster, as shown in Figure 16-8. In such
applications, the Nearest Neighbor classifier is more effective than the
Minimum Mean Distance classifier.


Euclidean distance (L2)


Sum distance, also known as the
City-Block metric or Manhattan
metric (L1)


Maximum distance (L∞)


d X Y
( , )
xi
yi
–
(
)2


i
1
=


n
∑
=


d X Y
( , )
xi
yi
–


i
1
=


n
∑
=


d X Y
( , )
max
i
xi
yi
–
=


min
i


min
i



#### Figure 16-8. Class Samples Not Located in the Same Cluster



#### K-Nearest Neighbor Classifier


In K-Nearest Neighbor classification, an input feature vector X is classified
into class Cj based on a voting mechanism. The classifier finds the
K nearest samples from all of the classes. The input feature vector of the
unknown class is assigned to the class with the majority of the votes in the
K nearest samples.


The outlier feature patterns caused by noise in real-world applications can
cause erroneous classifications when Nearest Neighbor classification is
used. As Figure 16-9 illustrates, K-Nearest Neighbor classification is more
robust to noise compared with Nearest Neighbor classification. With X as
an input, K = 1 outputs Label 1, and K = 3 outputs Label 2.


x
x


x
x
x
x
x
x


x


x
x
x


x
x
x
x


x


o


o


o
o
o


o
o
o
o
o


o


o
o


o
o


o


o = Class 1
x = Class 2


o


o


o
o
o
o
o


o
o


x


x


x


x
x


x


x
x


x
x


x
x
x
x
x


x
x
x



#### Figure 16-9. How K-Nearest Classifier Works



#### Minimum Mean Distance Classifier


Let
be nj feature vectors that represent class Cj. Each
feature vector has the label of class j that you have selected to represent the
class. The center of the class j is defined as


.


The classification phase classifies an input feature vector X of unknown
class based on its distance to each class center.


X ∈Class Cj, if d(X,Mj) =
d(X,Mi)


where d(X,Mj) is defined as the distance function based on the distance
metric selected during the training phase.


In applications that have little to no feature pattern variability or a lot of
noise, the feature patterns of each class tend to cluster tightly around the


X


Label1
Label2


Label3


X1
j X2
j … Xnj
j
,
,
,
{
}


Mj
1
nj
---
Xi
j


i
1
=


nj
∑
=


min
i


class center. Under these conditions, Minimum Mean Distance classifiers
perform effectively—only the input vector distances to the centers of the
classes need to be calculated instead of all the representative samples in
real-time classification.



### Multiple Classifier System



#### Cascaded Classification System


In a cascaded classification system, cascaded multiple classifiers make
classification decisions based on multiple classification stages. Classifier 1
outputs several candidates for Classifier 2 in the second stage.
Classification is based on different features.



#### Parallel Classification Systems


Combining results from multiple classifiers may generate more accurate
classification results than any of the constituent classifiers alone.
Combining results is often based on fixed combination rules, such as the
product and/or average of the classifier outputs.


The NI Particle Classifier uses a parallel classification system with
three classifiers, as illustrated in Figure 16-10. Two classifiers are used for
scale-dependent classification. One of these classifiers uses scale-invariant
features, and the other uses a scale-dependant feature. Additionally, the
NI Particle Classifier uses a third classifier to distinguish samples with
mirror symmetry. The outputs of the classifiers are combined using
user-specified weights to get the result.



#### Figure 16-10. Weighted Parallel Classification System


Reflection
Classifier


Scale
Classifier


Shape
Classifier


Shape Feature Vector


Scale Feature Vector


Reflection Feature Vector


Scale Classifier Output


Shape Classifier output


Reflection Classifier Output


Particle
Classifier
Output


W1


W2


W3



## Custom Classification


You can define a custom feature extraction process for specific machine
vision applications using NI Vision.


Typical applications include sorting and inspection applications for which
you can define a feature descriptor to represent the different classes in a
specific application. Examples of such feature descriptors include statistics
about the grayscale pixel distribution in an image, measurements from a
Vision gauging tool, or color spectra from Vision color learning
algorithms.



### Concepts


With custom classification, you create a classifier by training it with
prelabeled training feature vectors. NI Vision custom classification uses the
same classification algorithms as the NI Particle Classifier, including the
Minimum Mean Distance, Nearest Neighbor, and K-Nearest Neighbor
classifications.



## In-Depth Discussion


This section provides additional information you may need for making a
successful classification application.



### Training Feature Data Evaluation


A good training data set should have both small intraclass variation and
large interclass variation. The NI Particle Classifier outputs an intraclass
deviation array to represent the deviation in each class, and a class distance
table to represent the deviation between the classes.



#### Intraclass Deviation Array


[Qj, Nj], j=1,2, ... L, where Nj is the number of samples in class j and L is
the number of classes. The number of samples Nj represents the statistical
significance of Qj that is defined as follows:


Let {X1j, X2j, ... XNjj} be Nj n-dimensional feature vectors that represent
class Cj with Xij = [xi1j, xi2 tj, ... xinj]T. Each feature vector has the label of
class j that you have selected to represent the class. Let
Mj = [m1j, m2j, ... mnj]T be the mean vector of the class j. Then


where each element of the mean vector


The standard deviation of feature element k of class j is defined as


The quality of feature data in class j is defined as


A small Qj indicates that the training data in class j is tightly clustered about
the class center. A large Qj indicates that the training data is spread out from
the class center, which may increase chances for misclassification.


M j
1
Nj
----
Xi j


i
1
=


Nj
∑
=


Mk
j
1
Nj
----
xik
j


i
1
=


Nj
∑
=


σk
j
1
Nj
----
xik
j
mk
j
–
(
)
2


i
1
=


Nj
∑
=


Qj
max
k σk
j
=



#### Class Distance Table


Let Mj = [m1j, m2j, ... mnj]T be the mean vector of the class j as defined
before. The distance between two classes i and j is defined as follows.


dij = D(Mi, Mj)


where D is the distance metric selected from the training option. You can
use the class distance table to examine statistical information, such as the
two closest class distances and the two most widely separated classes.
Additionally, you can use the class distance table with the intraclass
deviation array to evaluate the quality of different training data sets.



### Determining the Quality of a Trained Classifier


The NI Particle Classifier outputs a classification distribution table that you
can use to determine the quality of a trained classifier. Table 16-1 shows an
example classification distribution table.


In this example, assume that the classifier was given 30 samples to classify:
10 samples known to be in class C1, 10 samples known to be in class C2,
and 10 samples known to be in class C3.



#### Classifier Predictability


The classification predictive value indicates the probability that a sample
classified into a given class belongs to that class. Use the columns of the
table to determine the predictive value, per class, of the classifier. Each
column represents a class into which the classifier classifies samples.
The values in the columns indicate how many samples of each class have
been classified into the class represented by the column. For example,
10 samples known to be in class C1 were correctly classified into class C1.
However, 4 samples known to be in class C3 were also classified into C1.



#### Table 16-1. Example Classification Distribution Table


C1
C2
C3
Total
Accuracy


Samples of Class C1
10
0
0
10
10 / 10 = 100%


Samples of Class C2
0
8
2
10
8 / 10 = 80%


Samples of Class C3
4
0
6
10
6 / 10 = 60%


Total
14
8
8
30
24 / 30 = 80%


Predictive Value
10 / 14 = 71%
8 / 8 = 100%
6 / 8 = 75%


Note
The number of samples classified correctly into a class is located at the intersection
of row Samples of Class x and column Cx.


Looking down a column, notice the number of samples that were classified
correctly into the class. Count the total number of samples classified into
the class. The predictive value of the class is the ratio of


For example, the predictive value of class C1 is 71%.



#### Classifier Accuracy


The classification accuracy indicates the probability that a sample is
classified into the class to which it belongs. Use the rows of the table to
determine the accuracy, per class, of the trained classifier. The accuracy
indicates the probability that the classifier classifies a sample into the
correct class. Each row shows how the classifier classified all of the
samples known to be in a certain class. In the example classification
distribution table, 8 of the samples known to be in class C2 were correctly
classified into class C2, but 2 of the samples known to be in class C2 were
erroneously classified into class C3.


Looking across a row, the accuracy of a class is the ratio of


For example, the accuracy of class C1 is 100%.


Number of Samples Classified Correctly
Total Number of Samples Classified into the Class
------------------------------------------------------------------------------------------------------------------------


10
10
4
+
--------------
.71
=
71%
=


Number of Samples Classified Correctly
Number of Samples Known To Be in the Class
--------------------------------------------------------------------------------------------------------------


10
10
-----
1
100%
=
=



### Identification and Classification Score


The NI Particle Classifier outputs both identification confidence and
classification confidence for the evaluation of classification results. The
classification confidence outputs a meaningful score for both sorting and
inspection applications. Use the identification confidence only when you
cannot reach a decision about the class of a sample by using the
classification confidence score alone.



#### Classification Confidence


The classification confidence indicates the degree to which the assigned
class represents the input better than the other classes represent the input.
It is defined as follows:


Classification Confidence = (1– d1 / d2) × 1000


where d1 is the distance to the closest class, and d2 is the distance to the
second closest class. The distance is dependent on the classification
algorithm used. Because 0 ≤d1 ≤1 and 0 ≤d2 ≤1, the classification
confidence is a score between 0 and 1000.



#### Identification Confidence


The identification confidence indicates the similarity between the input and
the assigned class. It is defined as follows:


Identification Confidence = (1 – d) × 1000


where d is the normalized distance between the input vector and the
assigned class. Distance d is dependent on the classification algorithm
used.


The normalization factor is defined as the maximum interclass distance.


d
Distance Between Input Sample and its Assigned Class
Normalization Factor
-----------------------------------------------------------------------------------------------------------------------------------
=



#### Calculating Example Classification and Identification Confidences


Assume a normalized scalar feature with a distribution in [0,1] from
two classes of patterns, as shown in Figure 16-11. The centers of the
two classes are 0.33 and 0.67, respectively. If the Minimum Mean Distance
is used for classification with input feature x = 0.6, the classification output
is class 2, and the classification confidence is calculated as


and the identification confidence is calculated as



#### Figure 16-11. Two Classes with Gaussian Distribution


For a feature value x = 0.5, the sample can be classified into class 1 or
class 2 with the classification confidence value equal to 0. For
0.4 < x < 0.5, the sample is classified into class 1 with low classification
confidence, while 0.5 < x < 0.6 is classified into class 2 with low
classification confidence in a Minimum Mean Distance classification
system.


1
0.60
0.67
–
0.60
0.33
–
-----------------------------
–




1000
×
740,
=


1
0.60
0.67
–
0.67
0.33
–
-----------------------------
–




1000
×
794.
=



#### Evaluating Classifier Performance


For a systematic approach to evaluating a classifier in the design phase,
define a testing data set in addition to a training data set. After you train the
classifier using the training data set, run the classifier using the testing data
set. The output of the classification confidence distribution is a good
indicator of the classifier performance. The classification confidence
distribution is a histogram of the classification score. The amplitude is
the number of testing samples in a specific classification score.


Figure 16-12 shows the classification confidence distribution from a testing
database of the mechanical parts shown in Figure 16-1. You can set a
minimum classification score of 800 and get a high classification rate for
this testing database.



#### Figure 16-12. Classification Confidence from a Mechanical Parts Database


Figure 16-13 shows the classification confidence distribution from a testing
database of the animal crackers shown in Figure 16-2. If you use the same
minimum classification score for cracker image classification that you used
for mechanical parts classification, you get a high rate of false negatives
because a large portion of the cracker classification scores are less than 800.



#### Figure 16-13. Classification Confidence from a Cracker Database


A classification confidence distribution from a representative testing
database is a good indicator for selecting a good score threshold for a
specific inspection or sorting application.


Note
A score threshold that can be used to reject classification results is application
dependent. Experiment with your classifier to determine an effective threshold for your
application.
