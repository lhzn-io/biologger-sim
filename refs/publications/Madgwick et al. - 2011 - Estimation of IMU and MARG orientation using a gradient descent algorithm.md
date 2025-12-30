Estimation of IMU and MARG orientation using a
gradient descent algorithm

Sebastian O.H. Madgwick, Andrew J.L. Harrison, Ravi Vaidyanathan

Abstract—This paper presents a novel orientation algorithm
designed to support a computationally efﬁcient, wearable inertial
human motion tracking system for rehabilitation applications. It
is applicable to inertial measurement units (IMUs) consisting of
tri-axis gyroscopes and accelerometers, and magnetic angular
rate and gravity (MARG) sensor arrays that also include tri-axis
magnetometers. The MARG implementation incorporates mag-
netic distortion compensation. The algorithm uses a quaternion
representation, allowing accelerometer and magnetometer data to
be used in an analytically derived and optimised gradient descent
algorithm to compute the direction of the gyroscope measurement
error as a quaternion derivative. Performance has been evaluated
empirically using a commercially available orientation sensor
and reference measurements of orientation obtained using an
optical measurement system. Performance was also benchmarked
against the propriety Kalman-based algorithm of orientation
sensor. Results indicate the algorithm achieves levels of accuracy
matching that of the Kalman based algorithm; < 0.8◦ static
RMS error, < 1.7◦ dynamic RMS error. The implications of the
low computational load and ability to operate at small sampling
rates signiﬁcantly reduces the hardware and power necessary
for wearable inertial movement tracking, enabling the creation
of lightweight, inexpensive systems capable of functioning for
extended periods of time.

I. INTRODUCTION

The accurate measurement of orientation plays a critical
role in a range of ﬁelds including: aerospace [1], robotics [2],
[3], navigation [4], [5] and human motion analysis [6], [7]
and machine interaction [8]. In rehabilitation, motion tracking
is vital enabling technology,
in particular for monitoring
outside clinical environs; ideally, a patient’s activities could
be continuously monitored, and subsequently corrected. While
extensive work has been performed for motion tracking for
rehabilitation, an unobtrusive, wearable system capable of
logging data for extended periods of time has yet
to be
realized. Existing systems often require a laptop or handheld
PC to be carried by the subject due to the processing, data
storage, and power requirements of the sensory equipment.
This is not practical outside of a laboratory environment, thus
detailed data may only be obtained for short periods of time
for a limited range of subject’s motion. More precise data
representative of a subject’s natural behaviour over extended
periods of time (e.g. an entire day or even a week) would be

Sebastian Madgwick is with the Department of Mechanical Engineering,

University of Bristol, e-mail: <s.madgwick@bristol.ac.uk>.

Ravi Vaidyanathan is with the Department of Mechanical Engineering, Uni-
versity of Bristol, Queens Building, BS8 1TR and the Department of Sys-
tems Engineering at the US Naval Postgraduate School, Monterey, CA, USA,
93940. e-mail: <r.vaidyanathan@bristol.ac.uk>.

Andrew Harrison is with the Department of Mechanical Engineering, Uni-

versity of Bristol, e-mail: <andrew.j.l.harrison@bristol.ac.uk>.

of signiﬁcant utility in this realm. In a recent survey, Zhoua
[7], cited real time operation, wireless properties, correctness
of data, and portability as major deﬁciencies that must be
addressed to realize a clinically viable system.

A. Inertial Motion Tracking Systems

Whilst a variety of technologies enable the measurement of
orientation, inertial based sensory systems have the advantage
of being completely self contained such that the measurement
entity is constrained neither in motion nor to any speciﬁc
environment or location. An IMU (Inertial Measurement Unit)
consists of gyroscopes and accelerometers enabling the track-
ing of rotational and translational movements. In order to
measure in three dimensions, tri-axis sensors consisting of 3
mutually orthogonal sensitive axes are required. A MARG
(Magnetic, Angular Rate, and Gravity) sensor is a hybrid
IMU which incorporates a tri-axis magnetometer. An IMU
alone can only measure an attitude relative to the direction of
gravity which is sufﬁcient for many applications [2], [1], [6].
MARG systems, also known as AHRS (Attitude and Heading
Reference Systems) are able to provide a complete measure-
ment of orientation relative to the direction of gravity and the
earth’s magnetic ﬁeld. An orientation estimation algorithm is
a fundamental component of any IMU or MARG system. It is
required to fuse together the separate sensor data into a single,
optimal estimate of orientation.

The Kalman ﬁlter [9] has become the accepted basis for
the majority of orientation algorithms [2], [10], [11], [12]
and commercial inertial orientation sensors; xsens [13], micro-
strain [14], VectorNav [15], Intersense [16], PNI [17] and
Crossbow [18] all produce systems founded on its use. The
widespread use of Kalman-based solutions are a testament
they have a
to their accuracy and effectiveness, however,
number of disadvantages. They can be complicated to im-
plement which is reﬂected by the numerous solutions seen
in the subject literature [2], [10], [11], [12], [19], [20], [21],
[22], [23]. The linear regression iterations, fundamental to the
Kalman process, demand sampling rates which can far exceed
the subject bandwidth (e.g. a sampling rate between 512 Hz
[13] and 30 kHz [14] may be necessary for human motion
capture applications where system portability is critical). The
state relationships describing rotational kinematics in three-
dimensions typically require large state vectors and an ex-
tended Kalman ﬁlter implementation [2], [12], [19] to linearise
the problem.

