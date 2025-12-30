Inertial Navigation Meets Deep Learning: A Survey
of Current Trends and Future Directions

Nadav Cohen

and Itzik Klein

1

4
2
0
2

b
e
F
5
2

]

O
R
.
s
c
[

2
v
4
1
0
0
0
.
7
0
3
2
:
v
i
X
r
a

Abstract—Inertial sensing is used in many applications and
platforms, ranging from day-to-day devices such as smartphones
to very complex ones such as autonomous vehicles. In recent
years, the development of machine learning and deep learning
techniques has increased significantly in the field of inertial
sensing and sensor fusion. This is due to the development of
efficient computing hardware and the accessibility of publicly
available sensor data. These data-driven approaches mainly
aim to empower model-based inertial sensing algorithms. To
encourage further research in integrating deep learning with
inertial navigation and fusion and to leverage their capabilities,
this paper provides an in-depth review of deep learning methods
for inertial sensing and sensor fusion. We discuss learning
methods for calibration and denoising as well as approaches for
improving pure inertial navigation and sensor fusion. The latter
is done by learning some of the fusion filter parameters. The
reviewed approaches are classified by the environment in which
the vehicles operate: land, air, and sea. In addition, we analyze
trends and future directions in deep learning-based navigation
and provide statistical data on commonly used approaches.

Index Terms—Inertial sensing, Navigation, Deep learning,

Data-driven, Sensor fusion, Autonomous platforms

I. INTRODUCTION

R ESEARCH on the concepts of inertial sensing has been

conducted for several decades and has been used in
the navigation process for a variety of platforms during the
last century [1]. As of today, most inertial sensing relies on
accelerometers, which provide specific force measurements,
as well as gyroscopes, which provide angular velocity mea-
surements [2]. An inertial measurement unit (IMU) typically
consists of three orthogonal accelerometers and three orthog-
onal gyroscopes, each varying in performance and cost [3, 4].
The IMU readings are processed in real-time to provide
a navigation solution. Such a system, which executes the
strapdown inertial navigation algorithm, is known as an inertial
navigation system (INS) [5]. The INS provides the navigation
solution consisting of position, velocity, and orientation as
illustrated in Fig.1a.
The navigation solution accuracy and efficiency is affected by
the duration of the mission, the platform dynamics, as well
as the quality of the IMU. Using high-end sensors results
in a more accurate navigation solution for extended periods
of time, while using low-cost INS results in a much faster
accumulation of errors. There is, however, a common approach
for dealing with error accumulation in both cases, which is to
use an accurate external aiding sensor or information aiding
to ensure that the solution is bounded or the error is mitigated

N. Cohen and I. Klein are with the Hatter Department of Marine Technolo-

gies, Charney School of Marine Sciences, University of Haifa, Israel.
Corresponding author: <ncohe140@campus.haifa.ac.il> (N.Cohen)

[6, 7]. Sensors like the global navigation satellite system
(GNSS), which provides precise position measurements, and
the Doppler velocity log (DVL), which offers accurate velocity
readings, are considered external aiding sensors. Addition-
ally, supplementary information such as zero velocity updates
(ZUPT) and zero angular rates (ZAR) can be utilized, either
independently or in conjunction with physical sensors,
to
mitigate error accumulation in inertial navigation solutions.
The INS and aiding sensors are commonly fused in nonlinear
filters such as the extended Kalman filter (EKF) and the
uncentered Kalman filter (UKF). Filters of this kind have the
capability to incorporate the uncertainty of a model, consid-
ering both process and measurement noise covariances. This
enables them to furnish valuable additional information while
also averting error accumulation within an inertial navigation
algorithm [8]. A diagram of the sensor fusion is shown in Fig.
1b.
During the past decade, deep learning (DL) has made remark-
able progress due to advances in neural network architectures,
large datasets, and innovative training methods. In the field
of computer vision, convolutional neural networks (CNNs)
have revolutionized tasks such as image classification, object
detection, and semantic segmentation [9]. It has been demon-
strated that recurrent neural networks (RNNs), including long
short-term memory (LSTM) networks, are particularly effec-
tive at modeling sequences and undertaking language-related
tasks, such as translation and sentiment analysis when used
for natural language processing [10]. Moreover, techniques
such as generative adversarial networks (GANs) and transfer
learning have extended the capabilities of DL models to enable
tasks such as image synthesis and the use of pre-trained
models [11, 12]. In light of these advancements, DL has been
significantly enhanced, propelling it to new frontiers in the
field of artificial intelligence.
The recent advances in hardware and computational efficiency
have proven DL methods to be useful for dealing with real-
time applications ranging from image processing and signal
processing to natural
language processing by utilizing its
capabilities to address nonlinear problems [13, 14, 15, 16].
As a result, DL methods began to be integrated into inertial
navigation algorithms. One of the first papers to use neural
networks (NNs) in inertial navigation was written by Chiang
et al. [17] in 2003. A multi-sensor integration was proposed
using multi-layer, feed-forward neural networks and a back-
propagation learning algorithm to regress the accurate land
vehicle position. It demonstrated the effectiveness of the NN
in addressing navigation problems.
Motivated by their success and impact, researchers published
papers proposing utilizing deeper and more sophisticated

2

(a)

(b)

Fig. 1: (a) Strapdown inertial navigation algorithm. For a given initial condition, the gyroscope’s angular velocity and the
accelerometer’s specific force measurements are integrated over time to calculate the navigation solution in the desired reference
frame (local, geographic, and so on). (b) The process by which the navigation solution can be corrected using a nonlinear filter
and an aiding sensor. By looking at the output, the black diverging curve shows how the navigation solution accumulates error
and the red curve illustrates how the aiding sensor corrects this error, resulting in a chainsaw-like signal.

in [22],

neural networks. Noureldin et al. [18] designed a multi-layer
perceptron (MLP) network to predict the INS position error
during GNSS outages using the INS position component and
instantaneous time. This work was continued and modified
in [19], where the authors replaced the MLP network with
a radial basis function (RBF) neural network to address the
same scenario and successfully reduced the position error. In
[20], further improvements were described, utilizing multi-
layer feed-forward neural networks to regress the vehicle’s
position and velocity in an INS/differential-GNSS (DGNSS)
integration by employing a low-cost IMU. Further research
concerning GNSS outage and INS/GNSS fusion is available
in [21] using input-delayed neural networks that regress
velocity and position utilizing fully connected (FC) layers.
Additionally,
the development of fully connected
neural networks with hidden layers constructed of wavelet base
functions was proposed to develop INS/GNSS integration to
eliminate the complexities associated with KF by providing
a reliable positioning solution when GNSS signals are not
available. In addition to position regression, Chiang et al. in
[23, 24, 25] introduced NNs based on fully connected layers
for the enhancement of orientation measurements provided
by INS/GNSS fusions when using low-cost MEMS IMUs or
when GNSS signals are not available. Another concept is to
improve a specific block within the KF, and a suggestion in
[26] was to provide the innovation process in an adaptive KF
for an integrated INS/GNSS system using a three-layer, fully
connected network. Performance analysis for the networks
above was conducted in [27] for INS/GNSS fusion. The
researchers mentioned above were among the early adopters
of utilizing inertial data within deep neural networks (DNNs)
to enhance navigation capabilities.
Aside from this paper, there are several other papers that con-
ducted surveys on the general topic of data-driven navigation.
Most of them looked at specific platforms or DL methods. In
[28, 29], a review of the navigation of spacecraft was made
in addition to other concepts such as dynamics and control.
Furthermore, approaches of only deep-reinforcement learning
were reviewed for different platforms in [30, 31, 32]. In light
of DL’s significant advances in the fields of image processing
and computer vision, vision-based navigation surveys were
conducted for different platforms and in general [33, 34,

35, 36, 37]. Some papers focused only on machine-learning-
based navigation, which is based primarily on determining
the features through preprocessing data analysis [38, 39, 40].
In [41] there is a discussion of end-to-end DL methods
employed in autonomous navigation, including subjects other
than navigation such as obstacle detection, scene perception,
path planning, and control. A survey was conducted in [42]
to examine inertial positioning using recent DL methods. It
targeted tasks such as pedestrian dead-reckoning and human
activity recognition. An overview of all the survey papers is
provided in Table I.

TABLE I: A collection of fifteen surveys describing DL
methods applied to different aspects of navigation.

Paper
28
29
30, 31
32
33
34, 36

35

37
38
39
40
41

42

Topic
DL methods for spacecraft dynamics, navigation and control
DL methods of relative navigation of a spacecraft
DRL for mobile robot navigation
UAV autonomous navigation using RL
DL methods for visual indoor navigation
Visual navigation using RL
DL methods of perception and navigation
in unstructured environments
DL for perception and navigation in autonomous systems
Machine learning for maritime vehicle navigation
Survey of inertial sensing and machine learning
Machine learning for indoor navigation
DL applications and methods for autonomous vehicles
DL methods for positioning including
pedestrian dead-reckoning and human activity recognition

Contrary to all of the above, this paper examines DL meth-
ods utilized exclusively in inertial sensing and sensor fusion
algorithms and focuses entirely on vehicles regardless of their
operating environment. The contributions of this paper are:

1) Provide an in-depth review of DL methods applied to
inertial sensing and sensor fusion tasks for land, aerial,
and maritime vehicles.

