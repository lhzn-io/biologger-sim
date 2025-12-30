Calibration of Strapdown Magnetometers in the
Magnetic Field Domain

Demoz Gebre-Egziabher∗, Gabriel H. Elkaim†, J. David Powell ‡and Bradford W. Parkinson§

ABSTRACT

This paper presents an algorithm for calibrating strapdown magnetometers in the magnetic ﬁeld do-

main. In contrast to the traditional method of compass swinging, which computes a series of heading

correction parameters and, thus, is limited to use with two-axis systems, this algorithm estimates mag-

netometer output errors directly. Therefore, this new algorithm can be used to calibrate a full three-axis

magnetometer triad. The calibration algorithm uses an iterated, batch least squares estimator which is

initialized using a novel two-step nonlinear estimator. The algorithm is simulated to validate conver-

gence characteristics and further validated on experimental data collected using a magnetometer triad.

It is shown that the post calibration residuals are small and result in a system with heading errors on the

order of 1 to 2 degrees.

1

INTRODUCTION

Magnetometers measure the intensity of magnetic ﬁelds and are used in many scientiﬁc and engi-

neering applications. In vehicle navigation, for example, they are used as inexpensive heading sensors

∗Assistant Professor, Department of Aerospace Engineering and Mechanics, University of Minnesota, Twin Cities, 110

Union St., N.E., 107 Akerman Hall, Minneapolis, MN, 55455. <gebre@aem.umn.edu>

†Assistant Professor, Computer Engineering Department, University of California, Santa Cruz, 1156 High Street, Santa

Cruz, CA 95064. <elkaim@soe.ucsc.edu>

‡Professor Emeritus, Department of Aeronautics and Astronautics, Stanford University, Durand Building, 496 Lomita

Mall, Stanford, CA 94305-4035. <JDPowell@stanford.edu>

§Professor Emeritus, Department of Aeronautics and Astronautics, Stanford University, Durand Building, 496 Lomita

Mall, Stanford, CA 94305-4035. <brad@relgyro.stanford.edu>

(where heading is the angle between the vehicle and North). In these applications, heading is determined

by measuring the horizontal component of Earth’s magnetic ﬁeld vector, (cid:126)h, using a perpendicular pair (or
T

an orthogonal triad) of magnetometers. A magnetometer triad would measure (cid:126)hb =

x hb
hb

y hb
z

(cid:149)
which, as indicated by the superscript b, is Earth’s magnetic ﬁeld vector (cid:126)h expressed in a coordinate

(cid:148)

frame ﬁxed to the body of the vehicle. A pair of magnetometers would measure only two components

of the ﬁeld vector or (cid:126)hb =

x hb
hb
y

(cid:148)

T

.

(cid:149)

If the the x-y plane of the body coordinate system is level (i.e., is parallel to Earth’s local tangent), the

magnetometer readings are used to compute heading with respect to magnetic North using the following

formula:

ψ =

−

1

tan−

hb
y
hb

x (cid:33)

(cid:160)

(1)

If the x-y plane is not level, it can be levelled analytically by measuring the pitch and roll angles of the

vehicle. These angles are used to compute the body-to-locally-level transformation matrix,

w

b
→
C , which

is used to map the magnetometer measurement to the locally-level plane. Note that

w

b
→
C is the ”b” to ”w”

coordinate frame transformation matrix where the ”w” is the x-y-z coordinate frame having its x axis

coincident with the vehicle’s longitudinal axis and its x-y plane level or parallel to the local tangent (i.e.,

the wander azimuth plane).

Since the output of any sensor is, to some degree, corrupted by errors, the actual measurement made
ˆ(cid:126)hb, will be different from the true magnetic ﬁeld (cid:126)hb. The process

by the pair or triad of magnetometers,

of estimating these errors and removing them from the magnetometer measurements is the subject of

this paper.

For heading determination systems which use a pair of perpendicular magnetometers, a well known

calibration procedure called compass swinging has been used successfully [1, 2]. Compass swinging

has several shortcomings, however, which make it unsuitable for many current applications. Two of

most signiﬁcant shortcomings of this procedure are that (1) it requires an external or independent source

of heading and (2) the plane containing the pair of magnetometers must be level. These two factors

limit or even preclude in-situ calibration because the magnetometer being calibrated are normally the

only source of heading information. Furthermore, the ”b” and ”w” coordinate frames will not always be

coincident.

Another deﬁciency of compass swinging is that it is a heading domain calibration algorithm. That

is, it involves computing a series of heading correction parameters which, when added to heading (as

computed by Equation 1), cancel heading deviations caused by magnetometer errors. As such, the

algorithm is not applicable for applications other than heading determination (e.g., three axis attitude

determination as discussed in [3], [4] and [5]). Another shortcoming of compass swinging is the fact

that the quality of the calibration degrades as the vehicle with the magnetometers are moved farther

away from the geographical point where the calibration was performed. This is because the correction

parameters computed are functions of the local magnetic ﬁeld strength.

Recently, different magnetometer calibration methodologies that deal with some of the shortcoming

of compass swinging have been proposed. For example, [6] proposed a method which computes correc-

tion parameters for the magnetometer’s ﬁeld measurement errors instead of heading correction parame-

ters. Since this is a procedure for calibration in the magnetic ﬁeld domain, unlike compass swinging, the

results are location independent. In addition, the calibration is not limited to magnetometers used solely

for heading determination but applicable in cases where the magnetometers are used for any purpose

[3]). However, the method discussed in [6] does have some limitations. For example, it still requires

that the x

−

y body plane of the vehicle containing the magnetometers be level during calibration which

severely limits the algorithm from real time use in a vehicle that is moving.

In order to improve the performance the above discussed magnetic ﬁeld domain calibration pro-

cedure, this paper presents a reformulation and extension of the method discussed in [6]. Section 2

presents a uniﬁed error model for strapdown magnetometers and discusses the problem of calibrating

strapdown magnetometers in the context of the uniﬁed error model. In Section 3, prior art in calibra-

tion of magnetometers is presented. In particular, we will discuss compass swinging or the classical

method of calibrating magnetometers in the heading domain. This will serve as a motivation for the

methods presented in this paper as well as being a benchmark against which we will compare these new

calibration methods. Section 4 will develop an iterative, batch least squares algorithm for calibration in

the magnetic ﬁeld domain. We will also present a two step, non-linear estimator used to establish the

initial conditions for the iterative, batch least squares algorithm. In Section 5, the results of simulation

and trade studies will be presented. Experimental results are presented in Section 6 and Section 7 will

conclude this paper.

2 ERROR MODELLING

The output of magnetometers are corrupted by wide band measurement noise, stochastic biases due

to sensor imperfections, installation errors and unwanted magnetic interference in the vicinity of the

sensors.

The unwanted or interfering magnetic ﬁelds can be classiﬁed into two distinct groups. The ﬁrst

group consists of constant or slowly time-varying ﬁelds generated by ferromagnetic structural materials

in the proximity of the magnetometers. The ﬁeld measurement errors resulting from such interferences

are referred to as hard iron biases [7].

The second group of interfering magnetic ﬁelds result from materials that generate their own mag-

netic ﬁeld in response to an externally applied ﬁeld. This generated ﬁeld is affected by both the magni-

