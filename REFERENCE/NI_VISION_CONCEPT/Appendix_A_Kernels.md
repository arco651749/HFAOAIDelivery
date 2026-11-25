# Appendix A: Kernels

> **Part**: `Appendices` | **Pages**: `349 - 355`
> **Source**: `NI Vision Concepts Manual (April 2005 Edition)`

---


A
Kernels


A kernel is a structure that represents a pixel and its relationship to its
neighbors. This appendix lists a number of predefined kernels supported by
NI Vision.


Gradient Kernels


The following tables list the predefined gradient kernels.


3 × 3 Kernels


The following tables list the predefined gradient 3 × 3 kernels.


Prewitt Filters


The Prewitt filters have the following kernels. The notations West (W),
South (S), East (E), and North (N) indicate which edges of bright regions
they outline.



## Table A-1. Prewitt Filters


#0 W/Edge
#1 W/Image
#2 SW/Edge
#3 SW/Image


–1
0
1
–1
0
1
–1
0
1


–1
0
1
–1
1
1
–1
0
1


0
1
1
–1
0
1
–1 –1
0


0
1
1
–1
1
1
–1 –1
0


#4 S/Edge
#5 S/Image
#6 SE/Edge
#7 SE/Image


1
1
1
0
0
0
–1 –1 –1


1
1
1
0
1
0
–1 –1 –1


1
1
0
1
0 –1
0 –1 –1


1
1
0
1
1 –1
0 –1 –1


#8 E/Edge
#9 E/Image
#10 NE/Edge
#11 NE/Image


1
0 –1
1
0 –1
1
0 –1


1
0 –1
1
1 –1
1
0 –1


0 –1 –1
1
0 –1
1
1
0


0 –1 –1
1
1 –1
1
1
0



## Appendix A Kernels


Sobel Filters


The Sobel filters are very similar to the Prewitt filters, except that they
highlight light intensity variations along a particular axis that is assigned a
stronger weight. The Sobel filters have the following kernels. The notations
West (W), South (S), East (E), and North (N) indicate which edges of bright
regions they outline.


#12 N/Edge
#13 N/Image
#14 NW/Edge
#15 NW/Image


–1 –1 –1
0
0
0
1
1
1


–1 –1 –1
0
1
0
1
1
1


–1 –1
0
–1
0
1
0
1
1


–1 –1
0
–1
1
1
0
1
1



## Table A-2. Sobel Filters


#16 W/Edge
#17 W/Image
#18 SW/Edge
#19 SW/Image


–1
0
1
–2
0
2
–1
0
1


–1
0
1
–2
1
2
–1
0
1


0
1
2
–1
0
1
–2 –1
0


0
1
2
–1
1
1
–2 –1
0


#20 S/Edge
#21 S/Image
#22 SE/Edge
#23 SE/Image


1
2
1
0
0
0
–1 –2 –1


1
2
1
0
1
0
–1 –2 –1


2
1
0
1
0 –1
0 –1 –2


2
1
0
1
1 –1
0 –1 –2


#24 E/Edge
#25 E/Image
#26 NE/Edge
#27 NE/Image


1
0 –1
2
0 –2
1
0 –1


1
0 –1
2
1 –2
1
0 –1


0 –1 –2
1
0 –1
2
1
0


0 –1 –2
1
1 –1
2
1
0


#28 N/Edge
#29 N/Image
#30 NW/Edge
#31 NW/Image


–1 –2 –1
0
0
0
1
2
1


–1 –2 –1
0
1
0
1
2
1


–2 –1
0
–1
0
1
0
1
2


–2 –1
0
–1
1
1
0
1
2


Table A-1.  Prewitt Filters (Continued)


5 × 5 Kernels


The following table lists the predefined gradient 5 × 5 kernels.


Table A-3.  Gradient 5 × 5


#0 W/Edge
#1 W/Image
#2 SW/Edge
#3 SW/Image


0  –1
0
1
0
–1 –2
0
2
1
–1 –2
0
2
1
–1 –2
0
2
1
0 –1
0
1
0