2) Examine DL methods for calibrating and denoising
inertial sensor data suitable for any vehicle and any
inertial sensor.

3) Provide insights into current trends on the subject and
describe the common DL architectures for inertial nav-
igation tasks.

4) Discussion of potential future directions for the use of

DL approaches for improving inertial sensing and sensor
fusion algorithms.

The rest of the paper is organized as follows: Sections II, III
and IV address DL approaches for improving land, aerial, and
maritime inertial sensing, respectively, and are further divided
into subsections on pure inertial navigation and aided inertial
navigation. Section V discusses methods for enhancing the
calibration and denoising of inertial data using DL techniques.
Section VI delves into the survey findings and explores the
pros and cons of employing DL in inertial navigation, along
with future trends. Lastly, Section VII presents the conclusions
of this survey..

II. LAND VEHICLE INERTIAL SENSING

A. Pure Inertial Navigation

Several studies have investigated inertial deep learning ap-
proaches in situations when GNSS signals are not available.
Shen et al.
in [43] presented an approach for improving
MEMS-INS/GNSS navigation during GNSS outages. This
article proposed two neural networks for a dual optimization
process, wherein the first NN compensates for the INS error,
while the second NN compensates for the error generated
by a filter using the radial basis function (RBF) network for
accurate position data.
Considering the great interest in scenarios of GNSS outages,
many papers have been published suggesting more complex
DNNs. In scenarios where GNSS signals are unavailable, Lu
et al. introduced a multi-task learning method [44]. Initially,
inertial data undergo denoising through a convolutional auto-
encoder, followed by temporal convolutional network (TCN)
processing to address GNSS gaps and one-dimensional CNN
(1DCNN) application for zero velocity scenario detection.
Subsequently, this aiding data contributes to deriving an accu-
rate navigation solution in Kalman filtering (KF). Additionally,
Karlsson et al. proposed a CNN model for precise speed
estimation solely relying on inertial data in the absence of
aiding sensors like GNSS or wheel speed [45].
GNSS signals are not viable in all scenarios, such as indoor
navigation or tunnel navigation, requiring not only compensa-
tion for gaps in GNSS signal availability, but also accounting
for the entire process. For example, in [46, 47], Tong et al.
regressed the change in velocity and heading of a vehicle in
GNSS-blocked environments such as tunnels using a TCN
architecture with residual blocks used from low-cost, smart-
phone mounted, IMU readings. Additionally, ”DeepVIP”, an
LSTM-based architecture, was introduced for indoor vehicle
positioning and trained on low-cost inertial data from smart-
phones. ”DeepVIP” is available in two variations. The first
achieves a higher level of positioning accuracy by estimating
the velocity and change of heading and is appropriate for
scenarios requiring the highest degree of positioning accuracy,
and the other is more appropriate for situations requiring
computational efficiency,
therefore its accuracy is slightly
lower [48]. An illustration based on the DeepVIP model can
be seen in Fig. 2.
The use of data-driven methods in inertial vehicle navigation

3

also provides the benefit of improving the output of the inertial
sensors independent of the other aiding sensors. Zhao et al.
examined high-end sensors in [49] and proposed ”GyroNet”
and ”FoGNet”, which are based on bidirectional-LSTMs (bi-
LSTMs). The first estimates the bias and noise of a gyroscope
to improve angular velocity measurements, while the second
corrects the drift of the fiber optic gyroscope (FOG) to improve
vehicle localization. A similar approach was done in [50]
where the authors introduced a novel approach to produce
IMU-like data from GNSS data to train a fully connected-
based network to regress angular velocity and acceleration
for better positioning based on MEMS IMU data. Gao et al.
[51] introduced the ”VeTorch,” an inertial tracking system that
employs smartphone-derived inertial data for real-time vehicle
location tracking. Employing a TCN, they conducted acceler-
ation, orientation sequence learning, and pose estimation. In a
separate study, Freydin & Or proposed an LSTM-based model
to forecast vehicle speed using low-cost IMU readings from
smartphones [52].

Fig. 2: The figure illustrates an LSTM architecture based on
the DeepVIP architecture described in [48]. The DeepVIP
architecture involves passing inertial readings and additional
sensor data through LSTM cells to capture time dependencies.
Subsequently,
layers to prevent
overfitting before being processed by FC layers to extract
velocity and heading residual outputs.

the data traverses dropout

Apart from enhancing inertial reading abilities for more ac-
curate navigation, DL approaches have demonstrated a sig-
nificant impact in improving sensor fusion. Li et al. [53]
introduced a novel recurrent convolutional neural network
(RCNN)-based architecture for scan-to-scan laser/inertial data
fusion for pose estimation. Additionally, Srinivasan et al. [54]
proposed an end-to-end RNN-based approach that utilizes
IMU data along with wheel odometry sensor and motor
current data to estimate velocity, following an investigation
into the extreme dynamics of an autonomous race car. In the

”GALNet” framework, the authors utilized inertial, kinematic,
and wheel velocity data to train an LSTM-based network
that regressed the relative pose of a car [55]. In [56], a
smartphone gyroscope, magnetometer, and gravity sensor were
integrated to train ”XDRNet” architecture. Using 1DCNN, the
network regresses vehicle speed and heading changes and, as a
consequence, reduces inertial positioning error drift. Moreover,
Liu et al. presented a hybrid CNN-LSTM-based network that
integrates a dual-antenna satellite receiver and MEMS IMU to
forecast the residual of the position, velocity, and orientation
at each time step [57]. In the case of an agricultural wheeled
robot, velocity estimation was achieved by integrating inertial
readings, magnetometer data, and the absolute values of the
mean discrete Fourier transform coefficients of accelerometer
norms within a TCN architecture. These velocity estimates
were subsequently utilized in INS/GNSS fusion to estimate
2D position and velocity, reducing the reliance on GNSS
measurements, particularly in GNSS-denied environments, and
demonstrating good performance in such scenarios [58].

B. Aided Inertial Navigation

It has been demonstrated that using a filter such as the
extended KF (EKF) is a common approach to achieving a
high level of accuracy and reliability in sensor fusion. Aside
from providing a navigation solution, the filter also offers
insight into the propagation of navigation uncertainty over
time. Consequently, DL methods have shown great impact
in addressing different aspects of the filter that significantly
influence the solution. Hosseinyalamdary proposed a deep KF
[59], which includes a modeling step alongside the prediction
and update steps of the EKF. This addition corrects IMU
positioning and models IMU errors, with GNSS measurements
used to learn IMU error models using RNN and LSTM
methods. In the absence of GNSS observations, the trained
model predicts the IMU errors. Furthermore, SL-SRCKF (self-
learning square-root-cubature KF) employs an LSTM-based
network to continuously obtain observation vectors during
GNSS outages, learning the relationship between observation
vectors and internal filter parameters to enhance the accu-
racy of integrated MEMS-INS/GNSS navigation systems [60].
Additionally, DL methods identify specific scenarios in the
inertial data that may prevent the navigation solution from
accumulating errors. Using RNN, a zero velocity situation or
no lateral slip could be identified and incorporated later on
into a KF for localization processes [61].
The literature indicates that the covariance noise matrix plays
an important role in the KF, and therefore DL methods were
it consistently. According to Brossard,
employed to adapt
Barrau, & Bonnabel, a CNN-based method was used to
dynamically adapt the covariance noise matrix for an invariant-
EKF using moderate-cost IMU measurements [62]. Previously,
in [63], the authors devised a method that combined Gaussian
processes with RBF neural networks and stochastic variational
inference. This approach aimed to enhance a state-space
dynamical model’s propagation and measurement functions
by learning residual errors between physical predictions and
ground truth. Moreover, the study demonstrated how these

4

corrections could be utilized in the design of EKFs. An
alternative method of estimating the process noise covariance
relies on reinforcement learning, as explained in [64], which
uses an adaptive KF to determine position, velocity, and
orientation. In [65], not only the parameters of measurement
noise covariances but also the parameters of process noise
covariances were regressed. These parameters can be more
accurately estimated using a multitask TCN, resulting in
higher position accuracy than traditional GNSS/INS-integrated
navigation systems. The authors in [66] introduced a resid-
ual network incorporating an attention mechanism to predict
individual velocity elements of the noise covariance matrix.
As a result of the empirical study, it has been demonstrated
that adjusting the non-holonomic constraint uncertainty during
large dynamic vehicle motions rather than strictly setting the
lateral and vertical velocities to zero could improve positioning
accuracy under large dynamic motions.

TABLE II: A summary of thirty-five papers describing DL
inertial sensing and sensor fusion for land vehicles, categorized
by their improvement goals.

Improvement Goals

Position

Velocity

Orientation

Filter Parameters

Papers
17, 18, 19, 20, 23, 24, 25, 44
21, 22, 27, 43, 50, 51, 53, 55
57
20, 21, 44, 45, 46, 47, 49, 54
48, 52, 56, 57, 58
23, 24, 25, 44, 46, 47, 49, 55
48, 50, 51, 53, 56, 57, 61
26, 43, 59, 62, 63, 64, 65, 66
60

III. AERIAL VEHICLE INERTIAL SENSING

A. Pure Inertial Navigation