tude and direction of the externally applied magnetic ﬁeld. Such materials are called soft irons and the

error they generate is referred to as a soft iron bias. In a moving vehicle, the orientation of Earth’s mag-

netic ﬁeld relative to the vehicle (and any soft iron materials contained therein) changes continuously.

Thus, the resulting soft iron errors are time varying.

A comprehensive mathematical model for the output error of a strapdown magnetometer can be

written as:

ˆ(cid:126)hw =

w
b
→
C

Cm Csf Csi

(cid:126)hb + (cid:126)bb + (cid:126)wb
(cid:144)

T

(cid:145)(cid:105)

.

(2)

T

(cid:104)
and (cid:126)wb =

In this model, (cid:126)bb =

wb
band noise, respectively, and are additive errors which corrupt the true ﬁeld measurement (cid:126)hb. The

represent hard iron biases and wide-

x wb

y wb
z

bb
x

bb
y

bb
z

(cid:149)

(cid:149)

(cid:148)

(cid:148)

variables Csi, Csf and Cm are 3

errors, respectively. The matrix

3 matrices that account for soft iron, scale factor and misalignment
w

3 body-to-local tangent transformation matrix discussed

×
b
→
C is the 3

×

earlier. These errors are discussed in more detail next.

2.1 Hard Iron Errors ((cid:126)bb)

Normally, the largest errors tend to be null-shifts caused by unwanted magnetic ﬁelds in the vicinity

of the magnetometers. This can be seen clearly by examining Figure 1 which shows the output error from

a magnetometer measuring the vertical component of Earth’s magnetic ﬁeld vector, hb

z, at Stanford,

California (approximately N 37.5◦ latitude and W 122.1◦ longitude). Earth’s magnetic ﬁeld vector at
T

this location, (cid:126)h, in North-East-Down (NED) coordinates is equal to

0.23199 0.06361 0.43500

(cid:149)
Gauss [8]. Figure 1 shows the output of a magnetometer measuring the vertical component after hz

(cid:148)

(0.43500 Gauss) has been subtracted. What is shown in the ﬁgure, therefore, is a null-shift of 9.2 milli-

Gauss and the largest component of the output error.

2.2 Wide Band Noise (σw)

Removing the null-shift from the data shown in Figure 1 leaves errors due to magnetometer mea-

surement wide band noise. Figure 2 is a histogram of the data shown in Figure 1. From Figure 2 it can

be seen that the wide band noise has a standard deviation, σw, of approximately 5 milli-Gauss which is

smaller than the null shift.

2.3 Soft Iron Errors (Csi)

In this work we assume that a linear relationship exits between the ﬁeld a soft iron generates in

response to an externally applied ﬁeld. Even though this is a reasonable assumption in many applications,

there are cases where it is invalid due to hysteresis. Assuming no hysteresis, Csi can be written as:

αxx αxy αxz

αyx αyy αyz

αzx αzy αzz

.









Csi = 






(3)

The αij terms represent the effective soft iron coefﬁcients. They are the constants of proportionality

between the magnetic ﬁeld applied to a soft iron and the resulting induced magnetic ﬁeld. From a

notation point of view, αxy, for example, represents the effective coefﬁcient relating the ﬁeld generated

in the x-direction in response to an applied ﬁeld in the y-direction. The term “effective” is used to

describe these coefﬁcients because they represent the effect of all soft iron material present that may

corrupt the magnetometer outputs [4, 5].

2.4 Scale Factor (Csf )

Scale factor errors are modeled using the 3

3 matrix Csf given by:

×

(1 + sf x)

0

Csf = 






0

0

(1 + sf y)

0

(1 + sf z)







0

0



(4)

The scale factor errors sf x, sf y and sf z represent the uncertainty in knowledge of the constant of propor-

tionality relating magnetometer input to output.

2.5 Misalignments (Cm)

In an ideal installation, the magnetometer triad will be mounted in perfect alignment with the body

axis of the aircraft. Stated differently, the magnetometer axes will be identical to the body axes. In actual

practice, perfect alignment cannot always be achieved. The matrix Cm accounts for this misalignment

and is nothing more than the magnetometer axes to body frame direction cosine matrix,

p
b
→
C . Since the

misalignment between the two axes is normally very small (but not negligible), Cm can be modeled as

the following skew-symmetric matrix:

1

(cid:143)z

(cid:143)y

−

(cid:143)z

−
1

(cid:143)x

(cid:143)y

(cid:143)x

−
1

.









Cm = 






(5)

The three independent parameters deﬁning the matrix ((cid:143)x, (cid:143)y and (cid:143)x) represent small rotations about the

body axes of the vehicle that will bring the platform axes into perfect alignment with the body axes.

Thus, Cm is constant and only needs to be estimated once.

The process of calibrating a pair or triad of magnetometers involves estimating the various unknown

vectors and matrices deﬁned in Equations 2 through 5. Methods for estimating these unknown parame-

ters is the subject of the remainder of this paper.

3 COMPASS SWINGING

The compass swinging algorithm has been used for a some time in marine [1] and aviation [2]

applications. In these applications, the sensors traditionally used were a pair of ﬂux-gate or ﬂux-valve

magnetometers. The sensors are arranged perpendicular to each other and coincident with the x and y

body axes of the vehicle. For these systems, the heading error, δψ, due to both hard and soft iron biases

is given by:

δψ = A + B sin(ψ) + C cos(ψ) + D sin(2ψ) + E cos(2ψ).

(6)

This equation is derived in the appendix at the end of this paper and from that derivation it can be seen

that the coefﬁcients A through E are functions of the soft iron coupling terms, αij, and Earth’s local

horizontal magnetic ﬁeld strength, (cid:126)hh.

The unknown coefﬁcients A through E are estimated by levelling and rotating the vehicle through

a series of N known headings as shown schematically in Figure 3. At each known kth heading, the

heading error, δψk, is computed and used to form the following system of equations:

δψ1

δψ2
...

δψN























=












1 sin(ψ1)

cos(ψ1)

sin(2ψ1)

cos(2ψ1)

1 sin(ψ2)
...

cos(ψ2)
. . .

sin(2ψ2)

cos(2ψ2)
...

1 sin(ψN ) cos(ψN )

sin(2ψN ) cos(2ψN )

A

B

C

D

E








































(7)

A batch least squares solution of Equation 7 yields estimates for the coefﬁcients A through E.

Examination of Equations 6 and 7 reveals at least two short comings of the compass swinging pro-

cedure. First, the fact that the coefﬁcients A through E are functions of (cid:126)hh (see Appendix A) implies

that the calibration is location dependent. Thus, if the vehicle is expected to travel over a large distances,

multiple calibrations must be performed due to variations in Earth’s magnetic ﬁeld.

The second shortcoming of compass swinging becomes apparent when we note that heading is a

required input to the algorithm. Since heading errors due to hard and soft iron errors are heading depen-

dent, the heading input into the algorithm will be corrupted by a non-constant bias. Thus, an independent

measurement of heading is required when calibrating magnetometers using this method. In aviation ap-

plications, the standard practice is to use a compass rose painted on the tarmac similar to what is shown

in Figure 3, as the secondary independent heading measurement.

4 CALIBRATION ALGORITHM

In addition to the above noted limitations, the fact that the vehicle containing the magnetometers has