0  –1
0
1
0
–1  –2
0
2
1
–1  –2
1
2
1
–1  –2  0
2
1
0  –1
0
1
0


0
0
1
1
1
0
0
2
2
1
–1  –2
0
2
1
–1  –2  –2
0
0
–1  –1  –1
0
0


0
0
1
1
1
0
0
2
2
1
–1  –2
1
2
1
–1  –2  –2
0
0
–1  –1  –1
0
0


#4 S/Edge
#5 S/Image
#6 SE/Edge
#7 SE/Image


0
1
1
1
0
1
2
2
2
1
0
0
0
0
0
1  –2  –2  –2  –1
0  –1  –1  –1
0


0
1
1
1
0
1
2
2
2
1
0
0
1
0
0
–1  –2  –2  –2  –1
0  –1  –1  –1
0


1
1
1
0
0
1
2
2
0
0
1
2
0  –2  –1
0
0  –2  –2  –1
0
0  –1  –1  –1


1
1
1
0  0
1
2
2
0
0
1
2
1  –2  –1
0
0  –2  –2  –1
0
0  –1  –1  –1


#8 E/Edge
#9 E/Image
#10 NE/Edge
#11 NE/Image


0
1
0  –1
0
1
2  0  –2  –1
1
2
0  –2  –1
1
2
0  –2  –1
0
1
0  –1
0


0
1
0  –1
0
1
2
0  –2  –1
1
2
1  –2  –1
1
2
0  –2  –1
0
1
0  –1
0


0
0  –1  –1  –1
0
0  –2  –2  –1
1
2
0  –2  –1
1
2
2
0
0
1
1
1
0
0


0
0  –1  –1  –1
0
0  –2  –2  –1
1
2
1  –2  –1
1
2
2
0
0
1
1
1
0
0


#12 N/Edge
#13 N/Image
#14 NW/Edge
#15 NW/Image


0  –1  –1  –1
0
–1  –2  –2  –2  –1
0
0
0
0
0
1
2
2
2
1
0
1
1
1
0


0  –1  –1  –1
0
–1  –2  –2  –2  –1
0
0
1
0
0
1
2
2
2
1
0
1
1
1
0


–1  –1  –1
0  0
–1  –2  –2
0
0
–1  –2
0
2
1
0
0
2
2
1
0
0
1
1
1


–1  –1  –1
0
0
–1  –2  –2
0
0
–1  –2
1
2
1
0
0
2
2
1
0
0
1
1
1


7 × 7 Kernels
The following table lists the predefined gradient 7 × 7 kernels.


Table A-4.  Gradient 7 × 7


#0 W/Edge
#1 W/Image


0  –1  –1
0
1
1
0
–1  –2  –2
0
2
2
1
–1  –2  –3
0
3
2
1
–1  –2  –3
0
3
2
1
–1  –2  –3
0
3
2
1
–1  –2  –2
0
2
2
1
0  –1  –1
0
1
1
0


0  –1  –1
0
1
1
0
–1  –2  –2
0
2
2
1
–1  –2  –3
0
3
2
1
–1  –2  –3
1
3
2
1
–1  –2  –3
0
3
2
1
–1  –2  –2
0
2
2
1
0  –1  –1
0
1
1
0


#2 S/Edge
#3 S/Image


0
1
1
1
1
1
0
1
2
2
2
2
2
1
1
2
3
3
3
2
1
0
0
0
0
0
0
0
–1  –2  –3  –3  –3  –2  –1
–1  –2  –2  –2  –2  –2  –1
0  –1  –1  –1  –1  –1
0


0
1
1
1
1
1
0
1
2
2
2
2
2
1
1
2
3
3
3
2
1
0
0
0
1
0
0
0
–1  –2  –3  –3  –3  –2  –1
–1  –2  –2  –2  –2  –2  –1
0  –1  –1  –1  –1  –1
0


#4 E/Edge
#5 E/Image


0
1
1
0  –1  –1
0
1
2
2
0  –2  –2  –1
1
2
3
0  –3  –2  –1
1
2
3
0  –3 –2  –1
1
2
3
0  –3  –2  –1
1
2
2
0  –2  –2  –1
0
1
1
0  –1  –1
0