These challenges demand a large computational load for
implementation of Kalman-based solutions and provide a clear

2011 IEEE International Conference on Rehabilitation Robotics Rehab Week Zurich, ETH Zurich Science City, Switzerland, June 29 - July 1, 2011978-1-4244-9861-1/11/$26.00 ©2011 IEEE179motivation for alternative approaches. Previous approaches
to address these issues have implemented either fuzzy pro-
cessing [1], [3] or frequency domain ﬁlters [24] to favour
accelerometer measurements of orientation at
low angular
velocities and the integrated gyroscope measurements at high
angular velocities. Such an approach is simple but may only
be effective under limited operating conditions. Bachman et al
[25] and Mahony et al [26] present separate algorithms which
both employ a complementary ﬁlter process. This algorithm
structure has been shown to provide effective performance at
relatively little computational expense.

This paper introduces orientation estimation algorithm that
is applicable to both IMU and MARG systems. The algorithm
employs a quaternion representation of orientation (as in:
[25], [12], [19]) to describe the coupled nature of orientations
in three-dimensions and is not subject
to the problematic
singularities associated with an Euler angle representation.
A complete derivation and empirical evaluation of the new
algorithm is presented. Its performance is benchmarked against
existing commercial ﬁlters and veriﬁed with optical tracking
system.

II. ORGANISATION OF PAPER

Section III delineates the mathematical derivation of the
orientation estimation algorithm, including a description of the
parameterization and compensation for magnetic distortion.
Section IV describes the experimental equipment used to test
and verify the performance of the algorithm. Section V quanti-
ﬁes the experimental testing and accuracy of the algorithm and
compares it to existing systems. Section VII expands brieﬂy
gives details on implementations of the system underway
currently in our laboratory in human motion tracking while
Section VI summarizes conclusions and contributions of this
work. Throughout the paper, a notation system of leading
superscripts and subscripts adopted from Craig [27] is used
to denote the relative frames of orientations and vectors. A
leading subscript denotes the frame being described and a
leading superscript denotes the frame this is with reference
to. For example, For example, A
B ˆq describes the orientation of
frame B relative to frame A and A ˆv is a vector described in
frame A.

III. ALGORITHM DERIVATION

A. Orientation from angular rate

A tri-axis gyroscope will measure the angular rate about
the x, y and z axes of the senor frame, termed ωx, ωy and

