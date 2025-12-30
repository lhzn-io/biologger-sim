Article
Multi-Sensor Fusion for Underwater Vehicle Localization by
Augmentation of RBF Neural Network and Error-State
Kalman Filter

Nabil Shaukat 1,*

, Ahmed Ali 1

, Muhammad Javed Iqbal 1, Muhammad Moinuddin 2,3

and Pablo Otero 1

1 Oceanic Engineering Research Institute, University of Malaga, 29010 Malaga, Spain; <ahmedali@uma.es> (A.A.);

<mjavediqbal99@uma.es> (M.J.I.); <pablo.otero@uma.es> (P.O.)

2 Department of Electrical and Computer Engineering, King Abdulaziz University, Jeddah 21589, Saudi Arabia;

<mmsansari@kau.edu.sa>

3 Center of Excellence in Intelligent Engineering Systems, King Abdulaziz University,

Jeddah 21589, Saudi Arabia

* Correspondence: <nabilshaukat@uma.es>

Abstract: The Kalman ﬁlter variants extended Kalman ﬁlter (EKF) and error-state Kalman ﬁlter
(ESKF) are widely used in underwater multi-sensor fusion applications for localization and navi-
gation. Since these ﬁlters are designed by employing ﬁrst-order Taylor series approximation in the
error covariance matrix, they result in a decrease in estimation accuracy under high nonlinearity.
In order to address this problem, we proposed a novel multi-sensor fusion algorithm for underwater
vehicle localization that improves state estimation by augmentation of the radial basis function
(RBF) neural network with ESKF. In the proposed algorithm, the RBF neural network is utilized to
compensate the lack of ESKF performance by improving the innovation error term. The weights and
centers of the RBF neural network are designed by minimizing the estimation mean square error
(MSE) using the steepest descent optimization approach. To test the performance, the proposed
RBF-augmented ESKF multi-sensor fusion was compared with the conventional ESKF under three
different realistic scenarios using Monte Carlo simulations. We found that our proposed method
provides better navigation and localization results despite high nonlinearity, modeling uncertainty,
and external disturbances.

Keywords: underwater vehicle; navigation; multi-sensor fusion; localization; RBF; underwater
robotics

1. Introduction

The ocean ﬂoor has billions of dollars of natural resources in the form of precious
elements and medicinal herbs. To take advantage of ocean resources, seabed mapping is
the ultimate tool that depends on precise sensors and robust navigation fusion algorithms
for autonomous underwater vehicles (AUVs) and remotely operated underwater vehicles
(ROVs). Navigational accuracy is a key requirement for complex seabed mapping tasks [1].
However, primary sensors, three-axis gyros, and accelerometers have biases and drifts,
which vary with time and are affected by noise. In contrast, most commonly used fusion
algorithms based on extended Kalman ﬁlter (EKF) and its variant error-state Kalman
(ESKF) suffer from divergence and degraded mean square error (MSE) performance in the
nonlinear underwater condition because of linear approximation [2]. Thus, the higher the
nonlinearity present in the system, the greater the error of the EKF state prediction, and it
can also induce ﬁlter divergence.

Backpropagation multi-layer neural networks (BPNN) and radial basis neural net-
works (RBFNN) have excellent learning abilities and are well-known for their nonlinear
system identiﬁcation [3–5]. In comparison, the RBFNN has much greater accuracy of

Citation: Shaukat, N.; Ali, A.;

Javed Iqbal, M.; Moinuddin, M.;

Otero, P. Multi-Sensor Fusion for

Underwater Vehicle Localization by

Augmentation of RBF Neural

Network and Error-State Kalman

Filter. Sensors 2021, 21, 1149.

<https://doi.org/10.3390/s21041149>

Academic Editor: Jose M. Molina

Received: 1 January 2021

Accepted: 1 February 2021

Published: 6 February 2021

Publisher’s Note: MDPI stays neu-

tral with regard to jurisdictional clai-

ms in published maps and institutio-

nal afﬁliations.

Copyright: © 2021 by the authors. Li-

censee MDPI, Basel, Switzerland.

This article is an open access article

distributed under the terms and con-

ditions of the Creative Commons At-

tribution (CC BY)

license (https://

creativecommons.org/licenses/by/

4.0/).

Sensors 2021, 21, 1149. <https://doi.org/10.3390/s21041149>

<https://www.mdpi.com/journal/sensors>

sensors(cid:1)(cid:2)(cid:3)(cid:1)(cid:4)(cid:5)(cid:6)(cid:7)(cid:8)(cid:1)(cid:1)(cid:2)(cid:3)(cid:4)(cid:5)(cid:6)(cid:7)Sensors 2021, 21, 1149

2 of 26

prediction and versatility in their choice of base functions [6]. Furthermore, they have fast
convergence and less computation load compared to BPNN. These advantages of RBFNN
lead to a major research question: Can we incorporate the strengths of the RBFNN to
improve the underwater vehicle localization performance of ESKF?

1.1. State-of-the-Art Review

The basic form of an on-board navigation system on any underwater vehicle comprises
an inertial measurement unit (IMU) that can determine positions by integrating three-axis
acceleration and angular velocities [7,8]. This basic form of navigation suffers from drift,
typically 1.8 km per day to 1.5 km per hour based on the grade of IMU [7,9,10], which
makes them practically impossible to use for long missions. On top of that, most common
off-board positioning by global positing system (GPS) satellites does not work underwater
because of radio frequency attenuation [11]. Alternate communication means based on
acoustic positioning are widely used underwater, which suffers from communication uncer-
tainly and delays [12,13]. On-board aiding sensors, Doppler velocity log, pressure sensor,
and magnetometers can also help to reduce the effect of IMU drift, but all these sensors are
affected by noise. To improve the navigation accuracy and to minimize disturbance because
of noise, EKF-based algorithms are the most commonly used in underwater navigation
and localization [14–19].

On the other hand, the EKF algorithm has its shortcoming in that the accuracy of
estimation is reduced under high nonlinear system dynamics. However, many variants
of EKF have been proposed in academic research to cater to this problem [20,21]. Most of
the EKF and neural network estimation algorithms are designed for land-based vehicles.
In these approaches, when GPS data is present and valid, the neural network is trained
and, when GPS information is not available, the neural network output improves the EKF
prediction. For instance, a detailed study [22] proposed a hybrid ofﬂine trained RBFNN
with time series prediction for measurement update during GPS outage. Another study [23]
combined extreme learning machine neural network (ELM) and EKF to bridge the GPS
outage. They claimed to have a better real-time performance by improving the computation
load. In addition, some authors [24,25] also suggested using machine learning techniques to
improve localization via intelligent communication networks, but their research is limited
to land-based applications. Recently, an intelligent methodology was proposed that uses
deep learning neural networks with EKF [26]. Moreover, they claimed that, by using
recurrent neural networks (RNNs), state estimation can be improved and their model
can also work well with low-cost sensors. Nevertheless, they did not incorporate oceanic
parameters for state prediction besides the fact that RNNs have a high computational cost.
Another researcher group, in [27], used underwater model-aided dead reckoning to
improve EKF response. They calculated aided velocity using an identiﬁed surge dynamic
model. This work design reached a position accuracy of 92% during external position ﬁx
outage. However, using a model in this design makes the system difﬁcult to tune under
different sensors and working conditions because models depend on various factors such
as size, the weight of the AUV, and the physical characteristics of the sensors. The authors
of [23] proposed to embed underwater vehicle dynamic equations in the EKF and estimated
error in the navigation. This work claimed to have less computation load and better
accuracy compared to a full model integration. However, it is also dependent on the
physical parameters of the vehicle and has more implementation complexity.

Likewise, a study [28] compared underwater EKF and its statistical linearization
variant, also known as unscented Kalman ﬁlter (UKF) [29] in their project. They found that
the statistical form provides better accuracy in highly nonlinear conditions. Similar results
were found in [30]. Nonetheless, the UKF drawbacks include implementation complexity,
high computational time and cost, and round-off error [31,32].

Traditionally, the Kalman ﬁlter is used to train RBFNN [33,34] or in ofﬂine training of
the radial basis function (RBF) [35]. These methods underperform in uncertain conditions
with unmodeled dynamics. The authors of [36] introduced a forgetting factor, which is

Sensors 2021, 21, 1149

3 of 26

based on RFBNN, to improve the performance of central difference Kalman ﬁlter (CDKF)
for attitude-of-the-satellite estimation. They proposed the range of forgetting at 0.2 to 2 as
a multiplier to the Kalman gain, but limited description of the selection of the forgetting
factor was provided. Recently, the RBFNN-aided Kalman Filter was proposed to improve
the state estimation accuracy for spacecraft navigation [37]. Moreover, they did not use
multi-sensor fusion of high-rate and low-rate sensors.

1.2. Contributions of the Paper

The proposed work ﬁlls the gap by proposing a novel multi-sensor fusion architec-
ture based on the strengths of the RBF neural network and error-state Kalman ﬁlter for
underwater navigation, which has not been proposed to date to the authors’ knowledge.
We named this algorithm RBF-ESKF. The augmentation of both algorithms improves the
navigation of underwater vehicles in GPS-less environments. Our major contribution is the
derivation of a multi-sensor fusion algorithm that improves the accuracy of underwater
localization by taking advantage of a radial basis function (RBF) neural network that has
the capability of nonlinear universal approximation via recursive learning [38]. Moreover,
a simple structure of the RBF network can be trained online with less computation cost
compared to the backpropagation neural network (BPNN) [39].

The structure of this paper is organized as follows. Section 2 discusses kinematic
mathematical modeling with an ellipsoid Earth model. Section 3 discusses external and
internal sensors for underwater navigation. In addition, the mathematical models of the
sensors are described with their operating noise characteristics. The error dynamic model is
presented in Section 4. In Section 5, a multi-sensor fusion algorithm is derived for accurate
underwater integrated navigation. Section 6 shows the test results of the proposed multi-
sensor fusion ﬁlter in three different conditions. In addition, acoustic communication lost
and on-board sensor malfunctioning are tested and analyzed. Moreover, the performance
of the RBF-ESKF is compared with ESKF under different scenarios. A comparative analysis
is performed, showing that the proposed algorithm has promising results.

