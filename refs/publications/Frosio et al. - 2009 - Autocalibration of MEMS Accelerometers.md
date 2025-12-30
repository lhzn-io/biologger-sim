2034

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 58, NO. 6, JUNE 2009

Autocalibration of MEMS Accelerometers

Iuri Frosio, Member, IEEE, Federico Pedersini, and N. Alberto Borghese, Member, IEEE

Abstract—In this paper, we present a novel procedure for
the on-the-ﬁeld autocalibration of triaxial micro accelerometers,
which requires neither any equipment nor a controlled environ-
ment and allows increasing the accuracy of this kind of microsen-
sor. The procedure exploits the fact that, in static conditions, the
modulus of the accelerometer output vector matches that of the
gravity acceleration. The calibration model incorporates the bias
and scale factor for each axis and the cross-axis symmetrical
factors. The parameters are computed through nonlinear opti-
mization, which is solved in a very short time. The calibration
procedure was quantitatively tested by comparing the orientation
produced by MEMS with that measured by a motion capture
system. Results show that the MEMS output, after the calibration
procedure, is far more accurate with respect to the output obtained
using factory calibration data and almost one order of magnitude
more accurate with respect to using traditional calibration models.
Index Terms—Accelerometer, autocalibration, microelectro-

mechanical system (MEMS), motion capture, sensor model.

I. INTRODUCTION

T HE ADVENT of microelectromechanical

system
(MEMS) technology has allowed miniaturized, high-
performance, and cheap sensors to be built. These have found
applications in many ﬁelds, ranging from pressure measure-
ment to hard disk actuators and virtual reality [1]. MEMS
accelerometers have recently been introduced to track the
motion of both humans and machines [2]–[6] as they allow
accurate low-budget motion capture systems to be built. This
provides an alternative to costly traditional systems, which are
generally based on optoelectronic technology.

Different from classical MEMS applications (for example,
airbag control), where impulsive accelerations are measured,
motion analysis applications require position and orientation
data. To the scope, MEMS accelerometers are integrated with
gyroscopes [7] or detailed models of the moving body [1], [8],
and their output has to be integrated over time. The accuracy
of the accelerometer output is, therefore, fundamental, and a
good calibration is needed to proﬁtably use them. The technical
data reported by manufacturers are not accurate enough for this
kind of application [9]; moreover, the sensor output depends on
temperature and, in general, on environmental conditions [10],
[11]. Therefore, they have to be calibrated in the ﬁeld to obtain
high accuracy [9].

Manuscript received October 31, 2007; revised March 6, 2008. First pub-
lished October 21, 2008; current version published May 13, 2009. The Asso-
ciate Editor coordinating the review process for this paper was Dr. V. R. Singh.
The authors are with the Applied Intelligent Systems Laboratory, Depart-
ment of Computer Science, University of Milano, 20135 Milan, Italy (e-mail:
<borghese@dsi.unimi.it>; <frosio@dsi.unimi.it>; <pedersini@dsi.unimi.it>).

Color versions of one or more of the ﬁgures in this paper are available online

at <http://ieeexplore.ieee.org>.

Digital Object Identiﬁer 10.1109/TIM.2008.2006137

We present here a novel reliable autocalibration procedure. It
is based on the assumption that an inertial sensor, in static con-
dition, is subjected only to the gravity force. As a consequence,
the module of the acceleration vector measured by the sensor
has to be equal to g = 9.81 m/s2, independent of the sensor
orientation [12], [13]. The method only requires measuring the
output of the MEMS in at least nine random orientations, and it
produces an accuracy of almost one order of magnitude larger
compared with previously introduced techniques, like [11]. We
also introduce an innovative methodology to assess the sensor
accuracy based on comparing the MEMS measurements with
those obtained by a motion capture system.

II. METHOD

A. Sensor Model

Since the adopted accelerometer is designed to provide ratio-
metric output [10], we consider the normalized accelerometer
output VT = [vx, vy, vz], which is obtained by dividing the
output voltage by the power supply voltage VCC (that is, vi =
Vi/VCC , for i = x, y, z). Let us also deﬁne the acceleration
vector AT = [ax, ay, az], which is expressed in the sensor local
reference system [O, XMEMS, YMEMS, ZMEMS) (Fig. 1), with
the axes XMEMS, YMEMS lying on the sensor surface and
ZMEMS orthogonal to the surface.

A mathematical model describing the accelerometer output