1) are arranged
ωz respectively. If these parameters (in rads−
into the vector Sω deﬁned by equation (1), the quaternion
derivative describing rate of change of the earth frame relative
to the sensor frame S
E ˙q can be calculated [28] as equation (2).
The
operate denotes a quaternion product and the ˆ accent
denotes a normalised vector of unit length.

⊗

time t, E

The orientation of the earth frame relative to the sensor
S qω,t, can be computed by numerically
frame at
integrating the quaternion derivative S
E ˙qω,t as described by
equations (3) and (4), provided that
initial conditions are
known. In these equations, Sωt is the angular rate measured
at time t, ∆t is the sampling period and S
1 is the
previous estimate of orientation. The subscript ω indicates that
the quaternion is calculated from angular rates.

E ˆqest,t

−

S
E ˙qω,t =

1
2

S
E ˆqest,t

−

1 ⊗

Sωt

Eqω,t = S
S

E ˆqest,t

−

1 + S

E ˙qω,t∆t

(3)

(4)

B. Orientation from a homogenous ﬁeld

In the context of an orientation estimation algorithm, it will
initially be assumed that an accelerometer will measure only
gravity and a magnetometer will measure only the earth’s
magnetic ﬁeld. If the direction of an earth’s ﬁeld is known
in the earth frame, a measurement of the ﬁeld’s direction
within the sensor frame will allow an orientation of the
sensor frame relative to the earth frame to be calculated.
However, for any given measurement there will not be a unique
sensor orientation solution, instead there will inﬁnite solutions
represented by all those orientations achieved by the rotation
the true orientation around an axis parallel with the ﬁeld.
A quaternion representation requires a single solution to be
found. This may be achieved through the formulation of an
optimisation problem where an orientation of the sensor, S
E ˆq,
is found as that which aligns a predeﬁned reference direction
of the ﬁeld in the earth frame, E ˆd, with the measured ﬁeld
in the sensor frame, S ˆs; thus solving (5) where equation (6)
deﬁnes the objective function.

f (S

E ˆq, E ˆd, S ˆs)

min
S
4
E ˆq
∈(cid:60)

f (S

E ˆq, E ˆd, S ˆs) = S

E ˆq∗

E ˆd

S
E ˆq

−

⊗

S ˆs

⊗

(5)

(6)

Many optimisation algorithms exist but the gradient descent
algorithm is one of the simplest
to both implement and
compute. Equation (7) describes the gradient descent algorithm
for n iterations resulting in an orientation estimation of S
E ˆqn+1
based on an ‘initial guess’ orientation S
E ˆq0 and a variable
step-size µ. Equation (8) computes an error direction on the
solution surface deﬁned by the objective function, f , and its
Jacobian, J .

Eqk+1 = S
S

E ˆqk −

µ ∇

∇

f (S

f (S

E ˆqk, E ˆd, S ˆs)
E ˆqk, E ˆd, S ˆs)
(cid:13)
(cid:13)
(cid:13)
E ˆqk, E ˆd)f (S

(cid:13)
(cid:13)
(cid:13)
E ˆqk, E ˆd, S ˆs) = J T (S

f (S

∇

, k = 0, 1, 2...n (7)

E ˆqk, E ˆd, S ˆs)

(8)

Sω =

0 ωx ωy ωz

(cid:2)
S
E ˙q =

1
2

S
E ˆq

⊗

Sω

(cid:3)

(1)

(2)

Equations (7) and (8) describe the general form of the
algorithm applicable to a ﬁeld predeﬁned in any direction.
However, if the reference direction of the ﬁeld is deﬁned to
only have components within 1 or 2 of the principle axis of

180the earth coordinate frame then the equations simplify. An
appropriate convention would be to assume that the direction
of gravity deﬁnes the vertical, z axis as shown in equation (10).
Substituting E ˆg and normalised accelerometer measurement
S ˆa for E ˆd and S ˆs respectively, yields the simpliﬁed objective
function and Jacobian deﬁned by equations (12) and (13).

S
E ˆq =

q1

q2

q3

q4

(cid:2)
E ˆg =

0 0 0 1

(cid:3)

(cid:2)
0 ax ay

(cid:3)
az

S ˆa =

(cid:2)

fg(S

E ˆq, S ˆa) =

(cid:3)
2(q2q4 −
q1q3)
2(q1q2 + q3q4)
2( 1
q2
q2
3)
2 −
2 −
2q4 −
2q1
4q2 −

2q1
2q4
4q3

ax
ay
az



−
−
−


2q2
2q3
0 





2q3
−
2q2
0



Jg(S

E ˆq) =



−
The earth’s magnetic ﬁeld can be considered to have com-
ponents in one horizontal axis and the vertical axis; the vertical
component due to the inclination of the ﬁeld which is between
65◦ and 70◦ to the horizontal in the UK [29]. This can be
represented by equation (14). Substituting Eˆb and normalised
magnetometer measurement S ˆm for E ˆd and S ˆs respectively,
yields the simpliﬁed objective function and Jacobian deﬁned
by equations (16) and (17).

Eˆb =

0 bx

0 bz

S ˆm =

(cid:2)
0 mx my mz

(cid:3)

(cid:2)

(cid:3)

(14)

(15)

fb(S

E ˆq, Eˆb, S ˆm) =



−

q2
q2
2bx(0.5
4)+
3 −
q1q4)+
2bx(q2q3 −
2bx(q1q3 + q2q4)+

q1q3)
2bz(q2q4 −
2bz(q1q2 + q3q4)
q2
q2
3)
2bz(0.5
2 −

mx
my
mz

−
−
−

−





Jb(S

E ˆq, Eˆb) =

−

2bzq3
2bxq4 + 2bzq2
2bxq3



−


4bxq3 −
2bzq1 −
−
2bxq2 + 2bzq4 −
4bzq3
2bxq1 −

2bzq4
2bxq3 + 2bzq1
4bzq2
2bxq4 −
4bxq4 + 2bzq2
2bxq1 + 2bzq3
2bxq2



(17)



As has already been discussed, the measurement of gravity
or the earth’s magnetic ﬁeld alone will not provide a unique
orientation of the sensor. To do so, the measurements and refer-
ence directions of both ﬁelds may be combined as described by
equations (18) and (19). Whereas the solution surface created
by the objective functions in equations (12) and (16) have a
global minimum deﬁned by a line, the solution surface deﬁne

(9)

(10)

(11)

(12)

(13)

by equation (18) has a minimum deﬁne by a single point,
provided that bx (cid:54)

= 0.

(18)

fg(S
E ˆq, S ˆa)
E ˆq, Eˆb, S ˆm)
(cid:21)

fg,b(S

E ˆq, S ˆa, Eˆb, S ˆm) =

(19)

Jg,b(S

E ˆq, Eˆb) =

fb(S
(cid:20)
g (S
J T
E ˆq)
E ˆq, Eˆb)
b (S
J T
(cid:20)
(cid:21)
A conventional approach to optimisation would require
multiple iterations of equation (7) to be computed for each new
orientation and corresponding senor measurements. However,
it is acceptable to compute one iteration per time sample
provided that the convergence rate of the estimated orientation
governed by µt is equal or greater than the rate of change
of physical orientation. Equation (20) calculates the estimated
orientation S
,t computed at time t based on a previous
Eq
estimate of orientation S
1 and the objective function
f deﬁned by sensor measurements S ˆat and S ˆmt
error
f is chosen according to
sampled at time t. The form of
the sensors in use, as shown in equation (21). The subscript
indicates that the quaternion is calculated using the gradient

E ˆqest,t
−

∇

∇

∇

∇
descent algorithm.

S
Eq

∇

,t = S

E ˆqest,t

−

1 −

f
f

µt ∇
(cid:107)∇

(cid:107)

(20)

f =

∇

g,b(S
J T

(cid:26)

g (S
J T
E ˆqest,t

1)fg(S

E ˆqest,t
−
1, Eˆb)fg,b(S

E ˆqest,t

E ˆqest,t

1, S ˆat)

−
1, S ˆat, Eˆb, S ˆmt)

−

−

Eq

An appropriate value of µt

(21)
is that which ensures the
convergence rate of S
,t is limited to the physical orientation
rate as this avoids overshooting due an unnecessarily large step
size. Therefore µt can be calculated as equation (22) where
∆t is the sampling period, S
E ˙qω,t is the rate of change of
orientation measured by gyroscopes and α is an augmentation
of µ to account for noise in accelerometer and magnetometer
measurements.

∇

µt = α

S
E ˙qω,t

∆t, α > 1

(22)

(16)

C. Algorithm fusion process

(cid:13)
(cid:13)

(cid:13)
(cid:13)

∇

Eq

In practice, S

Eqω,t may start from incorrect initial conditions
and acclimate errors due to gyroscope measurement noise
and S
,t will provide an incorrect estimate when the ac-
celerometer is not stationary or the magnetometer exposed to
interferences. The goal of the fusion algorithm is to provide
an orientation estimate where S
Eqω,t is used to ﬁlter out high
frequency errors in S
,t is used both to com-
pensate for integral drift in S
Eqω,t and to provide convergence
from initial conditions.

,t, and S

Eq

Eq

∇

∇

An estimated orientation of the earth frame relative to the
Eqest,t, is obtained through the fusion of the two
Eqω,t and S
,t as described
γt) are weights applied