A number of the papers examined visual-inertial odometry as
a tool for aerial inertial navigation. Clark et al. [67] developed
the ”VINet” architecture. It comprises LSTM blocks that
process camera output at the camera rate and IMU LSTM
blocks that process data at the IMU rate. This study used
deep learning to determine a micro air vehicle’s (MAV’s)
orientation. In [68], a similar approach was employed; how-
ever,
the platform was not an MAV, but rather a bigger
and heavier unmanned aerial vehicle (UAV). Another vision-
inertial fusion study was conducted in [69] in which a camera
and IMU sensor fusion method were used to estimate the
position of an unmanned aircraft system (UAS) using a CNN-
LSTM-based network known as ”HVIOnet”, which stands
for hybrid visual-inertial odometry network. A more complex
method was introduced by Yusefi et al. where an end-to-end,
multi-model, DL-based, monocular, visual-inertial localization
system was utilized to resolve the global pose regression
problem for UAVs in indoor environments. Using the proposed
deep RCNN, experimental findings demonstrate an impressive
degree of time efficiency, as well as a high degree of accuracy
in UAV indoor localization [70].

5

for integrated INS/GNSS navigation in the event of GNSS
outages[81, 82, 83]. A similar approach to deal with scenarios
of denied GNSS environments was implemented by [84], in
which a GRU-based network was used to estimate position and
velocity. A novel method known as ”QuadNet” was proposed
by Shurin & Klein in [85]. They enforced the quadrotor motion
to be periodic and utilized its inertial readings to develop
1DCNN and LSTM methods for regression of the distance
and altitude changes of the quadrotor. In the study by Hurwitz
and Klein, the ”QuadNet” architecture was revisited to explore
the benefits of using multiple IMUs and to devise effective
methods for leveraging the excess inertial data. In a different
paper and scenario involving GNSS-denied environments, the
researchers employed a combination of optical odometry, radar
height estimates, and multi-sensory data fusion. To enhance
optical flow velocity estimates in these challenging conditions,
they utilized an LSTM network alongside angular velocity
readings from the IMU to predict velocity increments [86].

B. Aided Inertial Navigation

To enhance the quality of Kalman attitude estimates, Al-
Sharman et al. proposed a fully connected network in [71].
This network takes the Kalman state estimates, derived from
inertial readings and control vectors, as inputs, and regresses
the UAV attitude. Figure 3 illustrates the approach based on the
one presented in the aforementioned paper. Another recurring
approach involves predicting noise covariance information us-
ing DL. In [87], the authors introduced a CNN-based adaptive
Kalman filter designed to enhance high-speed navigation with
low-cost IMUs. Their approach employs a 1DCNN to predict
noise covariance information for 3D acceleration and angular
velocity, utilizing windowed inertial measurements. The aim is
to outperform classical Kalman filters and Sage-Husa adaptive
filters in high dynamic conditions. In a subsequent paper,
Or & Klein [88] developed a data-driven, adaptive noise
covariance approach for an error state EKF in INS/GNSS
fusion. Using a 1DCNN, they were able to estimate the process
noise covariance matrix and use the information to provide
a better navigation solution for a quadrotor drone. Solodar
and Klein [89] proposed VIO-DualProNet, consisting of two
1DCNNs tasked with estimating the covariance matrices of the
accelerometer and gyroscope, respectively. These estimates are
utilized to dynamically assess the process noise covariance
matrix, enhancing the optimization process in visual-inertial
odometry. Experimental findings on MAVs demonstrate a 25%
enhancement
in absolute trajectory error compared to the
baseline approach.

IV. MARITIME VEHICLE INERTIAL SENSING

A. Pure Inertial Navigation

Zhang et al. [91, 92] were the first to apply deep learning tech-
niques to autonomous underwater vehicle (AUV) navigation.
To regress the position displacements of an AUV, the authors
used an LSTM-based network trained over GNSS data that
was utilized as the position displacement training targets. The

Fig. 3: The figure illustrates the architecture presented in
[71], which is based on a simple MLP network. This network
utilizes the estimated attitude states from the Kalman filter and
enhances them through training with data containing accurate
reference attitude information.

For assessing a vehicle’s attitude with only inertial sensing,
Liu et al. employed an LSTM-based network based on IMU
data from a UAV [72]. While in [73], the authors utilized
a hybrid, more complex network that incorporates CNN and
LSTM blocks to estimate MAV pose utilizing the current
position and unit quaternion. Esfahani et al. introduced an
inertial odometry network named ”AbolDeepIO” [74]. Based
on LSTM, this network architecture leverages IMU readings
for inertial odometry in MAVs. In their study, they compared
the performance of AbolDeepIO with that of ”VINet” [67],
demonstrating superior results in MAV data analysis. Seven
sub-architectures were also tested and evaluated. As a follow-
up to ”AbolDeepIO”, the authors brought forward ”OriNet”,
which is also based on LSTM and capable of estimating the
full 3D orientation of a flying robot with a single particular
IMU in the quaternion form [75]. A robust inertial attitude es-
timator called ”RIANN” was also proposed, a network whose
name stands for Robust IMU-based Attitude Neural Network.
Several motions, including MAV motion, were regressed using
a gated recurrent units (GRUs) network. As well as proposing
three domain-specific advances in neural networks for inertial
attitude estimation, they also propose two methods that enable
neural networks to handle a wide variety of sampling rates
[76]. It has been suggested by Chumuang et al. [77] that CNNs
and LSTMs are both effective for predicting the orientation of
a MAV, the former using the quaternions predicted from data
from the IMU using Madgwick’s adaptive algorithm [78], and
the latter using raw gyroscope measurements. For improving
MAV navigation, rather than using two separate networks,
the authors in [79] suggested three models including CNN,
RNN, and a CNN and LSTM hybrid model, and performed a
comparison amongst them.
In aerial navigation, as in other areas, GNSS signals can be
useful when integrating with the INS, and in the absence
of these signals, the inertial navigation solution drifts. To
achieve better performance than traditional GNSS/INS fusion,
an LSTM-based network was proposed in [80] to estimate
the 3D position of an aerial vehicle. When the aerial vehicle
encounters GNSS-denied environments, DL approaches are
used to compensate. Continuing their research in [72], as dis-
cussed above, Liu et al. proposed a 1DCNN/GRU hybrid deep
learning model that predicts the GNSS position increments

6

Fig. 4: The figure depicts the architecture based on A-KIT introduced in [90], where an adaptive Kalman-informed transformer
is employed. In this approach, inertial data along with observable states, such as position from GNSS, are fed through the
block diagram presented. The output obtained from this process provides the scale factors required for dynamically estimating
the process noise covariance matrix of the extended Kalman filter.

TABLE III: A summary of twenty-two papers describing
DL inertial sensing and sensor fusion for aerial vehicles,
categorized by their improvement goals.

Improvement Goals

Position

Velocity

Orientation

Filter Parameters

Papers
69, 79, 80, 81, 82, 83, 84, 85
70, 73
79, 84
67, 68, 70, 72, 73, 74, 75, 76
77, 79, 85, 86
71, 87, 88, 89

output of this network is incorporated into EKF for the purpose
of making the position directly observable. Later, the authors
developed a system called ”NavNet”, which utilizes data from
the IMU and DVL sensors through a deep learning framework
using LSTM and attention mechanisms to regress the position
displacement of an AUV and compares it to the EKF and
UKF [93]. Further improvements and revisions were made in
[94], which used TCN blocks instead of LSTM blocks. As
a way of rectifying the error accumulation in the navigation
system, Ma et al. proposed a similar procedure, as previously
mentioned, and developed an adaptive navigation algorithm
for AUV navigation that uses deep learning to generate low-
frequency position information as a method of generating low-
frequency positioning information. Based on LSTM blocks,
the network receives velocity measurements from the DVL and
Euler angles from the attitude and heading reference system
(AHRS) [95]. Weizman et al. [96] investigated the maneuvers
of ocean gliders and utilized their periodic motion to introduce
GilderNet, a 1DCNN that regresses glider distance and depth
based solely on inertial sensors and inspired by methods from
pedestrian dead reckoning.

B. Aided Inertial Navigation

A task such as navigation on or underwater may encounter
difficulties due to the dynamics of the environment or the
inaccessibility of GNSS signals. In [97] the authors used a
hybrid TCN-LSTM network to predict the pitch and heave
movement of a ship in different challenging scenarios. A
fully connected network is suggested in [98] to improve AUV
navigation in rapidly changing environments, such as in waves
near or on the surface. This network is based on data from
an accelerometer and is used to predict the pitch angle. The