can be described in matrix form as

A = S(V − O)

where

S =

⎡

Sxx Sxy Sxz
Syx Syy Syz
Szx Szy Szz

,

⎤

O =

Ox
Oy
Oz

⎡

⎤

(1)

(2)

⎣

⎦

⎣

⎦

are the scale factor matrix and the bias vector, respectively. The
diagonal elements of S represent the scale factors along the
three axes, whereas the other elements of S are called cross-axis
factors. These terms allow describing both the axes’ misalign-
ment and the crosstalk effect between different channels caused
by the sensor electronics [13]. For an ideal accelerometer, the
cross-axis factors should all be equal to zero, whereas for a
real one, they can be as large as 2% of the sensor sensitivity,
as reported in Table I. The highest accuracy is achieved by
considering the cross-axis factors in S, as shown in Section IV.
Imposing the symmetry constraint on the scale factor matrix S
(that is, Sxy = Syx, Sxz = Szx, and Syz = Szy), the resulting
model has nine independent parameters. Calibration consists of
a procedure capable to determine these parameters.

0018-9456/$25.00 © 2008 IEEE

FROSIO et al.: AUTOCALIBRATION OF MEMS ACCELEROMETERS

2035

(a) Angles ϕ and ρ that describe the orientation of the MEMS accelerometer with respect to an absolute reference system having the Z-axis oriented
Fig. 1.
parallel to the gravity vector. The local reference system is indicated as [0 XMEMS, YMEMS, ZMEMS]. (b) Sensitivity for the acceleration is computed. The
continuous line refers to (9) and expresses the sensitivity of ϕ with respect to ax. The dotted and dashed lines refer to (10). The ﬁrst expresses the sensitivity of ϕ
with respect to ax and the second as a function of az. For simplicity, these two functions are computed for ay = 0.

TABLE I
SOME OF THE MOST SIGNIFICANT PARAMETERS OF THE
LIS3L02AL MEMS ACCELEROMETER

B. Autocalibration

The autocalibration procedure is based on the fact that the
modulus of the acceleration, in static conditions, is equal to that
of the gravity acceleration g, that is

x + a2
a2

y + a2

z = g.

(3)

(cid:6)

To compute the model parameters, we placed the sensor
in N different random orientations. For each orientation, we
evaluated the sensor output while maintaining it in a strictly
static condition. We deﬁne an error ek equal to the squared
difference between the modulus of the acceleration output by
the MEMS and g for the kth orientation as

ek = a2

x + a2

y + a2

z − g2

which is a nonlinear function of the sensor parameters S and O.
The parameters, which best ﬁt the observation data in the least-
squares sense, can be determined by minimizing the cumulative
error E with respect to the parameters. To the scope, we have
adopted Newton’s method, which is an iterative optimization
procedure that guarantees quadratic convergence [14]. Starting
from an initial guess of the sensor parameters, which is the one
provided by the sensor manufacturer, the solution is iteratively
updated as

xt+1 = xt − α · H−1(xt) · J(xt)

(6)

where xt is the unknown vector at the tth iteration, con-
taining the bias vector and the six independent elements of
the scale factor matrix: xt = [x1, . . . , x9] = [Ox, Oy, Oz, Sxx,
Syy, Szz, Sxy, Sxz, Syz]t. J(xt) and H(xt) are the Jacobian
vector and the Hessian matrix of the error E, respectively,
deﬁned as follows:

J(xt) =

∂E
∂x1

(cid:15)

, . . . ,

∂E
∂x9 (cid:16)

,

H(xt) =

hij =

(cid:17)

∂2E
∂xi∂xj (cid:18)
(7)

.

α is a damping parameter smaller than 1 and is computed
at each iteration by means of a line search procedure [14].
Iterations are stopped when the following convergence criterion
is satisﬁed:

=

i=x,y,z
(cid:7)

⎧
⎨

j=x,y,z
(cid:7)

[Sij · (Vj,k − Oj)]2

− g2

(4)

⎫
⎬

max

l − xt−1
xt
l + xt−1
xt

l

l

< ε

(cid:24)

(8)

where Vj,k is the jth MEMS output for the kth orientation.

⎩

⎭

By adding e2

k’s over all the measured orientations, a cumula-

tive error E is obtained as

E = E(Ox, Oy, Oz, Sxx, Syy, Szz, Sxy, Sxz, Syz) =

N

e2
k

k=1
(cid:14)
N

(5)

