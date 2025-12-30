See discussions, stats, and author profiles for this publication at: <https://www.researchgate.net/publication/358117861>

Comparison of Attitude Estimation Algorithms With IMU Under External
Acceleration

Conference Paper · January 2022

DOI: 10.1109/iSES52644.2021.00037

CITATIONS
8

3 authors:

Dhruv Parikh

University of Pennsylvania

1 PUBLICATION   8 CITATIONS

SEE PROFILE

Maryam Kaveshgar

Ahmedabad University

10 PUBLICATIONS   10 CITATIONS

SEE PROFILE

READS
801

Sajil Vohra

Ahmedabad University

1 PUBLICATION   8 CITATIONS

SEE PROFILE

All content following this page was uploaded by Maryam Kaveshgar on 26 January 2022.

The user has requested enhancement of the downloaded file.

2021 IEEE International Symposium on Smart Electronic Systems (iSES)

Comparison of Attitude Estimation Algorithms With
IMU Under External Acceleration

Dhruv Parikh
School of Engineering and
Applied Science
Ahmedabad University
Ahmedabad,India
<dhruv.p@ahduni.edu.in>

Sajil Vohra
School of Engineering and
Applied Science
Ahmedabad University
Ahmedabad,India
<sajil.v@ahduni.edu.in>

Dr. Maryam Kaveshgar
School of Engineering and
Applied Science
Ahmedabad University
Ahmedabad,India
<maryam.kaveshgar@ahduni.edu.in>

Abstract—For improved ﬂight stability, the ﬂight controller
needs to compute precise attitudes of the quadrotor at a fast
update rate. This paper provides a comparison between different
sensor fusion algorithms for estimating attitudes using an Inertial
Measurement Unit (IMU), speciﬁcally when the accelerometer
gives erroneous readings. Three test cases with an emphasis on
the inﬂuence of external acceleration on attitudes are selected. For
each test case, noise ﬁltered data from the IMU is streamed into
four algorithms, namely Complementary, Kalman, Madgwick,
and Mahony fusion ﬁlters. Furthermore, each algorithm is
implemented on ESP32 (Xtensa® 32-bit LX6) microcontroller
to benchmark the execution time. The estimated attitudes show
that the Madgwick ﬁlter mitigates the effects of accelerations the
most, while the Kalman ﬁlter and Mahony ﬁlter are robust to
vibrations introduced to the system.

Keywords-Attitude Estimation, Sensor Fusion, Complementary

Filter, Kalman Filter, AHRS, UAV

I. INTRODUCTION

In recent decades, the growth of quadrotor systems has
been prodigious owing to miniaturization and cost reduc-
tion of onboard sensors. To estimate the orientation of the
quadrotor in real-time, an Inertial Measurement Unit (IMU)
is preferred as vision-based state estimation is more involved
and requires much more computational power. A 6-axis IMU
consists of a three-axis accelerometer and gyroscope. Ideally,
both accelerometer and gyroscope can independently provide
orientation data. However, due to vibrations, thermal noise and
other external disturbances, the estimates from independent
modules are unusable, especially in low-cost sensors. The
estimation in attitudes based on gyroscope introduces bias
in the system whereas the accelerometer has high noise. A
reliable orientation estimate can be obtained by fusing signals
obtained from both modules. For this purpose, numerous
fusion algorithms are available which give better attitude
estimates.

In [1], comparison of Extended Kalman Filter, Mahony, and
Madgwick ﬁlters is carried out with IMU mounted on a robotic
manipulator. The test cases comprised of individual rotations
around each axis and simultaneous rotations. It was concluded
that Extended Kalman Filter had a very high computational
load although with the least Root Mean Square Error (RMSE)
compared to other algorithms.

978-1-7281-8753-2/21/$31.00 ©2021 IEEE
DOI 10.1109/iSES52644.2021.00037

123

A similar comparison study was done in [2], where algo-
rithms were tested on a ﬂight dataset. Results concluded with
Mahony AHRS being superior to other algorithms based on
RMSE as an error metric. Both Complementary and Kalman
ﬁlters can accurately predict the attitude of quadrotor [3], [4].
Although both algorithms give a considerable performance,
the complementary ﬁlter is simpler to tune than the Kalman
ﬁlter, thus becoming easier to implement.

The aforementioned comparisons use algorithms that fuse
attitudes obtained from both gyroscope and accelerometer but
the attitudes obtained from accelerometers are only valid when
linear accelerations are nil. Fig. 1 illustrates that, under large
accelerations,
the attitudes derived from the accelerometer
are incorrect. Since quadrotors undergo high accelerations
during ﬂight, mitigating this error is an important aspect of
the tilt estimation problem. This paper speciﬁcally evaluates
the performance of algorithms when the accelerometer gives
erroneous readings. The following sections assess sensor fu-

