Sensors 2015, 15, 19302-19330; doi:10.3390/s150819302

OPEN ACCESS

sensors

ISSN 1424-8220
<www.mdpi.com/journal/sensors>

Article

Keeping a Good Attitude: A Quaternion-Based Orientation
Filter for IMUs and MARGs

Roberto G. Valenti 1, Ivan Dryanovski 2 and Jizhong Xiao 1,*

1 The City College of New York, The City University of New York, Convent Avenue and 140th Street,

New York, NY 10031, USA; E-Mail: <robertogl.valenti@gmail.com>

2 The Graduate Center, The City University of New York, 365 Fifth Avenue, New York, NY 10016,

USA; E-Mail: <ivan.dryanovski@gmail.com>

* Author to whom correspondence should be addressed; E-Mail: <jxiao@ccny.cuny.edu>;

Tel.: +1-212-650-7268; Fax: +1-212-650-8249.

Academic Editor: Gert F. Trommer

Received: 24 June 2015 / Accepted: 27 July 2015 / Published: 6 August 2015

Orientation estimation using low cost sensors is an important

task for
Abstract:
Micro Aerial Vehicles (MAVs) in order to obtain a good feedback for the attitude controller.
The challenges come from the low accuracy and noisy data of the MicroElectroMechanical
System (MEMS) technology, which is the basis of modern, miniaturized inertial sensors.
In this article, we describe a novel approach to obtain an estimation of the orientation
in quaternion form from the observations of gravity and magnetic ﬁeld. Our approach
provides a quaternion estimation as the algebraic solution of a system from inertial/magnetic
observations. We separate the problems of ﬁnding the “tilt” quaternion and the heading
quaternion in two sub-parts of our system. This procedure is the key for avoiding the
impact of the magnetic disturbances on the roll and pitch components of the orientation
when the sensor is surrounded by unwanted magnetic ﬂux. We demonstrate the validity of
our method ﬁrst analytically and then empirically using simulated data. We propose a novel
complementary ﬁlter for MAVs that fuses together gyroscope data with accelerometer and
magnetic ﬁeld readings. The correction part of the ﬁlter is based on the method described
above and works for both IMU (Inertial Measurement Unit) and MARG (Magnetic, Angular
Rate, and Gravity) sensors. We evaluate the effectiveness of the ﬁlter and show that it
signiﬁcantly outperforms other common methods, using publicly available datasets with
ground-truth data recorded during a real ﬂight experiment of a micro quadrotor helicopter.

Sensors 2015, 15

19303

Keywords: orientation estimation; inertial measurement unit; magnetic angular rate and
gravity; quaternions, micro aerial vehicles

1. Introduction

The accurate estimation of the orientation of a rigid body, relative to an inertial frame, is required
for a wide range of applications. For the purpose of navigation, such estimation has employed
high precision inertial and magnetic sensors, but the recent development of low-cost and light-weight
MicroElectroMechanical Systems (MEMS) has allowed smaller and cheaper inertial sensors to be
adopted for a wider range of applications and even in the daily use of consumer electronics such as
game consoles and mobile devices. In robotics, the evolution of Micro Aerial Vehicles (MAVs) has
increased in the last decade, and research is moving toward their full autonomization. Navigation and
control of MAVs are possible thanks to the MEMS-based Inertial Measurement Units (IMU) that meet
the MAVs’ limited size and payload requirement.

Data provided by low-cost IMU is affected by high noise levels and time-varying biases. Therefore,
a sensor-fusion algorithm must be used to process the data to obtain a smooth and bias-free estimation
of the orientation maintaining a low computational cost for running on the onboard processor. The
orientation can be generally represented in three principal forms: Euler angles, quaternion, and Direction
Cosine Matrix (DCM). The orientation in Euler form is expressed using three angles; it is conceptually
easy to understand, but may reach a singularity state commonly referred as “gimbal lock”. DCM and
quaternion do not incur a singularity state but the DCM represents the orientation by a 3
3 matrix.
Furthermore, the quaternion representation offers a linear formulation of the orientation dynamics.

×

In this article, we propose a deterministic approach to solve Whaba’s problem [1] given gravity and
magnetic ﬁeld observations provided by the MARG sensor. This method returns an estimation of the
attitude in quaternion form without leading to ambiguous results and avoiding singularity problems.
Moreover, it does not need a predeﬁned knowledge of the magnetic ﬁeld direction. We also propose
a new approach to a complementary ﬁlter for fusing together gyroscope data with acceleration and
magnetic ﬁeld measurements from IMU and MARG sensors to obtain an orientation estimation in
quaternion form. This algorithm is meant to be used onboard MAVs because of its low computational
burden, robustness, and fast convergence. However, we believe our contribution is applicable beyond the
ﬁeld of MAV and aerial robotics.

Further,

This article is organized as follows. Section 2 explores the literature of attitude estimation methods
previously proposed as solution to Whaba’s problem.
in the same section, we brieﬂy
survey several fusion algorithms that exploit the measurements given by gyroscope, accelerometer,
and magnetometer of an IMU/MARG sensor, to obtain a more accurate evaluation of the orientation.
Section 3 brieﬂy provides an overview of some properties of unit quaternions and how they can be used
to deﬁne rotations in the 3D space. Section 4 analyzes the novel approach taken to obtain the quaternion
orientation of a rigid body from earth-ﬁeld observations as a closed-form solution. Section 5 explains
the novel quaternion-based complementary ﬁlter. Section 6 is dedicated to the experiments and results
interpretations, and Section 7 concludes the article by summarizing the ﬁndings.

Sensors 2015, 15

2. Previous Work

19304

The problem of ﬁnding the optimal attitude estimation, given multiple unit vector correspondences
across two frames, was formulated by Whaba in 1965 [1]. Whaba’s problem was meant to estimate
the attitude of a satellite by ﬁnding the optimal orthogonal matrix (the attitude matrix) that minimizes a
least-square loss function using n numbers of unit vectors pairs where n
2. Many algorithmic solutions
of Whaba’s problem have been proposed. They are generally classiﬁed into two categories: deterministic
and optimal, according to the popular deﬁnition by Wertz [2]. Deterministic algorithms use a minimal set
of data and derive the attitude by solving nonlinear equations, whereas optimal algorithms use more than
a minimal set of measurements and compute the attitude by minimizing an appropriate cost function.

≥

A very well known deterministic algorithm is the three axis attitude determination (TRIAD) [3].
It constructs two triads of orthonormal unit vectors by combining the normalized measurement of two
nonparallel reference vectors and provides an estimation of the attitude matrix. QUaternion ESTimator
(QUEST) [3] is a famous optimal algorithm that produces the attitude estimation in quaternion form
given a set of 3D reference unit vectors in a ﬁxed frame and their corresponding observations in the
local frame. It is based on Davenport’s q-method [4] that ﬁnds the optimal quaternion by minimizing a
quadratic gain, which is a transformation of Whaba’s loss function through the parametrization of the
orientation matrix by the unit quaternion. Many other techniques have been proposed, such as Singular
Value decomposition (SVD) [5], Polar Decomposition (PD) [6], Euler-n [7], Fast Optimal Matrix
Algorithm (FOAM) [8], and Energy Approach Algorithm (EAA) [9]. All of them produce an optimal
attitude estimation and they differ from each other in their computational speed. A complete survey
and analysis of attitude estimation methods in quaternion form using vector observation is provided by
Markley and Mortari in [10].

It is well known that in applications based on inertial/magnetic sensors, to estimate the attitude,
the two local observations of the earth’s ﬁelds (gravity and local magnetic ﬁeld) are compared to the
reference vectors that are supposed to be ﬁxed. This assumption can lead to problems when the local
In these cases, when
magnetic ﬁeld is perturbed by ferromagnetic objects or electrical appliances.
algorithms such as QUEST are employed, the attitude estimation would be subject to errors not only
in the yaw component but also in the pitch and roll. To avoid this problem, Yun et al. [11] proposed the
Factored Quaternion Algorithm (FQA), which computes the orientation of a rigid body based on earth
gravity and magnetic ﬁeld measurements. The quaternion orientation is estimated by analyzing a series
of three sequential rotations. This approach allows to reduce the orientation error, caused by the presence
of local magnetic disturbances, only into the error in the yaw component maintaining the accuracy of the
QUEST algorithm. To obtain the quaternion orientation from gravity and magnetic ﬁeld observations,
the method presented in this article solves the problem described above by separating the quaternion
in only two parts, one for the roll and pitch components and one for the yaw. Both quaternions are
found as an algebraic solution of a system instead of the result of an optimization problem. As inertial
sensors provide at most the observation of 2 pairs of vectors (given a priori the global-frame gravity
and magnetic ﬁeld vectors), the use of optimal algorithms does not produce any improvement but only
reduces the convergence speed of the orientation.