2. Mathematical Modeling

This section discusses the mathematical modeling of the underwater vehicle taken
from [40–44]. The ﬁrst subsection explains the notations used for modeling. The sec-
ond subsection describes the frame of references used for the mathematical formulation
of IMU. The third subsection formulates the kinematics equation of motion for six de-
grees of freedom. The last subsection provides brief information on the sensors used for
underwater navigation.

2.1. Frame of References

The importance of frame of reference transformation for underwater navigation arises
from the fact that sensors are mounted on the vehicle’s body. The origin of the body is
deﬁned as the center of body frame (b) External position ﬁxes are in a rotating, Earth-
centered, Earth-ﬁxed (ECEF) frame (e). Moreover, Newton’s laws are applicable to the
Earth-centered inertial (ECI) frame (i). However, the north-east-down (NED) frame or
navigation frame (n) is the tangent plane to the Earth’s surface at the location of the
underwater vehicle and its x-axis points toward the true north of the Earth. Figure 1 shows
a frame of references used to develop navigation equations for underwater vehicles, with
slight modiﬁcation from [40].

Sensors 2021, 21, 1149

4 of 26

Figure 1. Frames of references: ECI, ECEF, NED and Body.

2.2. Mathematical Notation

The mathematical notations used in this work are standard notations used to model
underwater vehicle position, velocity, and attitude [40]. The position and velocity are three
dimensional (3D) vectors in Euclidean space. Rotations are represented by quaternion.
Subscripts and superscripts are used to represent the relationship between the frames.
For example, ωe
ie shows an angular velocity of frame (e) with respect to (i) represented
in (e) frame. The following Table 1 shows a list of symbols used in the development of
underwater vehicle navigation equations.

Table 1. Mathematical notations for underwater vehicle kinematics.

Notation

vb [u,v,w]
Θ
nb[φ, θ, ψ]
qn
b [η, (cid:101)]
ωb [p,q,r]
pn [n, e, d]
vn [vN, vE, vD]
ωn [ωN, ωE, ωD]
pe [x, y, z]
ve [vex, vey, vez]
pe[φlat, λlong, hd]
Re
b
Ω
Ωe
Ωb
ge
gn
RM
RN
a
e

Description

Linear velocity in the body frame (surge, sway, and heave)
Attitude in Euler angles from the body to NED frame
Attitude in quaternion from the body to NED frame
Angular velocity in the body frame (roll, pitch, and yaw)
Position in the NED frame (north, east, and down)
Linear velocity in the NED frame (north, east, and down)
Angular velocity in the NED frame
Position in the ECEF frame
Linear velocity in the ECEF frame
Position in the ECEF geoid (latitude, longitude, and depth)
Rotation matrix from the body to ECEF frame
Skew symmetric matrix of the angular velocity
Skew symmetric matrix in the ECEF frame
Skew symmetric matrix in the body frame
Earth gravity vector in the ECEF frame
Earth gravity vector in the NED frame
Radius of curvature of the prime vertical of Earth
Radius of curvature of the meridian of Earth
Semi-major axis of the ellipsoidal Earth model
Eccentricity of the ellipse approximation of Earth

2.3. Navigation Equations

The underwater vehicles are most commonly equipped with a strapdown inertial
navigation system [41]. In this conﬁguration, measurements are obtained directly in the

ECI (i)EquatorPrime MeridianTrue NorthEastDOWNBODY(b)z_Inertialz_ECEFx_bodyx_ECEFx_Inertialy_Inertialy_ECEFz_bodyNED(n)Sensors 2021, 21, 1149

5 of 26

body frame and sensors experience full rotation during maneuvers. Moreover, this con-
ﬁguration requires an initial condition for position, velocity, and attitude. The kinematics
equations for the underwater vehicles used in this work are described in [42–44]. The rate
of change in position ˙pe and velocity ve of vehicle in (e) frame is related by the following
differential equation:

˙pe = ve

(1)

The rate of change in velocity ˙ve of the underwater vehicle in (e) frame is dependent
ie, and gravity vector ge in ECEF and can be

on accelerometer output f b, angular velocity ωe
expressed by the following differential equation:

˙ve = Re

b f b − 2Ωe

ieve + ge

(2)

where Ωe
that transforms a speciﬁc force vector from the (b) frame to the (e) frame.

ie is a skew symmetric matrix of angular velocity ωe

ie and Re

b is the rotation matrix

The rate of change of rotation matrix ˙Re

angular velocity Ωb
with respect to frame (i) is expressed by the following equation:

ib of the body with respect to frame (i), and angular velocity ωb

b represented in frame (e) is dependent on
ie of Earth

˙Re

b = Re

b(Ωb

ib − Ωb
ie)

(3)

The relationship between the change in latitude of the vehicle ˙φlat and velocity is

represented by the following differential equation:

˙φlat = vN/RM + hd

(4)

where RM =

a√

1−e2 sin φ

The change in longitude of the vehicle ˙λlong in the form of the east velocity is repre-

sented by following mathematical relationship:

˙λlong = vE/(RN + hd) cos φlat

(5)

where RN = RM

√

1−e2
1−e2 sin φlat

The change in height of the vehicle ˙hd is expressed in the form of the down velocity as

The latitude φlat, longitude λlong, and depth hd are given as

˙hd = −vD

φlat = tan−1

(cid:34)

(cid:112)

z/

x2 + y2

(cid:35)

1 − e2RM/(RM + hd)

λlong = tan−1[y/x]

hd =

(cid:112)

x2 + y2
cos φlat

− RM

(6)

(7)

(8)

(9)

The rate of change in velocity of the vehicle in the (n) frame ˙vn

eb is expressed by the

following differential equation:

eb = Rn
˙vn

b f b

in − (Ωn

en + 2Ωn

ie)vn

eb + gn
eb

(10)

where Ωn
respect to the (e) frame and 2Ωn

envn is the centripetal acceleration related to the motion of the (n) frame with

ievn is the Coriolis acceleration.

Sensors 2021, 21, 1149

6 of 26

The local gravity vector gn

depending on the latitude, longitude,
radius of curvature of the meridian, and radius of curvature of the prime vertical is given by

0

eb = (cid:2) 0

g (cid:3)T

gn
eb =

(cid:16)

g0
1 + hd√

RN RM

(cid:17)2

(11)

where g0 = 9.780318 × (cid:0)1 + 5.3024 × 10−3 sin2 φ − 5.9 × 10−6 sin2 2φ(cid:1) [44]. The rate of
change in the rotation matrix ˙Rn
b represented in frame (n) is dependent on the angular
velocity of the body with respect to frame (i) and on the angular velocity of frame (n) with
respect to frame (i):

˙Rn

b = Rn

b (Ωb

ib − Ωb

in)

(12)

The attitude of the vehicle is represented by quaternion. It has only one constraint
compared to the direction cosine matrix (DCM), and this method is also singularity free in
comparison to the Euler angle representation, which has a singularity problem [45].
The attitude of the vehicle represented in quaternion ˙qn

b is given as

˙qn
b =

1
2

qn
b ⊗

(cid:20) o
ωb
ib

(cid:21)

−

1
2

(cid:20) 0
ωn
in

(cid:21)

⊗ qnb

(13)

where qn
represents a quaternion product.

b has two parts: η is the scalar part; (cid:101)i is the vector part; and i = 1,2,3. The ⊗ sign

This section developed the motion equations of an underwater vehicle in starpdown
conﬁguration. The measurements from accelerometers were obtained in (b) frame as a
speciﬁc force vector and were not the true acceleration of the vehicle. To obtain the true
acceleration or rate of change in velocity of the vehicle in e frame, as shown by Equation (2),
the (b) frame speciﬁc forces are transformed into the e frame by a rotational matrix and
by compensating for the gravitation and rotation effects of the Earth. Equation (1) shows
that the rate of change in the position and acceleration has an integral relationship. Since
the position from an acoustic ﬁx is obtain in the geoid ECEF frame, for compatibility,
Equations (4)–(9) convert the position of the vehicle in latitude, longitude, and depth.
Equation (13) shows a quaternion representation of the roll, pitch, and yaw angles of
the vehicle. Interested readers can ﬁnd more details for mathematical modeling of an
underwater vehicle in starpdown conﬁguration in [40–44].

3. Sensors on the Vehicle

The following subsections give a brief overview of the sensors used in the AUV with a
mathematical formulation of errors. For detail about the mathematical model of the sensors
used for navigation, readers can refer to [40,46,47].

3.1. Inertial Measurement Unit

The inertial measurement unit (IMU) provides a three-axis accelerometer and three-
axis gyro outputs [48]. These measurements are affected by variable factors such as
temperature, manufacturing process, scale factor, noise, and drift.

The accelerometer measurement output vector f b

acc in (b) frame is modeled as

acc = f b
f b

ib + bacc + (cid:36)acc

(14)

where (cid:36)acc is white noise and bacc is acceleration bias, which is modeled as a 1st-order
Markov process.

The accelerometer bias bacc is expressed by the random walk and the random constant

shown as

˙bacc = −τ−1

acc bacc + ρacc

(15)

Sensors 2021, 21, 1149

7 of 26

where τacc is the correlation time given by the manufacturer. Its value depends on the
accelerometer sensors used in the IMU. The value ρacc depends on standard deviation,
and it is known as a process driving noise.

The accelerometer in IMU does not directly measure the true kinematic acceleration
of vehicles due to the presence of Earth’s gravitation. For that reason, the measurement
from the accelerometer is known as the relative acceleration or speciﬁc force f b
ib and it is
related to the kinematics acceleration of the vehicle as follows:

ib = ˙Rb
f b

i ¨pi − gb

(16)

where ¨pi is acceleration represented in an inertial frame and gb is gravitation sensed by the
accelerometer in the body frame.

The actual output of the gyro ωb