Kalman filter, neural network, and velocity compensation are
then combined in the ”NN-DR” method to provide a more
accurate navigation solution.
The DVL is used in underwater applications as a sensor to
assist in navigation, similar to GNSS data used by above-water
applications. Several papers have been published examining
scenarios of DVL failure. There was, for example, a proposal
in [99] to aid dead-reckoning navigation for AUVs with limited
sensor capabilities. Using RNN architecture, the algorithm
predicts relative velocities based on the data obtained from
the IMU, pressure sensors, and control actions of the actu-
ators on the AUV. In [100] the Nonlinear AutoRegressive
with Exogenous Input (NARX) approach is used in cases
where DVL malfunctions occur to determine the velocity
measurements using INS data. For receiving the navigation
solution, the output of the network is integrated into a robust
Kalman filter (RKF). Cohen & Klein proposed ”BeamsNet”,
which replaces the model-based approach to derive the AUV
velocity measurements out of the DVL raw beam measure-
ments using 1DCNN that uses inertial readings [101]. The
authors continued the work by looking at cases of partial DVL
measurements and succeeded in recovering the velocity with a
similar architecture called ”LiBeamsNet” [102]. In the case of
a complete DVL outage, in [103] the authors introduced ”ST-
BeamsNet”, which is a Set-Transformer based network that
uses inertial reading and past DVL measurements to regress
the current velocity.
Lately, Topini et al. [104] conducted an experimental com-
parison of data-driven strategies for AUV navigation in
DVL-denied environments where they compared MLP, CNN,
LSTM, and hybrid CNN-LSTM networks to predict the veloc-
ity of the AUV. According to the authors of [105], the RBF
network can be augmented with error state KF to improve
the state estimation of an underwater vehicle. Through the
application of the RBF neural network, the proposed algorithm
compensates for the lack of error state KF performance by
enhancing innovation error terms. Or & Klein [88, 106, 107]
developed an adaptive EKF for velocity updates in INS/DVL
fusions. Initially, they demonstrated that by correcting the
noise covariance matrix using 1DCNN to predict the variance
in each sample time using a classification problem, they could
significantly improve navigation results. In recent work, the
authors introduced ”ProNet”, which uses regression instead
of classification to accomplish the same task. In [90], an

7

adaptive Kalman-informed transform (A-KIT) was presented.
This method utilized inertial readings along with Kalman
estimates of the velocity vector within a transformer-based
network to regress the scale factors required for adjusting
the process noise covariance matrix. The results demonstrated
superior performance compared to standard EKF and various
adaptive versions. Additionally, a Kalman-informed loss was
introduced to ensure that the output aligns with the Kalman
theory. The A-KIT approach is illustrated in Fig 4.

TABLE IV: A summary of nineteen papers describing DL
inertial sensing and sensor fusion for maritime vehicles, cate-
gorized by their improvement goals.

Yuan et al. proposed ”IMUDB” as a self-supervised IMU
denoising method inspired by natural
language processing
techniques. This approach addresses the challenge of obtaining
sufficient and accurate annotations for supervised learning
while achieving promising results [120]. Engelsman et al.
developed a bidirectional LSTM-based network specifically
for gyrocompassing, particularly suitable for low-performance
gyroscopes affected by the limited signal strength of Earth’s
rotation rate, which is often overshadowed by gyro noise
[121]. They subsequently demonstrated the effectiveness of
this approach in unmanned underwater vehicle applications
[122].

Improvement Goals
Position
Velocity
Orientation
Filter Parameters

Papers
91, 92, 93, 94, 95, 96, 97, 98
98, 99, 100, 101, 102, 103, 104
97, 98
88, 90, 105, 106, 107

V. CALIBRATION AND DENOISING
Since the INS is based on the integration of inertial data over
time, it accumulates errors due to structured errors in the
sensors. Calibration and denoising are crucial to minimizing
these errors. In Chen et al. [108], deep learning was used
for the first time to reduce IMU errors. IMU data, containing
deterministic and random errors, is fed as input to CNN,
which filters the data, an illustration van be seen in Fig. 5.
According to Engelsman & Klein [109, 110], an LSTM-based
network can be used for de-noising accelerometer signals and
a CNN-based network can be used to eliminate bias in low-
cost gyroscopes.
Apart from the papers mentioned above, the majority of re-
search focuses on the denoising and calibration of gyroscopes.
A series of papers [111, 112, 113] examined the denoising of
gyroscope data by utilizing various variations of RNNs. One
paper demonstrated the performance of a simple RNN struc-
ture, while the others utilized LSTMs. A comparison was made
between LSTM, GRU, and hybrid LSTM-GRU approaches
for gyroscope denoising in [114]. Additional comparisons be-
tween GRU, LSTM, and hybrid GRU-LSTM were conducted
in [115]. In Brossard et al. [116], a deep learning method is
presented for reducing the gyroscope noise in order to achieve
accurate attitude estimations utilizing a low-cost IMU. For
feature extraction, a dilated convolutional network was used
and for training on orientation increments, an appropriate loss
function was utilized. Various CNN-based architectures have
been explored to address gyroscope corrections. One study
showcased a denoising autoencoder architecture, constructed
on a deep convolutional model, aimed at restoring clean and
undistorted output from corrupted data. It was found that
the KF angle prediction was boosted in this scenario [117].
Furthermore, a TCN and 1DCNN were integrated for MEMS
gyroscope calibration in [118]. Liu et al. introduced ”LGC-
Net” as a method for extracting local and global characteristics
from IMU measurements to regress gyroscope compensation
components dynamically. This model utilizes special convolu-
tion layers and attention mechanisms for this purpose [119].

Fig. 5: The figure is based on the architecture introduced
in [108], where a CNN architecture is proposed to address
IMU errors by analyzing a window of inertial measurements,
enabling the detection and removal of noisy features. The
block diagram depicts noisy data passing through convolu-
tional layers, with subsequent smoothing or filtering of the
input.

VI. DISCUSSION

In this section, we delve into the survey findings, summarizing
the contributions, which encompass common techniques and
approaches. Subsequently, we weigh the pros and cons of
using DL approaches for inertial navigation tasks. Finally, we
explore future trends in inertial navigation with deep learning..

A. Summary

The purpose of this section is to provide a comprehensive
trends in DL methods for inertial
analysis of the current
sensing and sensor fusion, drawing insights from previously
discussed studies.
Taking a closer look at the most common courses of action,
it appears there are four repeating baseline approaches to
embed inertial sensing an DL, as illustrated in Fig. 6. The
first approach involves inserting the inertial data into a DL
architecture and regressing one or more states of the full
navigation solution as shown in Fig. 6a. Other studies took a
different approach, focusing on analyzing the desired residual
or delta required to update the current measurements, rather
than regressing the entire state of navigation components.
Analyzing these residuals has proven to be more effective,
particularly due to the high-rate solutions provided by the
inertial sensors, which often hover close to zero with a small

8

(a) Using an end-to-end DL approach to regress the full
state of the vehicle.

(b) Using an end-to-end DL approach to regress the residual
between the current state and the previous one of the vehicle.

(c) Implementing sensor fusing with an end-to-end DL block to
regress the full state or the required increment.

(d) In sensor fusion scenarios, DL methods are applied
to obtain one or more filter parameters.

Fig. 6: Different techniques for improving inertial navigation using DL

standard deviation, resembling a normal distribution. This
characteristic makes it easier for the network to handle the
problem efficiently. An illustration of this concept is depicted
in Fig. 6b.
Rather than relying solely on inertial data, and as discussed
before, most navigation solutions integrate inertial data with
other sensors to provide a more accurate result. Fig. 6c and
Fig. 6d show how DL is incorporated in the sensor fusion
operation. The former uses both the inertial data and the
aiding measurements as input to the end-to-end network to
give the navigation solution. The latter target parameters of
the nonlinear filter, which are responsible for the sensor fusion,
such as the noise covariance matrix estimation.
The methods outlined in this paper are applicable across all
three domains: land, aerial, and maritime, as the navigation
solution remains consistent regardless of the platform or
environment. While the dynamics may vary between these
domains, the fundamental navigation principles remain the
same. Therefore, for example, DL-based orientation estimation
developed for land vehicles could be adapted for use in aerial
or maritime applications with appropriate adjustments for the
specific dynamics of each domain. By examining the details
of the survey, we determined what are the most common goals
that current research focuses on improving, and present them
in a pie chart, in Fig. 7. According to the chart, 79% of the
papers focus on improving position, velocity, and orientation,
while 21% addressed filter parameter improvement. Most of

the latter papers were published within the past three years.
In addition to the initial analysis, we observed the general
DL architectures that have been employed. We identified
four distinct architectural streams: MLP, CNN, RNN, and
others. MLP includes only fully connected networks, CNN
includes networks such as 1DCNN and TCN, RNN includes
LSTM and GRU, and ’others’ encompass architectures such as
transformers, reinforcement learning, and more, which are not
included in the previously mentioned categories. As shown
the networks are also divided into single and
in Fig. 8,
combined networks, where combined refers to architectures
that comprise more than one method, such as CNN-RNN.
The bar plot indicates that the primary architecture is RNN,
along with its variations. This observation is sensible given that
this architecture was explicitly developed for time-series prob-
lems, enabling it to detect temporal dependencies effectively.
Furthermore, CNN methods play a significant role in inertial
navigation, establishing themselves as the second most popular
architecture in the field. In certain scenarios, they showcase
superior accuracy when compared to RNNs. Their capability
to excel at extracting informative features from small time
windows, typically spanning just a few seconds, makes them
particularly effective. Moreover, CNN architectures serve as
the backbone for numerous denoising and calibration methods,
underscoring their versatility and effectiveness within this
domain. The MLP is a fundamental architecture and was one
of the earliest to be adopted in inertial navigation. However,

while it is common for modern networks to incorporate FC
layers in the final block,
the MLP itself does not excel
at extracting sufficient features independently. Its simplicity
may limit its effectiveness in capturing complex patterns and
relationships within inertial navigation data. Despite its current
status as the least popular, the ’others’ category is gaining
momentum, largely due to its newfound recognition. With
the advancements in natural language processing, architectures
such as transformers and bidirectional encoder representa-
tions from transformers (BERT) have started to surface in
recent literature, displaying significant potential and delivering
promising results. Notably, they have demonstrated superiority
over MLPs, CNNs, and RNNs in various fields, marking a
notable shift in the landscape of NN architectures.