where ε is a threshold, which has empirically been set equal
to 1.5 · 10−6. Less than ten iterations are generally sufﬁcient
to converge. The accuracy on the parameter estimate can be
assessed through the covariance analysis [15] carried out on
the linearized version of (4) and (5) around the ﬁnal value
of the parameters. The results of this analysis are reported in
Table II.

(cid:19)(cid:20)
(cid:20)
(cid:20)
(cid:20)
(cid:20)

(cid:21)

2 (cid:20)
(cid:20)
(cid:20)
(cid:20)
(cid:20)

(cid:22) (cid:23)

2036

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 58, NO. 6, JUNE 2009

TABLE II
PARAMETERS ESTIMATED WITH THE CLASSICAL SIX-PARAMETER MODEL [5] (CALIB I) AND THE NINE-PARAMETER MODEL
INTRODUCED HERE (CALIB II). EACH PARAMETER IS REPORTED ALONG WITH ITS STANDARD DEVIATION

The adoption of a least-squares method for ﬁnding the so-
lution of the calibration problem is based on the assumption
that the noise affecting the measured data is additive and zero
mean. The output of a MEMS is mainly affected by the thermal
and electronic noise [11], [13], which are usually modeled as
additive white Gaussian noise (AWGN) added to the analogic
output of each sensor channel. These signals are then sampled
and quantized, introducing a quantization noise characterized
by zero-mean uniform probability density and white power
spectral density. It can, therefore, be assumed that the output of
the MEMS is corrupted by an unbiased additive white noise that
is statistically independent from the signal. Consequently, by
averaging many samples of the MEMS output for a sufﬁciently
long time, the standard deviation of this noise can largely
be reduced. This is sufﬁcient when considering the optimal
estimate of the model parameters, which minimizes the error
E in a least-square sense.

C. Orientation Computation

Once the autocalibration procedure has been completed, the
accelerometer is ready to be used. We ﬁrst observe that the
orientation of MEMS in 3-D space can be deﬁned by only
two angles, which represent the orientation of the device with
respect to the gravity vector g; the rotation around an axis
parallel to g cannot be observed since the sensor output is
invariant for rotations around such an axis.

Fig. 2. Orientation of the MEMS accelerometer expressed both with the
orientation angles (φ and ρ) and with the Euler angles (α, β, γ). Because
the value of α is irrelevant, it is arbitrarily set to 0; consequently, the nodes’
axis N coincides with the X-axis.

Let us deﬁne an absolute reference frame having the Z-axis
parallel to g. Let us indicate as (ϕ, ρ) the angles between the
XMEMS and YMEMS axes and the horizontal plane [Fig. 1(a)].
From the acceleration vector obtained through (1), the angles ϕ
and ρ could be computed by means of the following equations:

ϕ = arcsin(ax),

ρ = arcsin(ay).

(9)

The equations in (9) are frequently used with biaxial ac-
celerometers, but they suffer from a critical drawback: The
sensitivity on the estimated value of ϕ and ρ depends on the
value of ϕ and ρ itself, as shown in Fig. 1(b). To overcome this

FROSIO et al.: AUTOCALIBRATION OF MEMS ACCELEROMETERS

2037

Fig. 3.
MEMS is attached is shown with ﬁve markers rigidly connected to the MEMS sensor.

(a) Zoom of the MEMS mounted on a board is shown along with the MEMS local reference system set by the manufacturer. (b) Structure on which the

problem, the following trigonometric equations are used here to
compute ϕ and ρ:

ϕ = arctan

ax
a2
y + a2
z

,

⎞

⎠

⎛

⎝

(cid:6)

ρ = arctan

(cid:29)

(cid:30)

ay
x + a2
a2

.

z (cid:31)
(10)

These equations guarantee that the accuracy is almost con-
stant inside the whole range of values that ϕ and ρ can assume,
as shown by the dotted and dashed lines in Fig. 1(b).

The two angles deﬁned in (10) represent two independent
orientation parameters in the sense that any error on the esti-
mate of ϕ does not inﬂuence the estimate on ρ and vice versa.
Another possible angles system used to describe orientation is
through Euler angles. These do not enjoy the same property of
(ϕ, ρ) angles because they are deﬁned as a sequence of rotations
(cf. Fig. 2 and the Appendix).

To express the sensor orientation in terms of the Euler angles
(α, β, γ), we have derived the relationship between (ϕ, ρ) and
(α, β, γ), which is reported in the Appendix [see (A3) and
(A8)]. The following relationships are obtained:

α = 0

sin(β) =

sin2(ϕ) + sin2(ρ),

(0 ≤ β ≤ π)

sin(γ) =

(cid:6)
sin(ϕ)
sin(β)

=

sin(ϕ)
sin2(ϕ) + sin2(ρ)

.

(11)

Since the angle α expresses a rotation around the absolute
vertical axis, it cannot be measured by MEMS. It remains
undetermined, and it can be set equal to zero.

(cid:30)

III. RESULTS

The proposed calibration procedure has been applied to
four MEMS accelerometers produced by ST Microelectronics
(model LIS3L02AL) [10]. They are triaxial linear analogic
accelerometers that are capable of measuring accelerations in
the range [−2g, +2g] along each axis. The typical bias and
scale parameter, as provided by the manufacturer, are reported
in Table I. If a normalized voltage is considered, the typical
value of the parameters is 0.5 and 5 m/s2, respectively.

The output of the MEMS accelerometers is acquired by a
host computer at a rate of 960 Hz through a NI-DAQ board. An
analog low-pass RC ﬁlter has been added to the accelerometer

output to ﬁlter high-frequency noise and avoid aliasing, which
would have been introduced by sampling. The bandwidth of the
ﬁlter was set to 285 Hz, which is large enough for the human
ﬁnest-motion frequency content [16].

is,

that

To evaluate the accuracy of the autocalibration procedure,
we have compared the orientation angles computed in (10) with
the same angles computed by a commercial motion capture
system,
the SMART3D [17]. This system is able
to compute the 3-D position of a set of retroreﬂective markers
whose position is surveyed by six cameras. The work-
ing volume of the motion capture system was approximately
500 mm × 500 mm × 500 mm, which allowed accommodating
different MEMS orientations with optimal marker visibility.
With this working volume, the markers are localized with an
accuracy of 0.1 mm (RMS error).

The markers and accelerometer, which are rigidly connected
to each other, were ﬁxed on a frame that could be oriented in
any direction, as shown in Fig. 3(b). Five markers were located
the vicinity of the accelerometer. The orientation of the MEMS
supporting structure is then computed as the mean rotational
component of the rigid motion undergone by the markers. The
angular accuracy in the measurement of this orientation can
be derived from the spatial accuracy in the localization of the
markers. This can be done by determining the sensitivity of the
angular displacement with respect to a spatial displacement,
as described in [18]. For the adopted setup (ﬁve markers,
spatial accuracy of 0.1 mm (RMS) and minimum distance of
100 mm from the accelerometer), the angular accuracy in the
measurement of the orientation of the MEMS results in being
better than 0.025◦ (RMS).

The vertical direction of the motion capture reference system
was carefully established to guarantee that it is parallel to
gravity by surveying two markers put onto the wire of a plumb
line held along the vertical.

From the 3-D position of the ﬁve markers positioned on the
MEMS board, we computed the angles ϕ and ρ, which deﬁne
the orientation of the structure and consequently of the MEMS
accelerometer in the motion capture reference system. This has
been done by using quaternions [20] that allow determining
the rotation by solving a linear system, thereby guaranteeing
the orthonormality of the obtained rotation matrix. At the
same time, for each sampled orientation, the angles ϕ and
ρ are also estimated by processing the MEMS sensor output
through (10).

The high accuracy of the motion capture system lets us
take its orientation measurements as the ground truth. For this

2038

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 58, NO. 6, JUNE 2009

TABLE III
MEAN ERROR AND STANDARD DEVIATION OF THE MEASURED ORIENTATION, EXPRESSED BY ANGLES ϕ AND ρ (FIRST TWO BLOCKS) AND WITH THE
EULER ANGLES β AND γ (SECOND TWO BLOCKS), FOR THE FOUR ACCELEROMETERS CALIBRATED WITH THE FACTORY CALIBRATION DATA
(COLUMN FACTORY), WITH THE CLASSICAL SIX-PARAMETER MODEL REPORTED IN [11] (COLUMN CALIB I) AND THE NOVEL
NINE-PARAMETER MODEL INTRODUCED HERE (COLUMN CALIB II). ERRORS ARE IN DEGREES

reason, we adopted a comparative approach to evaluate the
accuracy of the orientation angles ϕ and ρ, comparing the value
output by the MEMS with those computed through the motion-
capture system data.