Fig. 1. Error in Accelerometer attitude due to linear accelerations

sion algorithms, namely Kalman Filter, Complementary Filter,
Madgwick AHRS and Mahony AHRS during linear accel-
erations encountered by quadrotor. As the effects of linear
accelerations are not seen on magnetometers, the evaluation
of the Yaw axis is beyond the scope of this paper. Each
algorithm parameter was tuned based on experimental data
which comprises of three different test cases. Performance was
evaluated using multiple error metrics.

II. ATTITUDE ESTIMATION ALGORITHMS

In low-cost systems, the sensors are less accurate and the
processing platforms are comparatively slower in execution

of algorithms. It is necessary that the algorithms cope up
with the sample rate of sensor data for a consistent attitude
refresh rate. Four algorithms - Complementary Filter, Kalman
Filter, Mahony Filter and Madgwick Filter are suitable for
such systems and provide effective synchronization between
attitude and sensor update rates.

A. Complementary Filter

Complementary Filter is an elementary sensor fusion algo-
rithm for estimating attitudes. The ﬁlter considers more weight
of gyroscope and a complemented weight of accelerometer.
This rectiﬁes gyroscope integration drift by accelerometer
attitude and outputs a reliable, drift-free and noise suppressed
attitude. Complementary Filter is computationally very light
and it updates every iteration with direct use of rotation rates
and acceleration-based angles. Since it has only one tuning
parameter, it is very easy and intuitive to tune, making it ideal
for initial implementation.

B. Kalman Filter

For a linear system with white gaussian noise, Kalman Filter
is an optimal state estimator. The algorithm works in two steps

- Prediction and Correction. In the prediction step, it predicts
the current state based on previous states of the system. In
the correction step, the states are corrected by actual sensor
measurements [5]. In this paper, Kalman Filter is modeled with
gyroscopic rate as system input and accelerometer attitude
as correction [4]. The measurement model of the system is
expressed in equation (1).

θt = θt−1 + (ωt − bt) · Δt

(1)

Where b is bias, θ is the estimated attitude, ω is the gyroscopic
rate. The state (xt) and output (yt) vector chosen is shown in
(2).

(cid:2)

(cid:3)

xt =

yt =

θ
b
1

(cid:4)

(cid:5)

0

· xt

(2)

C. Mahony Filter

Mahony Filter is a sensor fusion algorithm where gyro-
scopic bias is corrected using accelerometer through feedback
via a Proportional Integral (PI) controller. The mathematical
form of Mahony Filter is shown in (3) and (4) [6].
ep,t = θacc,t − ˆ
ei,t = ei,t−1 + ep,t · Δt

θt−1

(3)

Here, ˆ
error, ei is the integral error.

θt is the angle estimated at time ‘t’, ep is the proportional

θt = ˆ
ˆ

θt−1 + (ωt + Kp · ep,t + Ki · ei,t) · Δt

(4)

where, ωt is angular rate at time ‘t’, Kp and Ki are the
proportional and integral gains respectively which can be
tuned to adjust the performance. With this feedback system,
gyroscopic drift is minimised, providing an accurate attitude
estimation.

124

(6)

(7)

D. Madgwick Filter

Unlike traditional attitude computation with accelerometers
and gyroscopes, Madgwick ﬁlter uses gradient descend ap-
proach to correct quaternion errors and provides gyro drift
compensation, giving orientation estimations using MARG
(Magnetic-Angular Rate-Gravity) or IMU sensor arrays.
The gradient descend step can be formulated as:
I ˆa) = J

W ˆq,
(5)
W ˆq is the normalized quaternion transformed from
world frame (W) to inertial frame (I). W ˆg and I ˆa are normal-
ized gravity vector in world frame and normalized acceleration
vector in inertial frame respectively. J is the Jacobian and f
is the simpliﬁed objective function [7].
(cid:6)

∇f (I
In (5), I

W ˆg)f (I

W ˆg,

W ˆg,

I ˆa)

W ˆq,

W ˆq,