Fig. 7: DL goals in improving the navigation performance.

Fig. 8: Common DL architectures for improving navigation
tasks, divided into single architectures and combined architec-
tures.

B. Pros and Cons

There are a number of advantages to using DL methods in
inertial navigation, including:

1) Modeling Nonlinear Problems - Inertial navigation
presents a nonlinear challenge where DL methods excel,
as supported by survey findings. DL approaches have
demonstrated effectiveness across various aspects of in-
ertial navigation and have shown practical impact across
different platforms and domains.

9

2) Parameter Estimation - In nonlinear inertial sensor
fusion,
the survey indicates that employing DL for
estimating various filter parameters, such as process or
measurement noise covariance, can markedly enhance
performance.

3) Robustness - DL approaches exhibit the capacity to
generalize across diverse scenarios, a critical attribute
in navigation tasks. Variations in platform maneuvers,
coupled with external factors like wind, waves, and
obstacles, can be effectively learned and handled through
DL techniques.

4) Real-time Processing - The advancement in computa-
tional hardware, coupled with the temporal nature of
inertial data, makes DL methods particularly efficient.
Unlike image processing tasks, which demand heavier
computational loads, inertial data processing requires
fewer computational resources. Once trained, DL models
can operate in real-time, offering swift and effective
navigation solutions.

5) Multimodal Integration - Inertial navigation often in-
volves INS fusion with various sensors like GNSS and
DVL, among others. The DL approaches highlighted in
this survey illustrate how to fuse these sensors using
end-to-end methods and hybrid approaches to improve
the overall system performance.

As well as the above benefits, there are some cons that need
to be taken into account as well. Among them are:

1) Data Dependency - DL models necessitate substantial
amounts of high-quality data to effectively general-
ize the problem. Navigation presents a challenge as
each platform exhibits unique dynamics and maneuvers.
Training a model on specific dynamics may lead to
overfitting, and variations in environmental conditions
such as weather, wind, and temperature can influence
sensor performance and dynamics, requiring adaptable
learning approaches or more data.

2) Computational Resources -Training DL models typi-
cally requires significant computational resources, such
as high-performance GPUs or TPUs, which are often
characterized by high costs and limited availability.
This challenge is particularly relevant in the context
of the increasing adoption of networks designed for
large language models, such as transformers, in inertial
sensing and sensor fusion applications.

3) Interpretability - DL models are often regarded as
”Black Boxes,” meaning that while the inputs and out-
puts are known, the internal workings of the learning
system remain opaque. This presents a significant chal-
lenge in safety-critical navigation applications where
users rely on understanding and trusting the system’s
behavior.

4) Lack of Datasets and Benchmarks - Although inertial
navigation has a long history, publicly available inertial
and reference data is lacking, often of poor quality.
For example, while GNSS position references offer
accuracy with a standard deviation of a few meters,
GNSS-RTK data provides centimeter-level accuracy and

would be more appropriate as a reference. Furthermore,
the field of DL and inertial navigation lacks common
benchmarks across platforms, hindering clear indications
of improvement over time.

5) Sensor Fusion Cross-Correlation - A common ap-
proach to using DL with inertial navigation is to enhance
either the aiding updates or the actual inertial readings
by fusing the inertial data with aiding sensors such as
GNSS and DVL. While this approach often demon-
strates good performance, it sometimes introduces cross-
correlation between the sensors, which are typically
ignored. Addressing these cross-correlations poses a
challenge, as DL approaches inherently involve nonlin-
ear functions. Consequently, incorporating the network’s
output into a nonlinear filter requires careful considera-
tion of these cross-correlations.

C. Future Trends

Figure 9 depicts the burgeoning trend in the field of in-
ertial navigation aided by DL. The significant increase in
publications, evident from 2019 onwards and continuing to
rise, underscores the growing integration of DL approaches
in this domain. During the initial phase of this trend, from
2019 to 2022, conventional architectures such as MLP, CNN,
and RNN predominated. However, from 2022 onwards, there
has been a noticeable shift towards employing more complex
architectures, aligning with the broader trend in DL research.
Upon reviewing the papers included in the survey, a clear
trajectory emerges at
the intersection of DL and inertial
navigation. Previously, the focus was on employing end-to-end
models to directly predict navigation states such as position,
velocity, and orientation. However, there has been a notable
shift in recent times towards leveraging the model itself. The
shift towards leveraging DL techniques in inertial navigation
is evident in the adoption of DL for denoising and calibration
tasks, followed by the integration of refined inertial data into
the navigation filter. Additionally, there is a growing trend
towards enhancing filter parameters to achieve more accurate
estimates of the navigation solution. Rather than directly
estimating navigation components, improvements in filter pa-
rameters, such as estimating the process or measurement
noise covariance, not only enhance the navigation solution
but also contribute to the DL model’s deeper understanding
of the underlying model. Finally, while in the past, most
models relied on RNNs, CNNs, and MLPs, there is now a
trend toward employing more complex models derived from
large language models. Specific adaptations of these models
improvements over the previously
have shown significant
mentioned architectures.

VII. CONCLUSIONS

Inertial navigation has garnered significant attention over the
past decade due to the versatility of inertial sensors across
diverse platforms and environments. Historically, navigation
solutions have relied on model-based algorithms. However,
there has been a notable shift towards data-driven methods,
particularly with the increasing popularity and capabilities of

10

Fig. 9: The number of papers published from 2003 to 2023.
Each year is represented by blue stars, while the cumulative
sum of papers is depicted by the red curve.

DL techniques. This integration of DL represents a signifi-
cant advancement in the approach to developing navigation
solutions. This paper provides a comprehensive survey of DL
methods applied to inertial navigation, specifically focusing
on different platforms and practical applications. It reviewed
research conducted across three distinct domains: land, aerial,
and maritime. Additionally, the paper delves into calibration
and denoising methods within the context of inertial navigation
and DL. Furthermore, it offers insights into the trajectory of
research in this area through statistical analysis.
Our findings indicate that the majority of research in this
area has focused on land vehicles rather than aerial or mar-
itime vehicles, or on calibration and denoising techniques.
that despite differences in
However, some papers suggest
mechanics, maneuvers, etc.,
techniques can be adapted to
various platforms, as the task of navigation remains consistent
across all platforms, and data-driven networks can potentially
learn these differences. While most reviewed papers aimed
to enhance one or more aspects of the inertial navigation
algorithm for improved solutions, recent years have seen a
shift towards improving filter parameters for enhanced sensor
fusion processes and increased reliance on the algorithm,
incorporating mathematical models as well. Although leading
DL architectures have traditionally been based on RNNs and
CNNs, recent research has been inspired by approaches from
natural language processing, importing and adapting leading
architectures from that field.
In conclusion, since 2019, there has been a notable surge in the
utilization of DL methods for inertial navigation applications.
These approaches have demonstrated superior performance
compared to traditional model-based techniques, indicating
significant potential for future research in inertial sensing.
This evolution suggests a promising trajectory for further
advancements in the field of inertial navigation aided by DL
algorithms.

ACKNOWLEDGMENT

N.C.
is supported by the Maurice Hatter Foundation and
University of Haifa presidential scholarship for outstanding
students on a direct Ph.D. track.

REFERENCES

[1] D. MacKenzie, Inventing accuracy: A historical sociol-
ogy of nuclear missile guidance. MIT press, 1993.
[2] D. Titterton, J. L. Weston, and J. Weston, Strapdown

inertial navigation technology.

IET, 2004, vol. 17.

[3] A. Noureldin, T. B. Karamat, and J. Georgy, Fundamen-
tals of inertial navigation, satellite-based positioning
and their integration.
Springer Science & Business
Media, 2012.

[4] N. El-Sheimy and A. Youssef, “Inertial sensors tech-
nologies for navigation applications: State of the art
and future trends,” Satellite Navigation, vol. 1, no. 1,
pp. 1–21, 2020.

[5] K. R. Britting, Inertial navigation systems analysis.

Artech House, 2010.

[6] J. Farrell, Aided navigation: GPS with high rate sensors.

McGraw-Hill, Inc., 2008.

[7] D. Engelsman and I. Klein, “Information aided naviga-
tion: A review,” arXiv preprint arXiv:2301.01114, 2023.
[8] P. Groves, Principles of GNSS, inertial, and multisensor
integrated navigation systems, second edition. Artech
House, 2013.

[9] S. S. A. Zaidi, M. S. Ansari, A. Aslam, N. Kanwal,
M. Asghar, and B. Lee, “A survey of modern deep
learning based object detection models,” Digital Signal
Processing, p. 103514, 2022.

[10] D. W. Otter, J. R. Medina, and J. K. Kalita, “A survey
of the usages of deep learning for natural language
processing,” IEEE Transactions on Neural Networks
and Learning Systems, vol. 32, no. 2, pp. 604–624,
2020.

[11] M. Durgadevi et al., “Generative adversarial network
(GAN): a general review on different variants of GAN
and applications,” in 2021 6th International Conference
on Communication and Electronics Systems (ICCES).
IEEE, 2021, pp. 1–8.

[12] F. Zhuang, Z. Qi, K. Duan, D. Xi, Y. Zhu, H. Zhu,
H. Xiong, and Q. He, “A comprehensive survey on
transfer learning,” Proceedings of the IEEE, vol. 109,
no. 1, pp. 43–76, 2020.