to be level during calibration prevents use of compass swinging in motion. To deal with these short-

coming, an alternative calibration algorithm has been developed. The new algorithm works with both a

pair or triad of magnetometers. We ﬁrst develop the algorithm assuming only a pair of magnetometers

are used. Once the basic algorithm has been developed, it is extended to three dimensions such that

it is applicable to magnetometer triads. The method developed, corrects the ﬁeld measurement errors

directly and not the effect of ﬁeld measurement errors on heading. Thus, as noted earlier, we will refer

to this as a method of calibration in the magnetic ﬁeld domain.

The fundamental idea behind calibration in the magnetic ﬁeld domain is the fact that the locus of

error-free measurements from a pair of perpendicular magnetometers is a circle.

It is easy to show

that this is the case by examining the expressions for hb

x and hb

y. From Figure 3 it is clear to see that

hb
x = hh cos(ψ) and hb

y =

−

hh sin(ψ). Squaring these expressions and adding them together leads to

the following equation:

(hb

x)2 + (hb

y)2 = h2

h cos2 ψ + h2

h sin2 ψ = h2
h

(8)

This is the equation of a circle with its center at the origin. The radius of the circle is equal to the

magnitude of the horizontal component of the local Earth magnetic ﬁeld vector which is a function of

geographical location. The magnitude of the radius varies with latitude, longitude and altitude because

Earth’s magnetic ﬁeld vector varies with location. This variation of Earth’s magnetic ﬁeld vector can be

modeled with reasonable accuracy using the current International Geomagnetic Reference Field model

(IGRF) [8].

The effect of the various magnetometer errors described in Equation 2 is to alter the shape of the

locus of measurements described by Equation 8. In this instance, as noted in Equation 2, the erroneous

x and y magnetometer outputs will be ˆhb

x and ˆhb

y. Hard iron errors, for example, shift the origin of the

basic locus. This can be shown mathematically by considering a hard iron bias vector with components

bx and by. If the x and y ﬁeld measurements in the platform axes are biased by bx and by, respectively,

the equation for the locus of the magnetometer measurements becomes:

ˆhb
x −
(cid:144)

2

+

bx

(cid:145)

(cid:144)

ˆhb
y −

by

2

= h2
h.

(cid:145)

(9)

This is still the equation of a circle but instead of having its center located at the origin, its center is at

(bx, by). In the absence of other forms of errors, scale factor errors cause the body x and y magnetome-

ter measurements to be different when both are subjected to an identical magnetic ﬁeld. This can be

expressed mathematically as follows:

ˆhb
x = (1 + sf x) hh cos ψ,

ˆhb
y =

−

(1 + sf y) hh sin ψ.

(10)

(11)

Squaring Equations 10 and 11 and adding them together leads to

2

ˆhb
x
1 + sf x (cid:33)

(cid:160)

2

ˆhb
y
1 + sf y (cid:33)

+

(cid:160)

= hh

2,

(12)

which is the equation of an ellipse centered at the origin. The major and minor axes’ magnitudes are

determined by the scale factor errors, sf x and sf y. When the hard iron erros bx and by are included in

Equations 10 and 11, the resulting locus is still an ellipse but its center is moved away from the origin to

(bx, by). That is,

2

ˆhb
bx
x −
1 + sf x (cid:33)

(cid:160)

2

ˆhb
by
y −
1 + sf y (cid:33)

+

(cid:160)

= hh

2.

(13)

Soft iron errors will modify the error-free circular locus into an ellipse but also rotate the major and

minor axes of the ellipse. To show this mathematically, consider expressions for ˆhb

x and ˆhb

y when soft

iron biases are the only sources of error. In this instance ˆhb

x and ˆhb

y become (see Equations 55 and 56 of

Appendix A):

ˆhb
x = hh cos ψ(1 + αxx)

αxyhh sin ψ

−

ˆhb
y =

hh sin ψ(1 + αyy)

−

αyxhh cos ψ.

−

In matrix form these equations become:

ˆhb
x
ˆhb
y






= 









(1 + αxx)

αxy

hh cos ψ

αyx

(1 + αyy)











hh sin ψ

−






(14)

(15)

(16)

Inverting this matrix equation and noting that hb

x = hh cos(ψ) and hb

y =

hh sin(ψ) leads to the follow-

−

ing:



hb
x

hb
y

=









1

(1 + αxx)(1 + αyy)

−

(1 + αyy)

αyx

−

αxy

−

(1 + αxx)

ˆhb
x
ˆhb
y














αxyαyx








(17)

If the two equations represented by this matrix are squared and added, the resulting locus will describe

an ellipse with rotated major and minor axes. If, in addition to soft iron errors, hard iron errors are

present, the locus will still be a rotated ellipse but its center will be displaced from the origin. Figure 4

is a graphical summary of the effect of the various errors on the locus of magnetometer measurements.

For the remainder of this paper, we will assume that Cm and αij where i

= j are zero. This is not

always a reasonable assumption. However, for the experimental work that will be discussed later in the

paper, Cm was made as small as possible by careful installation of the magnetometers and accounting for

the residuals in post process. Furthermore, examination of experimental data indicated that the ellipse (or

ellipsoid in the three dimensional case) had major and minor axes aligned with the body axes justifying

the assumption that αij = 0 when i

= j. With these simpliﬁcations, the hard iron errors affect the center

of the elliptical measurement locus while the scale factor errors and the αii soft iron terms affect the size

of the major and minor axes.

The calibration algorithm that will be developed is nothing more than a parameter estimation prob-

lem. The algorithm is an attempt to ﬁt the best ellipse (in the least squares sense) to the measured

magnetometer data. In the case of a magnetometer triad, the error-free locus of outputs is a sphere.

This sphere will be centered at the origin with a radius equal to the magnitude of Earth’s magnetic ﬁeld

vector.

The various magnetometer errors alter the spherical locus into an ellipse and displace it from the

center. In particular, the scale factor and αii soft iron terms reshape the sphere into an ellipsoid centered

at the origin. Hard iron errors shift the ellipsoid away from the origin and the effect of the wide-band

noise is to roughen the smooth surface of the measurement locus.

Thus, the calibration algorithm is the problem of determining the parameters of an ellipsoid that best

ﬁt the data collected from a magnetometer triad. Mathematically, the locus of measurements is described

by the following equation:

2

(cid:126)h
(cid:107)
(cid:107)

= h2 =

2

ˆhb
bx
x −
γx (cid:33)

(cid:160)

2

ˆhb
by
y −
γy (cid:33)

+

(cid:160)

+

ˆhb
bz
z −
γz (cid:33)

(cid:160)

2

(18)

(cid:54)
(cid:54)
where,

γx = (1 + sf x)(1 + αxx),

γy = (1 + sf y)(1 + αyy),

γz = (1 + sf z)(1 + αzz).

(19)

(20)

(21)

The parameters to be estimated are the hard iron biases denoted by bx , by, bz and the combined effect

of scale factor error and the αii soft iron terms denoted by γx, γy and γz. The given or known inputs to

the calibration algorithm are the measured magnetometer outputs, ˆhb

x, ˆhb

y, and ˆhb

z, and the magnitude of

Earth’s magnetic ﬁeld vector,

(cid:126)h
(cid:107)
(cid:107)