The mean estimated value of the biases and the scale factors
± their standard deviation obtained by using the six- and nine-
parameter model introduced here are reported in Table II, in
the rows indicated with “Calib I” and “Calib II,” respectively.
N represents the number of random orientations acquired for
each accelerometer. The residuals, i.e., E in (5), for the four
accelerometers were, respectively, 0.0151, 0.0069, 0.0365, and
0.0085 for Calib I and 0.0117, 0.0032, 0.0263, and 0.0039
for Calib II. As can be appreciated, the estimate uncertainty
is below 0.5% and is often much lower. In particular, the
uncertainty on the scale factor consistently improves when the
nine-parameter model is adopted.

The estimated orientation angles along with their standard
deviation are reported in Table III, which describes the metro-
logical performance of the sensor in the attitude estimate.

The error in the angle estimate ranges from −23.10◦ to
+6.15◦ when factory calibration data are used. It decreases to
the range −1.54◦ to +1.15◦ when the six-parameter model was
used in (1), and it further decreases to the range −0.26◦ to
+0.26◦ when the nine-parameter model was adopted.

To investigate the spatial distribution of the errors, we deﬁne

the error angles ∆ϕ and ∆ρ as

∆ϕ = ϕMEMS − ϕSMART3D
∆ρ = ρMEMS − ρSMART3D

(cid:17)

(12)