g is inﬂuenced by noise and bias that is given by

ωb

g = ωb

ib + bg + (cid:36)g

(17)

where (cid:36)g is the white noise and bg is the gyro bias, which is modeled as a 1st-order
Markov process.

The gyro bias bg is represented by a random walk and a random constant given as

follows:

˙bg = −τ−1

g bg + ρg

(18)

where τg is the gyro correlation time obtained from manufacturer documentation. Its
value depends on the quality of the accelerometer sensors used in the IMU. The value
ρg depends on thte standard deviation, and it is called process driving noise. The IMU
used for simulation is tactical grade Emcore SDI-1500. It uses high-precision micro-electro-
mechanical systems (MEMS) quartz sensor technology with 1◦/h gyro bias and 1 mg
accelerometer bias stability. The IMU offers the best cost to performance ratio compared to
other technologies. It consists of three orthogonal accelerometer sensors that provide the
measurement of speciﬁc forces. Three gyros provide the angular rates of the body with
respect to the inertial frame of reference.

3.2. Underwater Acoustic Positing System

The underwater acoustic positing system measures the distance and direction of the
vehicle from the reference positions. For this work, HiPaP 502 is used for simulation. This
system provides a typical range detection accuracy of 0.2 m, with an operating range of
1 to 5000 m. It has an acoustic operating area of 200◦/200◦ with the capability of narrow
beamforming of 10◦, which improves the signal-to-noise ratio. It can be interfaced by
GPS to provide Earth-related coordinates. However, acoustic position estimate is effected
by GPS accuracy, system installation, ship attitude, sound velocity proﬁle, ray bending,
and measurement noise.

Assuming the system is precisely calibrated, installation and ship attitude have negli-

gible effects. The mathematical model of the system actual output ˆp is given as

ˆph = ph + bh + (cid:36)h

(19)

where ph is true output position, whereas bh is the time-varying bias modeled as a 1st-order
Markov process and depends on the sound velocity proﬁle and ray bending effect. (cid:36)h
represents measurement white noise.

3.3. Doppler Velocity Log

The Doppler velocity log (DVL) measures the change in acoustic frequency for de-
termining the speed of the vehicle with reference to the seabed. In deep water, when
the seabed is not available, the DVL measures the speed with respect to water. The DVL
sends a known frequency signal to the seabed and receives the signal that bounces back
to the vehicle. The speed of the underwater vehicle is a dependent doppler effect [49].

Sensors 2021, 21, 1149

8 of 26

The work used Nortek DVL-500, which has a range of 0.3 to 200 m and long-term accuracy
of ±0.1% ±0.1 cm/s. The DVL can be operated in a 4-beam Janus conﬁguration complete
performance testing of DVL; readers may refer to [50].

Considering that the attitude and installation error are negligible, the actual output of
DVL ˆvdvl can be modeled for the true velocity measurement vector, noise, and bias given
as [51].

ˆvdvl = vdvl + bdvl + (cid:36)dvl

(20)

where vdvl is the true output and random velocity error, bdvl is modeled as the 1st-order
Markov process, and (cid:36)dvl is white noise.

3.4. Depth Sensor

Depth and underwater pressure have a direct relationship [52]. As the vehicle goes
deep into water, the pressure reading increases linearly. The depth sensor modeled in this
work is from Paroscientiﬁc, Inc. part number 8CDP700-I, which provides an accuracy of
0.01% and high stability under tough conditions.

The depth sensor actual output ˆhd is modeled by adding true depth hd with noise:

ˆhd = hd + (cid:36)d

(21)

where (cid:36)d is measurement noises modeled as white noise.

3.5. Magnetometer

The magnetometer or compass measures the magnitude and direction of Earth’s
magnetic ﬁeld [53]. The magnetometer used in the work is jewel instrument ECS-AC-
RS232 e-compass, which has a 3-axis magnetometer and a 2-axis tilt sensor. The tilt sensor
is used for the initialization of roll and pitch [40]. It offers an accuracy of ±0.5◦ root mean
square RMS, a repeatability of ±0.3◦, and a response time of 36 milliseconds. The pitch
and roll are ±42◦ whereas the dip angle range ±80◦. The major error sources of the
magnetometer include the declination angle, which is the difference between true north
and sensor north; the hard and soft magnetic distortion due to motors and ferromagnetic
materials [54]; and sensor imperfection, misalignment, and noise. However, with proper
calibration, most of the errors in measurement can be removed.

The actual output qm of the magnetometer is a combination of noise and true output

qm written as

ˆqm = qm ⊗ (cid:36)m

(22)

where (cid:36)m is the sensor noise modeled as white noise.

4. Error Dynamic Model

The position p, velocity v, attitude q, gyro bias bg , accelerometer bias bacc, and

acoustic ﬁx bias bh in full state vector x form are given as

x = (cid:2) p v q bg bacc bh

(cid:3)T

sv

(23)

where sv is the sound velocity model underwater used to calculation underwater acous-
tic transmission.

The estimated state vector ˆx is written as

ˆx = (cid:2)

ˆp

ˆv

ˆq

ˆbg

ˆbacc

ˆbh

ˆsv

(cid:3)T

(24)

The design used in this worked estimate an error-state vector, which offers the main
advantages of ﬂexible sampling rate, robustness, and low computation burden [55,56]. The
error-state vector δ ˙x is the difference between the true state and estimated state ˙ˆx of the
model and is given as

δx = x − ˆx

(25)

Sensors 2021, 21, 1149

9 of 26

The error-state vector can be represented as

δx = (cid:2) δp δv δq δbg

δbacc

δbh

δsv

(cid:3)T

(26)

where the position, velocity, and attitude error equations are provided as under. For com-
plete derivation of this error model, readers can refer to [42,57].

Assuming that the underwater vehicle travel at low speed and that the depth of
operation is much less than the Earth’s radius, the rate of change in errors in longitude
˙λlong,latitude δ ˙φlat, and depth δ ˙hd are given by
δ





δ ˙λlong
δ ˙φlat
δ ˙hd


 =







0
ve sin(λlong)
(RN +hd) cos2(λlong)
0

0

0

0






+

1
RM+hd
0

0

−vn
(RN +hd)2
−ve
(RN +hd)2 cos(λlong)
0











δλlong
δφlat
δhd

0
1
(RN +h) cos(λlong)
0










0
0
−1

δvn
δve
δvd









The velocity error δ ˙vn

eb is given by the following differential equation:

δ ˙vn

eb =δgn

eb + δRn

b f b

acc + Rn

b δ f b

ib − (2(δΩn

ie) + (δΩn

en)) ˆvn

eb − (2(Ωn

ie) + (Ωn

en))δvn
eb

(27)

(28)

If the vehicle operates at low speed underwater, angler velocity ωn

ie can be
neglected. Gravity error is also neglected because of the small operating area and accurate
estimation [44,58].

ie and δωn

Thus, the velocity error δ ˙vn

eb differential equation can be re- written as

δ ˙vn

eb = δRn

b f b

acc + Rn

b δ f b
ib

(29)

Assuming that the angular velocity of rotation of Earth with respect to the inertial
frame ωie is accurately known, using the attitude error model in the form of the quaternion,
it is given as

˙δq =

1
2

δωb

ib +

1
2

The error of gyro bias δ ˙bg is given as

(cid:16)

(cid:17)

δq

δΩb
ib

δ ˙bg = ˙bg − ˙ˆbg

The error of accelerometer bias δbacc is given as

δbacc = ˙bacc − ˙ˆbacc

The error of hydro-acoustic system bias δbacc is given as

δbh = ˙bh − ˙ˆbh

(30)

(31)

(32)

(33)

Since the ESKF employed in this work used an error-state or indirect-form-state vector
z, it is obtained by subtracting the outputs of the inertial measurement unit (INS) and
aiding sensors measurement [59].

The position error δzp between the INS position pI NS and acoustic position system

measurement ph is written as

δzp = pI NS − ph

(34)

Sensors 2021, 21, 1149

10 of 26

The velocity error δzv between the INS velocity vI NS and DVL measurement vd is

given by the following equation:

δzv = vI NS − vd

(35)

The attitude error δzv between the INS attitude qI NS and magnetometer measurement
qm is not a vector quantity; it cannot be subtracted as position and velocity. Quaternion
multiplication ⊗ is used to ﬁnd the error term as follows:

δzq = q−1

m ⊗ qI NS

(36)

5. RBF-ESKF Mulit-Sensor Fusion

The proposed modiﬁcations improve ESKF performance and make use of the advan-
tages of the RBF neural network. The RBF neural network can approximate any nonlinear
function, and they are also known as universal function approximators [60]. The RBF center,
its width, and the linear weights for each output neuron are altered at every iteration of a
learning algorithm. When each RBF center is as close to the input vector as possible and the
network output error is within the target limit, the training phase is completed. Therefore,
it is possible to express the approximation of any functional dependency between variables
as a linear combination of a best possible number of RBF neurons with appropriate weight
and center. The top level block diagram of our proposed fusion algorithm is depicted in
Figure 2.

Figure 2. Top level diagram of the RBF-ESKF multi-sensor fusion navigation architecture.

As shown by Figure 2, the algorithm takes the error of the aiding sensors and INS as
input. The RBF-ESKF fusion algorithm after processing gives an output to INS for error
correction and reset. The RBF neural network used for processing has a basic three layer
structure; input, hidden, and output layer. Furthermore, compared to BPNN, the RBF
variants have less computational load and fast online learning. The ﬁrst layer is the input
layer, which provides an interface between the data and neural network. The data from the

ΣINSDVLΣΣΣIMUPositionVelocityAttitudeDepthPressure sensorCompass----Corrected Full StateEstimated Error Error CorrectionAccGyroRBF-ESKF Multi-Sensor FusionAcoustic fixPosition errorVelocityerrorAttitude errorDepth errorSensors 2021, 21, 1149

11 of 26

input layer to the second hidden layer is transferred in such a manner that the output value
of every hidden neuron is inversely related to the Euclidean distance from that neuron’s
input vector to the RBF neuron’s center. The third layer is the output layer, which takes
into account the cumulative weights and biases of all RBF neuron outputs.