[13] Y. LeCun, Y. Bengio, and G. Hinton, “Deep learning,”
Nature, vol. 521, no. 7553, pp. 436–444, 2015.
[14] I. Goodfellow, Y. Bengio, and A. Courville, Deep

learning. MIT press, 2016.

[15] P. P. Shinde and S. Shah, “A review of machine learning
and deep learning applications,” in 2018 Fourth In-
ternational Conference on Computing Communication
Control and Automation (ICCUBEA).
IEEE, 2018, pp.
1–6.

[16] M. Mahrishi, K. K. Hiran, G. Meena, and P. Sharma,
Machine learning and deep learning in real-time appli-
cations.

IGI Global, 2020.

[17] K.-W. Chiang, A. Noureldin, and N. El-Sheimy, “Mul-
tisensor integration using neuron computing for land-
vehicle navigation,” GPS Solutions, vol. 6, no. 4, pp.
209–218, 2003.

[18] A. Noureldin, A. Osman, and N. El-Sheimy, “A neuro-

11

wavelet method for multi-sensor system integration for
vehicular navigation,” Measurement Science and Tech-
nology, vol. 15, no. 2, p. 404, 2003.

[19] R. Sharaf, A. Noureldin, A. Osman, and N. El-Sheimy,
“Online INS/GPS integration with a radial basis func-
tion neural network,” IEEE Aerospace and Electronic
Systems Magazine, vol. 20, no. 3, pp. 8–14, 2005.
[20] N. El-Sheimy, K.-W. Chiang, and A. Noureldin, “The
utilization of artificial neural networks for multisensor
system integration in navigation and positioning in-
struments,” IEEE Transactions on Instrumentation and
Measurement, vol. 55, no. 5, pp. 1606–1615, 2006.
[21] A. Noureldin, A. El-Shafie, and M. Bayoumi, “GPS/INS
integration utilizing dynamic neural networks for vehic-
ular navigation,” Information Fusion, vol. 12, no. 1, pp.
48–57, 2011.

[22] X. Chen, C. Shen, W.-b. Zhang, M. Tomizuka, Y. Xu,
and K. Chiu, “Novel hybrid of strong tracking Kalman
filter and wavelet neural network for GPS/INS during
GPS outages,” Measurement, vol. 46, no. 10, pp. 3847–
3854, 2013.

[23] K.-W. Chiang, A. Noureldin, and N. El-Sheimy, “Con-
structive neural-networks-based MEMS/GPS integra-
tion scheme,” IEEE Transactions on Aerospace and
Electronic Systems, vol. 44, no. 2, pp. 582–594, 2008.
[24] K.-W. Chiang, H.-W. Chang, C.-Y. Li, and Y.-W. Huang,
“An artificial neural network embedded position and
orientation determination algorithm for low cost MEMS
INS/GPS integrated sensors,” Sensors, vol. 9, no. 4, pp.
2586–2610, 2009.

[25] K.-W. Chiang and H.-W. Chang, “Intelligent sensor
positioning and orientation through constructive neural
network-embedded INS/GPS integration algorithms,”
Sensors, vol. 10, no. 10, pp. 9252–9285, 2010.

[26] J. J. Wang, W. Ding, and J. Wang, “Improving adaptive
Kalman Filter in GPS/SDINS integration with neural
network,” in Proceedings of the 20th International Tech-
nical Meeting of the Satellite Division of The Institute
of Navigation (ION GNSS 2007), 2007, pp. 571–578.

[27] M. Malleswaran, V. Vaidehi, A. Saravanaselvan, and
M. Mohankumar, “Performance analysis of various ar-
tificial intelligent neural networks for GPS/INS integra-
tion,” Applied Artificial Intelligence, vol. 27, no. 5, pp.
367–407, 2013.

[28] S. Silvestrini and M. Lavagna, “Deep learning and artifi-
cial neural networks for spacecraft dynamics, navigation
and control,” Drones, vol. 6, no. 10, p. 270, 2022.
[29] J. Song, D. Rondao, and N. Aouf, “Deep learning-based
spacecraft relative navigation methods: A survey,” Acta
Astronautica, vol. 191, pp. 22–40, 2022.

[30] H. Jiang, H. Wang, W.-Y. Yau, and K.-W. Wan, “A
brief survey: Deep reinforcement learning in mobile
robot navigation,” in 2020 15th IEEE Conference on
Industrial Electronics and Applications (ICIEA). IEEE,
2020, pp. 592–597.

[31] K. Zhu and T. Zhang, “Deep reinforcement learning
based mobile robot navigation: A review,” Tsinghua
Science and Technology, vol. 26, no. 5, pp. 674–691,

2021.

[32] F. AlMahamid and K. Grolinger, “Autonomous un-
manned aerial vehicle navigation using reinforcement
learning: A systematic review,” Engineering Applica-
tions of Artificial Intelligence, vol. 115, p. 105321,
2022.

[33] X. Ye and Y. Yang, “From seeing to moving: A survey
on learning for visual indoor navigation (VIN),” arXiv
preprint arXiv:2002.11310, 2020.

[34] F. Zeng, C. Wang, and S. S. Ge, “A survey on visual
navigation for artificial agents with deep reinforcement
learning,” IEEE Access, vol. 8, pp. 135 426–135 442,
2020.

[35] D. C. Guastella and G. Muscato, “Learning-based meth-
ods of perception and navigation for ground vehicles in
unstructured environments: A review,” Sensors, vol. 21,
no. 1, p. 73, 2020.

[36] F. Zhu, Y. Zhu, V. Lee, X. Liang, and X. Chang, “Deep
learning for embodied vision navigation: A survey,”
arXiv preprint arXiv:2108.04097, 2021.

[37] Y. Tang, C. Zhao, J. Wang, C. Zhang, Q. Sun, W. X.
Zheng, W. Du, F. Qian, and J. Kurths, “Perception and
navigation in autonomous systems in the era of learning:
A survey,” IEEE Transactions on Neural Networks and
Learning Systems, 2022.

[38] S. Azimi, J. Salokannel, S. Lafond, J. Lilius, M. Sa-
lokorpi, and I. Porres, “A survey of machine learn-
ing approaches for surface maritime navigation,” in
Maritime Transport VIII: proceedings of the 8th Inter-
national Conference on Maritime Transport: Technol-
ogy, Innovation and Research: Maritime Transport’20.
Barcelona, 2020, pp. 103–117.

[39] Y. Li, R. Chen, X. Niu, Y. Zhuang, Z. Gao, X. Hu,
and N. El-Sheimy, “Inertial sensing meets machine
learning: opportunity or challenge?” IEEE Transactions
on Intelligent Transportation Systems, 2021.

[40] P. Roy and C. Chowdhury, “A survey of machine learn-
ing techniques for indoor localization and navigation
systems,” Journal of Intelligent & Robotic Systems, vol.
101, no. 3, p. 63, 2021.

[41] A. A. Golroudbari and M. H. Sabour, “Recent ad-
vancements in deep learning applications and methods
for autonomous navigation–A comprehensive review,”
arXiv preprint arXiv:2302.11089, 2023.

[42] C. Chen, “Deep learning for inertial positioning: A
survey,” arXiv preprint arXiv:2303.03757, 2023.
[43] C. Shen, Y. Zhang, J. Tang, H. Cao, and J. Liu, “Dual-
optimization for a MEMS-INS/GPS system during GPS
outages based on the cubature Kalman filter and neural
networks,” Mechanical Systems and Signal Processing,
vol. 133, p. 106222, 2019.

[44] S. Lu, Y. Gong, H. Luo, F. Zhao, Z. Li, and
J. Jiang, “Heterogeneous multi-task learning for mul-
tiple pseudo-measurement estimation to bridge GPS
outages,” IEEE Transactions on Instrumentation and
Measurement, vol. 70, pp. 1–16, 2020.

[45] R. Karlsson and G. Hendeby, “Speed estimation from
vibrations using a deep learning CNN approach,” IEEE

12

Sensors Letters, vol. 5, no. 3, pp. 1–4, 2021.

[46] Y. Tong, S. Zhu, Q. Zhong, R. Gao, C. Li, and
L. Liu, “Smartphone-based vehicle tracking without
GPS: Experience and improvements,” in 2021 IEEE
27th International Conference on Parallel and Dis-
tributed Systems (ICPADS).
IEEE, 2021, pp. 209–216.
[47] Y. Tong, S. Zhu, X. Ren, Q. Zhong, D. Tao, C. Li,
L. Liu, and R. Gao, “Vehicle inertial
tracking via
mobile crowdsensing: Experience and enhancement,”
IEEE Transactions on Instrumentation and Measure-
ment, vol. 71, pp. 1–13, 2022.

[48] B. Zhou, Z. Gu, F. Gu, P. Wu, C. Yang, X. Liu,
L. Li, Y. Li, and Q. Li, “DeepVIP: Deep learning-based
vehicle indoor positioning using smartphones,” IEEE
Transactions on Vehicular Technology, vol. 71, no. 12,
pp. 13 299–13 309, 2022.

[49] X. Zhao, C. Deng, X. Kong, J. Xu, and Y. Liu, “Learn-
ing to compensate for the drift and error of gyroscope in
vehicle localization,” in 2020 IEEE Intelligent Vehicles
Symposium (IV).