sensor frame, S
separate orientation calculations, S
by equation (23) where γt and (1
to each orientation calculation.

Eq

−

∇

S
Eqest,t = γt

S
Eq

,t + (1

∇

−

γt)S

Eqω,t, 0

γt ≤

1

≤

(23)

181An optimal value of γt is therefore that which ensures the
weighted rate of divergence of S
Eqω due to integral drift is
equal to the weighted rate of convergence of S
. This is
∇
represented by equation (24) where µt
is the convergence
∆t
rate of S
Eqω expressed as
the magnitude of a quaternion derivative corresponding to the
gyroscope measurement error. Equation (24) can be rearranged
to deﬁne γt as equation (25).

and β is the divergence rate of S

Eq

Eq

∇

(1

−

γt)β = γt

µt
∆t

γt =

β
µt
∆t + β

Accelerometer S ˆat

J T

g (S

E ˆqest,t

1)f g(S

E ˆqest,t

1, S ˆat)

−

−

f
f

∇
k∇

k

β

Gyroscope Sωt

1
2

S
E ˆqest,t

Sωt

1 ⊗

−

.dt

Z
S
E ˙qest,t

q
q

k

k

1

z−

1

z−

S
E ˆqest,t

(24)

(25)

Fig. 1. Block diagram representation of the complete orientation estimation
algorithm for an IMU implementation

∇

The fusion process ensures the optimal fusion of S
,t assuming that the convergence rate of S

Eqω,t and
S
governed
Eq
by α is equal or greater than the physical rate of change of
orientation. Therefore α has no upper bound. If α is assumed
to be very large then µt, deﬁned by equation (22), also
becomes very large and the equations simplify. A large value
of µt used in equation (20) means that S
1 becomes
negligible and the equation can be re-written as equation (26).

E ˆqest,t

Eq

∇

−

S
Eq

∇

,t ≈ −

µt ∇
(cid:107)∇

f
f

(cid:107)

(26)

The deﬁnition of γt in equation (25) also simpliﬁes if the β
term in the denominator becomes negligible and the equation
can be rewritten as equation (27). It is possible from equation
0.
(27) to also assume that γt ≈

γt ≈

β∆t
µt

(27)

Substituting equations (4), (26) and (27) into equation (23)
directly yields equation (28). It is important to note that in
equation (28), γt has been substituted as both as equation (26)
and 0.

f
f

β∆t
µt (cid:18)

−

0)

S
Eqest,t =