Several variants of RBF exist in literature that depend on the application [61]. However,
in this work, we used the Gaussian-type RBF function. The weights of neurons in the
hidden layer for the Gaussian RBF function indicate the center of the symmetrical Gaussian
distribution curve. The novelty of the RBF-ESKF algorithm is that it includes system
information within the weight and center learning update rules.

5.1. RBF-ESKF Mathematical Formulation

The underwater vehicle navigation system has nonlinear dynamics and measure-
ment characteristics, which can be represented in state space form by Equation (37) and
Equation (38) [40]

˙x(t) = f (x(t), u(t), t) + α(t)

(37)

where the state of the system is represented by ˙x(t). The u(t) is a known system input and
α(t) is Gaussian white noise.

The measurement output z(t) in state space can be written as

z(t) = h(x(t), t) + β(t)

(38)

where f and h are nonlinear functions. The measurement is corrupted by Gaussian white
noise β(t).

Dropping time and noise in the above equations for simpliﬁcation, the linear form of

error state can represented by Equation (39) and Equation (40): [40]

δ ˙x = F( ˆx, u, t)δx

(39)

where F( ˆx, u, t) = ∂ f
∂x

(cid:12)
(cid:12)
(cid:12)x= ˆx

However because the deterministic component F( ˆx, u, t), is always incomplete, which
means the model does not incorporate, for instance, AUV underwater movements due to
waves, the stochastic component α(t) takes these effects into account.

The linear residual measurement output δz can represented by

where H( ˆx, t) = ∂h
∂x
ics equations.

(cid:12)
(cid:12)
(cid:12)x= ˆx

δz = H( ˆx, t)δx

(40)

, ˆx is deﬁned as the trajectory obtained by using vehicle kinemat-

The Kalman ﬁlter [62], in its basic form, is based on linear system and measurement
models, which in reality might not be the case. In our underwater vehicle, navigation
equations are used to construct the mathematical model and are not linear with respect to
the state variables. This is done by linearization of any predicted trajectory, leading to an
error-state model as discussed in Section 4. This linear approximation was proven to be
incomplete and requires special consideration in underwater navigation, which leads to
derivation of the RBF-ESKF algorithm.

For mathematical formulation of RBF-ESKF, we start with ESKF implementation,
which utilizes deﬁnitions of measurement error and state dynamics error, as described by
the Equations (39) and (40) [63]. The ESKF algorithm has three major components. The
ﬁrst component is initialization, in which state, covariance, process, and measurement
covariance are initialized [64].

x−
0 = Initialization of the state variables.
P−
0 = Initialization covariance matrix.

Sensors 2021, 21, 1149

12 of 26

Q0 = Initialization process noise covariance.
R0 = Initialization of measurement noise covariance.

where superscript minus − denotes the a priori state that occurs before innovation is
updated. Superscript plus + denotes the posteriori state after innovation calculation.

The second component is time update, in which the error state and error-state covari-

ance are updated, give by

δx−

k+1 = Φ

kδx−
k

(41)

where δx−

k+1 is the predicted error state and Φ

k is the state transition matrix in discrete form.

P−
k+1 = Φ

kP+
k

Φ(cid:62)

k + Qk

(42)

where P−

k+1 is the predicted error covariance and Qk is the process noise covariance vk.
The third component is measurement update, in which the residual of measurement
is updated. The residual of measurement δzk is given by the difference between the actual
measurement zk and the prediction of measurement h( ˆxk)

δzk = zk − h( ˆxk)

The kalman Kk gain is given as

Kk = P−

k H(cid:62)

k

(cid:16)

HkP−

k H(cid:62)

k + Rk

(cid:17)−1

The posteriori error estimate δx+

k is given as

δx+

k = δx−

k + Kk

(cid:0)δzk − Hkδx−

k

(cid:1)

(43)

(44)

(45)

The expression (cid:0)δzk − Hkδx−

(cid:1) is referred to as innovation. It is the difference between

k
the error of observation and its expected error,represented by sk as

sk = δzk − Hkδx−
k

The posteriori error-state covariance P+
k

is given as

k = (I − Kk Hk)P−
P+

k

(46)

(47)

The complete corrected navigation state ˆx+

estimate from Equation (6) and prior full state estimate ˆx−

k as

k can be written as the sum of the error

k = ˆx−
ˆx+

k + δx+

k

(48)

The major assumption for obtaining proper results from ESKF is that the time in-
terval should be short for error calculation and nonlinearity should not be dominant in
the calculation of the innovation term. To compensate the effect of nonlinearity in the
innovation Equation (46), we propose to modify it by incorporating an RBF neural network.
The modiﬁed innovation term ˜sk is given as

˜sk = sk − Wkyk

(49)

where the term Wkyk is the output of the RBF neural network. The term yk is the output
of the hidden layer of the RBF neural network and Wk is the weight matrix that provides
the link between output and hidden layers of RBF neural network. These weights can be
designed by minimizing the the mean square error (MSE) cost function J, deﬁned by

J = (cid:107)sk − Wkyk(cid:107)2

(50)

Sensors 2021, 21, 1149

13 of 26

To improve the estimation of multi-sensor fusion under nonlinear conditions, the

Gaussian RBF function utilize an a priori error-state estimate, which is given as

(cid:32)

yk(i) = exp

−

(cid:33)

2

(cid:13)
(cid:13)

(cid:13)
(cid:13)δx−

k − cik
2σ2
i

,

i = 1, 2, . . . , Nc

(51)

where cik is the neuron center and σi is the width of the Gaussian RBF function. The weights
of the neurons in matrix form wk are represented as








Wk =

w1k(1) w1k(2)
w2k(1) w2k(2)

...

...

wMk(1) wMk(2)

· · · w1k(Nc)
· · · w2k(Nc)
. . .
· · · wMk(Nc)

...








where M donates the size of the state vector and Nc represents the number of neuron
centers. The size of Wk is M × Nc. The size of Wkyk is M × 1, and the size of yk is Nc × 1.

5.2. Derivation of Weight Update of RBF-ESKF

For the weight matrix Wk, we only consider weight associated with the mth-speciﬁc
output. Thus, the weight vector of the mth output of RBF can be denoted by wmk. Therefore,
the weight update rule of the speciﬁc mth output is given as

wmk+1 = wmk − ηw

1
2

∂J
∂wmk

(52)

where ηw is the learning rate, and its value is selected by experimentation. Too small a
value of ηw can cause unsuitability, and too large a value can make the response sluggish.
A gradient descent method, namely the steepest decent, is used to minimize the cost
function J relative to the RBF neural network weight. By using Equation (50), the gradient
of cost function can be written as

∂J
∂wmk

=

∂(cid:107)sk − Wkyk(cid:107)2
∂wmk

The result of the derivative is given as

∂J
∂wmk

= −2(δzk(m) − Hk(m)δx−

k (m) − wmkyk)yT

k

(53)

(54)

Thus, putting Equation (54) in Equation (52), we get the complete weight update equation:

wmk+1 = wmk + ηw(δzk(m) − Hk(m)δx−

k (m) − wmkyk)yT

k

5.3. Derivation of Center Update of RBF-ESKF

The center update rule for the jth element of the mth neuron center is given as

cik+1(j) = cik(j) − ηc

1
2

∂J
∂cik(j)

(55)

(56)

where ηc is the learning rate of center update. It is determined experimentally. By apply-
ing the steepest descent method, we minimized cost function J with respect to weight.
The result of derivative is shown in the following equation:

∂J
∂cik(j)

= −2

M
∑
i=1

(sk(m) + wmkyk) · (

wmk(i)yk(i)(δx−
σ2
i

k (j) − cik(j))

)

(57)

Sensors 2021, 21, 1149

14 of 26

Plugging Equation (57) into Equation (56), the new center update equation becomes

cik+1(j) = cik(j) + ηc

M
∑
i=1

(sk(m) + wmkyk) · (

wmk(i)yk(i)(δx−
σ2
i

k (j) − cik(j))

)

(58)

It is evident from the weight update Equation (55) and center update Equation (58)
that our algorithm uses system information to train the RBF neural network to overcome
the drawbacks of ESKF.

The complementary form block diagram representation of the RBF-ESKF fusion algo-
rithm is shown in Figure 3. The vehicle kinematics combined with IMU high-rate sensors of
IMU provide the estimated output. This estimated output is then subtracted from low-rate
sensors and fed into RBF-ESKF. RBF and ESKF work together to ﬁnd the best error estimate,
which is then added into the underwater vehicle kinematics in feed-forward fashion to
obtain the total state.

Figure 3. Complementary form representation of RBF-ESKF.

Algorithm 1 shows iterative steps of the proposed method. The term ˜sk is RBF
modiﬁed innovation term used by RBF-ESKF to improve accuracy of ﬁlter in highly non-
linear conditions.

ESKFRBFNNHigh rate sensors (IMU)Underwater Vehicle Kinematics Low rate aiding  sensorsΣ+-Estimated outputCorrected outputerrorRBF outputSensors outputEstimated errorSensors 2021, 21, 1149

15 of 26

Algorithm 1 RBF-ESKF multi-sensor fusion for underwater navigation

Initialization:

1: Initialize ESKF variables x−
2: Initialize RBF variables w,
Kalman gain update:

0 , P−
0 , Q0, R0
0c0, σ0, ηw, ηc

3: calculate Kalman gain

Kk = P−

k H(cid:62)

k

(cid:16)

HkP−

k H(cid:62)

k + Rk

(cid:17)−1

RBF Gaussian function update:

4: Learning non-linearity of error state vector

(cid:32)

yk(i) = exp

−

2

(cid:33)

(cid:13)
(cid:13)

(cid:13)
(cid:13)δx−

k − cik
2σ2
i

,

i = 1, 2, . . . , Nc

Innovation update:

5: Non-linearity inﬂuence is minimized by using output of RBF neural network in innovation term

˜sk = δzk − (Hkδx−

k + Wkyk)