IEEE, 2020, pp. 852–857.

[50] Z. Fei, S. Jia, and Q. Li, “Research on GNSS/DR
method based on B-spline and optimized BP neural
network,” in 2021 IEEE 33rd International Conference
on Tools with Artificial Intelligence (ICTAI).
IEEE,
2021, pp. 161–168.

[51] R. Gao, X. Xiao, S. Zhu, W. Xing, C. Li, L. Liu,
L. Ma, and H. Chai, “Glow in the dark: Smartphone
inertial odometry for vehicle tracking in GPS blocked
environments,” IEEE Internet of Things Journal, vol. 8,
no. 16, pp. 12 955–12 967, 2021.

[52] M. Freydin and B. Or, “Learning car speed using inertial
sensors for dead reckoning navigation,” IEEE Sensors
Letters, vol. 6, no. 9, pp. 1–4, 2022.

[53] C. Li, S. Wang, Y. Zhuang, and F. Yan, “Deep sensor
fusion between 2D laser scanner and IMU for mobile
localization,” IEEE Sensors Journal, vol. 21,
robot
no. 6, pp. 8501–8509, 2019.

[54] S. Srinivasan, I. Sa, A. Zyner, V. Reijgwart, M. I. Valls,
and R. Siegwart, “End-to-end velocity estimation for
autonomous racing,” IEEE Robotics and Automation
Letters, vol. 5, no. 4, pp. 6869–6875, 2020.

[55] R. C. Mendoza, B. Cao, D. Goehring, and R. Ro-
jas, “GALNet: An end-to-end deep neural network for
ground localization of autonomous cars.” in ROBOVIS,
2020, pp. 39–50.

[56] B. Zhou, P. Wu, Z. Gu, Z. Wu, and C. Yang, “XDR-
Net: Deep learning-based pedestrian and vehicle dead
reckoning using smartphones,” in 2022 IEEE 12th Inter-
national Conference on Indoor Positioning and Indoor
Navigation (IPIN).

IEEE, 2022, pp. 1–8.

[57] N. Liu, Z. Hui, Z. Su, L. Qiao, and Y. Dong, “Integrated
navigation on vehicle based on low-cost SINS/GNSS
using deep learning,” Wireless Personal Communica-
tions, vol. 126, no. 3, pp. 2043–2064, 2022.

[58] Y. Du, S. S. Saha, S. S. Sandha, A. Lovekin, J. Wu,
S. Siddharth, M. Chowdhary, M. K. Jawed, and M. Sri-
vastava, “Neural-Kalman GNSS/INS navigation for
precision agriculture,” in International Conference on

Robotics and Automation (ICRA), 2023.

[59] S. Hosseinyalamdary, “Deep Kalman filter: Simul-
integration and modelling; A
taneous multi-sensor
GNSS/IMU case study,” Sensors, vol. 18, no. 5, p. 1316,
2018.

[60] C. Shen, Y. Zhang, X. Guo, X. Chen, H. Cao, J. Tang,
J. Li, and J. Liu, “Seamless GPS/inertial navigation sys-
tem based on self-learning square-root cubature Kalman
filter,” IEEE Transactions on Industrial Electronics,
vol. 68, no. 1, pp. 499–508, 2020.

[61] M. Brossard, A. Barrau, and S. Bonnabel, “RINS-
W: Robust inertial navigation system on wheels,” in
2019 IEEE/RSJ International Conference on Intelligent
Robots and Systems (IROS).
IEEE, 2019, pp. 2068–
2075.

[62] ——, “AI-IMU dead-reckoning,” IEEE Transactions on

Intelligent Vehicles, vol. 5, no. 4, pp. 585–595, 2020.

[63] M. Brossard and S. Bonnabel, “Learning wheel odom-
etry and IMU errors for localization,” in 2019 Interna-
tional Conference on Robotics and Automation (ICRA).
IEEE, 2019, pp. 291–297.

[64] X. Gao, H. Luo, B. Ning, F. Zhao, L. Bao, Y. Gong,
Y. Xiao, and J. Jiang, “RL-AKF: An adaptive Kalman
filter navigation algorithm based on reinforcement
learning for ground vehicles,” Remote Sensing, vol. 12,
no. 11, p. 1704, 2020.

[65] F. Wu, H. Luo, H. Jia, F. Zhao, Y. Xiao, and X. Gao,
“Predicting the noise covariance with a multitask learn-
ing model for Kalman filter-based GNSS/INS integrated
navigation,” IEEE Transactions on Instrumentation and
Measurement, vol. 70, pp. 1–13, 2020.

[66] Y. Xiao, H. Luo, F. Zhao, F. Wu, X. Gao, Q. Wang, and
L. Cui, “Residual attention network-based confidence
estimation algorithm for non-holonomic constraint in
GNSS/INS integrated navigation system,” IEEE Trans-
actions on Vehicular Technology, vol. 70, no. 11, pp.
11 404–11 418, 2021.

[67] R. Clark, S. Wang, H. Wen, A. Markham, and
N. Trigoni, “Vinet: Visual-inertial odometry as a
sequence-to-sequence learning problem,” in Proceed-
ings of the AAAI Conference on Artificial Intelligence,
vol. 31, no. 1, 2017.

[68] F. Baldini, A. Anandkumar, and R. M. Murray, “Learn-
ing pose estimation for UAV autonomous navigation
and landing using visual-inertial sensor data,” in 2020
American Control Conference (ACC).
IEEE, 2020, pp.
2961–2966.

[69] M. F. Aslan, A. Durdu, A. Yusefi, and A. Yilmaz,
“HVIOnet: A deep learning based hybrid visual–inertial
odometry approach for unmanned aerial system position
estimation,” Neural Networks, vol. 155, pp. 461–474,
2022.

[70] A. Yusefi, A. Durdu, M. F. Aslan, and C. Sungur,
“LSTM and filter based comparison analysis for indoor
global localization in UAVs,” IEEE Access, vol. 9, pp.
10 054–10 069, 2021.

13

learning-based neural network training for state estima-
tion enhancement: Application to attitude estimation,”
IEEE Transactions on Instrumentation and Measure-
ment, vol. 69, no. 1, pp. 24–34, 2019.

[72] Y. Liu, Y. Zhou, and X. Li, “Attitude estimation of un-
manned aerial vehicle based on LSTM neural network,”
in 2018 International Joint Conference on Neural Net-
works (IJCNN).

IEEE, 2018, pp. 1–6.

[73] J. P. Silva do Monte Lima, H. Uchiyama, and R.-i.
Taniguchi, “End-to-end learning framework for IMU-
based 6-DOF odometry,” Sensors, vol. 19, no. 17, p.
3777, 2019.

[74] M. A. Esfahani, H. Wang, K. Wu, and S. Yuan, “AbolD-
eepIO: A novel deep inertial odometry network for
autonomous vehicles,” IEEE Transactions on Intelligent
Transportation Systems, vol. 21, no. 5, pp. 1941–1950,
2019.

[75] ——, “OriNet: Robust 3-D orientation estimation with a
single particular IMU,” IEEE Robotics and Automation
Letters, vol. 5, no. 2, pp. 399–406, 2019.

[76] D. Weber, C. G¨uhmann, and T. Seel, “RIANN—A
robust neural network outperforms attitude estimation
filters,” AI, vol. 2, no. 3, pp. 444–463, 2021.

[77] N. Chumuang, A. Farooq, M. Irfan, S. Aziz, and
M. Qureshi, “Feature matching and deep learning mod-
els for attitude estimation on a micro-aerial vehicle,”
in 2022 International Conference on Cybernetics and
Innovations (ICCI).

IEEE, 2022, pp. 1–6.

[78] S. O. Madgwick, A. J. Harrison, and R. Vaidyanathan,
“Estimation of IMU and MARG orientation using a
gradient descent algorithm,” in 2011 IEEE International
Conference on Rehabilitation Robotics.
IEEE, 2011,
pp. 1–7.

[79] A. A. Golroudbari and M. H. Sabour, “End-to-end
deep learning framework for real-time inertial atti-
tude estimation using 6DOF IMU,” arXiv preprint
arXiv:2302.06037, 2023.

[80] P. Narkhede, A. Mishra, K. Hamshita, A. K. Shubham,
and A. Chauhan, “Inertial sensors and GPS fusion using
LSTM for position estimation of aerial vehicle,” in 2022
4th International Conference on Smart Systems and
Inventive Technology (ICSSIT).
IEEE, 2022, pp. 671–
675.

[81] Y. Liu, Q. Luo, W. Liang, and Y. Zhou, “GPS/INS inte-
grated navigation with LSTM neural network,” in 2021
4th International Conference on Intelligent Autonomous
Systems (ICoIAS).

IEEE, 2021, pp. 345–350.

[82] Y. Liu, Y. Zhou, and Y. Zhang, “A novel hybrid attitude
fusion method based on LSTM neural network for
unmanned aerial vehicle,” in 2021 IEEE International
Conference on Robotics and Biomimetics (ROBIO).
IEEE, 2021, pp. 1630–1635.

[83] Y. Liu, Q. Luo, and Y. Zhou, “Deep learning-enabled
fusion to bridge GPS outages for INS/GPS integrated
navigation,” IEEE Sensors Journal, vol. 22, no. 9, pp.
8974–8985, 2022.