+(1

µt ∇
(cid:107)∇

E ˙qω,t∆t
(28)
Equation (28) can be simpliﬁed to equation (29) where
S
E ˙qest,t is the estimated orientation rate deﬁned by equation
(30).

(cid:107) (cid:19)

1 + S
−

S
E ˆqest,t

−

(cid:16)

(cid:17)

(29)

(30)

Eqest,t = S
S

E ˆqest,t

1 + S
−

E ˙qest,t∆t

f
f

(cid:107)

E ˙qest,t = S
S

β ∇
(cid:107)∇

E ˙qω,t −
It can be seen from equations (29) and (30) that

the
algorithm calculates the orientation S
Eqest by numerically inte-
grating the estimated rate of change of orientation S
E ˙qest. The
algorithm computes S
E ˙qest as the rate of change of orientation
measured by the gyroscopes, S
E ˙qω, with the magnitude of
the gyroscope measurement error, β, removed in a direction
based on accelerometer and magnetometer measurements.
Fig.1 shows a block diagram representation of the complete
orientation estimation algorithm implementation for an IMU.

D. Magnetic distortion compensation

Investigations into the effect of magnetic distortions on an
orientation sensor’s performance have shown that substantial
errors may be introduced by sources including electrical appli-
ances, metal furniture and metal structures within a buildings
construction [30], [31]. Sources of interference ﬁxed in the
sensor frame, termed hard iron biases, can be removed through
calibration [32], [33], [34], [35]. Sources of interference in the
earth frame, termed soft iron errors, may only be removed
if an additional reference of orientation is available. An
accelerometer provides a reference of attitude and so may
be used to compensate for inclination errors in the measured
earth’s magnetic ﬁeld.

The measured direction of the earth’s magnetic ﬁeld in the
earth frame at time t, E ˆht, can be computed as equation
(31). The effect of an erroneous inclination of the measured
direction earth’s magnetic ﬁeld, E ˆht, can be corrected if the
algorithm’s reference direction of the earth’s magnetic ﬁeld,
Eˆbt, is of the same inclination. This is achieved by computing
Eˆbt as E ˆht normalised to have only components in the earth
frame x and z axes; as described by equation (32).

E ˆht =

0 hx hy hz

(cid:2)

(cid:3)

= S

E ˆqest,t

−

S ˆmt ⊗

1 ⊗

S
E ˆq∗est,t

1
−
(31)

Eˆbt =

0

x + h2
h2
y

0 hz

(32)

(cid:104)

(cid:113)

(cid:105)

Compensating for magnetic distortions in this way ensures
the
that magnetic disturbances are limited to only affect
estimated heading component of orientation. The approach
also eliminates the need for the reference direction of the
earth’s magnetic ﬁeld to be predeﬁned; a potential disad-
vantage of other orientation estimation algorithm [12], [19].
Fig.2 shows a block diagram representation of the complete
algorithm implementation for a MARG sensor array, including
the magnetic distortion compensation.

E. Algorithm adjustable parameter

The orientation estimation algorithm requires 1 adjustable
parameter, β, representing the gyroscope measurement error
expressed as the magnitude of a quaternion derivative. It
is convenient to deﬁne β using the angular quantity ˜ωmax

182S
E ˆqest,t

1 ⊗

−

S
E ˆq∗est,t

1

−

S ˆmt ⊗
E ˆht

0

x + h2
h2
y

0 hz

h

q

E ˆbt

i

Magnetometer S ˆmt
Accelerometer S ˆat

J T

g,b(S

E ˆqest,t

1, E ˆbt)f g,b(S

E ˆqest,t

1, S ˆa, E ˆbt, S ˆm)

−

−

f
f

∇
k∇

k

β

Gyroscope Sωt

1
2

S
E ˆqest,t

Sωt

1 ⊗

−

.dt

q
q

k

k

Z

S
E ˙qest,t

)
s
e
e
r
g
e
d
(

100

50

0

−50

−100

)
s
e
e
r
g
e
d
(

5

0

−5

1

z−

1

z−

S
E ˆqest,t

Measured and estimated angle q

Measured
Kalman−based algorithm
Proposed filter (MARG)

42

44

46

48

50

52

54

56

58

60

62

Error

Kalman−based algorithm
Proposed filter (MARG)

42

44

46

48

50
time (seconds)

52

54

56

58

60

62

Fig. 2. Block diagram representation of the complete orientation estima-
tion algorithm for an MARG implementation including magnetic distortion
compensation

representing the maximum gyroscope measurement error of
each axis. Using the relationship described by equation (2),
β may be deﬁned by equation (33) where ˆq is any unit
quaternion.

β =

1
2

ˆq

⊗

(cid:13)
(cid:13)
(cid:13)
(cid:13)

0

˜ωmax

˜ωmax

˜ωmax

=

(cid:2)
IV. EXPERIMENTAL EQUIPMENT

(cid:13)
(cid:13)
(cid:3)
(cid:13)
(cid:13)

3
4

˜ωmax (33)

(cid:114)

The algorithm was tested using the xsens MTx orientation
sensor [13] containing 16 bit resolution tri-axis gyroscopes,
accelerometers and magnetometers. Raw sensor data was
logged to a PC at 512 Hz and imported accompanying software
to provide calibrated sensor measurements which were then
processed by the proposed orientation estimation algorithm.
The software also incorporates a propriety Kalman-based
orientation estimation algorithm. As both the Kalman-based
algorithm and proposed algorithm’s estimates of orientation
were computed using identical sensor data, the performance
of each algorithm could be evaluated relative to one-another,
independent of sensor performance.

A Vicon system, consisting of 8 MX3+ cameras connected
to an MXultranet server [36] and Nexus [37] software, was
used to provide reference measurements of the orientation
sensor’s actual orientation. To do so, the sensor was ﬁxed to
an orientation measurement platform. The positions of optical
markers attached to the platform were logged at 120 Hz and
then post-processed to compute the orientation of the measure-
ment platform and sensor. In order for the measurements of an
orientation in the camera coordinate frame to be comparable
to the algorithm estimate of orientation in the earth frame, an
initial calibration procedure was required where the direction
of the earth’s magnetic and gravitational ﬁelds in the camera
coordinate frame were measured using a magnetic compass
and pendulum with attached optical markers.

V. EXPERIMENTAL RESULTS

It is common [19], [21], [13], [14], [15], [16] to quantify
orientation sensor performance as the static and dynamic RMS

Fig. 3. Typical results for measured and estimated angle θ (top) and error
(bottom)

TABLE I
STATIC AND DYNAMIC RMS ERROR OF KALMAN-BASED ALGORITHM
AND PROPOSED ALGORITHM IMU AND MARG IMPLEMENTATIONS

Euler parameter

RMS[φ(cid:15)] static
RMS[φ(cid:15)] dynamic
RMS[θ(cid:15)] static
RMS[θ(cid:15)] dynamic
RMS[ψ(cid:15)] static
RMS[ψ(cid:15)] dynamic

Kalman-based
algorithm
0.789◦
0.769◦
0.819◦
0.847◦
1.150◦
1.344◦

IMU

MARG
algorithm algorithm
0.594◦
0.581◦
0.623◦
0.625◦
0.497◦
0.502◦
0.668◦
0.668◦
1.073◦
N/A
1.110◦
N/A

(Root-Mean-Square) errors in the decoupled Euler parameters
describing the pitch, φ, roll, θ and heading, ψ components of
an orientation, corresponding to rotations around the sensor
frame x, y, and z axis respectively. A total of 4 sets of Euler
parameters were computed, corresponding to the calibrated op-
tical measurements of orientation, the Kalman-based algorithm
estimated orientation and the proposed algorithm estimates
orientation for both the MARG and IMU implementations.
The errors of estimated Euler parameters, φ(cid:15), θ(cid:15) and ψ(cid:15), were
computed as the difference between estimated values and the
calibrated optical measurements. Results were obtained for a
sequence of rotations around each axis preformed by hand.
The experiment was repeated 8 times to compile a dataset rep-
resentative of system performance. The proposed algorithm’s
adjustable parameter, β, was set to 0.033 for the MARG
implementation and 0.041 for the IMU implementation. Trials
summarised in Fig.4, found these values to provide optimal
performance. Fig.3 shows the Kalman-based algorithm and
proposed algorithm MARG implementation results, typical of
the 8 experiments.

The static and dynamic RMS values of φ(cid:15), θ(cid:15), and ψ(cid:15)
were calculated assuming a static state when the measured
corresponding angular rate was < 5◦/s, and a dynamic when
5◦/s. This threshold was chosen to be sufﬁciently greater
≥
than the noise ﬂoor of the data. The results are summarised
in Table I where each value, represents the mean of all 8
experiments.

The results of an investigation into the effect of the ad-
justable parameter β on algorithm performance are sum-
marised in Fig.4. The experimental data was processed though
the separate proposed algorithm IMU and MARG implanta-

183q

q
e

)
s
e
e
r
g
e
d
(

]

]