Sensors 2015, 15

19305

In the class of deterministic methods, Euler-2 by Daniele Mortari [7] is a mathematical approach to
compute the Euler axis whose application is restricted when only two unit-vector pairs are available.
Overall, besides the TRIAD algorithm, deterministic attitude-determination algorithms are not very
frequent and their study is not extensive. Nonetheless, in IMU applications, only two sets of vector
observations are provided, thus even the optimal approaches would have the same level of accuracy as a
deterministic method.

To obtain a better estimation of the orientation, acceleration and magnetic ﬁeld data are fused together
with angular rate readings from a gyroscope. Although many approaches have been adopted for ﬁltering
gyroscope data with inertial measurements, the most commonly used techniques are Extended Kalman
ﬁltering (EKF) and complementary ﬁlters. A survey of other nonlinear attitude estimation methods can
be found in [12].

Kalman ﬁltering based techniques adopt a probabilistic determination of the state modeled as a
Gaussian distribution given the system’s model. They are widely used in aerospace applications [13,14],
human motion analysis [15–17] and robotics [18,19].

A Complementary ﬁlter is a common alternative to the EKF because of its simplicity and
effectiveness. It uses an analysis in the frequency domain to ﬁlter the signals and combine them together
to obtain an estimation of the orientation without any statistical description. In UAV applications, the
use of complementary ﬁlters [20–22] is often preferred to the EKF because EKFs can be complicated to
implement and the convergence is slower because of the time required for the linear regression iterations.
Most of the recent sensor fusion algorithms for inertial/magnetic sensors provide orientation
estimation in quaternion form. Quaternions are a useful mathematical tool that require less computation
time because of their minimal number of parameters and do not result in singularity conﬁgurations
as the Euler representation does. Further, rotations of vectors are simply performed by quaternion
multiplications.
Marins et al.

[23] propose two different Kalman ﬁlter approaches to estimate the orientation in
quaternion form from a MARG sensor. Both methods have the same 7-state (angular velocities and
quaternion) process model but different measurement models. The ﬁrst measurement model uses
each MARG output in a 9-element measurement vector resulting in a complicated EKF. The second
approach uses an external Gauss-Newton algorithm to directly estimate the quaternion measurement
that will be part, along with the angular velocities, of the measurement vector.
In this case, the
relation between the process and measurement model is linear allowing the use of a simpler Kalman
Filter. The quaternion-based EKF presented by Sabatini [16] is similar to the ﬁrst approach of
Marins et al. [23], but the state is composed by the unit quaternion augmented with accelerometer and
magnetometer bias vectors for on-line calibration. In [24] Sabatini presents a similar EKF where the
state is augmented with magnetic distortions vector, modeled as a Gauss-Markov process, to reduce the
heading drift in magnetically non-homogeneous environments. Choukroun et al. [14] present a novel
linear pseudo-measurement model that combined with the linear measurement model, yields a linear
Kalman Filter algorithm that eliminates the linearization procedure of an EKF. Bachman et al. [25]
present an efﬁcient quaternion-based complementary ﬁlter for human-body-motion tracking.

Euston et al.

[21] present a nonlinear quaternion-based complementary ﬁlter to estimate the
attitude of a UAV given measurement from a low-cost IMU. The ﬁlter is augmented by a ﬁrst-order

Sensors 2015, 15

19306

In the work by
model of the vehicle dynamics to compensate for external centripetal acceleration.
Madgwick et al.
[26], a constant gain ﬁlter is adopted to estimate the attitude in quaternion form
of a rigid body by using data from a MARG sensor. A ﬁrst quaternion estimation is obtained by
gyroscope output integration and then it is corrected by a quaternion from the accelerometer and
magnetometer data computed through a gradient descent algorithm. Madgwick’s method ensures good
attitude estimation at low computational cost. Further, it addresses the problem of the local magnetic
disturbances that, when present, affect all the orientation components (roll, pitch, and yaw). By
reducing the constraint of the magnetic ﬁeld vector rotation, it is able to limit the effect of the magnetic
disturbances to only affect the yaw component of the orientation. The last two constant gain ﬁlters, by
Euston et al.
[26], are commonly used because they offer good
performances at low computational cost and a comparative analysis of the two algorithms is presented
in [27]. The adaptive-gain complementary ﬁlter proposed by Tian et al.
[28] fuses a quaternion
estimation from fast moving gyroscope signal with a quaternion, from slow moving accelerometer and
magnetometer signals, computed through a Gauss-Newton algorithm. For more robust results, the gain is
adaptively adjusted according to the convergence rate of the low-frequency estimation and the divergence
rate of the high-frequency estimation. Fourati et al. [29] combine the output of a Levenberg-Marquardt
algorithm, the inputs for which are acceleration and local magnetic ﬁeld measurements, with the angular
rate measurements in a complementary observer based on the multiplicative correction technique.

[21], and by Madgwick et al.

To improve the performance of rigid body orientation estimation from low cost IMU/MARG under
dynamic motion, different approaches can be adopted. A simple switching method, as the one proposed
in the complementary ﬁlter presented in [30], can be used to determine the gain value under varying
dynamics sensed by the accelerometer. Another common method includes an adaptive measurement
noise covariance matrix that, in a Kalman ﬁlter framework, can be tuned adaptively to yield optimal
performance during the dynamic periods as proved in [31,32]. Alternatively, the acceleration can be
modeled to directly estimate the external acceleration and thus used to reduce the attitude error, as in the
Kalman ﬁlter proposed in [33].

The quaternion-based complementary ﬁlter proposed in this article can be used for both IMU and
MARG sensors. It ensures fast convergence and robustness thanks to the analytical derivation of the
correction quaternion. We address the problem of the magnetic disturbances by separating the quaternion
corrections in two different correction sequences and adopting the method presented in [26] that also
makes the algorithm independent on external parameters. Further, we adopt an adaptive-gain approach
to reduce the estimation error during high dynamic motion.

3. Background Theory

Any arbitrary orientation in the 3D space of a frame A with respect to a frame B can be represented

by a unit quaternion B

Aq deﬁned as following:

B
Aq =

q0

q1

q2

q3

T

=

cos α
2

ex sin α
2

ey sin α
2

ez sin α
2

T

(1)

(cid:104)

(cid:105)

(cid:104)

(cid:105)

where α is the rotation angle and e is the unit vector that represents the rotation axis. The quaternion
conjugate of B
Aq, given its unit norm, is equivalent to the inverse quaternion and describes the inverse

(3)

(4)

Sensors 2015, 15

19307

rotation. Therefore, the conjugate quaternion can be used to represent the orientation of frame B relative
to frame A, as deﬁned below.

B

Aq∗ = A

Bq =

q0 −

q1 −

q2 −

q3

(cid:104)

(cid:105)

T

(2)

The orientation quaternion after a sequence of rotations can be easily found by quaternion
multiplication where each quaternion represents the orientation of a frame with respect to the rotated
one. For example, given three frames A, B and C, and given the quaternion B
Aq orientation of frame A
expressed with respect to frame B and given the quaternion C
Bq orientation of frame B expressed with
respect to frame C, the orientation of frame A with respect to frame C is characterized by:

where quaternion multiplication, given two quaternions p and q, is deﬁned as

C

Aq = C
Bq

B
Aq

⊗

p0q0 −
p2q2 −
p1q1 −
p0q1 + p1q0 + p2q3 −
p0q2 −
p0q3 + p1q2 −

p3q3
p3q2
p1q3 + p2q0 + p3q1
p2q1 + p3q0








p

⊗

q = 





Unit quaternions can be applied to operate rotations of 3D vectors. For example a vector Av, expressed

with respect to the A frame, can be expressed with respect to the B frame by the following operation:

Bvq = B
Aq

Avq ⊗

⊗

B
Aq∗

(5)

where the symbol
vector v, in the two reference frames, written as pure quaternions as shown in Equation (6).

indicates the quaternion multiplication, and Avq and Bvq are the observations of the

⊗

vq =

0 v

T

=

0 vx vy vz

T

(6)

(cid:104)
The inverse rotation that describes the vector Bv relative to the frame A can be easily found by using

(cid:105)

(cid:104)

(cid:105)

the property of the conjugate quaternion and it is presented in Equation (7).

Bvq ⊗
The rotation deﬁned in Equation (5) can be written in matrix form as in Equation (8)

Bvq ⊗

Aq = A
Bq

Avq = B

A
Bq∗

Aq∗

⊗

⊗

B

Bv = R(B

Aq) Av

(7)

(8)

where R(B
(DCM) given in terms of the orientation quaternion B

Aq), which belongs to the 3D special orthogonal group SO(3), is the direct cosine matrix