T (I

(cid:7)

I
W ˙qest,t =

W ˆqest,t−1) ⊗ I
(I

ωt

− β

1
2

∇f
(cid:4)∇f (cid:4)

W qest,t = I
I

W qest,t−1 + I

W ˙qest,tΔt

In (6), the quaternion derivative is obtained by a quaternion
W ˆqest,t−1 with angular rate

multiplication of previous estimate I
measurement I ω at time t.

In (7), I

W qest,t is the estimate of orientation obtained by
numerical integration of rate of change of orientation I
W ˙qest,t
computed in (6). Here, β is gyroscope measurement error
which deﬁnes the magnitude of quaternion derivative.

III. EXPERIMENTATION AND ERROR METRICS

A. Experimentation Setup

For the experimentation, the ESP32 board, by Espressif
Systems was chosen. The board contains dual core Xtensa
32-bit LX6 microprocessors @240MHz with 600 DMIPS
performance and has a ﬂoating point unit (FPU).

For orientation measurement, the IMU from InvenSense,
MPU6050 [8] was selected considering the lower cost of the
system. The IMU has a 3D accelerometer with a sampling
rate of 1KHz and conﬁgured sensing range of ±8g. The 3D
gyroscope on the IMU has an update rate of 8KHz with a
chosen sensing range of ±500◦/s. The IMU is interfaced
via I2C interface. The data from the accelerometers and
gyroscopes were sampled at 200Hz by ESP32.

B. Data Collection and Signal Processing

Three test cases were selected for experiments:

1) System is not banking (0◦) and accelerating
2) System is banking in Roll/Pitch and accelerating
3) System is steady with heavy vibrations from high speed

motors.

The data for the banked system was collected at 15◦ using
a plank which can be set to a desired angle and can be locked
at that angle to prevent false measurement.

The IMU is calibrated and the data is passed through a
Butterworth Low pass ﬁlter of order 4 to remove noise and
effects of vibrations. The performance of the Butterworth ﬁlter
can be seen in Fig. 3.

IV. RESULTS
Fig. 4 - 7 show theperformance on test case 1 and 2.
Spider plot shows intuitively, the error metrics remain consis-
tent in both the cases with Madgwick AHRS outperforming
other algorithms relatively, followed by Kalman, Mahony and
Complemenentary ﬁlters respectively. It is evident from Fig. 4
and 6 that errors in accelerometer angles due to translational
accelerations are suppressed most effectively by Madgwick
AHRS and the the least effectively by complementary ﬁlter.

Flight Controller at 15◦, (X0, Y0, Z0) is the global frame and

Fig. 2.
(X, Y, Z) is Sensor frame

Fig. 3. Noise Suppression using Butterworth LPF

Fig. 4. Performance on Test Case - 1

C. Tuning of Filter Parameters

Parameters of all algorithms were tuned based on minimum
Root Mean Square Error (RMSE) criteria. Different values of
parameters were selected in a range and each set of values
were simulated under the given test case. The optimal values
based on RMSE are shown in table I. Test Case 2 was chosen

TABLE I
OPTIMAL PARAMETERS FOR ALGORITHM

Algorithms
Kalman Filter
Madgwick Filter
Mahony Filter
Complementary Filter

Optimal Parameters

Q = diag(0.01181,4.28e-6)
β = 0.00921

Kp = 0.89

α = 0.997

R = 2650

Ki = 0.01

Fig. 5. Spider Chart for Test Case - 1

to tune to parameters of the algorithms. All algorithms were
implemented in MATLAB software. Madgwick and Mahony
AHRS were implemented in quaternion form.

D. Error Metrics

To compare different algorithms, a set of error metrics
were chosen as there is no single error metric which can
provide a comprehensive review. When estimating attitudes,
extremely small errors can be neglected while large errors
need to be emphasized more. Error metrics such as RMSE,
Mean Absolute Percentage Error (MAPE), Median Absolute
Deviation (MAD) are dominated by relatively large errors, thus
providing an accurate metric on desired performance. For the
overall performance of the system, Geometric Average Error
(GAE) and Iterative Mid-Range Error (IMRE) are suitable [9].
The above mentioned ﬁve error metrics were used to assess the
performance providing a thorough overview on each reliable
error metric.

Fig. 6. Performance on Test Case - 2. Left ﬁgure shows the zoomed portion
where linear accelerations were encountered at banked angle. Right ﬁgure
shows the convergence of algorithm.

Fig. 8 and 9 shows the performance of all algorithms on test
case 3. In contrast to other test cases, with the introduction
of noise and vibration in the setup due to propellers, the
performance of Madgwick AHRS degrades. However, Kalman
to change in signal
Filter and Mahony Filter are robust
characteristics, in this case, effects of vibrations.

125

TABLE III
RMSE FOR ALL TEST CASES

Test Case

Case-1
Case-2
Case-3

Kalman
P
R
0.33
0.28
0.39
0.4
0.33
0.57

Madgwick
R
0.24
0.3
1.74