Measurement update:

6: Estimate error state by using innovation term and Kalman gain

δx+

k = δx−

k + Kk ˜sk

7: Error state covariance update.

k = (I − Kk Hk)P−
P+

k

Full State correction

8: Full state is corrected by error adding error estimate.

x = ˆx + δx+
k

RBF Neural Network Weight and Center update:

9: RBF weight update

wmk+1 = wmk + ηw(δzk(m) − Hk(m)δx−

k (m) − wmkyk)yT

k

10: RBF center update

cmk+1(j) = cik(j) + ηc(

wik(j)yk(j)cik(j)
σ2
i

)

.

M
∑
i=1

(δzk(i) − (Hk(i)δx−

k (i) + wikyk))

Time propagation:

11: Time propagation of error state and covariance

δx−

k+1

= Φ

kδx+
k

P−
k+1

= Φ

kP+
k

Φ(cid:62)

k + Qk

12: Next iteration (posterior becomes prior)

Sensors 2021, 21, 1149

16 of 26

5.4. Complexity of RBF-ESKF

The proposed algorithm uses RBFNN to enhance the performance of underwater
vehicle localization with a slight increased in time and space complexity compared to ESKF
due to matrix multiplications. Compared to BPNN and deep learning neural networks,
RBFNN has less complexity because of its simple three-layer structure because the time and
memory space complexity of the neural networks is directly related to the structure and
number of layers. However, faster matrix multiplication algorithms such as the Strassen
algorithm [65] can be used to decrease execution time. Table 2 shows the structure of the
RBFNN used in this work.

Table 2. RBF neural network structure with a Gaussian activation function.

RBFNN

Input layer neurons
Hidden layer neurons
output layer neurons
Learning rate of weights
Learning rate of centers

Numbers

20
50
20
0.001
0.001

6. Results and Discussion

In order to compare performances, the proposed algorithm and ESKF were simulated
in three different realistic scenarios. As the ESKF structure was modiﬁed by RBF in our
fusion algorithm, low-level functions were written for simulation. The noise speciﬁcations
of the sensors used in this work are comparable to their datasheets. The main purpose of the
simulation was to compare the maximum error (max) and root means square error (RMSE)
of position, velocity, and attitude. Practical failure mode tests cases were developed and
simulated with DVL and acoustic positioning loss of measurements for a short duration.
The simulation results were compared with conventional ESKF for performance evaluation.
Furthermore, for simulation, the assumption was made that underwater vehicles can move
in any direction and with any roll, pitch, and yaw angle. A reference trajectory of the
vehicle was generated by angular velocities and acceleration.

To consider the effects of random variations in the accuracy of the fusion algorithms,
a Monte Carlo simulation was used. The test consisted of 100 runs. Two ﬁlters processed
the same data during the test to ensure a fair contrast. For all three cases, the same RBF
neural network structure was used, as listed in Table 2. For the simulation, the RBF weights,
centers, and sigma were initialized randomly.

6.1. Test Case 1: Normal Working Condition

In the ﬁrst case, the vehicle was considered to be working in a normal operating mode
without any on-board and off-board sensor failure. To simulate a real situation, the noise
and drift characteristics of the sensors used for simulation were almost the same as listed
in the manufacturer’s documentation stated under Section 3. Both ESKF and RBF-ESKF
were tested on the same operating conditions. The performances of ESKF and RBF-ESKF
are compared side by side in Table 3.

From the results of the north position prediction displayed in Table 3, it can be
observed that ESKF has an almost three times higher maximum error than that of the
RBF-ESKF. Furthermore, for the east position, the ESKF maximum error was twice as high
as the RBF-ESKF. In the case of maximum error in the prediction of depth, the performance
of the two ﬁlters are approximately identical. The RBF-ESKF RMSE for position estimation
was even better, almost twice as high. Signiﬁcant improvement was seen in the north,
where it were three times higher than the one achieved by the ESKF. Overall, the RMSE
sum for the RBF-ESKF position estimate was approximately two times better than that of
the ESKF.

Sensors 2021, 21, 1149

17 of 26

The estimation of velocity showed considerable improvement compared to the ESKF.
The overall northern velocity error was almost double than that of the ESKF compared
to the RBF-ESKF. Small but noticeable improvements were seen in the maximum error
for east and depth velocities. The RMSE of the RBF-ESKF was roughly two times better
than the ESKF for the north, east, and down velocities. Overall, with our proposed fusion
algorithm, the sum of all RMSE states was almost three times better than ESKF.

Table 3. ESKF and RBF-ESKF results with all sensors working in normal condition by running
100 Monte Carlo simulations.

North Position Max error
East Position Max error
Down Position Max error
North Position RMSE
East Position RMSE
Down Position RMSE
Sum Position RMSE
North Velocity Max error
East Velocity Max error
Down Velocity Max error
North Velocity RMSE
East Velocity RMSE
Down Velocity RMSE
Sum Velocity RMSE
Roll Max error
Pitch Max error
Yaw Max error
Roll RMSE
Pitch RMSE
Yaw RMSE
Sum Attitude RMSE

ESKF

1.1509
0.8218
0.0081786
0.446124
0.3122
0.0040719
0.76239
0.038185
0.0045943
0.0032507
0.039455
0.033652
0.0035526
0.0766596
0.13268
0.1809
0.46624
0.00039554
0.00055597
0.00049874
0.00145025

RBF-ESKF

0.32578
0.45685
0.0071222
0.1464
0.1844
0.002709
0.333509
0.01844
0.0037403
0.0022476
0.011407
0.012919
0.020227
0.0263487
0.060874
0.16171
0.36001
0.00019122
0.00036354
0.00035049
0.00122578

Overall, in terms of attitude, relative to ESKF, the sum of all state RMSEs improved

signiﬁcantly by about double as much.

Figure 4 shows the 2D and 3D trajectories. It can be seen that the trajectory is not linear.
The position, velocity, and attitude errors are estimated on this trajectory. The star symbol
in the 2D trajectory shows an acoustic ﬁx from the external source. The performances of
these ESKF and ESKF-RBF were evaluated by how close the estimated path was to the
actual value.

(a)

(b)

Figure 4. (a) A comparison of the 2D trajectory of an underwater vehicle in the east and north
directions and (b) a comparison of the 3D trajectory of an underwater vehicle.

6000 5000 4000 ...... §. 30002000 z 1000 0 -1000-500 Position --- Real Position --- RBF-ESKF Estimated position ◊ Accoustic Fix--- - ESKF Estimated position50 East [m] 2300 2200 ......... , ............... , ... , . :i !: !JJ::!:::::::I:EE:i::r::i T ·l I t·•t"'l"t"r••J••l"l"l"l•·l••J •I I ............ , .... , .................... . ·; ;: c::t::c::�::c:·;::i::j::;::;:·;;:;::i::i. •· ................................... .. .. •··• ................................ .: •· !::! :!::!: ... : :::::::::::·.:::!:::::: : •· ,. . . : : : : : '.: :: . '. ": ..... � -� •·. ': ! : :i : . : .. : . ; ' ' ; ' : .. � . ; .. ' ' ; . ; .. � . ; . ; ' ' ; I· l••C ·I ·I· 1··1 ·I ·1··1· 1··1 ·I ·I ·I .................. ,,,, ......... ,, ;. , .. , ., .;. ; .. ; .; ,; I• I•·).;,; I 55 60 65 100 150 Sensors 2021, 21, 1149

18 of 26

Figure 5 shows comparison of ESKF and RBF-ESKF estimated the position, velocity

and attitude.

(a)

(c)

(e)

(b)

(d)

(f)

Figure 5. Simulation results of ESKF and RBF-ESKF for time 0–2500 s (x-axis) in case 1. (a,b) The
RBF-ESKF estimation for the east positions and depth error is close to the actual error value. (c,d)
Error velocity for down and north. (e,f) Euler angle errors for roll and pitch. It is evident from
(c–f) that ESKF has an oscillatory response that contributes to compromised accuracy compared
to RBF-ESKF.

6.2. Test Case 2: Acoustic Fix Not Available

In this case, the robustness of the multi-sensor fusion algorithm was tested by sim-
ulating the loss of the underwater acoustic ﬁx for a short period. The unavailability of
the position information from acoustic ﬁx mostly inﬂuenced the position estimate of both
ﬁlters, predominantly ESKF. In this case, the position estimate was only available from the
integration of the DVL velocity, which compensated the acoustic ﬁx loss effect and reduced
the drift error. The detailed comparison is shown in Table 4.