= h, in the geographic area where the calibration is being performed.

4.1 Least Squares Estimation

We can ﬁt an ellipsoid of revolution to measured magnetic ﬁeld data by using a batch least squares

estimator. The equations of the estimator can be obtained by linearizing Equation 18. The estimator

will have as states perturbations of the ellipsoid parameters deﬁned in Equations 18 through 21. Thus,

given an initial guess of the unknown parameters, the estimated perturbation are sequentially added to

the initial guess and the procedure is repeated until convergence is achieved.

To linearize Equation 18, we note that the pertubation of

h
(cid:107)

, written as δh, is given by [9]:
(cid:107)

bx

ˆhb
x −
h γ2

x (cid:33)

δbx +

(cid:160)

ˆhb
x −

bx
h γ3

δh =

−

+

+

(cid:160)

(cid:160)

(cid:160)

by

ˆhb
y −
h γ2

y (cid:33)

bz

ˆhb
z −
h γ2

z (cid:33)

δby +

δbz +

(cid:160)

(cid:160)

2

δγx

δγy

δγz

ˆhb
(cid:112)
y −

by
h γ3

x (cid:33)
2

y (cid:33)
2

ˆhb
(cid:112)
z −

bz
hγ3

z (cid:33)

(cid:112)

= ζx δbx + ηx δγx + ζy δby + ηy δγy + ζz δbz + ηz δγz,

(22)

(23)

where h =

(cid:126)h
(cid:107)
(cid:107)

. Note that the measured magnetometer outputs ˆhb

x, ˆhb

y, and ˆhb

z are functions of time even

though, for the sake of clarity, we have dropped the explicit notation of time in Equation 23. That is, is

should be noted that ˆhb

y is actually ˆhb

y(t = tk) and corresponds to the x-magnetometer ﬁeld measurement

at time step k. The same is true for the y and z ﬁeld measurements. Thus, given ﬁeld measurements

from k time steps, Equation 23 can be written as:

=

δh1

δh2
...

δhN









































ζx1

ζx2

ζx3
...

ηx1

ηx2

ηx3

ζy1

ζy2

ζy3
. . .

ηy1

ηy2

ηy3

ζz1

ζz2

ζz3

ηz1

ηz2

ηz3
...

ζxk

−

1 ηxk

1

−

ζyk

−

1 ηyk

1

−

ζzk

1 ηzk

−

1

−

ζxk

ηkN

ζkN

ηkN

ζkN

ηkN

δbx

δγx

δby

δγy

δbz

δγz























































Equation 24 is in the form δ(cid:126)h = H δ(cid:126)x where δ(cid:126)x is the vector of unknowns given by:

δ(cid:126)x =

δbx

δγx

δby

δγy

δbz

δγz

(cid:148)

T

(cid:149)

(24)

(25)

The vector δ(cid:126)h is the difference between the known magnetic ﬁeld vector magnitude and its magnitude

as computed from the magnetometer outputs. That is, δhk = hk −
IGRF model [8] and ˆhk is computed as:

ˆhk where hk is computed from the

ˆhk =

x + ˆhb
ˆhb

y + ˆhb
y.

(cid:113)

(26)

An estimate of the calibration parameters ˆbx, by, ˆbz, ˆγx, ˆγy, and ˆγz is obtained by using the following

iterative algorithm:

1. Select an initial guess for ˆbx, by, ˆbz, ˆγx, ˆγy, and ˆγz. The initial guess for γx, γy and γz must be

non-zero.

2. Using the values of ˆbx, by, ˆbz, ˆγx, ˆγy, and ˆγz form Equation 24.

3. Obtain a least squares estimate for δ(cid:126)x, denoted by δˆ(cid:126)x, as follows:

δˆ(cid:126)x =

H T H

1

−

H T δ(cid:126)h

(cid:128)

(cid:129)

(27)

4. Use the estimate for δˆ(cid:126)x and update the unknown parameters as follows (”(+)” denotes parameter

after update and ”(

−

)” denotes parameter before update):

−

−

bx(+) = bx(

) + δˆ(cid:126)x(1)

−

γx(+) = γx(

) + δˆ(cid:126)x(2)

by(+) = by(

) + δˆ(cid:126)x(3)

γy(+) = γy(

−

) + δˆ(cid:126)x(4)

bz(+) = bz(

−

) + δˆ(cid:126)x(5)

γz(+) = γz(

) + δˆ(cid:126)x(6)

−

(28)

(29)

(30)

(31)

(32)

(33)

5. Compute the covariance matrix P (which is a measure of the quality of the calibration) by using

P = σ2
w

H T H

1

−

,

(cid:128)

(cid:129)

(34)

where σw is the standard deviation of the magnetometer wide band noise.

6. Return to Step (2) and repeat until convergence is achieved. Convergence is achieved when the

estimate of bx, bY , bz, γx, γx and γx do not change from one iteration to the next.

The estimated calibration parameters can now be used compute the corrected ﬁeld measurements hb

x, hb
y

and hb

z from the measured magnetometer readings ˆhb

x, ˆhb

y and ˆhb

z using the following relations:

hb
x =

hb
y =

hb
z =

ˆbx

ˆby

ˆbz

ˆhb
x −
ˆγx

ˆhb
y −
ˆγy

ˆhb
z −
ˆγz

(35)

(36)

(37)

As will be shown later in the paper, the stability of the least squares solution is sensitive to at least

three factors. At this point, we will discuss one of these factor which is the quality of the initial conditions

used to start the algorithm. The closer the initial guesses are to the actual value of the six parameters,

the more stable the solution becomes. Since a judicious selection of initial conditions enhances the

performance of the calibration, we will develop an algorithm that can be used to establish the initial

conditions.

4.2 Establishing Initial Conditions

The algorithms used for establishing initial conditions, uses a non-linear, two-step estimator. This

non-linear, two-step estimator is an adaptation of an estimator presented in [10] and breaks the parameter

identiﬁcation problem given by Equation 18 into two steps. In the ﬁrst-step, a state vector called the

“ﬁrst-step state” is formed. The elements of this state vector are algebraic combinations of the elements

of the “second-step state” vector. The elements of the second-step state vector, on the other hand, are

hard iron biases and the scale factor-soft iron γ terms. The estimation problem is linear in the ﬁrst-

step state and, therefore, retains the desirable properties of a linear system. Following estimation of the

ﬁrst-step states, elements of the second-step state vector are extracted through algebraic manipulation.

Derivation of the equations for the non-linear two-step estimator begin by expanding Equation 18 as

follows:

h2 =

(ˆhb

x)2

−

−

2(ˆhb
x)(bx) + (bx)2
γ2
x
2(ˆhb
y)(by) + (by)2
γ2
y
2(ˆhb
z)(bz) + (bz)2
γ2
z

−

(ˆhb

y)2

(ˆhb

z)2

+

+

.

(38)

Note that the ﬁeld measurements are a function of time. Given k ﬁeld measurements, we can construct k

separate equations like Equation 38. Rearranging k Equation 38 like expressions into a matrix equation

of the standard (cid:126)z = H(cid:126)x + (cid:126)v form leads to:

(ˆhb

x(t1))2

(ˆhb

x(t2))2

(ˆhb

x(t3))2
...

(ˆhb

1))2