0  1
1
0  –1  –1
0
1
2
2
0  –2  –2  –1
1
2
3
0  –3  –2  –1
1
2
3
1  –3  –2  –1
1
2
3
0  –3  –2  –1
1
2
2
0  –2  –2  –1
0
1
1
0  –1  –1
0


#6 N/Edge
#7 N/Image


0  –1  –1  –1  –1  –1
0
–1  –2  –2  –2  –2  –2  –1
–1  –2  –3  –3  –3  –2  –1
0
0
0
0
0
0
0
1
2
3
3
3
2
1
1
2
2
2
2
2
1
0
1
1
1
1
1
0


0  –1  –1  –1  –1  –1
0
–1  –2  –2  –2  –2  –2  –1
–1  –2  –3  –3  –3  –2  –1
0
0
0
1
0
0
0
1
2
3
3
3
2
1
1
2
2
2
2
2
1
0
1
1
1
1
1
0


Laplacian Kernels


The following tables list the predefined Laplacian kernels.


Table A-5.  Laplacian 3 × 3


#0 Contour 4
#1 +Image×1
#2 +Image×2


0 –1
0
–1
4 –1
0 –1
0


0 –1
0
–1
5 –1
0 –1
0


0 –1
0
–1
6 –1
0 –1
0


#3 Contour 8
#4 +Image×1
#5 +Image×2


–1 –1 –1
–1
8 –1
–1 –1 –1


–1 –1 –1
–1
9 –1
–1 –1 –1


–1 –1 –1
–1 10 –1
–1 –1 –1


#6 Contour 12
#7 +Image×1


–1 –2 –1
–2 12 –2
–1 –2 –1


–1 –2 –1
–2 13 –2
–1 –2 –1


Table A-6.  Laplacian 5 × 5


#0 Contour 24
#1 +Image×1


–1 –1 –1 –1 –1
–1 –1 –1 –1 –1
–1 –1 24 –1 –1
–1 –1 –1 –1 –1
–1 –1 –1 –1 –1


–1 –1 –1 –1 –1
–1 –1 –1 –1 –1
–1 –1 25 –1 –1
–1 –1 –1 –1 –1
–1 –1 –1 –1 –1


Table A-7.  Laplacian 7 × 7


#0 Contour 48
#1 +Image×1


–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 48 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1


–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 49 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1
–1 –1 –1 –1 –1 –1 –1


Smoothing Kernels


The following tables list the predefined smoothing kernels.


Table A-8.  Smoothing 3 × 3


0
1
0
1
0
1
0
1
0


0
1
0
1
1
1
0
1
0


0
2
0
2
1
2
0
2
0


0
4
0
4
1
4
0
4
0


1
1
1
1
0
1
1
1
1


1
1
1
1
1
1
1
1
1


2
2
2
2
1
2
2
2
2


4
4
4
4
1
4
4
4
4


Table A-9.  Smoothing 5 × 5


1
1
1
1
1
1
1
1
1
1
1
1
0
1
1
1
1
1
1
1
1
1
1
1
1


1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1


Table A-10.  Smoothing 7 × 7


1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
0
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1


1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1


Gaussian Kernels


The following tables list the predefined Gaussian kernels.


Table A-11.  Gaussian 3 × 3


0
1
0
1
2
1
0
1
0


0
1
0
1
4
1
0
1
0


1
1
1
1
2
1
1
1
1


1
1
1
1
4
1
1
1
1


1
2
1
2
4
2
1
2
1


1
4
1
4 16
4
1
4
1


Table A-12.  Gaussian 5 × 5


1
2
4
2
1
2
4
8
4
2
4
8 16
8
4
2
4
8
4
2
1
2
4
2
1


Table A-13.  Gaussian 7 × 7


1
1
2
2
2
1
1
1
2
2
4
2
2
1
2
2
4
8
4
2
2
2
4
8 16
8
4
2
2
2
4
8
4
2
2
1
2
2
4
2
2
1
1
1
2
2
2
1
1