5 4 3 2 1ii 1 0 -1-2I -30 500 Position Error East --- Real North Position error --- RBF-ESKF Estimated North Position error 1000 ESKF Estimated North Position error 1500 1500 15 0 1540 2000 2500 Depth Error 1.5 ----------------------------------� 1 '.[ 0.5 :2 :i:' 0.. 0 -0.5-10 500 --- Real Depth error --- RBF-ESKF Estimated Depth Position error --- ESKF Estimated Depth Position error 1000 1500 2000 2500 0.06 0.04 0.02 � 0 ·c:;0 -0.020 -0.04-0.06-0.080 500 Down Error velocity --- Real Velocity error --- RBF-ESKF Estimated Velocity error --- ESKF Estimated Velocity error 1790 1791 1792 1793 1000 1500 2000 2500 0.6 0.5 ...... 0.4 >, :t::: 0.3 0.2 J: t: 0 z 0.1 0 -0.10 500 North Error velocity 1000 --- Real Velocity error --- RBF-ESKF Estimated Velocity error --- ESKF Estimated Velocity error 1500 1439 1440 1441 2000 2500 Estimated (J Error 3-----------------------------� 2 ---Real INS 0 error ---RBF-ESKF Estimated 0 error --- ESKF Estimated 0 error 1 -10.02 0.01 0 -2-0.011200 1220 1240 -30 500 1000 1500 2000 2500 Sensors 2021, 21, 1149

19 of 26

Table 4. Performance Comparison of ESKF and RBF-ESKF with loss of acoustic ﬁx for a short period
by running 100 Monte Carlo simulations.

North Position Max error
East Position Max error
Down Position Max error
North Position RMSE
East Position RMSE
Down Position RMSE
Sum Position RMSE
North Velocity Max error
East Velocity Max error
Down Velocity Max error
North Velocity RMSE
East Velocity RMSE
Down Velocity RMSE
Sum Velocity RMSE
Roll Max error
Pitch Max error
Yaw Max error
Roll RMSE
Pitch RMSE
Yaw RMSE
Sum Attitude RMSE

ESKF

5.2115
1.4275
0.033167
0.94036
0.66511
0.005613
1.611083
0.040376
0.0036513
0.0061216
0.0439324
0.065722
0.0065451
0.1161995
0.2567
0.41582
0.5494
0.0006135
0.00052358
0.00051363
0.00169071

RBF-ESKF

1.3849
0.4663
0.016192
0.50629
0.40109
0.0039411
0.9113211
0.029489
0.0030517
0.0036592
0.21818
0.035722
0.0039131
0.0614531
0.1231
0.19178
0.46001
0.00020485
0.00011917
0.0003413
0.00117532

It can be noted from Table 4 that the maximum error of RBF-ESKF was almost ﬁve
times better for the north and east directions as compared to ESKF. The down position
estimate was also two times better than that of ESKF. The overall RMSE in all three
directions is considerably improved by almost one and a half times that of ESKF. Overall,
compared to normal working conditions, the position accuracy had a detrimental effect,
but RBF-ESKF has proven to be more robust.

In contrast to standard operating conditions, the velocity estimation was marginally
inﬂuenced by acoustic ﬁx unavailability. The maximum ESKF error was worse than that
of RBF-ESKF for velocity in all directions. For RBF-ESKF, the RMSE of velocity was
signiﬁcantly better by almost two times that for ESKF. Overall, with our proposed method
of fusion, the sum of all RMSE velocity states was almost two times better than ESKF.

For RBF-ESKF, the RMSE of the roll, pitch, and yaw angles were substantially better
by about one and a half times that of ESKF. The maximum roll, pitch, and yaw angle errors
were two times better for RBF-ESKF. Overall, the sum of all state for RBF-ESKF was better
than that for ESKF.

Figure 6 below illustrates a comparison of the position and velocity errors when
acoustic ﬁx was not available for a short period from 1500 to 1700 s. The performances
of ESKF and ESKF-RBF were evaluated on similar trajectory. Moreover, the RBF-EKF is
consistent in the estimation and is close to the actual value.

Sensors 2021, 21, 1149

20 of 26

(a)

(b)

(c)

(d)

(e)

(f)

Figure 6. Simulation results of ESKF and RBF-ESKF for time 0–3000 s (x-axis) in case 2. (a–c) The
position error signiﬁcantly grows with a loss of acoustic ﬁx. The proposed algorithm estimation is
close to the actual error. (d–f) RBF-EKF has a minimal effect of acoustic ﬁx loss on velocity estimation,
and the response is much smoother than that of ESKF.

6.3. Test Case 3: DVL Unavailable

In this case, the robustness of both ﬁlters was tested when DVL was not available for
a short duration. The velocity estimate had a larger inﬂuence than the position estimate
because, when DVL was not available, it was calculated by taking the derivative of the
position measurement, which suffers from noise ampliﬁcation from the differentiation
process. Moreover, acoustic ﬁx measurement bias was negatively inﬂuenced by DVL
measurements that contribute to increasing the position error. Table 5 compares the
performance robustness multi-sensor fusion algorithm with DVL failure.

It can be observed from the above data that position estimate in this case was better
than case 2 but slightly less accurate than normal working conditions. However, in the
north direction, ESKF maximum error was almost two times worse and almost one and a
half times worse for east and depth. Furthermore, the RBF-ESKF RMSE for the position
was notably better than that for ESKF by around one and a half times in all directions.
Thus, the position of estimation for the overall mission was improved in all directions by
the RBF-ESKF algorithm.

050010001500200025003000-5051015North [m]Position Error NorthReal North Position errorRBF-ESKF Estimated North Position errorESKF Estimated North Position error1500160017000510050010001500200025003000-50510152025303540East [m]Position Error EastReal North Position errorRBF-ESKF Estimated North Position errorESKF Estimated North Position error160017001800102030050010001500200025003000-4-3-2-1012Depth(h) [m]Depth ErrorReal Depth errorRBF-ESKF Estimated Depth Position errorESKF Estimated Depth Position error150016001700-3-2-10050010001500200025003000-0.500.511.52North [m/s]VelocityReal North velocityRBF-ESKF North Estimated velocityESKF North Estimated velocity14141416141814201.8951.91.9051.911.915050010001500200025003000-0.500.511.522.5East [m/s]East VelocityReal East velocityRBF-ESKF East Estimated velocityESKF East Estimated velocity149614981500150215041.411.4151.421.4251.43050010001500200025003000-0.200.20.40.60.811.21.41.61.8Down [m/s]Down VelocityReal Down velocityRBF-ESKF Down Estimated velocityESKF Down Estimated velocity14921493149414951.571.581.591.6Sensors 2021, 21, 1149

21 of 26

The velocity estimation without DVL was less accurate compared to case 1 and case
2. However, the overall results of our method are much better than those of ESKF, which
were almost doubly improved with respect to the maximal error and RMSE. In addition,
the sum of all estimated velocity states from RBF-ESKF in all directions was approximately
two times better than that of ESKF. Hence, the RBF-ESKF velocity estimation was more
robust than that of ESKF. The RBF-ESKF attitude estimation of the roll, pitch, and yaw
angles had a lower maximum estimation error. Moreover, the RMSE for RBF-ESKF showed
considerable improvement. Overall, the sum of all estimated attitude states was one and
half times better than that of ESKF.

Table 5. Performance comparison of ESKF and RBF-ESKF with the Doppler velocity log (DVL)
measurement unavailable for a short duration by running 100 Monte Carlo simulations.

North Position Max error
East Position Max error
Down Position Max error
North Position RMS error
East Position RMS error
Down Position RMS error
Sum Position RMS error
North Velocity Max error
East Velocity Max error
Down Velocity Max error
North Velocity RMS error
East Velocity RMS error
Down Velocity RMS error
Sum Velocity RMS error
Roll Max error
Pitch Max error
Yaw Max error
Roll RMSE
Pitch RMSE
Yaw RMSE
Sum Attitude RMSE

ESKF

1.9455
0.91649
0.0084106
0.669324
0.53722
0.0049455
1.2114895
0.105751
0.099018
0.0178454
0.191296
0.15337
0.0092455
0.3539115
0.29935
0.51906
0.66041
0.00066481
0.00060017
0.00062205
0.00188703

RBF-ESKF

0.90707
0.63511
0.0072865
0.41818
0.30722
0.0035131
0.7289131
0.051603
0.061305
0.00897
0.09809
0.079982
0.005387
0.183459
0.171758
0.210442
0.42246
0.000450075
0.00042717
0.000422102
0.001299347

Figure 7 below shows comparison velocity errors and velocity when the DVL mea-
surement was not available for a short duration from 1900 to 2000 s. The performances of
ESKF and ESKF-RBF were evaluated on a similar trajectory as test case 1.

The time complexity of ESKF and ESKF-RBF was tested by running the algorithms on
an Intel I7 CPU with 4 GB RAM without any GPU. The testing software used was Matlab
2020b on Windows 7 platform. The timing comparison of both methods is given in Table 6.

Table 6. Execution time (seconds).

ESKF

0.0028

ESKF-RBF

0.0039

On a high-speed microcontroller or ﬁeld-programmable gate array FPGA, the exe-
cution time difference will be further reduced. Furthermore, the speed of surveying the
type of underwater vehicle is in the range of 2 km/h to 10 km/h; this difference has no
signiﬁcant effect on navigation and localization.

The work tried to ﬁll the gap by proposing a noval ESKF and RBF-augmented fusion
solution, which was assessed in three different underwater cases. The ESKF performance
strongly relies on the knowledge of the system models and noise properties, which was
degraded by nonlinearity. The errors in the RBF-ESKF are smaller than the errors in the
ESKF because of the recurcive learning of RBF. Moreover, the fusion algorithm based on

Sensors 2021, 21, 1149

22 of 26

RBF-ESKF with help from the aiding sensors was able to correct the drift problems in the
INS with better accuracy.

Nevertheless, the proposed algorithm is not limited to underwater; it can also be used
in other applications [66,67] such as improving aircraft navigation and tracking by using
aerial sensors. Moreover, autonomous ground vehicles are another area where this method
can be employed. Furthermore, by improving the Kalman ﬁler response, our methodology
can also enhance accuracy satellite attitude estimation [68].

(a)

(c)

(e)

(b)

(d)

(f)

Figure 7. Simulation results of ESKF and RBF-ESKF for time 0–3000 s (x-axis) in case 3. As the error
increases, nonlinearity in the error also increases. (a–c) The velocity error for the north, east, and
downward directions increase signiﬁcantly with DVL loss. The proposed velocity error estimate of
the algorithm is similar to real error. (d–f) RBF-ESKF has a smoother response and faster convergence
of the full state velocity estimation.

050010001500200025003000-0.5-0.4-0.3-0.2-0.100.1North velocity [m/s]North Error VelocityReal Velocity errorRBF-ESKF Estimated Velocity errorESKF Estimated Velocity error190019502000-0.1-0.0500.05050010001500200025003000-0.3-0.2-0.100.10.20.30.40.50.60.7East velocity [m/s]East Error velocityReal Velocity errorRBF-ESKF Estimated Velocity errorESKF Estimated Velocity error190020002100-0.2-0.10050010001500200025003000-0.06-0.04-0.0200.020.040.06Down velocity [m/s]Down Error velocityReal Velocity errorRBF-ESKF Estimated Velocity errorESKF Estimated Velocity error19061910-0.0100.01050010001500200025003000-0.500.511.522.533.5North [m/s]VelocityReal North velocityRBF-ESKF North Estimated velocityESKF North Estimated velocity1920196020003.023.043.063.083.13.123.14050010001500200025003000-0.6-0.4-0.200.20.40.60.811.2East [m/s]East VelocityReal East velocityRBF-ESKF East Estimated velocityESKF East Estimated velocity190019502000-0.0500.050.10.15050010001500200025003000-0.200.20.40.60.811.2Down [m/s]Down VelocityReal Down velocityRBF-ESKF Down Estimated velocityESKF Down Estimated velocity1950195519600.980.9911.01Sensors 2021, 21, 1149

23 of 26

7. Conclusions

This paper discusses the performance of the proposed algorithm RBF-ESKF for un-
derwater vehicle localization. The primary aim of this work is to take advantage of the
RBF neural network to improve the estimation performance of the conventional ESKF for
the position, velocity, and attitude of an underwater vehicle. It contrasts outcomes with
ESKF in three separate simulations, showing that RBF-ESKF performs better in estimating
position, velocity, and attitude. Why the standard ESKF has an inferior performance is
because it is designed by employing ﬁrst-order Taylor series approximation in the error
covariance matrix estimation, which results in a decrease in estimation accuracy under
high nonlinearity. Thus, important information about the dynamic of underwater is lost
because of this realization. However, RBF-ESKF efﬁciently handles nonlinearity due to its
inherent capability for nonlinear function approximation and learning ability.

The research also compared robustness in cases when there is no available position
information from the acoustic ﬁx. Here, relative to ESKF, RBF-ESKF demonstrated better
accuracy. When acoustic ﬁx becomes available, RBF-ESKF converges quickly. In addition,
when DVL fails due to short durations, RBF-ESKF also demonstrates less estimation error.
This work is part of an ongoing work on underwater vehicle localization. The novel
proposed algorithm is intended for use as a state estimation for underwater seabed map-
ping application.

In the future, we would like to test and analyze our algorithm with a different set of
sensors with different data rates in underwater environments. For instance, an enhanced
version of the multi-sensor fusion algorithm could be designed by using stereo vision and
underwater wireless sensor nodes to improve localization.

Author Contributions: All authors were involved in the research and preparation of this manuscript.
Conceptualization, N.S., M.M., and P.O.; formal analysis, N.S. and M.M.; funding acquisition, P.O.;
investigation, N.S.; methodology, M.J.I.; resources, M.J.I. and P.O.; software, N.S.; supervision, P.O.;
writing—original draft, N.S. and A.A.; writing—review and editing, M.M. and P.O.; all authors
reviewed and approved the manuscript.

Funding: This research was partially funded by the Campus de Excelencia Internacional Andalucia
Tech, University of Malaga, Malaga, Spain.

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Not applicable.

Data Availability Statement: Not applicable.

Acknowledgments: The authors express their gratitude to the Oceanic Engineering Research Insti-
tute, University of Malaga, Malaga, Spain.

Conﬂicts of Interest: The authors declare no conﬂict of interest.

References

1.

2.

3.

4.

5.

6.

Xu, C.; Xu, C.; Wu, C.; Qu, D.; Liu, J.; Wang, Y.; Shao, G. A novel self-adapting ﬁlter based navigation algorithm for autonomous
underwater vehicles. Ocean Eng. 2019, 187, 106146. [CrossRef]
Allotta, B.; Chisci, L.; Costanzi, R.; Fanelli, F.; Fantacci, C.; Meli, E.; Ridolﬁ, A.; Caiti, A.; Di Corato, F.; Fenucci, D. A comparison
between EKF-based and UKF-based navigation algorithms for AUVs localization. In Proceedings of the OCEANS 2015—Genova,
Genoa, Italy, 18–21 May 2015; pp. 1–5. [CrossRef]
Chen, H.; Gong, Y.; Hong, X.; Chen, S. A Fast Adaptive Tunable RBF Network For Nonstationary Systems. IEEE Trans. Cybern.
2016, 46, 2683–2692. [CrossRef] [PubMed]
Tomczyk, K.; Piekarczyk, M.; Sokal, G. Radial basis functions intended to determine the upper bound of absolute dynamic error
at the output of voltage-mode accelerometers. Sensors 2019, 19, 4154. [CrossRef]
Lu, S.; Ba¸sar, T. Robust nonlinear system identiﬁcation using neural-network models. IEEE Trans. Neural Netw. 1998, 9, 407–429.
[CrossRef]
Li, D.M.; Li, F.C. Identiﬁcation of chaotic systems with noisy data based on RBF neural networks.
In Proceedings of the
2009 International Conference on Machine Learning and Cybernetics, Hebei, China, 12–15 July 2009; Volume 5, pp. 2578–2581.
[CrossRef]

Sensors 2021, 21, 1149

24 of 26

7.
8.

Groves, P.D. Navigation using inertial sensors [Tutorial]. IEEE Aerosp. Electron. Syst. Mag. 2015, 30, 42–69. [CrossRef]
Kepper, J.H.; Claus, B.C.; Kinsey, J.C. A Navigation Solution Using a MEMS IMU, Model-Based Dead-Reckoning, and One-
Way-Travel-Time Acoustic Range Measurements for Autonomous Underwater Vehicles. IEEE J. Ocean. Eng. 2019, 44, 664–682.
[CrossRef]

9. Melo, J.; Matos, A. Survey on advances on terrain based navigation for autonomous underwater vehicles. Ocean Eng. 2017,

139, 250–264. [CrossRef]

10. González-García, J.; Gómez-Espinosa, A.; Cuan-Urquizo, E.; García-Valdovinos, L.G.; Salgado-Jiménez, T.; Escobedo Cabello, J.A.
Autonomous underwater vehicles: Localization, navigation, and communication for collaborative missions. Appl. Sci. 2020, 10,
1256. [CrossRef]

11. Ullah, I.; Chen, J.; Su, X.; Esposito, C.; Choi, C. Localization and Detection of Targets in Underwater Wireless Sensor Using

Distance and Angle Based Algorithms. IEEE Access 2019, 7, 45693–45704. [CrossRef]

12. Paull, L.; Saeedi, S.; Seto, M.; Li, H. AUV Navigation and Localization: A Review.

IEEE J. Ocean. Eng. 2014, 39, 131–149.

[CrossRef]

13. Qureshi, U.M.; Aziz, Z.; Shaikh, F.K.; Aziz, Z.; Shah, S.M.S.; Shah, S.M.S.; Sheikh, A.A.; Felemban, E.; Qaisar, S.B. RF path
and absorption loss estimation for underwaterwireless sensor networks in differentwater environments. Sensors 2016, 16, 890.
[CrossRef]

14. Diversi, R.; Guidorzi, R.; Soverini, U. Kalman ﬁltering in extended noise environments.

IEEE Trans. Autom. Control 2005,

50, 1396–1402. [CrossRef]

15. Almeida, J.; Matias, B.; Ferreira, A.; Almeida, C.; Martins, A.; Silva, E. Underwater localization system combining iusbl with

dynamic sbl in ¡vamos! trials. Sensors 2020, 20, 4710. [CrossRef] [PubMed]

16. Ko, N.Y.; Jeong, S.; Hwang, S.S.; Pyun, J.Y. Attitude estimation of underwater vehicles using ﬁeld measurements and bias

compensation. Sensors 2019, 19, 330. [CrossRef]

17. Huang, H.; Chen, X.; Zhou, Z.; Xu, Y.; Lv, C. Study of the algorithm of backtracking decoupling and adaptive extended kalman
ﬁlter based on the quaternion expanded to the state variable for underwater glider navigation. Sensors 2014, 14, 23041–23066.
[CrossRef]

18. Miller, A.; Miller, B.; Miller, G. On AUV control with the aid of position estimation algorithms based on acoustic seabed sensing

and DOA measurements. Sensors 2019, 19, 5520. [CrossRef]

19. Tal, A.; Klein, I.; Katz, R. Inertial navigation system/doppler velocity log (INS/DVL) fusion with partial dvl measurements.

Sensors 2017, 17, 415. [CrossRef] [PubMed]

20. Zhang, M.; Li, K.; Hu, B.; Meng, C. Comparison of Kalman Filters for Inertial Integrated Navigation. Sensors 2019, 19, 1426.

21.

[CrossRef]
Sun, C.; Zhang, Y.; Wang, G.; Gao, W. A new variational bayesian adaptive extended kalman ﬁlter for cooperative navigation.
Sensors 2018, 18, 2538. [CrossRef]

22. Chen, L.; Fang, J. A Hybrid Prediction Method for Bridging GPS Outages in High-Precision POS Application. IEEE Trans. Instrum.

23.

Meas. 2014, 63, 1656–1665. [CrossRef]
Jingsen, Z.; Wenjie, Z.; Bo, H.; Yali, W. Integrating Extreme Learning Machine with Kalman Filter to Bridge GPS Outages.
In Proceedings of the 2016 3rd International Conference on Information Science and Control Engineering, ICISCE 2016, Beijing,
China, 8–10 July 2016; pp. 420–424. [CrossRef]

24. Huang, X.L.; Ma, X.; Hu, F. Editorial: Machine Learning and Intelligent Communications. Mob. Netw. Appl. 2018, 23, 68–70.

[CrossRef]

25. Tsiropoulou, E.E.; Mitsis, G.; Papavassiliou, S. Interest-aware energy collection & resource management in machine to machine

communications. Ad Hoc Netw. 2018, 68, 48–57. [CrossRef]

26. Zhang, X.; Mu, X.; Liu, H.; He, B.; Yan, T. Application of Modiﬁed EKF Based on Intelligent Data Fusion in AUV Navigation. In

27.

Proceedings of the 2019 IEEE Underwater Technology (UT), Kaohsiung, Taiwan, 16–19 April 2019; pp. 1–4. [CrossRef]
Sabet, M.T.; Mohammadi Daniali, H.; Fathi, A.; Alizadeh, E. A Low-Cost Dead Reckoning Navigation System for an AUV Using
a Robust AHRS: Design and Experimental Analysis. IEEE J. Ocean. Eng. 2018, 43, 927–939. [CrossRef]

28. Allotta, B.; Caiti, A.; Chisci, L.; Costanzi, R.; Di Corato, F.; Fantacci, C.; Fenucci, D.; Meli, E.; Ridolﬁ, A. An unscented Kalman

29.

ﬁlter based navigation algorithm for autonomous underwater vehicles. Mechatronics 2016, 39, 185–195. [CrossRef]
Julier, S.; Uhlmann, J.; Durrant-Whyte, H. A new method for the nonlinear transformation of means and covariances in ﬁlters
and estimators. IEEE Trans. Autom. Control 2000, 45, 477–482. [CrossRef]

30. Karimi, M.; Bozorg, M.; Khayatian, A.R. A comparison of DVL/INS fusion by UKF and EKF to localize an autonomous
underwater vehicle. In Proceedings of the 2013 First RSI/ISM International Conference on Robotics and Mechatronics (ICRoM),
Tehran, Iran, 13–15 February 2013; pp. 62–67. [CrossRef]

31. Tsyganova, J.V.; Kulikova, M.V. SVD-Based Kalman Filter Derivative Computation. IEEE Trans. Autom. Control 2017, 62, 4869–4875.

[CrossRef]

32. Huang, G.; Mourikis, A.; Roumeliotis, S. On the complexity and consistency of UKF-based SLAM. In Proceedings of the 2009

IEEE International Conference on Robotics and Automation, Kobe, Japan, 12–17 May 2009; pp. 4401–4408. [CrossRef]
Simon, D. Training radial basis neural networks with the extended Kalman ﬁlter. Neurocomputing 2002, 48, 455–475. [CrossRef]

33.

Sensors 2021, 21, 1149

25 of 26

34. Wang, Y.; Chai, S.; Nguyen, H.D. Experimental and numerical study of autopilot using Extended Kalman Filter trained neural

networks for surface vessels. Int. J. Nav. Archit. Ocean. 2020, 12, 314–324. [CrossRef]

35. Kurban, T.; Be¸sdok, E. A Comparison of RBF Neural Network Training Algorithms for Inertial Sensor Based Terrain Classiﬁcation.

Sensors 2009, 9, 6312–6329. [CrossRef]

36. Dong, X.; Wu, J.; Wang, S.; Chen, T. An improved CDKF algorithm based on RBF neural network for satellite attitude
In Proceedings of the 2012 International Conference on Image Analysis and Signal Processing, IASP 2012,

determination.
Huangzhou, China, 9–11 November 2012; pp. 155–161. [CrossRef]

37. Pesce, V.; Silvestrini, S.; Lavagna, M. Radial basis function neural network aided adaptive extended Kalman ﬁlter for spacecraft

relative navigation. Aerosp. Sci. Technol. 2020, 96, 105527. [CrossRef]

38. Chen, T.; Chen, H. Approximation capability to functions of several variables, nonlinear functionals, and operators by radial

basis function neural networks. IEEE Trans. Neural Netw. 1995, 6, 904–910. [CrossRef]

39. Markopoulos, A.P.; Georgiopoulos, S.; Manolakos, D.E. On the use of back propagation and radial basis function neural networks

40.
41.

in surface roughness prediction. J. Ind. Eng. Int. 2016, 12, 389–400. [CrossRef]
Farrell, J.A. Aided Navigation GPS with High Rate Sensors, 1st ed.; The McGraw-Hill Companies: New York, NY, USA, 2008; p. 553.
Savage, P.G. Strapdown Inertial Navigation Integration Algorithm Design Part 2: Velocity and Position Algorithms. J. Guid.
Control. Dyn. 1998, 21, 208–221. [CrossRef]

42. Miller, P.A.; Farrell, J.A.; Zhao, Y.; Djapic, V. Autonomous Underwater Vehicle Navigation. IEEE J. Ocean Eng. 2010, 35, 663–678.

[CrossRef]

43. Karmozdi, A.; Hashemi, M.; Salarieh, H. Design and practical implementation of kinematic constraints in Inertial Navigation

System-Doppler Velocity Log (INS-DVL)-based navigation. Navigation 2018, 65, 629–642. [CrossRef]

44. Titterton, D.; Weston, J. Strapdown Inertial Navigation Technology, 2nd ed.; Institution of Engineering and Technology, The Institution

of Engineering and Technology, Michael Faraday House: Hertfordshire, UK, 2004. [CrossRef]

45. Valenti, R.G.; Dryanovski, I.; Xiao, J. Keeping a good attitude: A quaternion-based orientation ﬁlter for IMUs and MARGs.

Sensors 2015, 15, 19302–19330. [CrossRef]

46. Grewal, M.S.; Andrews, A.P.; Bartone, C.G. Global Navigation Satellite Systems, Inertial Navigation, and Integration; Wiley: New York,

NY, USA, 2020. [CrossRef]

47. Chatﬁeld, A.B. Fundamentals Of High Accuracy Inertial Navigation; American Institute of Aeronautics and Astronautics:

Reston,VA, USA, 1997. [CrossRef]

48. Wang, Q.; Cui, X.; Li, Y.; Ye, F. Performance enhancement of a USV INS/CNS/DVL integration navigation system based on an

adaptive information sharing factor federated ﬁlter. Sensor 2017, 17, 239. [CrossRef] [PubMed]

49. He, K.; Liu, H.; Wang, Z. A novel adaptive two-stage information ﬁlter approach for deep-sea USBL/DVL integrated navigation.

Sensors 2020, 20, 6029. [CrossRef]

50. Hegrenaes, O.; Ramstad, A.; Pedersen, T.; Velasco, D. Validation of a new generation DVL for underwater vehicle navigation.
In Proceedings of the 2016 IEEE/OES Autonomous Underwater Vehicles (AUV), Tokyo, Japan, 6–9 November 2016; pp. 342–348.
[CrossRef]

51. Kang, Y.; Zhao, L.; Cheng, J.; Wu, M.; Fan, X. A Novel Grid SINS/DVL Integrated Navigation Algorithm for Marine Application.

Sensors 2018, 18, 364. [CrossRef]

52. Christ, R.D.; Wernli, R.L. Underwater Acoustics and Positioning. In The ROV Manual; Elsevier Ltd.: Amsterdam, The Netherland,

2007; pp. 81–124. [CrossRef]

53. Healey, A.; An, E.; Marco, D. Online compensation of heading sensor bias for low cost AUVs.

In Proceedings of the 1998
Workshop on Autonomous Underwater Vehicles (Cat. No.98CH36290), Cambridge, MA, USA, 21 August 1998; pp. 35–42.
[CrossRef]
Fanelli, F. Development and Testing of Navigation Algorithms for Autonomous Underwater Vehicles, 1st ed.; Springer Theses; Springer
International Publishing: Cham, Sweden, 2020. [CrossRef]

54.

55. Roumeliotis, S.I.; Sukhatme, G.S.; Bekey, G.A. Circumventing Dynamic Modeling: Evaluation of the Error-State Kalman Filter
applied to Mobile Robot Localization. In Proceedings of the IEEE International Conference on Robotics and Automation, Detroit,
MI, USA, 10–15 May 1999. [CrossRef]

56. Rogers, R.M. Applied Mathematics in Integrated Navigation Systems, 3rd ed.; American Institute of Aeronautics and Astronautics:

57.

Reston ,VA, USA, 2007. [CrossRef]
Foss, H.T.H.; Meland, E. Sensor Integration for Nonlinear Navigation System in Underwater Vehicles. Ph.D. Thesis, Norwegian
University of Science and Technology, Trondheim, Norway, 2007.

58. Emami, M.; Taban, M.R. A Low Complexity Integrated Navigation System for Underwater Vehicles. J. Navig. 2018, 71, 1161–1177.

[CrossRef]

59. Dinc, M.; Hajiyev, C. Integration of navigation systems for autonomous underwater vehicles. J. Mar. Eng. Technol. 2015, 14, 32–43.

[CrossRef]

60. Yu, H.; Xie, T.; Paszczynski, S.; Wilamowski, B.M. Advantages of Radial Basis Function Networks for Dynamic System Design.

IEEE Trans. Ind. Electron. 2011, 58, 5438–5450. [CrossRef]

61. Wu, Y.; Wang, H.; Zhang, B.; Du, K.L. Using Radial Basis Function Networks for Function Approximation and Classiﬁcation.

ISRN Appl. Math. 2012, 2012, 1–34. [CrossRef]

Sensors 2021, 21, 1149

26 of 26

62. Kalman, R.E. A New Approach to Linear Filtering and Prediction Problems. J. Basic Eng. 1960, 82, 35–45. [CrossRef]
63.
64. Bjaili, H.A.; Moinuddin, M.; Rushdi, A.M. A State-Space Backpropagation Algorithm for Nonlinear Estimation. Circuits Syst.

Solà, J. Quaternion kinematics for the error-state Kalman ﬁlter. arXiv 2017, arXiv:1711.02508

Signal Process. 2019, 38, 3682–3696. [CrossRef]

65. Zhao, Y.; Wang, D.; Wang, L. Convolution Accelerator Designs Using Fast Algorithms. Algorithms 2019, 12, 112. [CrossRef]
66. Dul, F.; Lichota, P.; Rusowicz, A. Generalized Linear Quadratic Control for a Full Tracking Problem in Aviation. Sensors 2020,

20, 2955. [CrossRef] [PubMed]

67. Wei, L.; Cappelle, C.; Ruichek, Y. Camera/Laser/GPS Fusion Method for Vehicle Positioning Under Extended NIS-Based Sensor

Validation. IEEE Trans. Instrum. Meas. 2013, 62, 3110–3122. [CrossRef]

68. Pham, M.D.; Low, K.S.; Goh, S.T.; Chen, S. Gain-scheduled extended kalman ﬁlter for nanosatellite attitude determination system.

IEEE Trans. Aerosp. Electron. Syst. 2015, 51, 1017–1028. [CrossRef]