x(tk
(ˆhb

−
x(tk))2

−



















=

H11 H12

(cid:148)

(cid:149)



















bx

µ2(by)

µ3(bz)

µ1

µ3

µ4





































+ (cid:126)v.

(39)

The vector (cid:126)v represents the measurement noise. The measurement matrix H consists of two k

sub-matrices. The ﬁrst of these two sub-matrices, H11, is deﬁned as:

H11 =



















2ˆhb

x(t1)

−

2ˆhb

x(t2)

−

2ˆhb

y(t1)

−

2ˆhb

y(t2)

−

2ˆhb

z(t1)

−

2ˆhb

z(t2)

−

−

2ˆhb
x(t3)
...

−

2ˆhb
y(t3)
...

−

2ˆhb
z(t3)
...

−

2ˆhb

1)

x(tk
2ˆhb

−
x(tk)

−

−

2ˆhb

1)

y(tk
2ˆhb

−
y(tk)

−

−

2ˆhb

1)

z(tk
2ˆhb

−
z(tk)

−

.



















3

×

(40)

The second sub-matrix H12 is given by:

H12 =



















(ˆhb

y(t1))2

(ˆhb

y(t2))2

(ˆhb

y(t3))2
...

(ˆhb

z(t1))2

(ˆhb

z(t2))2

(ˆhb

z(t3))2
...

1

1

1
...

(ˆhb

1))2