[q

S
M
R

,
]

[f

S
M
R

[

n
a
e
m

2

1.5

1

0.5

0

b  vs. filter performance (IMU)

Static performance
Dynamic performance

  b  = 0.033

0.2

0.4

)
s
e
e
r
g
e
d
(

]

]

[y

S
M
R

,
]

[q

S
M
R

,
]

[f

S
M
R

[

n
a
e
m

2

1.5

1

0.5

0

b  vs. filter performance (MARG)

Static performance
Dynamic performance

  b  = 0.041

0.2

0

3

2.8

2.6

2.4

2.2

foot x−axis
foot y−axis
foot z−axis

Recovered foot position (meters)

2

1.8

1.6

1.4

1.2

1

0.8

0.6

0.4

0.2

0

−0.2

0
0.2

0.2

0.4

Fig. 6. Recovered foot position plotted at 20 samples per second

Fig. 4. The effect of the adjustable parameter, β, on the performance of the
proposed algorithm IMU (left) and MARG (right) implementations

30

25

20

15

10

5

)
s
e
e
r
g
e
d
(

]

]

[q

S
M
R

,
]

[f

S
M
R

[
n
a
e
m

0
0
10

Sampling rate vs. filter performance (IMU)

Static performance
Dynamic performance

1
10

2
10

Sampling rate (Hz)

)
s
e
e
r
g
e
d
(

]

]

[y

S
M
R

,
]

[q

S
M
R

,
]