Aq as shown below.

q2
3

q2
0 + q2
q2
1 −
2 −
2(q1q2 + q0q3)
q0q2)
2(q1q3 −

q0q3)

2(q1q2 −
1 + q2
q2
q2
0 −
2 −
2(q2q3 + q0q1)

q2
3

2(q1q3 + q0q2)
q0q1)
2(q2q3 −
2 + q2
q2
q2
q2
3
1 −
0 −

R(B

Aq) = 






(9)




Given the properties of the elements of the SO(3), the inverse rotation can be deﬁned as:

Av = R

A
Bq

Bv = RT(B

Aq) Bv

(10)

(cid:0)

(cid:1)

Sensors 2015, 15

19308

4. Quaternion from Earth-Field Observations

In this section, we analyze the algebraic derivation of a quaternion from the observation of the earth’s
ﬁelds. For a clear understanding of the following derivation, let us ﬁrst deﬁne a notation that will be
used throughout this article. We refer to the local (sensor) frame as L, and the global (earth) frame as
G. We can deﬁne the measured acceleration La and the true earth gravitational acceleration Gg as the
unit vectors:

La =

ax ay az

(cid:104)

Gg =

0 0 1

T

(cid:105)

T

,

= 1

a
(cid:107)

(cid:107)

(cid:105)
Similarly, we deﬁne the measured local magnetic ﬁeld Lm and the true magnetic ﬁeld Gh as the

(cid:104)

unit vectors:

Lm =

mx my mz

(cid:104)

Gh =

hx hy hz

T

,

(cid:105)
T
,

m
(cid:107)

(cid:107)

= 1

= 1

h
(cid:107)
(cid:107)

Finally, the gyroscopes measure the angular velocity Lω around the three sensor frame axes:

(cid:104)

(cid:105)

Lω =

ωx ωy ωz

T

Note that most IMUs usually measure a non-normalized vector a and m. However, for the purposes
of derivation in this article, we assume that the quantities have been normalized. The only relevant units
are those of ω, which we assume are radians per second.

(cid:104)

(cid:105)

We present an algebraic derivation of the orientation quaternion L

Gq, of the global frame (G) relative
to the local frame (L), as a function of La and Lm. We have two independent sensors observing two
independent ﬁelds; a straightforward way to formulate the quaternion is through the inverse orientation
which rotates the measured quantities La and Lm into the reference quantities Gg and Gh:

RT(L

Gq) La = Gg




RT(L

Gq) Lm = Gh

(11)



This system, however, is overdetermined - each of the two equations provides two independent
constraints on the orientation L
Gq, whereas the orientation only has three degrees of freedom. In the
case when there is a disagreement between the gravitational and magnetometer readings, the system
will not have a solution. The disagreement could arise from random sensor noise or unmodeled ﬁeld
disturbances (nongravitational accelerations or magnetic ﬁeld variations). A possible solution would be
to deﬁne an error metric and ﬁnd the quaternion which minimizes this error. However, this could still
result in disturbances in the magnetic ﬁeld affecting the roll and pitch, which we are trying to avoid.

To address this problem, we present a modiﬁed system of equations. The deﬁnition of the system
(but not its solution) is based on the approach presented in [26]. First, we redeﬁne the global coordinate
frame G to be aligned with the magnetic north. Speciﬁcally, the global frame’s x-axis points in the same
direction as the local magnetic ﬁeld (the z-axis remains vertical). Obviously, this global frame is only
“ﬁxed” in the case when the local magnetic ﬁeld does not change its heading.

Sensors 2015, 15

19309

Next, we modify the system in Equation (11) so that the second equation provides only one constraint.
Let GΠzx+ be the half-plane which contains all points that lie in the global xz-plane such that x is
non-negative. We require that the magnetic reading, when rotated into the global frame, lies on the
half-plane GΠzx+. Thus, we guarantee that the heading will be measured with respect to magnetic north,
but do not enforce a constraint on the magnetic inclination.

RT(L

Gq) La = Gg

RT(L

Gq) Lm

GΠzx+






(12)

∈
Note that when deﬁned in this manner, the system no longer needs a priori knowledge of the direction

of the earth’s magnetic ﬁeld Gh.

In the remainder of the section, we present a novel algebraic solution to obtain L

Gq as a function of La

and Lm. We begin by decomposing L

Gq into two auxiliary quaternions, qacc and qmag, such that:

and:

L

Gq = qacc ⊗

qmag

R(L

Gq) = R(qacc) R(qmag)

We further deﬁne qmag to have only a single degree of freedom, by setting it to:

qmag =

q0mag 0 0 q3mag

T

(13)

(14)

(15)

It follows from the quaternion deﬁnition in Equation (1) that qmag represents a rotation around the
z-axis only. Informally, qacc rotates a vector from the sensor frame to the horizontal plane of the global
frame, and qmag rotates it around the z axis to point North. In the following subsections, we present an
algebraic derivation of qacc and qmag.

(cid:104)

(cid:105)

4.1. Quaternion from Accelerometer Readings

In this subsection, we present a derivation for the auxiliary quaternion qacc as a function of La. The
observations of the gravity vector in the two reference frames allows us to ﬁnd the quaternion that
performs the transformation between the two representations. The rotation in the ﬁrst equation of system
Equation (12) can be re-written as:

and decomposed by using Equation(14) obtaining:

R(L

Gq) Gg = La

(16)

(17)



R(qacc)R(qmag) 

= 



0
0
1

ax
ay
az



The representation of the gravity vector in the global frame only has a component on the z-axis;
therefore any rotation about this axis does not produce any change on it. Consequently, Equation (17) is
equivalent to:










R(qacc) 




0
0
1

ax
ay
az






= 









(18)

19310

(19)

(20)

(21)

Sensors 2015, 15

expanding the multiplication we obtain the following system:

2(q1accq3acc + q0accq2acc) = ax

2(q2accq3acc −
q2
q2
1acc −
0acc −

q0accq1acc) = ay

2acc + q2
q2

3acc = az






It is clear that the above system is underdetermined and has an inﬁnite number of solutions. This is
not an unexpected result because the alignment of the gravity vector from its representation in the global
frame into the local frame does not give any information about the rotation around the z-axis (yaw). Thus,
such alignment can be achieved by inﬁnite rotations with deﬁnite roll and pitch angles and arbitrary yaw.
To restrict the solutions to a ﬁnite number we choose q3acc = 0 simplifying the system in Equation (19) to:

2q0accq2acc = ax

2q0accq1acc = ay






−
q2
0acc −

q2
1acc −

q2
2acc = az

The above system is fully determined; solving it results in four solutions for qacc. Two can be
discarded since they have a negative norm. The remaining two are equivalent, with all the quaternion
elements switching signs between one solution and the other. For convenience, we choose the solution
with positive quaternion scalar (q0), which corresponds to the shortest-path quaternion formulation [34].
Thus, we get:

qacc =

az+1
2

ay
√2(az+1)

−

ax
√2(az+1)

0

(cid:20) (cid:113)

T

(cid:21)

The formulation in Equation (21) is valid for all values of az except az =

1 in which it has a
singularity. Further, it may arise numerical instability when in proximity of the singularity point. To
address this issue we provide an alternative solution to the system in Equation (19). By simply setting
q2acc = 0 instead of q3acc = 0 in Equation (19) we obtain the reduced system:

−

q2
0acc −
which admits the following two real solutions:

q2
1acc −

q2
3acc = az

2q1accq3acc = ax

2q0accq1acc = ay






qacc1 =

−

(cid:20)

and

ay
√2(1

az)

−

1

az
−
2

0

(cid:113)

ax
√2(1

az)

−

qacc2 =

ay
√2(1

−

(cid:20)

az) −

(cid:113)

1

az
−
2

0

−

ax
√2(1

az)

−

(22)

(23)

(24)

T

(cid:21)

T

(cid:21)

Sensors 2015, 15

19311

and we choose the solution in Equation (23). This formulation for qacc has a singularity at az = 1.
Therefore, the ﬁnal formulation of qacc that avoids the singularity problem can be obtained by combining
Equations (21) and (23):

az+1
2

ay
√2(az+1)

−

ax
√2(az+1)

0

(cid:20) (cid:113)

ay
√2(1

−

−

az)

(cid:20)

(cid:113)

1

az
−
2

0

ax
√2(1

az)

−

T

(cid:21)
T

(cid:21)

, az ≥

0

, az < 0

(25)

qacc = 



Effectively, we solve the singularity problem by having two separate formulations for qacc depending
on the hemisphere in which a is pointing. Note that, deﬁned in this manner, qacc is not continuous at the
az = 0 point. However, we will demonstrate that this problem is resolved with the formulation of qmag
in the following subsection.

4.2. Quaternion from Magnetometer Readings

In this subsection, we present a derivation for the auxiliary quaternion qmag as a function of Lm
and qacc. First we use the quaternion qacc to rotate the body frame magnetic ﬁeld vector Lm into an
intermediate frame whose z-axis is the same as the global coordinate frame with orthogonal x-, y- axes
pointing in unknown directions due to the unknown yaw of qacc.

RT(qacc) Lm = l

(26)

where l is the rotated magnetic ﬁeld vector. Next, we ﬁnd the quaternion (qmag) that rotates the vector l
into the vector that lies on the GΠzx+ of Equation (12) using the following system:

where

RT(qmag) 



lx
ly
lz

√Γ
0
lz






= 









Γ = l2

x + l2
y

(27)

(28)

This quaternion performs a rotation only about the global z-axis by aligning the x-axis of the
intermediate frame into the positive direction of the magnetic north pole, which coincides with the x
direction of our global frame. This rotation will only change the heading component of the orientation
without affecting the roll and pitch components. Therefore, in presence of magnetic disturbances, their
inﬂuence is only limited on affecting the heading angle. The quaternion qmag has the following form:

qmag =

q0mag 0 0 q3mag

T

(29)

By reordering the system in Equation (27) and substituting qmag with its components we ﬁnd the

(cid:104)

(cid:105)

following simpliﬁed system:






(q2

0mag −

0mag )√Γ = lx
q2

2q0mag q3mag √Γ = ly

(30)

(q2

0mag + q2

3mag )lz = lz

Sensors 2015, 15

the solution of the above system which ensures the shortest rotation is the following:

qmag =

(cid:20)

√Γ+lx√Γ
√2Γ

0 0

ly
√2√Γ+lx√Γ

T

(cid:21)

19312

(31)

It is clear from the formulation of qmag that the latter quaternion incurs in a singularity state for
negative lx and zero ly. To avoid the singularity of qmag we prevent the l vector from having negative
x- component using the following procedure. If lx < 0 we rotate l of 180◦ around the world z- frame,

T

applying the quaternion qπ =
. Finally the rotated vector is used to ﬁnd qmag+, which
has the same form of Equation (31) and aligns l with the magnetic north. The sequences of rotations are
summarized in the quaternion multiplications below:

0 0 0 1

(cid:105)

(cid:104)

q∗mag+

q∗π ⊗

q∗acc ⊗

mq ⊗

qacc ⊗

⊗

qπ

⊗

qmag+

(32)

qacc = lq.
where mq is the local magnetic ﬁeld vector written as pure quaternion and q∗acc ⊗
For the sake of simplicity we consider the quaternion product between qπ and qmag+ as the alternative
formulation of qmag in the case of lx < 0 as following.

mq ⊗

The result of the above multiplication is shown in Equation (34):

qmag = qπ

qmag+

⊗

qmag =

ly
√2√Γ

−

lx√Γ

(cid:20)

0 0

√Γ

lx√Γ

−
√2Γ

(33)

(34)

T

(cid:21)

The complete formulation of qmag that avoids the singularity problem discussed above, is eventually

obtained by combining Equation (31) with Equation (34):

√Γ+lx√Γ
√2Γ

0 0

ly
√2√Γ+lx√Γ

(cid:20)

qmag = 


the multiplication of the two quaternions qacc and qmag as below.

ly
√2√Γ

0 0

−
√2Γ

√Γ

lx√Γ

lx√Γ

(cid:20)

−

T

(cid:21)

T

,

,

(cid:21)

0

lx ≥

lx < 0

(35)

Finally, we can generalize the quaternion orientation of the global frame relative to the local frame as

L

Gq = qacc ⊗

qmag

(36)

Note that the quaternion L

Gq does not suffer from the discontinuity problem of the yaw angle given
by the switching formulation of qacc of Equation (25) thanks to the multiplication with qmag, which
performs the alignment of the intermediate frame into the global frame as previously discussed.

Sensors 2015, 15

19313

(a)

(b)

(c)

Figure 1. Simulated experiment showing the orientation output in quaternion form (left)
(a) Orientation reference; (b) Orientation output
and in Euler representation (right).
of the presented method with noisy acceleration data and noise-free magnetometer data;
(c) Orientation output of the presented method with noise-free acceleration data and
magnetic readings affected by magnetic disturbances.

To test the effectiveness of our method, we implemented a MatLab simulation. The results of which
are shown in Figure 1. We simulate three consecutive constant velocity (1 rad/s) rotations of 360◦
about each axis. First, we test the result of the quaternion solution of our proposed method by using

Sensors 2015, 15

19314

perfect accelerometer and magnetometer data obtained by rotating the global frame vectors (gravity and
magnetic ﬁeld) into the local frame by using the orientation reference computed through the integration
of the angular velocity vector, obtaining the same output of Figure 1a. Note, on the right side of
Figure 1, that during the rotation about the y-axis, besides the variation of the pitch angle, we also observe
an instantaneous jump of the roll and yaw angles because of the singularity conﬁguration that affects the
Euler representation. However, as shown on the left side of the ﬁgure, the quaternion representation
does not incur in a singularity state; moreover, our formulation ensures the continuity of the quaternion
throughout the rotation.
In Figure 1b we prove that our method works with noisy acceleration data
affected by Gaussian noise. When the sensor is close to some conﬁguration where the yaw angle’s value
is either π or
π, because of the noise, the yaw ﬂips between the two values, which are two alternate
representation of the same rotation. Finally, in the simulation of Figure 1c, we show the result of our
orientation estimation from noise-free acceleration data and magnetometer data affected by magnetic
disturbances. It is clear, from the Euler representation of the orientation, that the magnetic disturbances
affect only the yaw angle.

−

5. Quaternion-Based Complementary Filter

A complementary ﬁlter uses an analysis in the frequency domain of the signals to combine them to
obtain a better estimation of a particular quantity. If the signals are affected by noises with different
frequency, two ﬁlters, with an appropriate bandwidth, can be applied such that the sum of the two
ﬁltered signals cover the full range of useful frequency. For attitude estimation from IMU readings,
a complementary ﬁlter performs high-pass ﬁltering on the orientation estimated from gyroscope data
affected by low-frequency noise, and low-pass ﬁlter on accelerometer data affected by high-frequency
noise. The fusion between the two ﬁltered estimations will ideally obtain an all-pass and noise-free
attitude estimation. The term “complementary” derives from the cut-off frequency value, which is the
same for both ﬁlters. Thus, its correct value is found as a trade-off between the preserved bandwidth of
each single signal.

The complementary ﬁlter we propose in this article can be used for both IMU and MARG sensors,
and is described in the diagrams of Figures 2 and 3. It fuses attitude estimation in quaternion form from
gyroscope data, with accelerometer data in the form of a delta quaternion, which serves as correction
only for roll and pitch components of the attitude maintaining the yaw estimation from the gyroscope.
If magnetometer data is provided, a second step is added to the algorithm where a delta quaternion, from
magnetic ﬁeld readings, is derived to correct the heading of the previous estimation by performing a
small rotation about the global z-axis in order to align the current frame with the magnetic ﬁeld.

Sensors 2015, 15

19315

Lωt

Lat

1
2

−

Lωq,t ⊗

L

Gq(cid:48)t
−

1

R

L

Gqω,t

(cid:16)

(cid:17)

R

G

L qω,t

Lat

(cid:16)

(cid:17)

Ggp

L

G ˙qω,t

L

Gqω,t

(cid:90)
Gqω,t

L

L

Gq(cid:48)t

×

•
∆qacc

∆qacc

(cid:99)
LERP / SLERP

Figure 2. Block diagram of the complementary ﬁlter for IMU implementation (no
magnetometer data).

Figure 3. Block diagram of the complementary ﬁlter for MARG implementation (with
magnetometer data).

5.1. Prediction

In the prediction step, the angular velocity vector, measured by the tri-axis gyroscope, is used to
compute a ﬁrst estimation of the orientation in quaternion form. Assuming known the initial conditions,
we ﬁrst calculate the quaternion describing the rate of change of the orientation as a quaternion derivative,
by multiplying the previous state with the angular velocity vector arranged as a pure quaternion as in
Equation (6). In the literature, the quaternion derivative from an angular rate measurement is usually
calculated for the forward quaternion, that is, the one representing the orientation of the local frame
with respect to the global frame. Because in this article we use the inverse orientation, for the sake
of clarity, we compute the quaternion derivative for our convention, starting from the formula for the
forward quaternion.

Sensors2015,xx14Figure2.BlockdiagramofthecomplementaryﬁlterforIMUimplementation(nomagnetometerdata).LωtLatLGq0t−12Lωq,t⊗LGq0t−1Z×R(cid:16)LGqω,t(cid:17)R(cid:16)GLqω,t(cid:17)Lat∆qacc•LERP/SLERPLG˙qω,tLGqω,tLGqω,tGgpc∆qaccFigure3.BlockdiagramofthecomplementaryﬁlterforMARGimplementation(withmagnetometerdata).LωtLatLmtLGqt−12Lωq,t⊗LGqt−1Z×R(cid:16)LGqω,t(cid:17)R(cid:16)GLqω,t(cid:17)Lat∆qaccR(GLq0t)R(GLq0t)LmtLERP/SLERP∆qmagLERP/SLERP×••LG˙qω,tLGqω,tLGqω,tGgpc∆qaccLGq0tlc∆qmagweﬁrstcalculatethequaterniondescribingtherateofchangeoftheorientationasaquaternionderivative,bymultiplyingthepreviousstatewiththeangularvelocityvectorarrangedasapurequaternionasinEq.(6).Intheliterature,thequaternionderivativefromanangularratemeasurementisusuallycalculatedfortheforwardquaternion,thatis,theonerepresentingtheorientationofthelocalframewithrespecttotheglobalframe.Becauseinthisarticleweusetheinverseorientation,forthesakeofclarity,wecomputethequaternionderivativeforourconvention,startingfromtheformulafortheforwardquaternion.ItiswellknownthattheangularrateLωandthe“forward”quaternionderivativearerelatedbythefollowingidentity:GL˙qω,t=12GLqt−1⊗Lωq,t(37)whereLωq,tistheangularvelocityvectorarrangedaspurequaternionattimeinstantt.Inourcase,wewanttodeterminethederivativeoftheinverseunitquaternion,whichissimplytheconjugateof(37),therefore:LG˙qω,t=GL˙q∗ω,t=12(GLqt−1⊗Lωq,t)∗=12Lω∗q,t⊗GLq∗t−1(38)

(39)

Sensors 2015, 15

19316

It is well known that the angular rate Lω and the “forward” quaternion derivative are related by the

following identity:

1
2
where Lωq,tk is the angular velocity vector arranged as pure quaternion at time instant tk and G
L qtk−1 is
the previous estimate of the orientation. In our case, we want to determine the derivative of the inverse
unit quaternion, which is simply the conjugate of Equation (37), therefore:

L qtk−1 ⊗

Lωq,tk

L ˙qω,tk

(37)

=

G

G

L

G ˙qω,tk

= G

L ˙q∗

ω,tk

=

1
2

(G
L qtk−1 ⊗

Lωq,tk

)∗ =

1
2

Lω∗

q,tk ⊗

G
L q∗

tk−1

as the conjugate of the pure quaternion Lωq is just its negative (zero scalar component), we can
ﬁnally write:

The above equation can be rewritten in matrix form as shown in Equation (39):

L

G ˙qω,tk

=

−

Lωq,tk ⊗

L

Gqtk−1

1
2

where

L

G ˙qω,tk

= Ω

L

Gqtk−1

Lωtk
(cid:0)

(cid:1)

Lωtk
0
Lωtk×
Lωtk −
−
and, regardless of the time dependence, the term [Lω
] denotes the cross-product matrix that is
(cid:3)
(cid:2)
×
associated with Lω and is equal to:

Lωtk
(cid:0)

(40)

Ω

=

(cid:34)

(cid:35)

(cid:1)

T

[Lω

] = 

×




ωz ωy
0
−
ωx
ωz
0
ωy ωx
0

−

−






(41)

The orientation of the global frame relative to local frame at time tk can be ﬁnally computed by

numerically integrating the quaternion derivative using the sampling period ∆t = tk −

tk

1.

−

L

Gqω,tk

= L

Gqtk−1

* L

G ˙qω,tk

∆t

(42)

5.2. Correction

The correction adopted is based on a multiplicative technique. The predicted quaternion L

Gqω (for

clarity we omit the time t) is corrected by means of two delta quaternions as in Equation (43):

L

Gq = L

∆qmag

Gqω ⊗

∆qacc ⊗
(cid:99)
Each delta quaternion is computed and ﬁltered by the high-frequency noise independently; thus we
divide the correction into two separated steps. The ﬁrst step corrects the predicted quaternion only in the
∆qacc computed with data from the accelerometer. The
roll and pitch components by the application of
second step is used only when the magnetic ﬁeld readings are provided and corrects the yaw component
of the quaternion orientation by applying

(43)

(cid:99)

(cid:99)

∆qmag.

(cid:99)

Sensors 2015, 15

19317

5.2.1. Accelerometer-Based Correction

We use the inverse predicted quaternion G

L qω to rotate the normalized body frame gravity vector La

(measured by the accelerometer) into the global frame as shown below.

R

G
L qω

La = Ggp

(44)

(cid:1)
obtaining the vector Ggp that we call “predicted gravity”. The predicted gravity will have a small
deviation from the real gravity vector; therefore, we compute the delta quaternion, ∆qacc, which rotates
Gg into Ggp (because we represent the orientation of the global frame relative to the local frame), by
using the following system:

(cid:0)

R(∆qacc) 




0
0
1

= 









gx
gy
gz

where

(45)







gx
gy
gz







Gg = 

,



Ggp = 

0
0
1







Note that the system in Equation (45) is similar to the system in Equation (18); therefore, we proceed
in the same manner to ﬁnd a closed-form solution. We deﬁne the component ∆q3acc = 0 thus obtaining
the following simpliﬁed system.

2∆q0acc∆q2acc = gx

2∆q0acc∆q1acc = gy

0acc −

∆q2

1acc −

∆q2

2acc = gz

−
∆q2






Proceeding as for system in Equation (18) we ﬁnd the following solution:

∆qacc =

(cid:20) (cid:113)

gz+1
2

gy
√2(gz+1)

−

gx
√2(gz+1)

0

T

(cid:21)

(46)

(47)

which is the one that ensures the shortest rotation. Although Equation (47) has a singularity for gz =
1,
we do not resolve it because the delta quaternion is applied at each step to correct the small deviation
between the predicted gravity and the real gravity. Therefore, the value of gz will always be very close
to 1. However, for a more rigorous formulation, the approach used in Equation (22) can be adopted.

−

As the delta quaternion is affected by the accelerometer’s high frequency noise, before applying it
to the predicted quaternion, we scale it down by using an interpolation with the identity quaternion qI.
We use two different interpolation approaches based on the angle between qI and ∆qacc. Given two
quaternions p and q, the cosine of the angle Ω subtended by the arc between them is equal to the dot
product of the two quaternions as shown below:

cos Ω = p

·

q = p0q0 + p1q1 + p2q2 + p3q3

(48)

Sensors 2015, 15

In our case, as the identity quaternion has the following components

qI =

1 0 0 0

T

19318

(49)

the dot product is equal to the ∆q0acc component of ∆qacc. If ∆q0acc > (cid:15), where (cid:15) is a threshold value
(in our case (cid:15) = 0.9), we use a simple Linear intERPolation (LERP) as in the equation below.

(cid:104)

(cid:105)

∆qacc = (1

−

α)qI + α∆qacc

(50)

where α
maintain the unit norm of the delta quaternion ∆qacc that is then normalized immediately after:

[0, 1] is the gain that characterizes the cut-off frequency of the ﬁlter [35]. LERP does not

∈

∆qacc
∆qacc(cid:107)

(cid:107)

(51)

∆qacc =

(cid:99)

If ∆q0acc ≤

(cid:15), we use the Spherical Linear intERPolation (SLERP) [36]. The SLERP algorithm gives
a correct evaluation of the weighted average of two points lying on a curve. In the case of quaternions,
the points lie on the surface of the 4D sphere (hypersphere). A simple 2D visualization of LERP and
SLERP mapping processes is shown in Figure 4. The SLERP formula we used is the following:

∆qacc =

sin([1

α]Ω)

−
sin Ω

qI +

sin(αΩ)
sin Ω

∆qacc

(52)

(cid:99)

The ∆qacc may have a large value when the predicted gravity has a signiﬁcant deviation from the
real gravity. If that condition does not occur, the delta quaternion is very small; thus, we prefer using
the LERP formula because it is computationally more efﬁcient. Finally, the quaternion estimated from
gyroscope data is multiplied by the ﬁltered delta quaternion, providing correction in the roll and pitch
component, while the heading is preserved from the predicted orientation.

L

Gq(cid:48) = L

Gqω ⊗

qa

Ω

qint

qb

(53)

∆qacc

(cid:99)

qa

Ω

qint

qb

LERP

SLERP

Figure 4. 2-D representation of two different interpolation methods between quaternion qa
and qb resulting in quaternion qint. On the left is represented the linear interpolation (LERP),
whereas on the right the spherical linear interpolation (SLERP) showing the correct result.

Sensors 2015, 15

19319

5.2.2. Magnetometer-Based Correction

If magnetic ﬁeld data is provided, a second step performs the correction on the heading component.
We proceed in the same way as in the ﬁrst step by computing a delta quaternion. First, we use the
Gq(cid:48), calculated in Equation (53), to rotate the body frame magnetic ﬁeld vector Lm
quaternion inverse of L
into the world frame magnetic vector.

R

G
L q(cid:48)

Lm = l

(54)

Next, we ﬁnd the delta quaternion (∆qmag), which rotates the vector l into the vector that lies on the

(cid:0)

(cid:1)

xz-semiplane deﬁned in Section 4 such that:

lx
ly
lz

RT(∆qmag) 



= 









l2
x + l2
y
0
lz

(cid:112)



(55)




(cid:105)

This delta quaternion performs a rotation only about the global z-axis by aligning the global x-axis
into the positive direction of the magnetic north pole. Further, with this formulation, such rotation does
not affect the roll and pitch components even in the presence of magnetic disturbances, limiting their
inﬂuence only on the heading angle. Thus, the delta quaternion ∆qmag has the following shape:

∆qmag =

∆q0mag 0 0 ∆q3mag

T

(56)

By rearranging the system in Equation (55) and substituting ∆qmag with its component, we ﬁnd the

(cid:104)

following simpliﬁed system:

∆q2

3mag )