y(tk
(ˆhb

−
y(tk))2

(ˆhb

z(tk
(ˆhb

1))2 1
−
z(tk))2

1

.



















(41)

The vector on the right side of Equation 39, denoted as (cid:126)x, is the ﬁrst-step state vector and consists of the

variables µ1 through µ4 which are deﬁned as follows:

µ1 = h2γ2
x

µ2 =

µ3 =

γ2
x
γ2
y
γ2
x
γ2
z

µ4 = (bx)2 + µ2(by)2 + µ3(bz)2

µ1.

−

An estimate for (cid:126)x, denoted as ˆ(cid:126)x, is obtained by:

ˆ(cid:126)x =

H T H

1

−

H T (cid:126)y

(cid:128)

(cid:129)

(42)

(43)

(44)

(45)

(46)

Once the ﬁrst-step state vector is estimated, ˆbx, by, ˆbz, ˆγx, ˆγy, and ˆγz are extracted from ˆ(cid:126)x by the following

inverse relations:

ˆbz =

ˆby =

ˆbx = ˆ(cid:126)x (1)
ˆ(cid:126)x (2)
ˆ(cid:126)x (4)
ˆ(cid:126)x (3)
ˆ(cid:126)x (5)
µ1
h2
µ1
µ2h2
µ1
µ3h2

ˆγz =

ˆγy =

ˆγx =

(cid:114)

(cid:114)

(cid:114)

(47)

(48)

(49)

(50)

(51)

(52)

It was found that Equations 39 through 52 provide a very good estimate of the calibration parameters.

It is conceivable, therefore, that this initialization algorithm alone can be used as a ”snap-shot” solution

in lieu of the iterative least squares solution developed earlier. This was avoided, however, because

the two-step formulation as discussed here does not provide for an easy way to compute the posterior

covariance matrix P which will be used as a metric for the quality of the calibration. This is because

the measurement noise vector (cid:126)v is the result of squaring the outputs of the magnetometers (i.e. vector on

the right side of Equation 39) and thus is neither zero mean nor Gaussian distributed. While novel, non-

linear estimation techniques which combine the unscented transformation [11] with Kalman or Particle

Filtering [12, 13] can be used to directly estimate the posterior covariance matrix, for the work reported

in this paper, we will use the linearized estimate of P given by Equation 34. As will be shown in the next

section, this estimate of P generally tends to over bound the actual estimation errors at a 1

σ level.

−

5 SIMULATION STUDIES

A series of simulation studies was performed to assess the performance of the magnetometer cali-

bration algorithms. The results show that the iterative batch least squares estimator is primarily sensitive

to three factors. First, the algorithm is sensitive to initial values; unless the hard iron biases and γ factors

close to their actual values, the algorithm can diverge. Second, the algorithm is sensitive to sampling

and sensor noise. The amount of noise that can be tolerated is, however, a function of the third factor

which is the shape of the measurement locus. Each of these sensitivity factors will be discussed next.

It will be recalled that the iterative batch least squares estimator requires an initial guess of hard

iron biases (b) and scale-factor/soft iron error terms (γ). The ﬁrst set of simulation studies evaluated

the performance of the algorithm where the initial conditions were chosen randomly without using the

two-step non-linear estimator. The initial guesses for the hard iron biases were picked from a normal

distribution with a mean equal to the actual biases and a standard deviation of 0.5 Gauss. Similarly, the

initial guesses for the scale-factor/soft iron error term,γ, were picked from a normal distribution centered

at the actual value of γ with a standard deviation 0.5.

Two values of measurement noise standard deviation, σw, were evaluated. One of the values consid-

ered was 5 milli-Gauss and is based on the data shown in Figure 2. The data shown in Figure 2, however,

was collected on a system that used a digital pre-ﬁlter to process that ﬁeld measurements before they

were recorded. In the absence of such a ﬁlter, the value of the wide band noise can be as high at 10

milli-Gauss. As such, the second value of σw considered was 10 mili-Gauss.

Figure 5 is a schematic that illustrates the metric used for quantifying the measurement locus geom-

etry. If during the calibration procedure the magnetometer assembly is rotated through space such that

the entire Euler angle space is spanned, the locus of magnetometer measurements obtained would be as

shown in Figure 5(a). As can be seen from the experimental data shown in Figure 6, this is not always

possible. Figure 6 shows that only a small portion of the ellipsoid is present. Thus, for the simulation

studies we will also assume that only a small portion of the ellipsoid is present (Figure 5(b)). The central

angle spanned by the strip of the ellipsoid, Φ, is used to characterize the geometry of the measurement

locus (Figure 5(c)).

Table 1 shows the four cases simulated study to quantify estimation accuracy as a function of the

three sensitivity factors discussed above. The results of these trade-off studies are shown in Figures 7

through 13. Figures 7 and 8 show the performance of the iterative batch least squares estimator in the

presence of a 5 milli-Gauss wide-band noise and when 10◦ and 20◦ strips of measurement locus are

Case & Strip
Size

I, 10◦

II, 20◦

III, 10◦

IV, 20◦

Hard Iron
Bias
1 Gauss
2 Gauss
-3 Gauss
1 Gauss
2 Gauss
-3 Gauss
1 Gauss
2 Gauss
-3 Gauss
1 Gauss
2 Gauss
-3 Gauss

bx
by
bz
bx
by
bz
bx
by
bz
bx
by
bz

Scale Factor &
Soft Iron

Wide-Band
Noise

γx
γy
γz
γx
γy
γz
γx
γy
γz
γx
γy
γz

4
3
2
4
3
2
4
3
2
4
3
2

5 milli-Gauss

5 milli-Gauss

10 milli-Gauss

10 milli-Gauss

Table 1: Parameters for Magnetometer Calibration Simulations.

available. The algorithm is seen to converge in both cases. When the measurement noise is increased

to 10 milli-Gauss, the results shown in Figures 9 and 10 are obtained. Figure 11 shows the results from

another run with a 10◦ strip and 10 mili-Gauss of wide band noise.

In this case, it is seen that the

algorithm diverges when only a 10◦ strip of the measurement locus is available. Actually, of fact the

algorithm diverges just about as frequently as it converges with the available measurement locus is small

and the wide band noise is large. The algorithm also diverged when Φ = 20◦ but not as often as it did

when Φ = 10◦. The divergence is primarily due to the initial conditions assigned to hard iron biases and

γ being too far away from the actual values. This becomes apparent when we note that in Figures 9, 10

and 11 the initial conditions are not the same because, as noted earlier, the initial conditions were varied

randomly from one try to the next. Observe, for example, that the initial conditions assigned to bx and

by for the run shown in Figure 9 are closer to the actual values than assigned for the run shown in Figure

11.

The difference in initial conditions, however, is not the only cause of the divergence because these

plots show the results for just one simulation run out of many. The algorithm diverged repeatedly when

only a 10◦ strip of the locus was used while, it converged more often when a 20◦ strip of the measurement

locus was available. As noted earlier, the measurement noise on low cost magnetometers can be as high

as the 10 milli-Gauss ﬁgure used in some of these simulations. Therefore, it is concluded that for

relatively low cost magnetometers with relatively large magnitude output noise, this algorithm is not

suitable unless a large portion of the ellipsoid is available.

This sensitivity to measurement locus geometry has a very important practical implication. When

discussing the methods for calibrating a two-magnetometer system, it was noted that the parameter esti-

mation problem is one where the best circle (in the least squares sense) is ﬁt to the noisy magnetometer

measurement data. A simple 360◦ turn on a level surface yielded the required measurement locus. In

extending this method to the three-dimensional case, a tacit assumption was that the entire sphere would

be available for the parameter estimation problem. Unfortunately this is not always the case because get-

ting a complete sphere requires spanning the entire Euler angle space. Thus, unless the magnetometer

triad is installed in an aerobatic airplane, spanning the entire Euler angle space is not possible. So the

three dimensional calibration algorithms must be able to work with data that comprises only a portion of

the entire sphere. Actual data collected from a ﬂight test is shown in Figure 6. It is clear from this ﬁgure

that an entire ellipsoid can not be obtained in a non-aerobatic aircraft.

The simulation results for the cases where the non-linear, two-Step estimator is used to initialize the

iterative batch least squares estimator are shown in Figures 12 and 13. These ﬁgures are histograms for

the bias and γ estimation errors (or residuals) for 10,000 Monte Carlo simulation runs. For each run,

simulated magnetometer outputs were corrupted with bias and scale factor errors as well as wide-band

noise. The bias and scale factor errors were held constant for all 10,000 simulation runs and had the

values given in Table 1. The wide-band noise, however, was varied for each run.

It was a random

sequence with a standard deviation of 5 or 10 milli-Gauss.

Figure 12 shows the bias estimation residuals. In none of the 10,000 cases did the solution diverge.

For the x and y axes hard iron biases, the estimation errors are seen to be less than

0.5 milli-Gauss.

±

In comparison to the x and y axes, the z axis estimation errors are slightly larger. However, this error

is smaller when the locus of magnetometer measurements is larger. A similar trend is seen in Figure 13

which shows the scale factor estimation errors. The fact that the estimation errors for both the z axis hard

iron biases and scale factor errors are larger in comparison to the x and y axes errors is not surprising

Bias Estimation
10−

×

Simulation
Case

I

II

III

IV

Error (
δbx
δby
δbz
δbx
δby
δbz
δbx
δby
δbz
δbx
δby
δbz

3 Gauss)
1.73
1.30
9.00
1.34
1.01
3.90
3.46
2.60
17.0
2.70
2.03
7.55

γ Estimation
Error (no units)
0.00549
δγx
0.00410
δγy
0.361
δγz
0.00402
δγx
0.00304
δγy
0.0756
δγz
0.0108
δγx
0.00809
δγy
0.631
δγz
0.00805
δγx
0.00606
δγy
0.143
δγz

Table 2: State Estimation Errors (1

σ).

−

because even in the 20◦ locus case the data spans only a small amount of space in the z direction.

The 1

−

σ standard deviation of the hard iron bias and γ estimation errors for one representative run

are summarized in Table 2. The 1

−

σ estimation errors are nothing more than the square root of the

diagonal elements of the covariance matrix P . As noted earlier and is conﬁrmed by observing Figure

12, Figure 13, and the data in Table 2, the estimated covariance over bounds the actual errors. Thus, P

can be used as conservative metric for the quality of the calibration.

In conclusion, initializing the iterative batch least squares estimator using the Non-Linear, two-Step

Estimator is seen to provide superior performance. More speciﬁcally, the algorithm does not diverge

even in the case when the wide-band noise on the magnetometer measurements is large. Thus, it requires

a smaller portion of the measurement locus than the case where the iterative least squares algorithm is

used alone.

6 EXPERIMENTAL RESULTS

As a ﬁnal veriﬁcation, a triad of low cost magnetometers was calibrated using the algorithms devel-

oped in this paper. The data was collected from an experimental set up where a set of low cost mag-

netometers were strapped to a long wooden boom as shown in Figure 14. The wooden boom was used

in order to isolate the magnetometers from magnetic ﬁeld generating electronics in the data collecting

computer and associated hardware. To verify the quality of the calibration, the post-calibration heading

solution was compared with the heading solution from an expensive navigation grade INS (Honeywell

YG1851 IRU). The INS and the experimental set up are shown in Figure 14.

Figure 15 shows a histogram of the residual in the magnetic ﬁeld domain after the calibration is

complete. These residuals were computed by resolving the known magnetic ﬁeld vector in the area

where this calibration took place (i.e., the San Francisco Bay Area) and resolving it into the axes of the

magnetometer triad using the precise INS attitude information. The largest residual, which is on the

x-axis magnetometer, has a mean of -0.007 Gauss and a standard deviation of 0.004 Gauss.

Figure 16 shows a one-minute trace comparing the heading solution computed using the magnetome-

ters with the heading solution generated by the INS. The heading residuals for this one-minute trace are

less than 3◦ RMS. Figure 17 is a histogram of the heading errors for the entire experiment. It is seen that

the heading error has a standard deviation of 3.6◦ and a mean of 1.2◦. The largest heading error observed

was 18◦ and was the result of the wooden boom ﬂexing relative the the INS (i.e., the truth reference)

during the data collection maneuvers. Once the mean is removed, the remaining heading error is, to a

large extent, in the form of wide-band noise which can be easily ﬁltered using a a low-pass ﬁlter.

7 CONCLUSIONS

An algorithm for calibrating strapdown magnetometers used in heading determination systems was

developed. Unlike the classic method of compass swinging which computes a series of heading correc-

tion parameters, this algorithm estimates magnetometer output errors directly and, thus, is not limited to

heading determination systems.

The calibration algorithm uses an estimator where the states are the hard iron biases, soft iron biases,

and scale factor errors. The estimator is a linearized, iterative batch least squares estimator. The initial

conditions for the estimator are established using a non-linear, two-step estimator. When initialized

thusly, monte carlo simulations show the estimation procedure to be very robust.

As presented in this paper, the calibration algorithm is limited to estimation of the hard iron biases

and combined scale factor and some soft iron effects. However, it should be possible to extend the

applicability of this method to all magnetometer errors including misalignment and all soft iron errors.

8 ACKNOWLEDGEMENTS

The authors wish to acknowledge the FAA Satellite Navigation Product Team and The Ofﬁce of

Technology and Licensing at Stanford University for sponsoring the research reported in this paper.

A APPENDIX: COMPASS SWINGING EQUATIONS

In this appendix, we derive Equations 6 and 7 which are used in the compass swinging algorithm. In

what follows, it will be assumed that the pair of magnetometers are level and there are no misalignment

errors. The effect of misalignment errors will be considered later. A level and error-free pair of magne-

tometers measures the strength of the horizontal component of the local Earth magnetic ﬁeld vector, (cid:126)hh.

The measurement made by each of the magnetometers will be:

hb
x = hh cos(ψ)

hb
y =

hh sin(ψ).

−

(53)

(54)

where hh =

(cid:126)hh (cid:107)

(cid:107)

Since the magnetometer assembly is assumed to be level, the body coordinate system

is the same as the wander-azimuth coordinate system and hb

x and hb

y can be used in lieu of hw

x and hw

y in

Equation 1.

If measurement errors are present, the output from the magnetometers in the body frame will not be

equal to hb

x and hb

y given by Equations 53 and 54. Instead, the output of the x-magnetometer will be ˆhb
x:

ˆhb
x = hb

x + δhx0 + αxxhb

x + αxyhb
y

= hb

x + δhx0 + αxxhH cos ψ

αxyhh sin ψ,

−

Similarly, the y-magnetometer output will be ˆhb
y:

ˆhb
y = hb

y + δhy0 + αyxhb

x + αyyhb
y

= hb

y + δhy0 + αyxhH cos ψ

αyyBH sin ψ.

−

(55)

(56)

The terms δhx0 and δhy0 represent the hard iron biases while the remaining terms account for errors

due to soft iron. Our objective is to evaluate heading errors as function of magnetometer measurement

errors. An expression relating heading errors to magnetometer measurement errors can be arrived at by

taking a perturbation of Equation 1. This leads to:

δψ =

∂ψ
∂hy (cid:147)

(cid:146)

δhy +

∂ψ
∂hx (cid:147)

(cid:146)

δhx

=

1
hh

−

(δhx sin ψ + δhy cos ψ)

(57)

The perturbation quantities δhx and δhy represent magnetometer measurement errors and are given by:

δhx = ˆhb

x −

δhy = ˆhb

y −

hb
x

hb
y

(58)

(59)

Substituting these values into Equation 57 and rearranging leads to the following equation for heading

error:

δψ =

(cid:146)
+

αyy

αxy −
2
αxx −
2

(cid:146)

(cid:147)
αyx

−

(cid:147)

cos(ψ)

δhx0
hh

sin(ψ)

sin(2ψ) +

(cid:146)

δhy0
hh
−
αyy −
2

αxy

This reduces to Equation 6 when the following substitutions are made:

A =

B =

C =

D =

E =

αxy −
2

(cid:146)
δhx0
hh
δhy0
hh
αxx −
2
αyy −
2

(cid:146)

(cid:146)

αyy

(cid:147)

αyx

αxy

(cid:147)

(cid:147)

cos(2ψ).

(cid:147)

(60)

(61)

(62)

(63)

(64)

(65)

Up to this point, misalignments have been ignored. Misalignment errors can be classiﬁed into two

categories. The ﬁrst category is the case of pitch and roll misalignment. Pitch and roll misalignments

are installation errors that result in the magnetometers not being level when the vehicle is level. The two

dimensional swinging algorithm cannot deal with with pitch and roll misalignments because the errors

introduced by such misalignments are time varying. The second category is a yaw misalignment. This is

the case where installation errors result in the magnetometer assembly being installed with an azimuth

bias. Mathematically, a constant azimuth bias, δψ0, due to installation errors modiﬁes Equation 60 in

the following manner:

δψ = A + B sin(ψ + δψ0) + C cos(ψ + δψ0) + D sin(2ψ + 2δψ0) + E cos(2ψ + 2δψ0).

(66)

When this equation is expanded using trigonometric identities and rearranged, one gets

δψ = ¯A + ¯B sin(ψ) + ¯C cos(ψ) + ¯D sin(2ψ) + ¯E cos(2ψ),

(67)

which is identical to Equation 6 except that the coefﬁcients are now modiﬁed. Thus, swinging can deal

with yaw misalignments. This also implies that a compass rose is not really required when using a

swinging algorithm. All that is required is to swing the magnetometer assembly through equally spaced

headings around the compass rose followed by one ﬁnal known heading. In this instance, the offset

term, δψ0, will be the sum of the installation error and the constant heading error introduced by the fact

that a compass rose was not used. Thus, the ﬁnal known heading is used to separate the two individual

components of δψ0.

References

[1] Nathaniel Bowditch. The American Practical Navigator. Defense Mapping Agency, Hydro-

graphic/Topographic Center, Bethesda, Maryland, USA, 1995.

[2] LITEF Corporation. LCR-92 Attitude Heading Reference System. LITEF Corporatoin, Freiberg,

Germany, 2001.

[3] D. Gebre-Egziabher, G. H. Elkaim, J. D. Powell, and B. W. Parkinson. A Gyro-Free, Quaternion

Based Attitude Determination System Suitable for Implementation Using Low-Cost Sensors. In

Proceedings of the IEEE Position Location and Navigation Symposium, PLANS 2000, pages 185 –

192. IEEE, 2000.

[4] Demoz Gebre-Egziabher. Design and Performance Analysis of a Low-Cost Aided-Dead Reckoning

Navigation System. PhD thesis, Department of Aeronautics and Astronautics, Stanford University,

Stanford, California 94305, December 2001.

[5] Gabriel H. Elkaim. System Identiﬁcation for Precision Control of a GPS-Autonomous Catamaran.

PhD thesis, Stanford University, Stanford, California 94305, August 2001.

[6] Michael J. Caruso. Application of Magnetic Sensors for Low Cost Compass Systems. In Proceed-

ings of the IEEE Position Location and Navigation Symposium, PLANS 2000, pages 177 – 184.

IEEE, 2000.

[7] Myron Kayton and Walter R. Fried. Avionics Navigation Systems. John Wiley and Sons, Inc, New

York, New York, 2nd edition, 1997.

[8] C.E. Barton. Revision of International Geomagnetic Reference Field Release. EOS Transactions,

77(16), April 1996.

[9] Wilfred Kaplan. Advanced Calculus, pages 86 – 88. Addison-Wesley, Reading, Massachusetts,

USA, 1952.

[10] Gordon Thomas Haupt. Development and Experimental Veriﬁcation of A Nonlinear Data Reduc-

tion Algorithm for Gravity Probe B Relativity Mission. PhD thesis, Stanford University, Stanford,

California 94305, March 1996.

[11] S. J. Julier. The Scaled Unscented Transformation. In Proceedings of the American Control Con-

ference. ACC, 2002.

[12] S. J. Julier and J. K. Uhlmann. A New Extenstion of the Kalman Filter to Nonlinear Systems.

In Proceedings of AeroSense: The 11th International Symposium on Aerospace/Defence Sening,

Simulation and Controls, Orlando, Florida. AerSense, 1997.

[13] R. van der Merwe, A. Doucet, J. F. G. de Freitas, and E. Wan. The Unscented Particle Filter. Tech-

nical Report CUED/F-INFENG/TR 380, Cambridge University, Engineering Department, Cam-

bridge, UK, August 2000.

Figure 1: Magnetometer Null-Shift Time History (Output from a Honeywell HMC2003 Magnetometer
Triad).

0123Time (min)hbz  (Gauss)-0.15-0.14-0.13-0.12-0.11-0.09-0.08-0.07-0.06-0.100.501.51.5Figure 2: Histogram of the Magnetometer Output Error shown in Figure 1.

Figure 3: Graphical Description of Swinging.

-0.12-0.08-0.06-0.04-0.020010020030040050060070080090010001100# of Samples-0.10Mean (m) = 92 mili-GaussStandard Deviation (sw) = 4.7 mili-GaussNorthSouthEastWestNESENWSW (cid:147)Swing(cid:148) the airplaneto estimate theFourier CoefficientsFigure 4: Effect of Errors on Magnetic Field Measurement Locus in 2-D.

Hard Iron EffectsScale Factor & Soft Iron EffectsMisalignment & Soft Iron Effectshh + dhhdhhhhFigure 5: Quantifying the Size of the Magnetometer Measurement Locus Available For Estimation.

YZXFYZ(b)YZ(a)(c)Figure 6: Portion of the Ellipsoid Representing the Locus of Magnetometer Measurements from Actual
Experimental Data. The Actual Measurement Data is Shown by the Dark Color Dots on the Smaller
(Inner) Sphere. After Calibration the Locus of Measurements will lie on the Larger Outer Sphere which
has a Radius Equal to the Magnitude of the Local Magnetic Field Vector .

-0.500.5-0.500.5-0.5-0.4-0.3-0.2-0.100.10.20.30.40.5hzhxhyFigure 7: Hard Iron Caused Null-Shift (in Gauss) and and γ (Unit-less) for the Iterative Least Squares
Estimator.

204060801000.511.5bx2040608010011.522.5by204060801003.532.5bzIteration204060801003.544.5gx 204060801001.522.53gy204060801001.522.5gzIterationF = 10osw = 5 milli-GaussActual ValueEstimated ValueFigure 8: Hard Iron Caused Null-Shift (in Gauss) and and γ (Unit-less) for the Iterative Least Squares
Estimator.

204060801000.511.5bx204060801001.522.5by2040608010043.532.5bzIteration20406080100234gx20406080100345gy204060801001.522.5gzIterationF = 20osw = 5 milli-GaussActual ValueEstimated ValueFigure 9: Hard Iron Caused Null-Shift (in Gauss) and and γ (Unit-less) for the Iterative Least Squares
Estimator.

204060801000.60.811.21.41.61.8bx2040608010022.53by204060801003.532.5bzIteration20406080100234gx 204060801002.533.5gy2040608010011.52gzIterationF = 10osw = 10 milli-GaussActual ValueEstimated ValueFigure 10: Hard Iron Caused Null-Shift (in Gauss) and and γ (Unit-less) for the Iterative Least Squares
Estimator.

204060801000.511.5bx204060801001.41.61.822.22.4by204060801003.83.63.43.232.82.6bzIteration20406080100234gx 20406080100123gy2040608010011.522.5gzIterationF = 20osw = 10 milli-GaussActual ValueEstimated ValueFigure 11: Divergence of the Hard Iron Caused Null-Shift (in Gauss) and and γ (Unit-less) Estimates
for the Iterative Least Squares Estimator.

2040608010000.51bx2040608010011.52by2040608010002468x 104bzIteration20406080100100200300gx2040608010050100150200gy2040608010051015x 104gzIterationF = 10osw = 10 milli-GaussActual ValueEstimated ValueFigure 12: Hard Iron Bias Estimation Errors for the when using the Non-Linear, Two-Step Estimator for
Initialization. Result from 10,000 Monte Carlo Runs .

-505 010002000300040005000 -505 010002000300040005000 -505010002000300040005000 -505 010002000300040005000 -505 010002000300040005000 -505010002000300040005000 505 0-10002000300040005000 -505 010002000300040005000 -505010002000300040005000 -505 3010002000300040005000 -505 010002000300040005000 -505010002000300040005000yx 10-3b Errorsx 10-3b Errorsx 10-3b Errorsx 10-3b Errorsyyyxx 10-3b Errorsx 10-3b Errorsx 10-3b Errorsx 10-3b Errorsxxxzx 10-3b Errorsx 10-3b Errorsx 10-3b Errorsx 10-3b Errorszzz# of Samples# of Samples# of SamplesCASE ICASE IICASE IVCASE IIIFigure 13: Scale Factor/Soft Iron (γ) Estimation Errors when using the Non-Linear, Two-Step Estimator
for Initialization. (Note: The Errors Are Unit-less).

-505 010002000300040005000 -505 010002000300040005000 0.100.1010002000300040005000gz Errors -505 010002000300040005000 -505 010002000300040005000 0.100.1010002000300040005000gz Errors -505 010002000300040005000 -505 010002000300040005000 0.100.1010002000300040005000gz Errors -505 010002000300040005000 -505 010002000300040005000 0.100.1010002000300040005000gz Errors----yx 10-3 g  Errorsx 10-3g  Errorsx 10-3g  Errorsx 10-3g Errorsyyyxx 10-3 g Errorsx 10-3g Errorsx 10-3g Errorsx 10-3g Errorsxxx# of Samples# of Samples# of SamplesCASE ICASE IICASE IVCASE IIIFigure 14: Experimental Setup for Ground Test.

Data Logging(cid:13)Computer  &(cid:13)INS Power(cid:13)Supply(cid:13)INS(cid:13)Magnetometers(cid:13)Figure 15: Magnetometer Calibration Residuals.

0.0500.05051015202530Bx Residual(cid:13)(Gauss)-0.0500.05051015202530By Residual(cid:13)(Gauss)-0.0500.05051015202530Bz Residual(cid:13)(Gauss)-s = 0.004 Gauss(cid:13)m = - 0.007 Gauss(cid:13)s = 0.006 Gauss(cid:13)m = - 0.003 Gauss(cid:13)s = 0.004 Gauss(cid:13)m = - 0.001 Gauss(cid:13)Figure 16: Comparison of INS Heading and Magnetometer Heading After Calibration.

0(cid:13)10(cid:13)20(cid:13)30(cid:13)40(cid:13)50(cid:13)60(cid:13)150(cid:13)100(cid:13)50(cid:13)0(cid:13)50(cid:13)100(cid:13)150(cid:13)d (cid:13)y  (Degrees)Time (sec)(cid:13)Figure 17: Histogram of Post Calibration Heading Errors.

-20(cid:13)-15(cid:13)-10(cid:13)-5(cid:13)0(cid:13)5(cid:13)10(cid:13)15(cid:13)20(cid:13)0(cid:13)200(cid:13)400(cid:13)600(cid:13)800(cid:13)1000(cid:13)1200(cid:13)Heading Error (deg)(cid:13)Heading Error Standard Deviation, sy = 3.6o(cid:13)(cid:13)Heading Error Standard Mean, my = 1.2o