[71] M. K. Al-Sharman, Y. Zweiri, M. A. K. Jaradat,
R. Al-Husari, D. Gan, and L. D. Seneviratne, “Deep-

[84] P. Geragersian, I. Petrunin, W. Guo, and R. Grech, “An
INS/GNSS fusion architecture in GNSS denied envi-

ronment using gated recurrent unit,” in AIAA SCITECH
2022 Forum, 2022, p. 1759.

payloads,” in OCEANS 2021: San Diego–Porto.
2021, pp. 1–9.

IEEE,

14

[85] A. Shurin and I. Klein, “QuadNet: A hybrid framework
for quadrotor dead reckoning,” Sensors, vol. 22, no. 4,
p. 1426, 2022.

[86] A. A. Deraz, O. Badawy, M. A. Elhosseini, M. Mostafa,
H. A. Ali, and A. I. El-Desouky, “Deep learning based
on LSTM model for enhanced visual odometry naviga-
tion system,” Ain Shams Engineering Journal, vol. 14,
no. 8, p. 102050, 2023.

[87] Z. Zou, T. Huang, L. Ye, and K. Song, “CNN based
adaptive Kalman filter in high-dynamic condition for
low-cost navigation system on highspeed UAV,” in
2020 5th Asia-Pacific Conference on Intelligent Robot
Systems (ACIRS).

IEEE, 2020, pp. 103–108.

[88] B. Or and I. Klein, “A hybrid model and learning-
based adaptive navigation filter,” IEEE Transactions on
Instrumentation and Measurement, vol. 71, pp. 1–11,
2022.

[89] D. Solodar and I. Klein, “VIO-DualProNet: Visual-
Inertial Odometry with Learning Based Process Noise
Covariance,” arXiv preprint arXiv:2308.11228, 2023.
I. Klein,
transformer,”

“A-KIT: Adaptive
preprint

[90] N. Cohen

and
Kalman-informed
arXiv:2401.09987, 2024.

arXiv

[91] X. Zhang, X. Mu, H. Liu, B. He, and T. Yan, “Ap-
plication of modified EKF based on intelligent data
fusion in AUV navigation,” in 2019 IEEE Underwater
Technology (UT).

IEEE, 2019, pp. 1–4.

[92] X. Mu, B. He, X. Zhang, Y. Song, Y. Shen, and C. Feng,
“End-to-end navigation for autonomous underwater ve-
hicle with hybrid recurrent neural networks,” Ocean
Engineering, vol. 194, p. 106602, 2019.

[93] X. Zhang, B. He, G. Li, X. Mu, Y. Zhou, and T. Mang,
“NavNet: AUV navigation through deep sequential
learning,” IEEE Access, vol. 8, pp. 59 845–59 861, 2020.
[94] X. Zhang, B. He, S. Gao, L. Zhou, and R. Huang,
“Sequential
learning navigation method and general
correction model for Autonomous Underwater Vehicle,”
Ocean Engineering, vol. 278, p. 114347, 2023.
[95] H. Ma, X. Mu, and B. He, “Adaptive navigation algo-
rithm with deep learning for autonomous underwater
vehicle,” Sensors, vol. 21, no. 19, p. 6406, 2021.
[96] A. Weizman, M. Groper, and I. Klein, “On the Enhance-
ment of an Ocean Glider Navigation System,” in 2023
IEEE Underwater Technology (UT).
IEEE, 2023, pp.
1–4.

[97] G. He, Y. Chaobang, D. Guohua, and S. Xiaoshuai,
real-
“The TCN-LSTM deep learning model
time prediction of ship motions,” Available at SSRN
4405121.

for

[98] S. Song, J. Liu, J. Guo, J. Wang, Y. Xie, and J.-
H. Cui, “Neural-network-based AUV navigation for
fast-changing environments,” IEEE Internet of Things
Journal, vol. 7, no. 10, pp. 9773–9783, 2020.

[99] I. B. Saksvik, A. Alcocer, and V. Hassani, “A deep
learning approach to dead-reckoning navigation for
autonomous underwater vehicles with limited sensor

[100] D. Li, J. Xu, H. He, and M. Wu, “An underwater
integrated navigation algorithm to deal with DVL mal-
functions based on deep learning,” IEEE Access, vol. 9,
pp. 82 010–82 020, 2021.

[101] N. Cohen and I. Klein, “BeamsNet: A data-driven
approach enhancing Doppler velocity log measurements
for autonomous underwater vehicle navigation,” Engi-
neering Applications of Artificial Intelligence, vol. 114,
p. 105216, 2022.

[102] ——, “Libeamsnet: AUV velocity vector estimation
in situations of limited DVL beam measurements,” in
OCEANS 2022, Hampton Roads.
IEEE, 2022, pp. 1–5.
[103] N. Cohen, Z. Yampolsky, and I. Klein, “Set-transformer
BeamsNet for AUV velocity forecasting in complete
DVL outage scenarios,” in 2023 IEEE Underwater
Technology (UT), 2023, pp. 1–6.

[104] E. Topini, F. Fanelli, A. Topini, M. Pebody, A. Ridolfi,
A. B. Phillips, and B. Allotta, “An experimental com-
parison of deep learning strategies for AUV navigation
in DVL-denied environments,” Ocean Engineering, vol.
274, p. 114034, 2023.

[105] N. Shaukat, A. Ali, M. Javed Iqbal, M. Moinuddin, and
P. Otero, “Multi-sensor fusion for underwater vehicle
localization by augmentation of RBF neural network
and error-state Kalman filter,” Sensors, vol. 21, no. 4,
p. 1149, 2021.

[106] B. Or and I. Klein, “Adaptive step size learning with ap-
plications to velocity aided inertial navigation system,”
IEEE Access, vol. 10, pp. 85 818–85 830, 2022.
[107] ——, “ProNet: Adaptive process noise estimation for
INS/DVL fusion,” in 2023 IEEE Underwater Technol-
ogy (UT), 2023, pp. 1–5.

[108] H. Chen, P. Aggarwal, T. M. Taha, and V. P. Cho-
davarapu, “Improving inertial sensor by reducing errors
using deep learning methodology,” in NAECON 2018-
IEEE National Aerospace and Electronics Conference.
IEEE, 2018, pp. 197–202.

[109] D. Engelsman, “Data-driven denoising of accelerometer
signals,” Ph.D. dissertation, University of Haifa (Israel),
2022.

[110] D. Engelsman and I. Klein, “A learning-based approach
for bias elimination in low-cost gyroscopes,” in 2022
IEEE International Symposium on Robotic and Sensors
Environments (ROSE).

IEEE, 2022, pp. 01–05.

[111] C. Jiang, S. Chen, Y. Chen, Y. Bo, L. Han, J. Guo,
Z. Feng, and H. Zhou, “Performance analysis of a
deep simple recurrent unit recurrent neural network
(SRU-RNN) in MEMS gyroscope de-noising,” Sensors,
vol. 18, no. 12, p. 4471, 2018.

[112] C. Jiang, S. Chen, Y. Chen, B. Zhang, Z. Feng, H. Zhou,
and Y. Bo, “A MEMS IMU de-noising method using
long short
term memory recurrent neural networks
(LSTM-RNN),” Sensors, vol. 18, no. 10, p. 3470, 2018.
[113] Z. Zhu, Y. Bo, and C. Jiang, “A MEMS gyroscope noise
suppressing method using neural architecture search
neural network,” Mathematical Problems in Engineer-

15

ing, vol. 2019, pp. 1–9, 2019.

[114] C. Jiang, Y. Chen, S. Chen, Y. Bo, W. Li, W. Tian,
and J. Guo, “A mixed deep recurrent neural network
for MEMS gyroscope noise suppressing,” Electronics,
vol. 8, no. 2, p. 181, 2019.

[115] S. Han, Z. Meng, X. Zhang, and Y. Yan, “Hybrid
deep recurrent neural networks for noise reduction
of MEMS-IMU with static and dynamic conditions,”
Micromachines, vol. 12, no. 2, p. 214, 2021.

[116] M. Brossard, S. Bonnabel, and A. Barrau, “Denois-
ing IMU gyroscopes with deep learning for open-loop
attitude estimation,” IEEE Robotics and Automation
Letters, vol. 5, no. 3, pp. 4796–4803, 2020.

[117] P. Russo, F. Di Ciaccio, and S. Troisi, “DANAE: A de-
noising autoencoder for underwater attitude estimation,”
arXiv preprint arXiv:2011.06853, 2020.

[118] F. Huang, Z. Wang, L. Xing, and C. Gao, “A MEMS
IMU gyroscope calibration method based on deep
learning,” IEEE Transactions on Instrumentation and
Measurement, vol. 71, pp. 1–9, 2022.

[119] Y. Liu, W. Liang, and J. Cui, “LGC-Net: A lightweight
gyroscope calibration network for efficient attitude es-
timation,” arXiv preprint arXiv:2209.08816, 2022.
[120] K. Yuan and Z. J. Wang, “A simple self-supervised IMU
denoising method for inertial aided navigation,” IEEE
Robotics and Automation Letters, 2023.

[121] D. Engelsman and I. Klein, “Towards Learning-Based
Gyrocompassing,” arXiv preprint arXiv:2312.12121,
2023.

[122] ——, “Underwater MEMS Gyrocompassing: A Vir-
tual Testing Ground,” arXiv preprint arXiv:2402.05790,
2024.