(∆q2

0mag −
2∆q0mag ∆q3mag

(cid:112)
x + l2
l2

y = ly

x + l2
l2

y = lx

(∆q2

0mag + ∆q2

(cid:112)
3mag )lz = lz






the solution of the above system that ensures the shortest rotation is the following:

∆qmag =

(cid:20)

√Γ+lx√Γ
√2Γ

0 0

ly
√2(Γ+lx√Γ)

T

(cid:21)

(57)

(58)

with Γ as per Equation (28). The delta quaternion ∆qmag is affected by the noise of the magnetometer,
which is ﬁltered by using the procedure we adopted for ∆qacc, switching between LERP and SLERP
according to the same criterion. Another advantage of using two correction steps is the possibility to
apply two different ﬁltering gains. As the two delta quaternions are completely independent to each
other, and each of them is related to a particular sensor (accelerometer and magnetometer), they might
be affected by different frequency noise. Thus, The LERP and SLERP formulas applied to ∆qmag are the
same as the ones in Equations (50) and (52), respectively, where the gain α is replaced with β, obtaining
∆qmag is applied to the quaternion in Equation (53) obtaining
∆qmag. Eventually, the delta quaternion
the ﬁnal quaternion, which expresses the orientation of the global frame with respect to the local frame.
(cid:99)

(cid:99)
Gq = L
L

Gq(cid:48)

∆qmag

⊗

(cid:99)

(59)

Sensors 2015, 15

5.3. Adaptive Gain

19320

A drawback of a typical implementation of the complementary ﬁlter is the constant gain that often
causes inaccurate orientation estimation during highly dynamic motion. When the vehicle moves with
high acceleration, the magnitude and direction of the total measured acceleration vector are different
from gravity; therefore the attitude is evaluated using a false reference, resulting in signiﬁcant, possibly
critical errors. However, the gyroscope readings are not affected by linear acceleration, thus they can
still be used to compute a relatively accurate orientation estimation that, under this condition, should
be treated as the main source of the estimate. A constant gain fusion algorithm cannot overcome the
aforementioned problem if the optimal gain has been evaluated for static conditions.
In this paper
we address this issue adopting an adaptive gain whose strategy is slightly different from the switching
approach proposed in [30].

First we deﬁne the magnitude error em as in the following equation:

em = |(cid:107)

L ˜a

(cid:107) −
g

g

|

(60)

L ˜a
(cid:107)

(cid:107)

is the norm of the measured local frame acceleration vector before normalization and
where
g = 9.81 m/s2. Given Equations (50) and (52), we make the ﬁltering gain α function of the magnitude
error em through the gain factor f , meaning:

α = α(em) = ¯αf (em)

(61)

where ¯α is the constant value that gives the best ﬁltering result in static conditions and f (em) is what we
call the “gain factor”, which is a piecewise continuous function of the magnitude error as shown in
Figure 5. The gain factor is constant and equal to 1 when the magnitude of the nongravitational
acceleration is not high enough to overcome the acceleration of gravity and the value of the error
magnitude does not reach the ﬁrst threshold.
If the nongravitational acceleration rises and the error
magnitude exceeds that ﬁrst threshold, the gain factor decreases linearly with the increase of the
magnitude error until reaching zero for error magnitude equal to the second threshold and over.
Empirically, we found that the two thresholds’ values that give the best results are respectively
0.1 and 0.2.

Figure 5. The gain factor function used in the adaptive gain to reduce the attitude error
deriving from the external linear acceleration because of vehicle motion.

Sensors 2015, 15

19321

In this article we do not address the problem of the centripetal acceleration; however, if conditions

warrant, one can easily add the centripetal force model used in [21].

5.4. Filter Initialization and Bias Estimation

The complementary ﬁlter proposed in this article is initialized with the orientation quaternion
calculated using the procedure explained in Section 4. The values of the current body-frame acceleration
and magnetic ﬁeld vectors are used to produce the quaternion representing the initial orientation of the
rigid body in any conﬁguration. Therefore, for the initialization, the ﬁlter does not need any assumption
and it is performed in one single step.

Before using the angular velocity vector for the quaternion prediction, we correct it for the bias. The
bias of a sensor’s reading is a slow-varying signal considered as low frequency noise. Therefore, we
adopt a low-pass ﬁlter to separate the bias from the actual angular velocity reading. To avoid ﬁltering
useful information, the low-pass ﬁltering is applied only when the sensor is in a steady-state condition
that is previously checked. If the sensor is in the steady-state condition, the bias is updated, otherwise it is
assumed to be equal to the previous step value. The estimated bias is then subtracted from the gyroscope
reading obtaining a bias-free angular velocity measurement. The low-pass ﬁlter cut-off frequency can be
selected by the user as well as parameters for the steady-state condition, to apply the bias-estimation to
different sensors.

6. Experiments

In this section, we evaluate the performances of the proposed complementary ﬁlter under different
conditions and we compare it against other common estimation methods. At ﬁrst we evaluate the overall
performances during MAV ﬂights, then we evaluate and compare the behavior of the different methods
under, respectively, magnetic disturbances and high nongravitational acceleration.

6.1. MAV Flight Experiment

In the ﬁrst experiment, we evaluated the accuracy of the orientation estimation algorithm using
publicly-available MAV datasets [37] with ground-truth orientation in Euler-angles form from a
motion-capture system.

×

×

10 m

The datasets are recorded using an AscTec “Pelican” quadrotor, ﬂying in an indoor environment of
size 10 m
10 m, equipped with eight Vicon cameras, performing 1, 2, and 3 loops, respectively.
Figure 6 shows the trajectory traveled by the quadrotor during the “1loop” experiment, tracked by the
motion capture system. The datasets include acceleration and angular velocity readings from the IMU,
and no magnetic ﬁeld data. We compare our method against the orientation estimation proposed by
Madgwick et al.
in [26], the quaternion-based EKF proposed by Sabatini [24], and the algorithm
embedded in the low-level processor of the AscTec quadrotor, whose output, in Euler angles form, is
provided in the datasets. Tables 1–3 show the Root Mean Square (RMS) error for roll, pitch, and yaw
angles, respectively, in the three datasets, proving that our algorithm outperforms the other methods for
all the sets. Note that the proposed method and one of the algorithms against which we compare it, by

Sensors 2015, 15

19322

Madgwick et al. are constant gain ﬁlters. Therefore, their performance will vary based on the value of
the chosen gain. To obtain a fair qualitative comparison, we chose the gains that minimize the RMS error
of the estimation for each method. Figure 7 shows the orientation in Euler angles for the four different
algorithms using the data from the “1LoopDown” dataset. Note that as the magnetic ﬁeld readings are
not provided, no correction is available for the yaw component. However, enabling our bias estimation
allows a signiﬁcant reduction of the drift error.

Figure 6. 2D top view (left) and 3D side view (right) of the trajectory traveled by the
quadrotor during the “1LoopDown” experiment.

Table 1. RMS roll angle error [radians].

Dataset

Proposed Madgwick AscTec

EKF

1LoopDown
2LoopsDown
3LoopsDown

0.0233
0.0292
0.0277

0.0370
0.0470
0.0405

0.0464
0.0338
0.0315

0.0287
0.0314
0.0331

Table 2. RMS pitch angle error [radians].

Dataset

Proposed Madgwick AscTec

EKF

1LoopDown
2LoopsDown
3LoopsDown

0.0209
0.0223
0.0202

0.0336
0.0369
0.0360

0.0369
0.0313
0.0329

0.0284
0.0384
0.0392

Table 3. RMS yaw angle error [radians].

Dataset

Proposed Madgwick AscTec

EKF

1LoopDown
2LoopsDown
3LoopsDown

0.1429
0.1309
0.2890

0.2543
0.9229
1.3327

0.3388
0.3182
0.3255

0.1888
0.3345
0.3545

Sensors 2015, 15

19323

(a)

(b)

(c)

Figure 7. Comparison of the orientation Euler angles output of the three methods during the
“1LoopDown” experiment. (a) Roll; (b) Pitch; (c) Yaw.

Sensors 2015, 15

6.2. Magnetic Disturbances

19324

In the second experiment, we used a Phidgets Spatial 3/3/3 sensor. It provides acceleration, angular
rate, and magnetic ﬁeld strength measurements in three axes. In this case, we computed the orientation
using acceleration as well as magnetic ﬁeld data. We held the sensor in a steady state while reading the
output of our complementary ﬁlter, the EKF, and the ﬁlter by Madgwick et al. We induced magnetic
disturbances by approaching a magnet to the sensor and repeated this action thrice. The ﬁrst two times
we applied the magnetic disturbance only for a couple of seconds, whereas for the third time, we retained
the disturbance until the end of the experiment. Figure 8 shows the results of the experiment. The roll
and pitch angles from our complementary ﬁlter are completely immune to magnetic disturbances. The
roll and pitch from the Madgwick ﬁlter are affected by the magnetic disturbances when we approach the
magnet to the sensor, converging back to the right value when the disturbance is removed. When we
induce the disturbance the third time, the roll and pitch of the Madgwick ﬁlter present a similar behavior,
but with a slower convergence, showing that the roll and pitch angles are only immune to constant
magnetic ﬂux. The EKF has a random behavior because it is already affected by the magnetic ﬂux
present in the room caused by electric devices, as a consequence of the coupled nature of the acceleration
and magnetic ﬁeld correction. In fact, although the norm of the measured magnetic ﬁeld is constant at
the beginning of the experiment, its value is different from the norm of the reference magnetic ﬁeld
vector (about 0.54 Gauss in this area), vector that is needed as input to the EKF. At the bottom of
Figure 8 we show the yaw angles output of the three algorithms, during the same experiment, compared
against the reference yaw angle extracted from the magnetic ﬁeld vector. Unlike the Madgwick ﬁlter, the
proposed complementary ﬁlter has the advantage of having a dedicated gain (β) to ﬁlter the magnetic
ﬁeld measurement noise. This allows us to change the yaw sensitivity to the reference variations. For
this experiment, we chose the gain value that gives the best trade-off between the error because of the
magnetic disturbances and the rate of the convergence. Note that although the Madgwick ﬁlter can vary
its magnetic sensitivity by changing the ﬁltering gain, this would also cause a performance degradation
in the estimation of the roll and pitch components because only one gain controls the cut-off frequency of
the signals coming from two different sensors. In the case of the EKF, when the measurement covariance
comes directly from the sensor’s standard deviation, the yaw output is very sensitive to the magnetic
disturbances as can be seen in the ﬁgure. However, it is well known that the measurement covariance
can be changed to make the algorithm less sensitive to the selected measurement.

6.3. High Nongravitational Acceleration

In this experiment, we analyze the efﬁciency of our complementary ﬁlter adopting the adaptive
gain introduced in Section 5.3 under the condition of high nongravitational acceleration. We used the
previously described Phidgets Spatial 3/3/3 sensor, attached to a slider, free to translate over a camera rail
track, such that the sensor’s x-axis is pointing along the direction of the translation. This setup allows us
to create accelerated motion even as maintaining the IMU on the same plane throughout the experiment
with constant zero attitude. We induced a high linear acceleration on the x
body axis by moving the
slider abruptly back and forth. Note that because the sensor moves in the horizontal plane, the inertial

−

Sensors 2015, 15

19325

forces measured by the IMU are completely decoupled: gravitational acceleration on the z-axis, and
total body motion acceleration on the x-axis.

(a)

(b)

(c)

(d)

Figure 8. Comparison of the different estimation methods in the presence of magnetic
disturbances. (a) Norm of the measured magnetic ﬁeld vector; (b) Roll; (c) Pitch; (d) Yaw.

Sensors 2015, 15

19326

We evaluate the improvement of our method from the addition of the adaptive gain. Figure 9 shows
the pitch angle output of the proposed algorithm with constant and adaptive gain, as well as the pitch
angle output of the EKF and the Madgwick ﬁlter. The acceleration because of the rigid-body motion
has a varying value reaching a maximum of 50 m/s2. This causes an error of the output of the constant
gain complementary ﬁlter to reach 0.3 radians, whereas the output of the adaptive gain ﬁlter has an
error which never exceeds 0.02 radians. Moreover, the proposed adaptive gain complementary ﬁlter
clearly outperforms the other two methods that do not have a solution to reduce the attitude error during
accelerated motion.

(a)

(b)

Figure 9. Pitch estimation under the condition of high nongravitational acceleration; (a) Non
gravitational acceleration applied during the experiment; (b) Pitch angle output of the
different algorithms

Sensors 2015, 15

19327

Ultimately, we analyzed the computational time of the three methods. We proﬁled a reasonably
optimized C++ implementation of all the algorithms running on an Intel core I7, 3.6 GHz processor.
Table 4 summarizes the results for the average execution time of a prediction-correction update cycle.
The results demonstrate that the proposed complementary ﬁlter and the Madgwick algorithm have very
similar processing times suitable for small embedded processors, whereas the EKF has a runtime almost
six times higher. Note that given the higher standard deviation of the average time measurement relative
to the Madgwick ﬁlter, we can consider negligible the small difference of 0.14 µs between the two
faster approaches.

Table 4. Computational time of estimation algorithms.

Algorithm Average Time (µs) Standard Deviation (µs)

Proposed
Madgwick
EKF

1.4243
1.2839
7.0408

0.4761
0.7101
0.2342

7. Conclusions

In this article we presented a novel deterministic solution to the Whaba’s problem to ﬁnd the
orientation in quaternion form given two pairs of vector observations from inertial sensors. We are
able to ﬁnd the orientation of the global frame with respect to the local frame without leading to
ambiguous results or singularity problems. The subdivision of the quaternion in two parts makes the
roll and pitch components immune to magnetic distortions. Further, the procedure adopted to ﬁnd the
heading component of the orientation eliminates the need for a direction magnetic ﬁeld to be predeﬁned.
We demonstrated analytically and empirically the validity of the proposed method.

We also presented a novel quaternion-based complementary ﬁlter, which fuses together gyroscope
data with accelerometer and magnetic ﬁeld data. The predicted quaternion is calculated by using the
well-known linear formulation of the quaternion rate of change from the gyroscope’s angular rate.
The correction is applied by means of two delta quaternions that are computed using an approach
based on the method described in Section 4. The presented algorithm offers several advantages over
other implementations:

•
•

•
•

Fast initialization in quaternion form allowing any starting conﬁguration.
Fast convergence of the orientation quaternion because of the algebraic formulation of the
delta quaternions.
Two different gains to separately ﬁlter acceleration and magnetic ﬁeld noises.
Magnetic distortion compensation that involves a two-fold advantage:
it avoids the impact of
the magnetic disturbances on the roll and pitch components of the orientation when the sensor
is surrounded by unwanted magnetic ﬂux and eliminates the need of a predeﬁned magnetic
ﬁeld direction.

Moreover, our algorithm does not compute any matrix inversion or matrix multiplication, maintaining

a low computational cost making it suitable for onboard implementation.

Sensors 2015, 15

19328

We evaluated our complementary ﬁlter using publicly available data of a micro quadrotor helicopter
ﬂying in an indoor environment. We compared our results against other algorithms, showing better
performances of our method.

Acknowledgments

This

study has been supported in part by U.S. Army Research Ofﬁce under grant
IIS-0644127 and

No. W911NF-09-1-0565, U.S. National Science Foundation under grants No.
No. CBET-1160046.

Author Contributions

Roberto G. Valenti and Ivan Dryanovski conceived the mathematical derivation of the presented
approach and wrote the implementation of the algorithm; Roberto G. Valenti performed the experiments,
analyzed the data and wrote the paper; Jizhong Xiao contributed material/analysis tools and mentorship.

Conﬂicts of Interest

The authors declare no conﬂict of interest.

References

1. Wahba, G. A Least Square Estimate of Spacecraft Attitude. Soc. Ind. Appl. Math. (SIAM) Rev.

1965, 7, 409–1965.

2. Wertz, J.R. Spacecraft Attitude Determination and Control; Wertz, J.R., Ed.; Kluwer Academic

Publishers: Dordrecht, The Netherlands, 1978; pp. 427–428.

3. Shuster, M.; Oh, S. Three-axis attitude determination from vector observations. J. Guid. Control

1981, 4, 70–77.

4. Keat,

J. Analysis of Least-Squares Attitude Determination Routine DOAOP; Report

CSC/TM-77/6034; Computer Sciences Corporation: Greenbelt, MD, USA, February 1977.

5. Markley, F.L. Attitude Determination Using Vector Observations and the Singular Value

Decomposition. J. Astronaut. Sci. 1988, 36, 245–258.

6. Bar-Itzhack, I.Y. Polar Decomposition for Attitude Determination from Vector Observations. In
Proceedings of the AIAA Guidance, Navigation, and Control, Hilton Head Island, SC, USA, 10–12
August 1992.

7. Mortari, D. Euler-2 and Euler-n Algorithms for Attitude Determination from Vector Observations.
In Proceedings of the IFAC Space Technology International Conference on Intelligent Autonomous
Control in Aerospace, Beijing, China, 14–16 August 1995.

8. Markley, F.L. Attitude Determination Using Vector Observations: A Fast Optimal Matrix

Algorithm. J. Astronaut. Sci. 1993, 41, 261–280.

9. Mortari, D. Energy Approach Algorithm for Attitude Determination from Vector Observations.

Adv. Austronaut. Sci. 1995, 89, 773–784.

Sensors 2015, 15

19329

10. Markley, F.L.; Mortari, D. Quaternion Attitude Estimation Using Vector Observations.

J. Austronaut. Sci. 2000, 48, 359–380.

11. Yun, X.; Bachmann, E.R.; Mcghee, R.B. A Simpliﬁed Quaternion-Based Algorithm for Orientation
Estimation From Earth Gravity and Magnetic Field Measurements. IEEE Trans. Instrum. Meas.
2008, 57, 638–650.

12. Crassidis, J.L.; Markley, F.L.; Cheng, Y. Survey of nonlinear attitude estimation methods. J. Guid.

Control Dyn. 2007, 30, 12–28.

13. Gebre-Egziabher, D.; Hayward, R.C.; Powell, J.D. Design of Multi-sensor Attitude Determination

Systems. IEEE Trans. Aerosp. Electron. Syst. 2004, 40, 627–649.

14. Choukroun, D.; Bar-Itzhack, I.Y.; Oshman, Y. Novel Quaternion Kalman Filter.

IEEE Trans.

Aerosp. Electron. Syst. 2006, 42, 174–190.

15. Tao, W.; Zheng, R.; Feng, H. Gait Analysis Using Wearable Sensors. Sensors 2012, 12, 2255–2283.
16. Sabatini, A.M. Quaternion-based extended Kalman ﬁlter for determining orientation by inertial and

magnetic sensing. IEEE Trans. Biomed. Eng. 2006, 53, 1346–1356.

17. Hung, T.N.; Suh, Y.S. Inertial Sensor-Based Two Feet Motion Tracking for Gait Analysis. Sensors

2013, 13, 5614–5629.

18. Barshan, B.; Durrant-Whyte, H.F. Inertial navigation systems for mobile robots.

IEEE Trans.

Robot. Autom. 1995, 11, 328–342.

19. Jun, M.; Roumeliotis, S.I.; Sukhatme, G.S. State estimation of an autonomous helicopter using
Kalman ﬁltering. In Proceedings of the IEEE/RSJ International Conference on Intelligent Robots
and Systems, Kyongju, Korea, 17–21 October 1999; Volume 3, pp. 1346–1353.

20. Baerveldt, A.J.; Klang, R. A low-cost and low-weight attitude estimation system for an autonomous
In Proceedings of the IEEE International Conference on Intelligent Engineering

helicopter.
Systems, Budapest, Hungary, 15–17 September 1997; pp. 391–395.

21. Euston, M.; Coote, P.; Mahony, R.; Hamel, T. A complementary ﬁlter for attitude estimation of a
ﬁxed-wing UAV. In Proceedings of the IEEE/RSJ International Conference on Intelligent Robots
and Systems, Nice, France, 22–26 September 2008; pp. 340–345.

22. Mahony, R.; Hamel, T.; Pﬂimlin, J. Nonlinear Complementary Filters on the Special Orthogonal

Group. IEEE Trans. Autom. Control 2008, 53, 1203–1218.

23. Marins, J.L.; Yun, X.; Bachmann, E.R.; McGhee, R.B.; Zyda, M.J. An extended Kalman ﬁlter for
quaternion-based orientation estimation using MARG sensors. In Proceedings of the IEEE/RSJ
International Conference on Intelligent Robots and Systems, Maui, HI, USA, 29 October–3
November 2001; pp. 2003–2011.

24. Sabatini, A.M. Kalman-Filter-Based Orientation Determination Using Inertial/Magnetic Sensors:

Observability Analysis and Performance Evaluation. Sensors 2011, 11, 9182–9206.

25. Bachmann, E.R.; McGhee, R.B.; Yun, X.; Zyda, M.J. Inertial and magnetic posture tracking for
inserting humans into networked virtual environments. In Proceedings of the ACM Symposium
on Virtual Reality Software and Technology VRST, Baniff, AB, Canada, 15–17 November 2001;
pp. 9–16.

Sensors 2015, 15

19330

26. Madgwick, S.O.H.; Harrison, A.J.L.; Vaidyanathan, A. Estimation of IMU and MARG orientation
In Proceedings of the IEEE International Conference on

using a gradient descent algorithm.
Rehabilitation Robotics, Zurich, Switzerland, 29 June–1 July 2011; pp. 1–7.

27. Alam, F.; ZhaiHe Z.; Jia, H. A Comparative Analysis of Orientation Estimation Filters using
MEMS based IMU. In Proceedings of the International Conference on Research in Science,
Engineering and Technology, Dubai, UAE, 21–22 March 2014.

28. Tian, Y.; Wei, H.; Tan, J. An adaptive-gain complementary ﬁlter for real-time human motion
tracking with MARG sensors in free-living environments. IEEE Trans. Neural Syst. Rehabil. Eng.
2013, 21, 254–264.

29. Fourati, H.; Manamanni, N.; Aﬁlal, L.; Handrich, Y. Complementary observer for body segments
motion capturing by inertial and magnetic sensors. IEEE/ASME Trans. Mechatronics 2014, 19,
149–157.

30. Yoo, T.S.; Hong, S.K.; Yoon, H.M.; Park, S. Gain-Scheduled Complementary Filter Design for a

MEMS Based Attitude and Heading Reference System. Sensors 2011, 11, 3816–3830.

31. Li, W.; Wang, J. Effective adaptive kalman ﬁlter for mems-imu/magnetometers integrated attitude

and heading reference systems. J. Navig. 2013, 66, 99–113.

32. Makni, A.; Fourati, H.; Kibangou, A.Y. Adaptive kalman ﬁlter for MEMS-IMU based attitude
estimation under external acceleration and parsimonious use of gyroscopes. In Proceedings of the
European Control Conference (ECC), Strasbourg, France, 24–27 June 2014; pp. 1379–1384.
33. Keun Lee, J.; Park, E.J.; Robinovitch, S.N. Estimation of attitude and external acceleration using
inertial sensor measurement during various dynamic conditions. IEEE Trans. Instrum. Meas. 2012,
61, 2262–2273.

34. Breckenridge, W.G. Quaternions—Proposed Standard Conventions; NASA Jet Propulsion

Laboratory, Technical Report Interofﬁce Memorandum IOM 343-79-1199; 1999.

35. De Franceschi, M.; Zardi, D. Evaluation of Cut-Off Frequency and Correction of
Filter-Induced Phase Lag and Attenuation in Eddy Covariance Analysis of Turbulence Data.
Bound.-Layer Meteorol. 2003, 108, 289–303.

36. Shoemaker, K. Animating Rotation with Quaternion Curves. In Proceedings of the Special Interest
Group on Graphics and Interactive Techniques (SIGGRAPH), 22–26 July 1985; pp. 245–254.
37. Lee, G.H.; Achtelik, M.; Fraundorfer, F.; Pollefeys, M.; Siegwart, R. A Benchmarking Tool for
MAV Visual Pose Estimation. In Proceedings of the Conference on Control, Automation, Robotics
and Vision (ICARCV), Singapore, 7–10 December 2010; pp. 1541–1546.

2015 by the authors; licensee MDPI, Basel, Switzerland. This article is an open access article
the Creative Commons Attribution license

the terms and conditions of

c
(cid:13)
distributed under
(<http://creativecommons.org/licenses/by/4.0/>).