and plot them in Fig. 4 for one of the sensors (sensor #1). As
can be seen, errors do not show any particular space depen-
dence. By using factory calibration data [Fig. 4(a)], errors are
distributed approximately inside a circle centered in [0, 0]. The
dimension of this circle is greatly reduced when autocalibration
is carried out and, in particular, when the nine-parameter model
is adopted [Fig. 4(b)]. Fig. 4(c) and (d) show that, thanks to
the particular trigonometric formulation of (10), the error is
isotropic, as it does not depend on the values assumed by ϕ
and ρ. Similar results are obtained for the other accelerometers
calibrated.

IV. DISCUSSION

MEMS calibration is usually carried out in the factory.
A dedicated machine positions a MEMS accelerometer in
several precisely known orientations. It reads the MEMS out-
put and estimates the diagonal parameters of the scale factor

FROSIO et al.: AUTOCALIBRATION OF MEMS ACCELEROMETERS

2039

Fig. 4. Error in the estimate of ϕ and ρ for the 72 orientations measured for sensor #1.

matrix S [Sx, Sy, Sz] and the three bias values [Ox, Oy, Oz].
This procedure is quite time consuming for large MEMS pro-
duction and not very effective as these parameters may change
when MEMS are placed in the operating environment, because
of their sensitivity to temperature.

To avoid these drawbacks, autocalibration has recently been
introduced with a six-parameter model [11], leading to a sig-
niﬁcant improvement with respect to using factory calibration
data. The results reported in Table III (“Calib I” column) show
a residual error on the order of a few degrees on the orientation
measurements, whereas the measurement error was as large as
20◦ with factory calibration data (MEMS #3 in Table III). How-
ever, the accuracy can further be improved by also considering
the cross-axis terms inside the scale factor matrix, leading to
the nine-parameter model proposed here (“Calib II” column
of Table III). With this model, the accuracy is reduced to less
than one degree (±0.26◦). The improvement with respect to the
classical six-parameter model is, therefore, almost one order of
magnitude and is consistent in all the calibration experiments.
This fact, together with the very low uncertainty in the param-
eter estimate (cf. Table II), can reasonably be interpreted as a
better model-ﬁtting capability of the proposed nine-parameter
model with respect to the six-parameter model. This allows us
to draw the conclusion that the three cross-axis scale parameters

in the present model allow a better ﬁtting of the physical MEMS
behavior.

The value of scale parameters and biases obtained through
autocalibration is generally close but not equal to that provided
by the manufacturer. The typical differences are on the
order of ±10% for the bias and ±5% for the scale factor
(cf. Table II). However, when they are used to compute the
MEMS orientation,
this error is ampliﬁed. The error was
in some cases larger than 20◦ (MEMS #3 in Table II), with
standard deviation exceeding 10◦, when the values of S and
O given by the factory (and null cross-axis scale factors)
were used. Nevertheless, factory parameters can be used as a
reliable initialization point for Newton’s optimization, and a
small number of iterations are sufﬁcient to obtain a reliable and
accurate estimate of the sensor parameters.

The symmetrical matrix S considered here can take into
account the crosstalk between axes. This is the electric coupling
between pairs of output channels, which usually produces a
symmetrical effect [13], [20]. It can also accommodate sym-
metrical axis misalignment, which can be described by what is
called a geometrical deformation [14, Fig. 5(a)].

Other parameters, that is, the anti-symmetric components,
could be accommodated inside the matrix S. However, they
would lead to overﬁtting, as we have experimentally veriﬁed

2040

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 58, NO. 6, JUNE 2009

nitude, the accuracy with respect to the classical autocalibration
models presented in the literature. A new and reliable procedure
to evaluate the calibration performance, based on a motion
capture system, has also been presented.

APPENDIX
RELATIONSHIP BETWEEN TILT (ϕ, ρ)
AND EULER ANGLES (α, β, γ)

The Euler angles considered here measure three sequen-
tial (not independent) rotations of the local reference system
[O XMEMS YMEMS ZMEMS] with respect to the absolute refer-
ence one [O X Y Z]. They are deﬁned as follows. The angle
α measures the rotation around the absolute vertical axis Z.
The angle β measures the rotation around the node axis N ,
that is, the X-axis after rotating around Z. Finally, the angle γ
measures the rotation around the local Z-axis ZMEMS. In this
particular case, α cannot be determined as the rotation of
MEMS around the absolute vertical axis cannot be appreciated.
For this reason, in the following, α = 0 will be assumed and the
node axis is coincident with the X-axis.

Deﬁning (uX, uY, uZ) as the three versors in the absolute
frame and (xS, yS, zS) as the versors of the sensor’s frame, we
can express the orientation angles through the inner product (cid:4).(cid:5)
as follows:

cos(β) = (cid:4)zS, uZ(cid:5),
cos(γ) = (cid:4)xS, uX(cid:5),

sin(ϕ) = (cid:4)xS, uZ(cid:5)
sin(ρ) = (cid:4)yS, uZ(cid:5).

(A1)

By imposing the unitary norm of the versor uZ, we obtain

(cid:6)uZ(cid:6)2 = (cid:4)xS, uZ(cid:5)2 + (cid:4)yS, uZ(cid:5)2 + (cid:4)zS, uZ(cid:5)2
= sin2(ϕ) + sin2(ρ) + cos2(β) = 1.

(A2)

Isolating β in the preceding equation, we obtain

sin2(ϕ) + sin2(ρ) = 1 − cos2(β) = sin2(β).

(A3)

Considering that sin(β) ≥ 0 because, in the Euler conven-
tion, 0 ≤ β ≤ π, β can be derived from the tilt angles as
follows:

sin(β) =

sin2(ϕ) + sin2(ρ),

(0 ≤ β < π).

(A4)

(cid:6)

As far as γ is concerned, let us consider the projection on
the XY plane of the unit circle on the plane xSyS, which is
represented in Fig. 6. The projection of this circle forms an
ellipse of axes OAX and OAY , where OAX = 1, and OAY =
cos(β). The vector OS, that is, the projection of the versor xS
on the plane XY , has the components

(cid:6)OB(cid:6) = (xS, uX) = cos(γ)

(cid:6)OC(cid:6) = (xS, uY) = sin(γ) cos(β).

(A5)

On the other hand, ϕ is deﬁned as the angle between xS and

OS; therefore, (cid:6)OS(cid:6) = cos(ϕ).

By imposing (cid:6)OS(cid:6)2 = (cid:6)OB(cid:6)2 + (cid:6)OC(cid:6)2, we obtain

cos2(ϕ) = cos2(γ) + sin2(γ) cos2(β).

(A6)

Fig. 5. Two-dimensional pictorial representation of two types of axis mis-
alignment (adapted from [14, Fig. 2.7]). (a) Geometrical deformation. The
two axes are rotated by an angle of the same amplitude but opposite sign. In this
case, the transformation can be expressed by a symmetrical matrix Ssym (ϕ).
(b) Deformation followed by a rotation. In this case, the angle between the
two axes, after the transformation, is the same as in (a), but they are both
rotated by the same amount ρ. In this case, the transformation is described by a
nonsymmetrical matrix, resulting from the product of the rotation matrix R(ρ)
and the same deformation matrix Ssym (ϕ) of (a).

that the accuracy of the sensor decreases in this case. For
this reason, a symmetrical scale factor matrix Ssym has been
considered in (1).

In the general case, however, axis misalignment is not sym-
metrical [cf. Fig. 5(b)], and it is described by the product of a
rotation matrix R and a symmetrical deformation matrix Ssym
[21], i.e.,

Sasym = R · Ssym

(13)

where Ssym is the symmetrical scale factor matrix used in our
model.

To understand the role R, we have to recall that the actual
orientation of the MEMS sensing axes [0 Xsens, Ysens, Zsens]
is implicitly established at calibration time. In fact, mini-
mizing (5), when MEMS is horizontal, the sensing axes are
oriented such that the sum of the angles between Zsens and
the gravity acceleration, and between Xsens and Ysens and the
horizontal plane, is minimum in the l2 norm. Any residual
rotation between sensing axes and the local reference sys-
tem, which speciﬁes the MEMS case orientation in space
[[0 XMEMS, YMEMS, ZMEMS] in Fig. 1(a)], is represented by
the matrix R. This rotation cannot be recovered by any autocali-
bration method, as it would require that the MEMS absolute ori-
entation is exactly known in all the calibration positions, which
cannot be done inside an autocalibration procedure. However, it
should be remarked that the residual error after calibration, by
using only a symmetrical scale factor matrix Ssym, is extremely
low (cf. Table III, column “Calib II”). Therefore, the type of
axis misalignment, which can be expressed as a pure rotation,
can be considered as having a little impact on the MEMS
accuracy.

V. CONCLUSION

In this paper, we have presented an on-the-ﬁeld autocali-
bration procedure for MEMS triaxial accelerometers, which
requires neither any equipment nor a controlled environment.
It computes the sensor bias and scale factor based on a novel
nine-parameter model, which also incorporates cross-axis scale
factors. This has allowed increasing, almost one order of mag-

FROSIO et al.: AUTOCALIBRATION OF MEMS ACCELEROMETERS

2041

[14] K. Madsen, H. B. Nielsen, and O. Tingleff, Methods for Non-Linear
Least Squares Problems, 2nd ed. Lyngby, Denmark: IMM, Tech. Univ.
Denmark, 2004.

[15] W. H. Press, S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery, Numer-
ical Recipes 3rd Edition: The Art of Scientiﬁc Computing. Cambridge,
U.K.: Cambridge Univ. Press, 2003.

[16] D. Winter, Biomechanics and Motor Control of Human Movement.

Hoboken, NJ: Wiley, 1990.

[17] [Online]. Available: <http://www.bts.it>
[18] N. C. Barford, Experimental Measurements: Precision, Error and Truth.

Hoboken, NJ: Wiley, 1985.

[19] O. Faugeras, Three-Dimensional Computer Vision. Cambridge, MA:

MIT Press, 1993.

[20] M. Alonso and E. J. Finn, Fundamental University Physics, vol. 2, Fields

and Waves. Amsterdam, The Netherlands: Inter Eur., 1974.

[21] R. Hartley and A. Zisserman, Multiple View Geometry in Computer
Vision, 2nd ed. Cambridge, U.K.: Cambridge Univ. Press, 2003.

Iuri Frosio (M’07) received the M.Sc. and Ph.D. de-
grees in biomedical engineering from Politecnico di
Milano, Milan, Italy, in 2002 and 2006, respectively.
Since 2006, he has been an Assistant Professor
with the Department of Computer Science, Univer-
sity of Milano. His research interests include medical
image processing, virtual reality, artiﬁcial intelli-
gence, and movement analysis.

Federico Pedersini received the “Laurea” (cum
laude) and Ph.D. degrees in electronics and telecom-
munication engineering from Politecnico di Milano,
Milan, Italy, in 1991 and 1994, respectively.

Until 2001, he was with the Department of Electri-
cal Engineering, Politecnico di Milano, where he was
doing research mainly in the ﬁeld of image process-
ing for 3-D reconstruction and camera calibration.
Since 2003, he has been with the Department of
Computer Science, University of Milano, where he
has been an Associate Professor of digital architec-
tures since 2005. His research interests include signal and image processing for
measurement and analysis, as well as architectures and algorithms for wireless
sensor networks.

N. Alberto Borghese (M’97) received the degree
with full marks and honors from Politecnico di
Milano, Milan, Italy, in 1985.

He was a Visiting Scholar with the Center
for Neural Engineering, University of Southern
California, Los Angeles, in 1991, with the Depart-
ment of Electrical Engineering, California Institute
of Technology, Pasadena, in 1992, and with the
Department of Motion Capture of Electronic Arts,
Vancouver, BC, Canada, in 2000. He is currently an
Associate Professor with the Department of Com-
puter Science, University of Milano, where he teaches courses on intelligent
systems and robotics and is the Director of the Applied Intelligent Systems Lab-
oratory. He has coauthored more than 40 peer-reviewed journal papers and is
the holder of several patents. His research interests include quantitative human
motion analysis and modeling, statistical learning from data, and applications
to vision, graphics, and medical imaging.

Fig. 6. Unit circle deﬁned by the versors xS and yS projected on the XY
plane.

A manipulation of (A5) gives

sin2(ϕ) = sin2(γ) − sin2(γ) cos2(β)

= sin2(γ)
= sin2(γ) sin2(β).

1 − cos2(β)

(cid:21)

(cid:22)

(A7)

Assuming that ϕ ≥ 0 for 0 ≤ γ ≤ π, as shown in Fig. 6, and

considering that sin(β) ≥ 0, γ can be computed as

sin(γ) =

sin(ϕ)
sin(β)

=

sin(ϕ)
sin2(ϕ) + sin2(ρ)

.

(A8)

(cid:30)

REFERENCES

[1] J. K. Perng, B. Fischer, S. Hollar, and K. S. J. Pister, “Acceleration sensing

glove (ASG),” in Proc. ISWC, 1999, pp. 178–180.

[2] M. S. Conover, “Using accelerometers to quantify infant general move-
ments as a tool for assessing motility to assist in making diagnosis
of cerebral palsy,” M.S. thesis, Virginia Polytech. Inst. State Univ.,
Blacksburg, VA, 2003.

[3] R. Barbieri, E. Farella, L. Benini, B. Ricco, and A. Acquiaviva, “A low
power motion capture system with integrated accelerometers,” in Proc.
CCNC, 2004, pp. 418–423.

[4] D. Giansanti, G. Maccioni, and V. Macellari, “The development and test
of a device for the reconstruction of 3-D position and orientation by means
of a kinematic sensor assembly with rate gyroscopes and accelerometers,”
IEEE Trans. Biomed. Eng., vol. 52, no. 7, pp. 1271–1277, Jul. 2005.
[5] D. Roetenberg, P. J. Slycke, and P. H. Veltink, “Ambulatory position and
orientation tracking fusing magnetic and inertial sensing,” IEEE Trans.
Biomed. Eng., vol. 54, no. 5, pp. 883–890, May 2007.

[6] C. W. Tan and S. Park, “Design of accelerometer-based inertial navigation
systems,” IEEE Trans. Instrum. Meas., vol. 54, no. 6, pp. 2520–2530,
Dec. 2005.

[7] T. Sakaguchi, T. Kanamori, and H. Katayose, “Human motion capture
by integrating gyroscopes and accelerometers,” in Proc. IEEE/SICE/RSJ
MFI, 1996, pp. 470–475.

[8] S. Kurata, M. Makikawa, H. Kobayashi, A. Takahashi, and R. Tokue,
“Joint motion monitoring by accelerometers set at both near sides around
the joint,” in Proc. IEEE EMBC, 1998, pp. 1936–1939.

[9] A. Krohn, M. Beigl, C. Decker, U. Kochendörfer, P. Robinson, and
T. Zimmer, “Inexpensive and automatic calibration for acceleration sen-
sors,” in Proc. UCS, 2004, pp. 245–258.

[10] STMicroelectronics, LIS3L02AL 3axis-2g linear accelerometer, 2004.

[Online]. Available: <http://www.st.com/stonline/>

[11] Z. C. Wu, Z. F. Wang, and Y. Ge, “Gravity based online calibration for
monolithic triaxial accelerometers’ gain and offset drift,” in Proc. 4th
World Congr. Intell. Control Autom., 2002, pp. 2171–2175.

[12] N. Yazdi, F. Ayazi, and K. Najaﬁ, “Micromachined inertial sensors,” Proc.

IEEE, vol. 86, no. 8, pp. 1640–1659, Aug. 1998.

[13] T. Mineta, S. Kobayashi, Y. Watanabe, S. Kanauchi, I. Nakagawa,
E. Suganurna, and M. Esashi, “Three-axis capacitive accelerometer with
uniform axial sensitivities,” in Proc. Solid-State Sens. Actuators, Eurosen-
sors IX. Transducers, 1995, vol. 2, pp. 554–557.