[f

S
M
R

[
n
a
e
m

Sampling rate vs. filter performance (MARG)

30

25

20

15

10

5

0
0
10

Static performance
Dynamic performance

1
10

2
10

Sampling rate (Hz)

Fig. 5.
algorithm IMU (left) and MARG (right) implementations

The effect of sampling rate on the performance of the proposed

tions, using ﬁxed values of β between 0 to 0.5. There is a
clear optimal value of β high enough to minimises errors due
to integral drift but sufﬁciently low enough that unnecessary
noise is not introduced by large steps of gradient descent
iterations.

The results of an investigation into the effect of sampling
rate on algorithm performance is summarised in Fig.5. The
experimental data was processed though the separate proposed
algorithm IMU and MARG implantations, using the previously
deﬁned, optimal values β. Experimental data was decimated
to simulate sampling rates between 1Hz and 512 Hz. It can be
seen from Fig.5 that the proposed algorithm achieves similar
levels of performance at 50 Hz as at 512 Hz. Both algorithm
implementations are able to achieve a static error < 2◦ and
dynamic error < 7◦ while sampling at 10 Hz. This level of
accuracy may be sufﬁcient for human motion applications
the bandwidth of the
though the sampling rate will
motion that may be measured.

limit

VI. CONCLUSIONS

Orientation estimation algorithms for inertial/magnetic sen-
sors is a is a mature ﬁeld of research. Modern techniques
[25], [26], [38] have focused on simpler algorithms that ame-
liorate the computational load and parameter tuning burdens
associated with conventional Kalman-based approaches. The
algorithm presented in this paper employs processes similar
to others but through a novel derivation, is able to offer some
key advantages:

•

Computing an error based on an analytically derived Jaco-
bian results in a signiﬁcant reduction in the computation

load relative to a Gauss-Newton method [25]; quantiﬁed
as 109 and 248 scalar arithmetic operations per update
for C code implementations of the IMU and MARG
implementations respectively.
Normalisation of the feedback error permits optimal gains
to be deﬁned based on observable system characteristics.
Magnetic distortion compensation algorithm eliminates
the need for a direction of magnetic ﬁeld to be predeﬁned
by the designer.

•

•

The elimination of a predeﬁned direction of magnetic ﬁeld
is an advantage over all other algorithms cited by this paper;
though this component may be easily incorporated to other
algorithms. Experimental studies have been presented for an
off-the-shelf, leading commercial unit with reference mea-
surements obtained via precision optical measurement system.
These studies enabled the algorithm to be benchmarked and
have indicated that the algorithm performs as well as the
proprietary Kalman-based system; even with a full order of
magnitude in reduction of sampling rate.

VII. FUTURE WORK

Research is presently underway to incorporate the orienta-
tion estimation algorithm into a self-contained human motion
tracking system for rehabilitative applications. As stated ear-
lier, Zhoua [7] cited real time operation, wireless properties,
correctness of data, and portability as major challenges to be
addressed. The reduction in computational load and relative
ease in tuning provided by the algorithm introduced in this
work addresses all of these issues; its efﬁciency allows im-
plementation on low power, low performance, hardware for
signiﬁcant reduction in size, while its sampling rates permits
longer periods of data storage and simpler implementation for
wireless data transfer.

The algorithm is currently being implemented as the core
of a self-contained system with a MARG suite, data storage
unit, and power supply that will be small enough to ﬁt within
the sole of a sports shoe for lower extremity motion tracking.
Fig.6 shows data obtained using a prototype unit for tracking
of the right foot of a test subject as they walked in a straight
line. Translational position data was recovered using methods
similar to [39], [40], [41], [42], [43]. The measured distance of
the 3 steps was 3.0 m, while the recovered displacement was
3.00 m. A complete system is currently under development to
allow long-term (1 week +) motion tracking in unstructured
environments.

184b

e

e

b

e

e

e

e

e

e

e

e

[25] E. R. Bachmann, R. B. McGhee, X. Yun, and M. J. Zyda, “Inertial and
magnetic posture tracking for inserting humans into networked virtual
environments,” pp. 9–16, 2001.

[26] R. Mahony, T. Hamel, and J.-M. Pﬂimlin, “Nonlinear complementary
ﬁlters on the special orthogonal group,” Automatic Control, IEEE
Transactions on, vol. 53, pp. 1203 –1218, june 2008.

[27] J. J. Craig, Introduction to Robotics Mechanics and Control. Pearson

Education International, 2005.

[28] D. R. P. R. B. M. Joseph M. Cooke, Michael J. Zyda, “Npsnet: Flight
simulation dynamic modelling using quaternions,” Presence, vol. 1,
pp. 404–420, 1994.

[29] J. A. Jacobs, The earth’s core, vol. 37 of International geophysics series.

Academic Press, 2 ed., 1987.

[30] E. R. Bachmann, X. Yun, and C. W. Peterson, “An investigation of the
effects of magnetic variations on inertial/magnetic orientation sensors,”
in Proc. IEEE International Conference on Robotics and Automation
ICRA ’04, vol. 2, pp. 1115–1122, Apr. 2004.

[31] C. B. F. v. d. H. W.H.K. de Vries, H.E.J. Veeger, “Magnetic distortion in
motion labs, implications for validating inertial magnetic sensors,” Gait
& Posture, vol. 29, no. 4, pp. 535–541, 2009.

[32] Speake & Co Limited, “Autocalibration algorithms for FGM type

sensors.” Application note.

[33] M. J. Caruso, Applications of Magnetoresistive Sensors in Navigation
Systems. Honeywell Inc., Solid State Electronics Center, Honeywell Inc.
12001 State Highway 55, Plymouth, MN 55441.

[34] J. F. Vasconcelos, G. Elkaim, C. Silvestre, P. Oliveira, and B. Cardeira,
“A geometric approach to strapdown magnetometer calibration in sensor
frame,” in Navigation, Guidance and Control of Underwater Vehicles,
vol. 2, 2008.

[35] D. Gebre-Egziabher, G. H. Elkaim, J. D. Powell, and B. W. Parkinson,
“Calibration of strapdown magnetometers in magnetic ﬁeld domain,”
Journal of Aerospace Engineering, vol. 19, no. 2, pp. 87–102, 2006.

[36] Vicon Motion Systems Limited., Vicon MX Hardware. 5419 McConnell

Avenue, Los Angeles, CA 90066, USA, 1.6 ed., 2004.

[37] Vicon Motion Systems Limited., Vicon Nexus Product Guide - Founda-
tion Notes. 5419 McConnell Avenue, Los Angeles, CA 90066, USA,
1.2 ed., November 2007.

[38] P. Martin and E. Salan, “Design and implementation of a low-cost
observer-based attitude and heading reference system,” Control Engi-
neering Practice, vol. 18, no. 7, pp. 712 – 722, 2010. Special Issue on
Aerial Robotics.

[39] X. Yun, E. R. Bachmann, H. Moore, and J. Calusdian, “Self-contained
position tracking of human movement using small inertial/magnetic
sensor modules,” in ICRA, pp. 2526–2533, 2007.

[40] E. Foxlin, “Pedestrian tracking with shoe-mounted inertial sensors,”

IEEE Comput. Graph. Appl., vol. 25, no. 6, pp. 38–46, 2005.

[41] H. M. Schepers, H. Koopman, and P. H. Veltink, “Ambulatory assess-
ment of ankle and foot dynamics,” IEEE Transactions on Biomedical
Engineering, vol. 54, no. 5, pp. 895–902, 2007.

[42] R. Stirling, K. Fyfe, and G. Lachapelle, “Evaluation of a new method of
heading estimation for pedestrian dead reckoning using shoe mounted
sensors,” The Journal of Navigation, vol. 58, no. 01, pp. 31–45, 2005.
[43] F. Cavallo, A. Sabatini, and V. Genovese, “A step toward gps/ins personal
navigation systems: real-time assessment of gait by foot inertial sensing,”
pp. 1187 – 1191, aug. 2005.

REFERENCES

[1] S. K. Hong, “Fuzzy logic based closed-loop strapdown attitude system
for unmanned aerial vehicle (uav),” Sensors and Actuators A: Physical,
vol. 107, no. 2, pp. 109 – 118, 2003.

[2] B. Barshan and H. F. Durrant-Whyte, “Inertial navigation systems for

mobile robots,” vol. 11, pp. 328–342, June 1995.

[3] L. Ojeda and J. Borenstein, “Flexnav: fuzzy logic expert rule-based
position estimation for mobile robots on rugged terrain,” in Proc. IEEE
International Conference on Robotics and Automation ICRA ’02, vol. 1,
pp. 317–322, May 11–15, 2002.

[4] D. H. Titterton and J. L. Weston, Strapdown inertial navigation tech-

nology. The Institution of Electrical Engineers, 2004.

[5] S. Beauregard, “Omnidirectional pedestrian navigation for ﬁrst respon-
ders,” in Proc. 4th Workshop on Positioning, Navigation and Communi-
cation WPNC ’07, pp. 33–36, Mar. 22–22, 2007.

[6] H. J. Luinge and P. H. Veltink, “Inclination measurement of human
movement using a 3-d accelerometer with autocalibration,” vol. 12,
pp. 112–121, Mar. 2004.

[7] H. Zhou and H. Hu, “Human motion tracking for rehabilitation–a
survey,” Biomedical Signal Processing and Control, vol. 3, no. 1, pp. 1
– 18, 2008.

[8] E. A. Heinz, K. S. Kunze, M. Gruber, D. Bannach, and P. Lukowicz,
“Using wearable sensors for real-time recognition tasks in games of
martial arts - an initial experiment,” in Proc. IEEE Symposium on
Computational Intelligence and Games, pp. 98–102, May 22–24, 2006.
[9] R. E. Kalman, “A new approach to linear ﬁltering and prediction
problems,” Journal of Basic Engineering, vol. 82, pp. 35–45, 1960.
[10] E. Foxlin, “Inertial head-tracker sensor fusion by a complementary
separate-bias kalman ﬁlter,” in Proc. Virtual Reality Annual International
Symposium the IEEE 1996, pp. 185–194,267, Mar. 30–Apr. 3, 1996.

[11] H. J. Luinge, P. H. Veltink, and C. T. M. Baten, “Estimation of
orientation with gyroscopes and accelerometers,” in Proc. First Joint
[Engineering in Medicine and Biology 21st Annual Conf. and the 1999
Annual Fall Meeting of the Biomedical Engineering Soc.] BMES/EMBS
Conference, vol. 2, p. 844, Oct. 13–16, 1999.

[12] J. L. Marins, X. Yun, E. R. Bachmann, R. B. McGhee, and M. J. Zyda,
“An extended kalman ﬁlter for quaternion-based orientation estimation
using marg sensors,” in Proc. IEEE/RSJ International Conference on
Intelligent Robots and Systems, vol. 4, pp. 2003–2011, Oct. 29–Nov. 3,
2001.

[13] Xsens Technologies B.V., MTi and MTx User Manual and Technical
Documentation. Pantheon 6a, 7521 PR Enschede, The Netherlands, May
2009.

[14] MicroStrain Inc., 3DM-GX3 -25 Miniature Attutude Heading Reference
Sensor. 459 Hurricane Lane, Suite 102, Williston, VT 05495 USA,
1.04 ed., 2009.

[15] VectorNav Technologies, LLC, VN -100 User Manual. College Station,

TX 77840 USA, preliminary ed., 2009.

[16] InterSense, Inc., InertiaCube2+ Manual. 36 Crosby Drive, Suite 150,

Bedford, MA 01730, USA, 1.0 ed., 2008.

[17] PNI sensor corporation, Spacepoint Fusion. 133 Aviation Blvd, Suite

101, Santa Rosa, CA 95403-1084 USA.

[18] Crossbow Technology, Inc., AHRS400 Series Users Manual. 4145 N.

First Street, San Jose, CA 95134, rev. c ed., February 2007.

[19] A. M. Sabatini, “Quaternion-based extended kalman ﬁlter for determin-
ing orientation by inertial and magnetic sensing,” vol. 53, pp. 1346–
1356, July 2006.

[20] H. J. Luinge and P. H. Veltink, “Measuring orientation of human body
segments using miniature gyroscopes and accelerometers,” Medical and
Biological Engineering and Computing, vol. 43, pp. 273–282, April
2006.

[21] D. Jurman, M. Jankovec, R. Kamnik, and M. Topic, “Calibration and
data fusion solution for the miniature attitude and heading reference
system,” Sensors and Actuators A: Physical, vol. 138, pp. 411–420,
August 2007.

[22] M. Haid and J. Breitenbach, “Low cost inertial orientation tracking
with kalman ﬁlter,” Applied Mathematics and Computation, vol. 153,
pp. 567–575, June 2004.

[23] D. Roetenberg, H. J. Luinge, C. T. M. Baten, and P. H. Veltink,
“Compensation of magnetic disturbances improves inertial and magnetic
sensing of human body segment orientation,” vol. 13, pp. 395–405, Sept.
2005.

[24] R. A. Hyde, L. P. Ketteringham, S. A. Neild, and R. J. S. Jones, “Esti-
mation of upper-limb orientation based on accelerometer and gyroscope
measurements,” vol. 55, pp. 746–754, Feb. 2008.

185