P
0.3
0.35
0.22

Mahony
P
R
0.34
0.29
0.4
0.41
0.82
0.57

CF
R
0.37
0.43
0.53

P
0.42
0.41
0.38

Kalman Filter has a very high computation time, a workaround
for attitude estimation is to set complementary ﬁlter gain
α = 1 − K1. This provides a near identical performance of
complementary ﬁlter and Kalman ﬁlter.

V. CONCLUSION

The paper presents a comparison of different sensor fusion
algorithms on a low cost IMU when the accelerometer gives
faulty readings. Algorithms were compared with each other
on three different test cases. Each algorithm gave satisfactory
results in computing attitudes with minor errors. In comparison
to the other algorithms, Complementary ﬁlter provides the
least suppression of acceleration effects, while Madgwick
AHRS was able to effectively suppress the accelerometer
errors the most. However, its parameter (β) was sensitive to
introduction of vibrations. It was observed that Kalman and
Mahony Filter were robust to vibrations. Mahony Filter was
found to be computationally inexpensive, however it is only
for attitude computation while Kalman Filter is generalised
for any linear system model. In future work, the selection of
threshold based adaptive gains should be applied to conven-
tional sensor fusion algorithms to improve their performance
under accelerometer anomaly.

REFERENCES

[1] A. Cavallo, A. Cirillo, P. Cirillo, G. Maria, P. Falco, C. Natale, and
S. Pirozzi, “Experimental comparison of sensor fusion algorithms for
attitude estimation,” IFAC Proceedings Volumes, vol. 47, pp. 7585–7591,
2014.

[2] S. A. Ludwig and K. D. Burnham, “Comparison of euler estimate using
extended kalman ﬁlter, madgwick and mahony on quadcopter ﬂight
data,” in 2018 International Conference on Unmanned Aircraft Systems
(ICUAS), 2018, pp. 1236–1241.

[3] H.-Q.-T. Ngo, T.-P. Nguyen, V.-N.-S. Huynh, T.-S. Le, and C.-T. Nguyen,
“Experimental comparison of complementary ﬁlter and kalman ﬁlter de-
sign for low-cost sensor in quadcopter,” in 2017 International Conference
on System Science and Engineering (ICSSE), 2017, pp. 488–493.

[4] P. Gui, L. Tang, and S. Mukhopadhyay, “Mems based imu for tilting
measurement: Comparison of complementary and kalman ﬁlter based data
fusion,” in 2015 IEEE 10th Conference on Industrial Electronics and
Applications (ICIEA), 2015, pp. 2004–2009.

[5] D. Simon, “The discrete-time kalman ﬁlter,” in Optimal State Estimation:
Kalman, H Inﬁnity, and Nonlinear Approaches. Hoboken, New Jersey,
USA: John Wiley Sons, Inc, 2006, pp. 123–148.

[6] R. Mahony, T. Hamel, and J.-M. Pﬂimlin, “Nonlinear complementary
ﬁlters on the special orthogonal group,” IEEE Transactions on Automatic
Control, vol. 53, no. 5, pp. 1203–1218, 2008.

[7] S. O. Madgwick, A. J. Harrison, and R. Vaidyanathan, “Estimation of
imu and marg orientation using a gradient descent algorithm,” in 2011
IEEE international conference on rehabilitation robotics.
IEEE, 2011,
pp. 1–7.

[8] MPU-6000 and MPU-6050 Product Speciﬁcation, InvenSense Inc., 8

2013, rev. 3.4.

[9] W. Peng, Y. Li, Y. Fang, Y. Wu, and Q. Li, “Radar chart for estimation
performance evaluation,” IEEE Access, vol. 7, pp. 113 880–113 888, 2019.

Fig. 7. Spider Chart for Test Case - 2

Fig. 8. Performance on Test Case - 3

For comparing execution time, all the fusion algorithms are
optimally implemented on the ESP32 board. Table II shows the
execution time for each algorithm. Quantitatively, the RMSE

TABLE II
EXECUTION TIME BENCHMARK

Algorithms
Kalman Filter
Madgwick Filter
Mahony Filter
Complementary Filter

Tri-axis Execution time
51 μs
17 μs
14 μs
10 μs

values of both pitch (P) and roll (R) axis of all test cases are
illustrated in table III. Although relatively one can compare
the difference of each ﬁlter, it is to be noted that every ﬁlter
performed satisfactorily on the system. In terms of RMSE,
analogous performance can be concluded if accounting for
any inherent true value measurement error in the system. Since

Fig. 9. Spider Chart for Test Case - 3

View publication stats

126
